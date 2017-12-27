# -*- coding:utf8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("conf")

db = SQLAlchemy(app)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.secret_key='sdgdhfjdfkl12345!@#$%^'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/reglogin/'
from application import views, module