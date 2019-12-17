# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for the main blueprint
"""
from flask import render_template
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

    return render_template('index.html', title='CONP | Home', user=current_user)
