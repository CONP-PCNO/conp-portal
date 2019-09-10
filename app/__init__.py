# -*- coding: utf-8 -*-
import os
import sys
import inspect
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevelopmentConfig, ProductionConfig
from app.threads import UpdatePipelineData

db = SQLAlchemy()
login_manager = LoginManager()
config = DevelopmentConfig()
migrate = Migrate()


def create_app(config_settings=DevelopmentConfig):

    app = Flask(__name__)
    app.config.from_object(config_settings)

    db.init_app(app)

    from app.main import main_bp  # noqa: E402
    app.register_blueprint(main_bp)

    from app.admin import admin_bp  # noqa: E402
    app.register_blueprint(admin_bp)

    from app.auth import auth_bp  # noqa: E402
    app.register_blueprint(auth_bp)

    from app.search import search_bp  # noqa: E402
    app.register_blueprint(search_bp)

    from app.forums import forums_bp  # noqa: E402
    app.register_blueprint(forums_bp)

    from app.profile import profile_bp  # noqa: E402
    app.register_blueprint(profile_bp)

    from app.pipelines import pipelines_bp  # noqa: E402
    app.register_blueprint(pipelines_bp)

    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # start updating data on startup
    thr = UpdatePipelineData(path=os.path.join(os.path.expanduser('~'), ".cache", "boutiques"))
    thr.start()
    thr.join()

    return app
