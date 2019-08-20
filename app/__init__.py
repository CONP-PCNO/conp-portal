import os
import sys
import inspect
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
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

    from app.search import search_bp
    app.register_blueprint(search_bp)
  
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    return app


