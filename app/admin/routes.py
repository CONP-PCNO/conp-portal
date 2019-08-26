from app import db
from datetime import datetime, timedelta
from app.models import User
from app.oauth import OAuthSignIn
from app.forms import SignUpForm
from flask import render_template, request, flash, session, redirect, url_for, send_file, Response, abort
from flask_login import current_user, login_user, logout_user, login_required

from app.admin import admin_bp

@admin_bp.route('/register_new_user', methods=['GET', 'POST'])
def register_new_user():
    error = None
    form = SignUpForm()

    # Handle the BooleanField to check if is_pi or not
    if not 'pi' in request.form:
        is_pi = False
    elif request.form['pi']:
        is_pi = True

    if request.method == 'POST':
        # Check if passwords match
        if request.form['password1'] == request.form['password2']:
            if form.validate_on_submit():
                # Check if email already exists
                user = User.query.filter_by(email=request.form['email']).first()
                # Create new user
                if not user:
                    user = User(
                        oauth_id=request.form['orcid'],
                        username=request.form['username'],
                        email=request.form['email'],
                        is_whitelisted=False,
                        is_pi= is_pi,
                        affiliation=request.form['affiliation'],
                        expiration=datetime.now() + timedelta(6 * 365 / 12),  # 6 months
                        date_created=datetime.now(),
                        date_updated=datetime.now()
                    )
                    user.set_password(request.form['password1'])
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('index'))
            error = form.errors
        error = {'Passwords do not match'}
    return render_template('register.html', title='CONP | Register', form=form, error=error)

@admin_bp.route('/admin')
def admin():
    return render_template('admin.html', title='Admin')