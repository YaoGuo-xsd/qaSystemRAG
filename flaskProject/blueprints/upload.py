from flask import Blueprint
from flask import request
from rag.uploadFile import load_txt, load_pdf, load_md, save_file_chroma, save_file_db
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from dotenv import load_dotenv
import time
import jwt
from models import DocumentModel
from extions import db
import os

bp = Blueprint("upload", __name__, url_prefix="/")

@bp.route('/uploadtxt', methods = ['POST'])
def file_save_txt():
    token = request.headers.get('token')
    decoded_token = jwt.decode(token, key="adwefszsdgwfwaf", algorithms=['HS256'])
    data_uid = decoded_token.get('user_id')
    print(data_uid)

    file = request.files['file']
    if file is None:  # 表示没有发送文件
        return {
            'message': "文件上传失败"
        }
    file_name = file.filename.replace(" ", "")
    file_path = 'uploadfiles/' + file_name
    if os.path.exists(file_path) and os.path.isfile(file_path):
        print("该文件已经存在")
        return {
            'code': 200,
            'messsge': "文件上传成功，该文件已经存在",
        }
    print("获取上传文件的名称为[%s]\n" % file_name)
    file.save('uploadfiles/' + file_name)  # 保存文件
    document = load_txt(file_name)  # 加载前端传来的文件
    docs = save_file_db(document)  # 分词切片并分词
    for data_doc in docs:
        docitem = DocumentModel(chunks=data_doc, uid=data_uid)
        db.session.add(docitem)
        db.session.commit()
    return {
        'code': 200,
        'messsge': "文件上传成功",
        'fileName': file_name,
        'url': '../uploadfiles/' + file_name
    }

@bp.route('/uploadpdf', methods = ['POST'])
def file_save_pdf():
    token = request.headers.get('token')
    decoded_token = jwt.decode(token, key="adwefszsdgwfwaf", algorithms=['HS256'])
    data_uid = decoded_token.get('user_id')
    print(data_uid)

    file = request.files['file']
    if file is None:  # 表示没有发送文件
        return {
            'message': "文件上传失败"
        }
    file_name = file.filename.replace(" ", "")
    file_path = 'uploadfiles/' + file_name
    if os.path.exists(file_path) and os.path.isfile(file_path):
        print("该文件已经存在")
        return {
            'code': 200,
            'messsge': "文件上传成功，该文件已经存在",
        }
    print("获取上传文件的名称为[%s]\n" % file_name)
    file.save('uploadfiles/' + file_name)  # 保存文件
    document = load_pdf(file_name)   # 加载前端传来的文件
    docs = save_file_db(document)
    for data_doc in docs:
        docitem = DocumentModel(chunks=data_doc, uid=data_uid)
        db.session.add(docitem)
        db.session.commit()
    return {
        'code': 200,
        'messsge': "文件上传成功",
        'fileName': file_name,
        'url': '../uploadfiles/' + file_name
    }

@bp.route('/uploadmd', methods = ['POST'])
def file_save_md():
    token = request.headers.get('token')
    decoded_token = jwt.decode(token, key="adwefszsdgwfwaf", algorithms=['HS256'])
    data_uid = decoded_token.get('user_id')
    print(data_uid)

    file = request.files['file']
    if file is None:  # 表示没有发送文件
        return {
            'message': "文件上传失败"
        }
    file_name = file.filename.replace(" ", "")
    file_path = 'uploadfiles/' + file_name
    if os.path.exists(file_path) and os.path.isfile(file_path):
        print("该文件已经存在")
        return {
            'code': 200,
            'messsge': "文件上传成功，该文件已经存在",
        }
    print("获取上传文件的名称为[%s]\n" % file_name)
    file.save('uploadfiles/' + file_name)  # 保存文件
    document = load_md(file_name)   # 加载前端传来的文件
    docs = save_file_db(document)
    for data_doc in docs:
        docitem = DocumentModel(chunks=data_doc, uid=data_uid)
        db.session.add(docitem)
        db.session.commit()
    return {
        'code': 200,
        'messsge': "文件上传成功",
        'fileName': file_name,
        'url': '../uploadfiles/' + file_name
    }

@bp.route('/uploadavatar', methods = ['POST'])
def upload_avatar():
    file = request.files['image']
    if file is None:  # 表示没有发送文件
        return {
            'message': "文件上传失败"
        }
    file_name = file.filename.replace(" ", "")
    print("获取上传文件的名称为[%s]\n" % file_name)
    load_dotenv()
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
    bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'xsd-learn')

    str1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    img_url = str1 + file_name
    bucket.put_object(img_url, file)
    return {
        'code': 200,
        'messsge': "文件上传成功",
        'data': "https://xsd-learn.oss-cn-beijing.aliyuncs.com/" + f'{img_url}'
    }