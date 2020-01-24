# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for the main blueprint
"""
from flask import render_template, request
from flask_login import current_user, login_required
from app.main import main_bp


@main_bp.route('/')
@main_bp.route('/index')
def index():
    """ Index Route

        The route to the non-public index page

        Args:
            None

        Returns:
            The rendered index.html template for the current_user
    """

    termsAccepted = request.cookies.get('termsAccepted')
    print('showTerms')
    print(termsAccepted)
    showTerms = not termsAccepted
    print(showTerms)

    return render_template('index.html', title='CONP | Home', user=current_user, showTerms=showTerms)


@main_bp.route('/share')
def share():
    """ Share Route

        Route to lead to the share page
        CURRENTLY NOT WORKING

        Args:
            None

        Returns:
            rendered template for share.html
    """
    return render_template('share.html', title='CONP | Share a Dataset', user=current_user)
