# -*- coding: utf-8 -*-
"""
Unit tests for endpoints in the profile blueprint
"""
import pytest
from urllib.parse import urlparse
from flask import url_for


def test_pipelines_route(test_client):
    """
    GIVEN calling the route "/profile"
    WHEN no user is logged in
    THEN should return success code
    """
    res = test_client.get("/profile")
    assert res.status_code == 200