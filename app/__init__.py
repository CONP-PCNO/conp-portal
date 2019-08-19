import os
import sys
import inspect
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login = LoginManager()
config = Config()

def create_app(config_settings=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # from app import routes, models

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
  
    migrate = Migrate(app, db)

    login.init_app(app)
    login.login_view = 'login'

    return app


