# -*- coding: utf-8 -*-
"""ORCHID MODILE

Module that constains the code necessary
to create a orchid blueprint for Flask-Dance

"""
from __future__ import unicode_literals

import os
import os.path
from functools import partial

from flask.globals import LocalProxy, _lookup_app_object
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask_dance.consumer.requests import OAuth2Session

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class JsonOath2Session(OAuth2Session):
    def __init__(self, *args, **kwargs):
        """
          custom json session to ensure we are getting back json from orchid
        """
        super(JsonOath2Session, self).__init__(*args, **kwargs)
        self.headers["Accept"] = "application/orcid+json"


def make_orcid_blueprint(
    client_id=None,
    client_secret=None,
    scope=None,
    offline=False,
    redirect_url=None,
    redirect_to=None,
    login_url=None,
    authorized_url=None,
    session_class=None,
    storage=None
):
    """
    This function actually creates a specific orchid blueprint for use with Flask Dance
    Args:
      client_id: Override the client id provided in config
      client_secret: Ovveride the client secret provided in the config
      scope: list of scopes for the oauth
      offline: is this online or offline
      redirect_url: Ovveride the redirect_url from Flask-Login
      redirect_to: OVveride the redirect_to from Flask-Login
      login_url: OVerrid the Login_url from Flask-login
      authorized_url: Override the authorized_url from Flask-Dance
      session_class: provide a custom OAuth session
      storage: storage for the token
    Result:
      Flask Blueprint for app
    """
    scope = scope or ["/authenticate", "/read-limited"]
    session_class = session_class or JsonOath2Session

    _base_url = "https://orcid.org/oauth"
    _token_url = "https://orcid.org/oauth/token"
    _authorization_url = "https://orcid.org/oauth/authorize"

    if os.environ.get("USE_ORCID_OAUTH_SANDBOX"):
        _base_url = "https://api.sandbox.orcid.org/v2.0"
        _token_url = "https://api.sandbox.orcid.org/oauth/token"
        _authorization_url = "https://sandbox.orcid.org/oauth/authorize"

    orcid_bp = OAuth2ConsumerBlueprint(
        "orcid",
        __name__,
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        base_url=_base_url,
        token_url=_token_url,
        authorization_url=_authorization_url,
        redirect_url=redirect_url,
        redirect_to=redirect_to,
        login_url=login_url,
        authorized_url=authorized_url,
        session_class=session_class,
        storage=storage
    )

    orcid_bp.from_config["client_id"] = "ORCID_OAUTH_CLIENT_ID"
    orcid_bp.from_config["client_secret"] = "ORCID_OAUTH_CLIENT_SECRET"

    @orcid_bp.before_app_request
    def set_applocal_session():
        """
          sets the orchid session in the current context
        """
        ctx = stack.top
        ctx.orchid_oauth = orcid_bp.session
    return orcid_bp


orcid = LocalProxy(partial(_lookup_app_object, "orcid_oauth"))
