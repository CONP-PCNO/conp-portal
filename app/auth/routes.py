# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for the auth blueprint
"""
from app import db
from app.models import User
from sqlalchemy import func, or_
from flask import render_template, request, flash, session, redirect,\
                  url_for, send_file, Response, abort
from flask_user import current_user, login_required, roles_accepted
from app.auth import auth_bp

# @auth_bp.route('/success', methods=['GET', 'POST'])
# @login_required
# def logged_in():
#     """ Success Route

#         This route catches a successful login
#         TO DO: This seems quite redudant

#         Args:
#             None

#         Returns:
#             redirect to non-public index page
#     """
#     if request.method == 'GET':
#         # Protected user content can be handled here
#         return redirect(url_for('main.index'))

# @auth_bp.route('/logout')
# def logout():
#     """ Logout Route

#         The route to log a user out of the portal

#         Args:
#             None

#         Returns:
#             redirect to the public index page
#     """
#     logout_user()

#     return redirect(url_for('main.public'))


# # This is the first step in the login process: the 'login with X' buttons
# # should direct users here with the provider name filled in
# @auth_bp.route('/authorize/<provider>')
# def oauth_authorize(provider):
#     """ Authorize Provider Route

#         First step in OATH dance to autorize the use to a provider

#         Args:
#             provider for oauth

#         Returns:
#             oauth.authorize function if successful
#             redirect to index if failed
#     """
#     if not current_user.is_anonymous:
#         return redirect(url_for('main.index'))
#     oauth = OAuthSignIn.get_provider(provider)
#     return oauth.authorize()


# # This is step two. The OAuth provider then sends its reply to this route
# @auth_bp.route('/callback/<provider>')
# def oauth_callback(provider):
#     """ Callback Provider Route

#         This is the second step in the OAuth process that assigns
#         a token to the session

#         Args:
#             provider for oauth

#         Returns:
#             Adds token to session if successful
#             If successful and no user is assigned to the oauth_id
#                 redirects to register account
#             If unsuccessful, returns redirect to login
#     """
#     if not current_user.is_anonymous:
#         return redirect(url_for('main.public'))

#     oauth = OAuthSignIn.get_provider(provider)
#     # This is step three. The code from the provider's reply is sent back to
#     # the provider and the provider returns an authentication token
#     access_token, oauth_id = oauth.callback()

#     if access_token is None or oauth_id is None:
#         flash('Authentication failed. Please contact an admin if '
#               'this problem is persistent')
#         return redirect(url_for('auth.login'))

#     user = User.query.filter_by(oauth_id=oauth_id).first()
#     if user is None:
#         return redirect(url_for("auth.register"))

#     login_user(user, remember=True)
#     session['active_token'] = access_token

#     return redirect(url_for('auth.logged_in'))


# @auth_bp.route('/register')
# def register():
#     """ Register Route

#         The route to lead to the register template

#         Args:
#             None

#         Returns
#             Rendered template for register.html
#     """
#     form = SignUpForm()
#     return render_template('register.html', title='CONP | Register', form=form)
