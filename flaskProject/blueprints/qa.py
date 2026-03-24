from flask import Blueprint
from flask import request, jsonify
from rag.getAnswer import get_answer_radar, get_answer_gpt, get_answer_radarbm25
from models import QaModel
from extions import db
import jwt
import time
from models import DocumentModel

bp = Blueprint("qa", __name__, url_prefix="/")

# 小雷达提交问题 回复接口
@bp.route('/answerradar', methods = ['POST'])
def answer():
    start_time = time.time()
    token = request.headers.get('token')
    decoded_token = jwt.decode(token, key="adwefszsdgwfwaf", algorithms=['HS256'])
    data_id = decoded_token.get('user_id')  # 用户id
    print(data_id)
    data_json = request.get_json()
    print(data_json)
    data_query = data_json.get("question")
    result = get_answer_radar(data_query)
    print(result)
    qa = QaModel(question=data_query, answer=result, type=0, uid=data_id)
    db.session.add(qa)
    db.session.commit()
    end_time = time.time()
    print("接口响应速度：")
    print(end_time-start_time)
    return jsonify(answer=result)

# 小雷达提交问题，回复接口，使用BM25算法进行查找
@bp.route('/answerradarBM25', methods = ['POST'])
def answerBM25():
    start_time = time.time()
    token = request.headers.get('token')
    decoded_token = jwt.decode(token, key="adwefszsdgwfwaf", algorithms=['HS256'])
    data_id = decoded_token.get('user_id')  # 用户id
    print(data_id)
    data_json = request.get_json()
    print(data_json)
    data_query = data_json.get("question")  # 获取用户提问
    documents = DocumentModel.query.filter_by(uid=data_id).all()  # 获取所有参考文档
    chunks = []
    for item in documents:
        chunks.append(item.chunks)
    # print(chunks)
    print(f"数据库中检索到的chunks中的元素数量：{len(chunks)}")
    data_answer = get_answer_radarbm25(data_query, chunks)
    qa = QaModel(question=data_query, answer=data_answer, type=0, uid=data_id)
    db.session.add(qa)
    db.session.commit()
    end_time = time.time()
    print("接口响应速度：")
    print(end_time - start_time)
    return jsonify(answer=data_answer)


# Chat-gpt提交问题 回复接口, 同时将qa保存数据库
@bp.route('/answergpt', methods = ['POST'])
def answergpt():
    start_time = time.time()
    token = request.headers.get('token')
    decoded_token = jwt.decode(token, key="adwefszsdgwfwaf", algorithms=['HS256'])
    data_id = decoded_token.get('user_id') # 用户id
    print(data_id)
    data_json = request.get_json()
    print(data_json)
    data_query = data_json.get("question")  # 问题
    result = get_answer_gpt(data_query)  # 答案
    print(result)
    qa = QaModel(question=data_query, answer=result, type=1, uid=data_id)
    db.session.add(qa)
    db.session.commit()
    end_time = time.time()
    print("接口响应速度：")
    print(end_time - start_time)
    return jsonify(answer=result)