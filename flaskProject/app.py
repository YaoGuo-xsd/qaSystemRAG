from flask import Flask
import config
from extions import db, cors
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from blueprints.upload import bp as upload_bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# 绑定配置文件
app.config.from_object(config)
# 绑定数据库
db.init_app(app)
# 迁移数据库
migrate = Migrate(app, db)

# 初始化JWT扩展
jwt = JWTManager(app)


# 前后端分离 绑定跨域请求
cors.init_app(app)


# 注册绑定蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)


if __name__ == '__main__':
    app.run(host='10.0.12.13',port=5000)
