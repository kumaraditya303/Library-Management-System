"""
The flask application package.
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail()
mail.init_app(app)
migrate=Migrate(app,db)
scheduler = BackgroundScheduler()

import Library_Management_System.views
