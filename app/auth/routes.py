# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for the auth blueprint
"""
from flask import render_template
from app.auth import auth_bp


@auth_bp.route('/user/confirmation_sent', methods=['GET'])
def confirmation_sent():
    """
    Provides a path for displaying a page when a users confirmation email is sent
    """
    return render_template('auth/flask_user/confirmation_sent.html')
