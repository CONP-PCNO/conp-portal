# -*- coding: utf-8 -*-
"""
Unit tests for endpoints in the main blueprint
"""
import pytest
from urllib.parse import urlparse
from flask import url_for


def test_public_route(test_client):
    """
    GIVEN calling the route "/public"
    WHEN no user is logged in
    THEN should return success code and fail on post
    """
    res = test_client.get("/public")
    assert res.status_code == 200


def test_private_index_route(test_client):
    # Test response code
    res = test_client.get("/index", follow_redirects=False)
    assert res.status_code == 302
    assert urlparse(res.location).path == url_for("user.login")

    # Test the redirect works
    res = test_client.get("/index", follow_redirects=True)
    assert res.status_code == 200
