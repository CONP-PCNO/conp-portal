# -*- coding: utf-8 -*-
import pytest
from flask import url_for
from urllib.parse import urlparse
from flask_dance.consumer.storage import MemoryStorage

def test_orcid_unauthorized(app, test_client, monkeypatch):
    """
    GIVEN a user tries to use ORCID
    WHEN they have not logged in
    THEN should be redirected to orcid authorization
    """
    storage = MemoryStorage()
    monkeypatch.setattr(app.blueprints['orcid'],"storage",storage)

    print(app.blueprints['orcid'].storage)

    res = test_client.get(url_for("orcid.login"))
    assert res.status_code == 302
    urlp = urlparse(res.headers['Location'])
    assert "{}://{}{}".format(urlp.scheme,urlp.netloc,urlp.path) == app.blueprints['orcid'].authorization_url
