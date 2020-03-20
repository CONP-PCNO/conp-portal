# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes in webhooks blueprint
"""
from app import config
from app.webhooks import webhooks_bp
from flask import request, abort, current_app
from flask_wtf.csrf import CSRFProtect
import git
import os

@webhooks_bp.route('/webhooks', methods=['POST', 'GET'])
def webhooks():
    """ Github webhooks

        This route executes git fetch and git merge when a notification of a new pull
        is received from github.

        Retuns:
            JSON empty
    """
    if not request.is_json:
        abort(404)
    payload = request.get_json()
    secret = payload \
        .get('hook', {}) \
        .get('config', {}) \
        .get('secret','')

    if not secret:
        # Pretend this endpoint do not exists if secret id not provided 
        abort(404)

    if current_app.config['WEBHOOKS_SECRET'] != secret:
        abort(400)

    # Initialize the git repository object
    repo = git.Repo(os.getcwd())

    # Update to latest commit
    origin = repo.remotes.origin
    origin.pull('master')

    bashCommand = "cwm --rdf test.rdf --ntriples > test.nt"
    import subprocess
    process = subprocess.run('')

    return 'OK'

