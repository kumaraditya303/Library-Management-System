"""
The flask application package.
"""

from flask import Flask
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail()
mail.init_app(app)

scheduler = BackgroundScheduler()
import Library_Management_System.views