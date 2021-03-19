# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes in webhooks blueprint
"""
from app.webhooks import webhooks_bp
from flask import request, abort, current_app
import git
import hmac
import os
import hashlib


@webhooks_bp.route('/webhooks', methods=['GET', 'POST'])
def webhooks():
    """ Github webhooks

        This route executes git fetch and git merge when a notification of a new pull
        is received from github.

        Retuns:
            JSON empty
    """
    if not request.is_json:
        abort(400)

    """ Security check. GitHub will send a header containing an HMAC of the
        contents of the POST body. We calculate this server side and update the
        code only if the hashes match.

        See: https://developer.github.com/webhooks/securing/
    """
    server_signature = 'sha1=' + hmac.new(
        bytes(current_app.config['WEBHOOKS_SECRET'], 'ascii'),
        request.data,
        digestmod=hashlib.sha1
    ).hexdigest()

    client_signature = request.headers['X-Hub-Signature']

    if not hmac.compare_digest(server_signature, client_signature):
        abort(400)

    # Initialize the git repository object
    repo = git.Repo(os.getcwd())

    # Update to latest commit
    origin = repo.remotes.origin
    origin.pull('master')

    return 'OK'
