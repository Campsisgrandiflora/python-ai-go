# -*- coding:utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
import pymysql
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/aigo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = '1df6604768744790ad0e936d596a8e8f'
app.config["UP_DEMO"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/demo/")
app.config["UP_DEMAND"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/demand/")
app.config["UP_RESOLVE"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/resolve/")
app.config["UP_IMPROVE"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/improve/")
app.config["UF_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/user/")
app.config["EF_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/enterprise/")
app.debug = True
app.config["UP_ARTICLE"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/article/")
app.config["UP_REVIEW"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/review/")
db = SQLAlchemy(app)

from app.main import main as main_blueprint
from app.user import user as user_blueprint
from app.enterprise import enterprise as enterprise_blueprint
from app.admin import admin as admin_blueprint
from app.bbs import bbs as bbs_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(enterprise_blueprint, url_prefix="/enterprise")
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(bbs_blueprint, url_prefix="/bbs")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404
