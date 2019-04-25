from flask import Flask
from flask_script import Manager

from hd.models import db
from hd.views import hbp
from qd.views import bp

app = Flask(__name__)
app.register_blueprint(blueprint=bp)
app.register_blueprint(hbp,url_prefix='/hd')

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:nana-520@127.0.0.1:3306/weibo'
db.init_app(app)

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
