# 数据库配置信息
DATABASE = "xsd-design"     # mysql上连接数据库的名称
HOSTNAME = "159.75.105.50"      # mysql所在的主机名
PORT = 3306                 # mysql监听的端口号，默认3306
USERNAME = "root"           # 连接mysql的用户名
PASSWORD = "123456"         # 连接mysql的密码
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# JWT配置 可以任意设置的字符串
JWT_SECRET_KEY = "adwefszsdgwfwaf"