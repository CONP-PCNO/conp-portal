import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATA_PATH = os.environ.get('DATA_PATH')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    OAUTH_CREDENTIALS = {'orcid': {'id': os.environ.get('OAUTH_ORCID_ID'),
                                   'secret': os.environ.get('OAUTH_ORCID_SECRET')}}

