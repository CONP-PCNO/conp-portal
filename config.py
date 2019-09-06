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
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATA_PATH = os.environ.get('DATA_PATH')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    OAUTH_CREDENTIALS = {'orcid': {'id': os.environ.get('OAUTH_ORCID_ID'),
                                   'secret':
                                   os.environ.get('OAUTH_ORCID_SECRET')}}
