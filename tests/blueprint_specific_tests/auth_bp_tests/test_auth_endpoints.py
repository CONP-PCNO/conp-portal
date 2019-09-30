# -*- coding: utf-8 -*-
"""
Unit tests for endpoints in the auth blueprint
"""
import pytest
from urllib.parse import urlparse
from flask import url_for


def test_login_route(test_client):
    """
    GIVEN calling the route "/login"
    WHEN no user is logged in
    THEN should return success code
    """
    res = test_client.get("/login")
    assert res.status_code == 200
