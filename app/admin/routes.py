# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for the admin console
    NOTE CURRENTLY WORKING
"""
from app import db
from datetime import datetime, timedelta
from app.models import User
from app.oauth import OAuthSignIn
from app.forms import SignUpForm
from flask import render_template, request, flash, session, redirect, url_for,\
                  send_file, Response, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.admin import admin_bp

@admin_bp.route('/admin')
def admin():
    """ Admin Route

        Route that leads to the admin page

        Args:
            None

        Returns:
            rendered admin.html page
    """
    return render_template('admin.html', title='Admin')
