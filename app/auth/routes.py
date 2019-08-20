from app import db
from app.models import User
from app.oauth import OAuthSignIn
from app.forms import SignInForm
from app.forms import SignUpForm

from sqlalchemy import func, or_
from flask import render_template, request, flash, session, redirect, url_for, send_file, Response, abort
from flask_login import current_user, login_user, logout_user, login_required

from app.auth import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = SignInForm()

    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    return render_template('login.html', title='CONP | Log In', form=form, error=form.errors)

@auth_bp.route('/success', methods=['GET', 'POST'])
@login_required
def logged_in():
    if request.method == 'GET':
        # Protected user content can be handled here
        return redirect(url_for('index'))

@auth_bp.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('main.public'))

# This is the first step in the login process: the 'login with X' buttons
# should direct users here with the provider name filled in
@auth_bp.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

# This is step two. The OAuth provider then sends its reply to this route
@auth_bp.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:

        return redirect(url_for('main.public'))

    oauth = OAuthSignIn.get_provider(provider)
    # This is step three. The code from the provider's reply is sent back to
    # the provider and the provider returns an authentication token
    access_token, oauth_id = oauth.callback()

    if access_token is None or oauth_id is None:
        flash('Authentication failed. Please contact an admin if '
                'this problem is persistent')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(oauth_id=oauth_id).first()
    if user is None:
        return redirect(url_for("auth.register"))

    login_user(user, remember=True)
    session['active_token'] = access_token

    return redirect(url_for('logged_in'))

@auth_bp.route('/register')
def register():
    form = SignUpForm()
    return render_template('register.html', title='CONP | Register', form=form)