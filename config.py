# -*- coding: utf-8 -*-
"""Configuration Module

Module that contains the Flask Configuration Class
"""
import os


class Config(object):
    """Configuration class

    This class contains all of the global configuration variables needed for
    the CONP Portal. Ideally, variables such as secret keys and such should
    be set by environment variable rather than explicitely here.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Needs to be consistent with the dataset git submodule
    DATA_PATH = '/static/data/projects/'
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'postgresql://localhost/conp')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH_CREDENTIALS = {'orcid': {'id': os.environ.get('OAUTH_ORCID_ID'),
                                   'secret':
                                   os.environ.get('OAUTH_ORCID_SECRET')}}
