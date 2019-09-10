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
    SECRET_KEY = os.environ.get('SECRET_KEY') or "conp-secret-key-for-here"
    DATA_PATH = os.environ.get('DATA_PATH') or os.path.join(basedir, "app/static/data")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False
    OAUTH_CREDENTIALS = {'orcid': {'id': os.environ.get('OAUTH_ORCID_ID'),
                                   'secret':
                                   os.environ.get('OAUTH_ORCID_SECRET')}}

class DevelopmentConfig(Config):
    """This is the config for Development"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               "sqlite:///{}".format(os.path.join(basedir, "app.db")))

class TestingConfig(Config):
    """This is the config used for pytest"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(basedir, "test.db"))
    TESTING = True

class ProductionConfig(Config):
    """This is for when we are full on production, needs to be elaborated"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               "sqlite:///{}".format(os.path.join(basedir, "app.db")))
