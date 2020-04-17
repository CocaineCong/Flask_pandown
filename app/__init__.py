import os
from flask import Flask
from flask_cors import CORS
from config import *
from redis import StrictRedis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
redis = StrictRedis()

from app.middleware.login_check import login_check


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] ="123"# os.urandom(12)

    # 注册蓝图
    from app.view.person import person

    app.register_blueprint(person)

    from app.view.share import share
    app.register_blueprint(share)

    from app.view.file_single_table import file_blueprint
    app.register_blueprint(file_blueprint)

    from app.view.file_double_table import file_blueprint
    app.register_blueprint(file_blueprint)

    #from app.view.tools import tools
    #app.register_blueprint(tools)

    app.config[data_base_url] = data_base
    app.config[data_base_track_modifications] = False
    db.init_app(app)
    CORS(app, supports_credentials=True)
    # 导入中间件
    app.before_request(login_check)

    return app
