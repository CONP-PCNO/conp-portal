"""Configuration Module

Module that contains the Flask Configuration Class
"""
import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))


class Config:
    """Configuration class

    This class contains all of the global configuration variables needed for
    the CONP Portal. Ideally, variables such as secret keys and such should
    be set by environment variable rather than explicitely here.
    """

    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or "conp-secret-key-for-here-ABC0321XYZHHHAAASSSHHH"
    DATA_PATH = os.environ.get('DATA_PATH') or os.path.join(
        basedir, "data")
    # Dataset cache
    DATASET_CACHE_PATH = os.environ.get('DATASET_CACHE_PATH') or os.path.join(
        basedir, "data/.cache/conp-dataset")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS') or False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # @todo: Remove shawntbrown@gmail.com - This should be set to a real email address for production.
    MAIL_DEFAULT_SENDER = '"CONP-PCNO Portal" <shawntbrown@gmail.com>'
    # @todo: Verify and document this email address: conp-test@mailinator.com
    ADMINS = (os.environ.get('ADMIN_EMAIL') or 'conp-test@mailinator.com',)
    LOG_TO_STDOUT = True
    TEMPLATES_AUTO_RELOAD = True

    SECURITY_APP_NAME = "CONP-PCNO Data Portal"
    SECURITY_BLUEPRINT_NAME = "user"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SINGLE_HASH = True
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT") or SECRET_KEY
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_PASSWORD_CONFIRM_REQUIRED = True
    SECURITY_POST_LOGIN_VIEW = "main.index"
    SECURITY_POST_LOGOUT_VIEW = "main.index"
    SECURITY_POST_REGISTER_VIEW = "auth.confirmation_sent"
    SECURITY_POST_CONFIRM_VIEW = "profile.current_user_profile_page"
    SECURITY_AUTO_LOGIN_AFTER_CONFIRM = True
    SECURITY_LOGIN_USER_TEMPLATE = "security/login.html"
    SECURITY_REGISTER_USER_TEMPLATE = "security/register.html"
    SECURITY_FORGOT_PASSWORD_TEMPLATE = "security/forgot_password.html"
    SECURITY_RESET_PASSWORD_TEMPLATE = "security/reset_password.html"
    SECURITY_SEND_CONFIRMATION_TEMPLATE = "security/resend_confirm_email.html"
    SECURITY_CHANGE_PASSWORD_TEMPLATE = "security/change_password.html"

    # ORCID PARAMETERS, must come from .flaskenv file!
    ORCID_OAUTH_CLIENT_ID = os.environ.get("ORCID_OAUTH_CLIENT_ID")
    ORCID_OAUTH_CLIENT_SECRET = os.environ.get("ORCID_OAUTH_CLIENT_SECRET")

    # GitHub webhooks
    WEBHOOKS_SECRET = os.environ.get("WEBHOOKS_SECRET")

    # GitHub token
    GITHUB_PAT = os.environ.get("GITHUB_PAT")

    # Matomo
    MATOMO_SERVER_URL = os.environ.get("MATOMO_SERVER_URL")
    MATOMO_SITE_ID = os.environ.get("MATOMO_SITE_ID", "2")
    MATOMO_TOKEN_AUTH = os.environ.get("MATOMO_TOKEN_AUTH")
    # OpenAlex API key for `flask update_research_use` (list and full-text searches)
    OPENALEX_API_KEY = os.environ.get("OPENALEX_API_KEY")

    # ARK identifier NAAN for CONP
    ARK_CONP_NAAN = os.environ.get("ARK_CONP_NAAN") or "99999"

    # Nexus SPARQL endpoint
    # @todo: remove hardcoded url
    NEXUS_SPARQL_ENDPOINT = os.environ.get(
        "NEXUS_SPARQL_ENDPOINT",
        "https://reservoir.global/v1/views/Public/CONP/graph/sparql"
    )

    # Experiments
    EXPERIMENTS_UPLOAD_DIRECTORY = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "data",
        "experiments"
    )


class DevelopmentConfig(Config):
    """This is the config for Development"""
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               or "sqlite:///{}".format(os.path.join(basedir, "app.db")))


class TestingConfig(Config):
    """This is the config used for pytest

    Python 3.14 compatibility: Flask 3.x requires SERVER_NAME and
    PREFERRED_URL_SCHEME to be explicitly set for url_for() to work outside
    request context during tests. These settings ensure test fixtures can
    generate URLs reliably without triggering "RuntimeError: Working outside
    of application context" or "RuntimeError: The server name '<name>' does
    not match the server name of the current request."
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
        os.path.join(basedir, "test.db"))
    TESTING = True
    SERVER_NAME = "localhost"
    APPLICATION_ROOT = "/"
    PREFERRED_URL_SCHEME = "http"
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}


class ProductionConfig(Config):
    """This is for when we are full on production, needs to be elaborated"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               or "sqlite:///{}".format(os.path.join(basedir, "app.db")))
