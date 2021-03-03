# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for profile blueprint
"""
from flask import render_template, redirect, url_for, flash, request, session
from flask_user import current_user, login_required, roles_accepted
from app import db
from app.profile import profile_bp
from app.profile.forms import UserProfileForm
from app.models import User, Role, AffiliationType


@profile_bp.route('/profile/edit_current_user_profile', methods=["GET", "POST"])
@login_required
def current_user_profile_page():
    """
    Route that provides a path to the current users profile page for editting
    """
    form = UserProfileForm(request.form, obj=current_user)
    session.pop('_flashes', None)

    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.affiliation = request.form.get('affiliation')

        aft_id = request.form.get('affiliation_type')
        aft = AffiliationType.query.filter(
            AffiliationType.id == int(aft_id)).first()
        current_user.affiliation_type = aft

        db.session.commit()
        flash("Profile Information Updated", "message")
        # TODO: Add a redirect

    return render_template('profile/edit_user_profile.html',
                           form=form,
                           form_user=current_user,
                           edit_roles=False,
                           can_associate=True)


@profile_bp.route('/profile/admin_edit_user_profile', methods=["GET", "POST"])
@roles_accepted('admin')
def admin_user_profile_page():
    """
    Route that provides an path to another users profile page for admin editting
    """
    user_id = request.args.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        redirect(url_for('main.index'))

    form = UserProfileForm(request.form, obj=user)
    roles = Role.query.all()
    form.roles.choices = [(r.id, r.name) for r in roles]
    current_roles = [r.id for r in user.roles]

    if request.method == "POST":
        user.full_name = request.form.get('full_name')
        user.affiliation = request.form.get('affiliation')

        aft_id = request.form.get('affiliation_type')
        aft = AffiliationType.query.filter(
            AffiliationType.id == int(aft_id)).first()
        user.affiliation_type = aft

        user.roles = []
        for r in form.roles.data:
            rl = Role.query.filter(Role.id == r).first()
            user.roles.append(rl)

        db.session.commit()
        flash("Profile Information Updated", "message")
        # TO DO: Add redirect

    return render_template('profile/edit_user_profile.html',
                           form=form,
                           form_user=user,
                           current_roles=current_roles,
                           edit_roles=True,
                           can_associate=False)
