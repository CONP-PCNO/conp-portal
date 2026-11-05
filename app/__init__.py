import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_wtf.csrf import CSRFProtect

from config import DevelopmentConfig, ProductionConfig

db = SQLAlchemy()
config = DevelopmentConfig()
migrate = Migrate(compare_type=True)
csrf_protect = CSRFProtect()
mail = Mail()
security = Security()


def create_app(config_settings=None):

    app = Flask(__name__, static_url_path='/static')
    if os.environ.get('FLASK_ENV') == 'production':
        config_settings = ProductionConfig
    elif not config_settings:
        config_settings = DevelopmentConfig
    app.config.from_object(config_settings)

    is_production_config = (
        os.environ.get('FLASK_ENV') == 'production'
        or (
            isinstance(config_settings, type)
            and issubclass(config_settings, ProductionConfig)
        )
    )
    if is_production_config and (
        not app.config['SECURITY_PASSWORD_SALT']
        or app.config['SECURITY_PASSWORD_SALT'] == app.config['SECRET_KEY']
    ):
        raise RuntimeError(
            "Production requires SECURITY_PASSWORD_SALT to be set to a "
            "stable value distinct from SECRET_KEY."
        )

    @app.template_global()
    def static_v(filename):
        """URL for a static file with a ?v=<mtime> suffix, so browsers fetch
        a changed stylesheet after a deploy instead of a cached copy."""
        from flask import url_for
        url = url_for('static', filename=filename)
        try:
            mtime = int(os.path.getmtime(os.path.join(app.static_folder, filename)))
        except OSError:
            return url
        return f'{url}?v={mtime}'

    from app.doi_sources import doi_source as _doi_source
    app.add_template_global(_doi_source, 'doi_source')

    db.init_app(app)
    migrate.init_app(app, db)
    csrf_protect.init_app(app)
    mail.init_app(app)

    from app.auth.forms import CustomRegisterForm
    from app.models import Role, User

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_form=CustomRegisterForm)

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.analytics import analytics_bp
    app.register_blueprint(analytics_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.search import search_bp
    app.register_blueprint(search_bp)

    from app.profile import profile_bp
    app.register_blueprint(profile_bp)

    from app.pipelines import pipelines_bp
    app.register_blueprint(pipelines_bp)

    from app.execution_records import execution_records_bp
    app.register_blueprint(execution_records_bp)

    from app.utils import utils_bp
    app.register_blueprint(utils_bp)

    from app.experiments import experiments_bp
    app.register_blueprint(experiments_bp)

    from app.oauth.orcid_blueprint import orcid_blueprint
    app.register_blueprint(orcid_blueprint, url_prefix="/login")

    from app.styleguide import styleguide_bp
    app.register_blueprint(styleguide_bp)

    from app.webhooks import webhooks_bp
    csrf_protect.exempt(webhooks_bp)
    app.register_blueprint(webhooks_bp)

    # Initialize Email and Logging
    init_email_and_logs_error_handler(app)

    return app

# Function to initialize the email and logs


def init_email_and_logs_error_handler(app):
    if app.debug and not app.testing:
        return

    import logging
    from logging.handlers import SMTPHandler

    if app.config['MAIL_SERVER']:
        auth = None

    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

        secure = None
        if app.config['MAIL_USE_TLS']:
            # To specify the use of a secure protocol (TLS), pass in a tuple
            # to the secure argument. This will only be used when
            # authentication credentials are supplied.
            secure = ()

        mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                                   fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                                   toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                                   credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/portal.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                                      '%(asctime)s %(levelname)s: %(message)s '
                                      '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
