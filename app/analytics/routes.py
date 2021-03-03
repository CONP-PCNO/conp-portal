# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes in the analytics blueprint
"""
from flask import render_template
from flask_login import current_user
from app.analytics import analytics_bp


@analytics_bp.route('/analytics')
def analytics():
    """ Analytics Route

        Route to lead to the analytics page

        Args:
            None

        Returns:
            rendered template for analytics.html for current_user
    """
    return render_template('analytics.html', title='CONP | Analytics', user=current_user)
