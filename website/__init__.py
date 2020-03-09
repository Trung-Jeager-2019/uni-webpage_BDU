from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_object('config')
CsrfProtect(app)
db = SQLAlchemy(app)
login_man = LoginManager()
login_man.init_app(app)

login_man.login_view = '/users/login'
login_man.login_message = 'You are not authorized to view this page.'

from website import views, models
