from flask import Blueprint
from flask import request
from models import UserModel, QaModel
from sqlalchemy import desc
from extions import db
import jwt
from config import JWT_SECRET_KEY

# /auth
bp = Blueprint("auth", __name__, url_prefix="/")


# 登录验证
@bp.route("/login", methods=['POST'])
def login():
    data_json = request.get_json()
    print(data_json)
    data_name = data_json.get("name")
    data_password = data_json.get("password")
    user = UserModel.query.filter_by(username=data_name, password=data_password).first()
    if user is None:
        return {
            'code': 403,
            'messsge': "未查询到个人信息",
        }
    else:
        payload = {
            'user_id': user.id,
            # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1) 设置失效时间
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
        return {
            'code': 200,
            'message': "查询成功，允许登录",
            'token': token,
        }


@bp.route("/verify", methods=['GET'])
def verify_jwt():
    token = request.headers.get('token')
    try:
        decoded_token = jwt.decode(token, key="adwefszsdgwfwaf", algorithms=['HS256'])
        print(decoded_token)
        # 如果验证成功，decoded_token将包含解码后的信息
        return {
            'code': 200,
            'message': "验证成功",
            'data': decoded_token
        }
    except jwt.ExpiredSignatureError:
        # token已过期
        return {
            'code': 401,
            'message': "验证失败"
        }
    except jwt.InvalidTokenError:
        # token无效
        return {
            'code': 401,
            'message': "验证失败"
        }


# 新用户注册
@bp.route("/register", methods=['POST'])
def register():
    data_json = request.get_json()
    print(data_json)
    data_name = data_json.get("name")
    data_password = data_json.get("password")
    data_email = data_json.get("email")
    data_image = data_json.get("image")
    user = UserModel(username=data_name, password=data_password, email=data_email, image=data_image)
    db.session.add(user)
    db.session.commit()
    user = UserModel.query.filter_by(username=data_name, password=data_password).first()
    payload = {
        'user_id': user.id,
    }
    print(user.id)
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    print(token)
    return {
        'code': 200,
        'message': "查询成功，允许登录",
        'token': token,
    }


# 请求用户的头像
@bp.route("/get-img", methods=['GET'])
def get_image():
    token = request.headers.get('token')
    decoded_token = jwt.decode(token, key="adwefszsdgwfwaf", algorithms=['HS256'])
    uid = decoded_token.get('user_id')
    print(uid)
    user = UserModel.query.filter_by(id=uid).first()
    return {
        'code': 200,
        'message': "验证成功",
        'data': user.image
    }


# 请求用户的信息
@bp.route("/get-info", methods=['GET'])
def get_info():
    token = request.headers.get('token')
    decoded_token = jwt.decode(token, key="adwefszsdgwfwaf", algorithms=['HS256'])
    uid = decoded_token.get('user_id')
    print(uid)
    user = UserModel.query.filter_by(id=uid).first()
    return {
        'code': 200,
        'message': "验证成功",
        'uname': user.username,
        'email': user.email,
        'img': user.image,
        'join_time': user.join_time.strftime('%Y-%m-%d %H:%M:%S')
    }


# 请求qa历史记录
@bp.route("/history", methods=['GET'])
def get_all():
    token = request.headers.get('token')
    decoded_token = jwt.decode(token, key="adwefszsdgwfwaf", algorithms=['HS256'])
    data_id = decoded_token.get('user_id')
    data_qa: [QaModel] = QaModel.query.order_by(desc("join_time")).filter_by(uid=data_id)
    qaList = [
        {
            'id': qa.id,
            'question': qa.question,
            'answer': qa.answer,
            'type': 'RAG问答服务' if qa.type == 0 else 'Chat-gpt',
            'join_time': qa.join_time.strftime('%Y-%m-%d %H:%M:%S')  # qa.join_time
        } for qa in data_qa
    ]
    return {
        'code': 200,
        'message': "查询成功，允许登录",
        "data": qaList
    }


# 删除某条历史记录
@bp.route("/delete", methods=['GET'])
def delete_by_id():
    id = request.args.get('qaId')
    print(id)
    qa = QaModel.query.get(id)
    if qa is None:
        return {
            'code': 405,
            'message': "删除失败，数据库中没有该数据"
        }
    db.session.delete(qa)
    db.session.commit()
    return {
        'code': 200,
        'message': "删除成功！"
    }
