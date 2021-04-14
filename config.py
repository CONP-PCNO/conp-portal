# -*- coding: utf-8 -*-
"""Configuration Module

Module that contains the Flask Configuration Class
"""
import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))


class Config(object):
    """Configuration class

    This class contains all of the global configuration variables needed for
    the CONP Portal. Ideally, variables such as secret keys and such should
    be set by environment variable rather than explicitely here.
    """

    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or "conp-secret-key-for-here"
    DATA_PATH = os.environ.get('DATA_PATH') or os.path.join(
        basedir, "app/static/data")
    DATASET_CACHE_PATH = os.environ.get('DATASET_CACHE_PATH') or os.path.join(
        basedir, "app/static/data/.cache/conp-dataset")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS') or False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = '"CONP-PCNO Portal" <shawntbrown@gmail.com>'
    ADMINS = [os.environ.get('ADMIN_EMAIL')] or ['conp-test@mailinator.com']
    LOG_TO_STDOUT = True

    # Flask-User Settings
    USER_APP_NAME = "CONP-PCNO Data Portal"
    USER_ENABLE_CHANGE_PASSWORD = True
    USER_ENABLE_CHANGE_USERNAME = False
    USER_ENABLE_CONFIFM_EMAIL = True
    USER_ENABLE_FORGOT_PASSWORD = True
    USER_ENABLE_EMAIL = True
    USER_ENABLE_REGISTRATION = True
    USER_REQUIRE_RETYPE_PASSWORD = True
    USER_ENABLE_USERNAME = False
    USER_EMAIL_SENDER = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = ADMINS[0]
    USER_AFTER_LOGIN_ENDPOINT = "main.index"
    USER_AFTER_LOGOUT_ENDPOINT = "main.index"
    USER_AFTER_REGISTER_ENDPOINT = "auth.confirmation_sent"
    USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = False
    USER_AUTO_LOGIN_AFTER_REGISTER = False
    USER_AUTO_LOGIN_AFTER_CONFIRM = True
    USER_LOGIN_TEMPLATE = "auth/flask_user/login.html"
    USER_FORGOT_PASSWORD_TEMPLATE = "auth/flask_user/forgot_password.html"
    USER_REGISTER_TEMPLATE = "auth/flask_user/register.html"
    USER_RESEND_CONFIRM_EMAIL_TEMPLATE = "auth/flask_user/resend_confirm_email.html"
    USER_RESET_PASSWORD_TEMPLATE = "auth/flask_user/reset_password.html"
    USER_EDIT_USER_PROFILE_TEMPLATE = "auth/flask_user/edit_user_profile.html"
    USER_CONFIRM_EMAIL_TEMPLATE = "auth/flask_user/emails/confirm_email"
    USER_REGISTERED_EMAIL_TEMPLATE = "auth/flask_user/emails/registered"

    # ORCID PARAMETERS, must come from .flaskenv file!
    ORCID_OAUTH_CLIENT_ID = os.environ.get("ORCID_OAUTH_CLIENT_ID")
    ORCID_OAUTH_CLIENT_SECRET = os.environ.get("ORCID_OAUTH_CLIENT_SECRET")

    # GitHub webhooks
    WEBHOOKS_SECRET = os.environ.get("WEBHOOKS_SECRET")

    # Matomo
    MATOMO_SERVER_URL = os.environ.get("MATOMO_SERVER_URL")
    MATOMO_SITE_ID = os.environ.get("MATOMO_SITE_ID", "2")
    MATOMO_TOKEN_AUTH = os.environ.get("MATOMO_TOKEN_AUTH")

    # Nexus SPARQL endpoint
    # TODO remove hardcoded url
    NEXUS_SPARQL_ENDPOINT = os.environ.get(
        "NEXUS_SPARQL_ENDPOINT",
        "https://reservoir.global/v1/views/Public/CONP/graph/sparql"
    )

    # Dataset cache
    DATASET_CACHE_PATH = os.environ.get("DATASET_CACHE_PATH")


class DevelopmentConfig(Config):
    """This is the config for Development"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               or "sqlite:///{}".format(os.path.join(basedir, "app.db")))


class TestingConfig(Config):
    """This is the config used for pytest"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
        os.path.join(basedir, "test.db"))
    TESTING = True


class ProductionConfig(Config):
    """This is for when we are full on production, needs to be elaborated"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               or "sqlite:///{}".format(os.path.join(basedir, "app.db")))
