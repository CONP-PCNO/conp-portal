# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for the main blueprint
"""
from flask import render_template
from flask_login import current_user, login_required
from app.main import main_bp


@main_bp.route('/')
@main_bp.route('/public')
def public():
    """Public Route

        This is the route that leads to the public main page

        Args:
            None

        Returns:
            rendered public.html template
    """
    return render_template('public.html', title='Home | CONP')


@main_bp.route('/index')
@login_required
def index():
    """ Index Route

        The route to the non-public index page

        Args:
            None

        Returns:
            The rendered index.html template for the current_user
    """
    if current_user.is_authenticated:
        return render_template('index.html', title='CONP | Home', user=current_user)
