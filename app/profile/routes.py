# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for profile blueprint
"""
from flask import render_template
from flask_login import current_user
from app.profile import profile_bp


@profile_bp.route('/profile')
def profile():
    """ Profile Route

        Route to lead to the users profile page
        CURRENTLY NOT WORKING

        Args:
            None

        Returns:
            rendered template for share.html
    """
    return render_template('profile.html', title='CONP | My Profile', user=current_user)
