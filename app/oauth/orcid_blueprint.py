# -*- coding: utf-8 -*-
"""ORCID Blueprint Module

Module that contains the full blueprint for ORCID OAuth

"""
from flask import flash, redirect, session, url_for, current_app, Markup
from flask_user import current_user
from flask_login import login_user
from app.oauth.orcid_flask_dance import make_orcid_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from app.models import db, User, OAuth
from datetime import datetime
from pprint import pprint


orcid_blueprint = make_orcid_blueprint(
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)


@oauth_authorized.connect_via(orcid_blueprint)
def orcid_logged_in(orcid_blueprint, token):
    """
    Handles the oauth dance for ORCID logins
    Args:
      orchid_blueprint: The instantiated orcid blueprint
      token: the ouath token
    Result:
      Will do one of four things:

      1. If user is not logged in, but there is an oauth, will login
      2. If user is not logged in, will create a new user using information from orchid, and login
      3. If a user is logged in, and oauth is associated already, will pass through
      4. If a user is logged in, but no oauth associated, will associate the oauth


    """
    # Check if I have an API token

    if not token:
        flash("Failed to log in.", category="error")
        return False

    # get the orcid id information
    # ORCID API calls require that the orcid id be in the request, so that needs
    # to be extracted from the token prior to making any requests
    orcid_user_id = token['orcid']

    response = orcid_blueprint.session.get("{}/record".format(orcid_user_id))

    if not response.ok:
        flash("Failed to get ORCID User Data", category="error")
        return False

    orcid_record = response.json()
    pprint(orcid_record)

    # Find this OAuth in the
    query = OAuth.query.filter_by(
        provider=orcid_blueprint.name, provider_user_id=orcid_user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=orcid_blueprint.name,
            provider_user_id=orcid_user_id,
            provider_user_login=orcid_user_id,
            token=token)

    if current_user.is_anonymous:
        print("Current user is anonymous")
        if oauth.user:
            # Case 1 (above)
            return current_app.user_manager._do_login_user(oauth.user, url_for("main.public"))
        else:
            # Case 2 (above)
            print("!!! No Oauth")
            orcid_person = orcid_record['person']

            # check if there is a user with this email address
            # Check to see if the ORCID user has an email exposed, otherwise, we cannot use it

            if len(orcid_person['emails']['email']) == 0:
                flash(Markup(
                    "Failed to create new user, must have at least one ORCID "
                    "email address accessible to restricted. Please login to your "
                    "ORCID account at http://orcid.org and update your permissions."
                    " Please see <a href='https://support.orcid.org/hc/en-us/articles/360006897614'>"
                    " Visibitility in ORCID</a> "
                    "for more information."))
                return redirect(url_for("user.login"))
                return False

            orcid_email = orcid_person['emails']['email'][0]['email']

            query = User.query.filter_by(email=orcid_email)
            try:
                nrc_u = query.one()
                oauth.user = nrc_u
                db.session.add(oauth)
                db.session.commit()
                login_user(oauth.user)

            except NoResultFound:
                print("!!!! we need to make an account")
                # Case 3
                try:
                    user = User(email=orcid_person['emails']['email'][0]['email'],
                                full_name="{} {}".format(orcid_person['name']['given-names']['value'],
                                                         orcid_person['name']['family-name']['value']),
                                active=True,
                                email_confirmed_at=datetime.utcnow(),

                                )

                    user.add_role("member")
                    user.add_role("registered-orcid", add_to_roles=True)

                    oauth.user = user

                    db.session.add_all([user, oauth])
                    db.session.commit()
                    # Need to use private method to bypass in this case
                    flash("Please update your Profile affiliation and affiliation type")
                    return current_app.user_manager._do_login_user(user, url_for('profile.current_user_profile_page'))
                except Exception as e:
                    flash("There was an error creating a user from the ORCID credentials: {}".format(e))
                    return redirect(url_for("user.login"))
    else:
        print("!!! Authenticated User")
        if oauth.user:
            flash("Account already associated with another user, cannot be associated")
            return redirect(url_for('profile.current_user_profile_page'))
        else:
            # Case 4 (above)
            print("!!! SHOULD BE HERE")
            oauth.user = current_user
            db.session.add(oauth)
            db.session.commit()
            flash("Successfully linked ORCID account")

    return False


@oauth_authorized.connect
def redirect_to_next_url(orcid_blueprint, token):
    """
    redirect function to handle properly redirec if
    login_next_url exists in the session
    """
    # retrieve `next_url` from Flask's session cookie
    if session.get('login_next_url') is not None:
        next_url = session["login_next_url"]

    # redirect the user to `next_url`
        return redirect(next_url)


@oauth_error.connect_via(orcid_blueprint)
def orcid_error(orcid_blueprint, **kwargs):
    """
    Handles passing back ouath errors elegantly
    Args:
      orchid_blueprint: Orcid Blueprint
    Result:
      Flashes error messages if they exist
    """
    msg = "OAuth error from {name}! ".format(name=orcid_blueprint.name)
    for k, v in kwargs.items():
        msg += "{} = {} ".format(k, str(v))
    print("msg= {}".format(msg))
    flash(msg, category="error")
