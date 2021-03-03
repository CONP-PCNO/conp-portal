# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes in the forum blueprint
"""
from flask import render_template
from flask_login import current_user
from app.forums import forums_bp


@forums_bp.route('/forums')
def forums():
    """ Forums Route

        Route to lead to the forums page

        Args:
            None

        Returns:
            rendered template for forums.html for current_user
    """
    return render_template('forums.html', title='CONP | Forums', user=current_user)
