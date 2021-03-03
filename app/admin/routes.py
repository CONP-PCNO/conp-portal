# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for the admin console
    NOTE CURRENTLY WORKING
"""
from flask import render_template
from app.admin import admin_bp


@admin_bp.route('/admin')
def admin():
    """ Admin Route

       Route that leads to the admin page#

        Args:
            None

        Returns:
            rendered admin.html page
    """
    return render_template('admin.html', title='Admin')
