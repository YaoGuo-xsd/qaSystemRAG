from extions import db
from datetime import datetime

# flask db init
# flask db migrate
# flask db upgrade
# flask db revision --rev-id a1c25fe0fc0e (报错中所提到的版本号)

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键 自增
    username = db.Column(db.String(100), nullable=False, unique=True) # 不可为空
    password = db.Column(db.String(100), nullable=False)              # 不可为空
    email = db.Column(db.String(100), nullable=True, unique=False)     # 可以为空
    image = db.Column(db.String(100), unique=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

class QaModel(db.Model):
    __tablename__ = "qa"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键 自增
    question = db.Column(db.String(1000), nullable=False, unique=False)
    answer = db.Column(db.TEXT, nullable=False, unique=False)
    type = db.Column(db.Integer, nullable=False)   # 0:radar  1:gpt
    uid = db.Column(db.Integer)
    join_time = db.Column(db.DateTime, default=datetime.now)

class DocumentModel(db.Model):
    __tablename__ = "document"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键 自增
    chunks = db.Column(db.TEXT, nullable=False, unique=False)
    uid = db.Column(db.Integer)
    join_time = db.Column(db.DateTime, default=datetime.now)