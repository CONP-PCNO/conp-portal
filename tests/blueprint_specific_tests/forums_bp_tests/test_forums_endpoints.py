# -*- coding: utf-8 -*-
"""
Unit tests for endpoints in the forums blueprint
"""
import pytest
from urllib.parse import urlparse
from flask import url_for


def test_forums_route(test_client):
    """
    GIVEN calling the route "/forums"
    WHEN no user is logged in
    THEN should return success code
    """
    res = test_client.get("/forums")
    assert res.status_code == 200
