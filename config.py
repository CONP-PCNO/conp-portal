import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
<<<<<<< HEAD
=======
    DATA_PATH = '/data/projects'
>>>>>>> cf3fb453b807df95f86cc0d3e63b4cf187db7fd0
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'postgresql://localhost/conp')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH_CREDENTIALS = {'orcid': {'id': os.environ.get('OAUTH_ORCID_ID'),
                                   'secret': os.environ.get('OAUTH_ORCID_SECRET')}}
<<<<<<< HEAD
    DATA_PATH = '/data'
=======

>>>>>>> cf3fb453b807df95f86cc0d3e63b4cf187db7fd0
