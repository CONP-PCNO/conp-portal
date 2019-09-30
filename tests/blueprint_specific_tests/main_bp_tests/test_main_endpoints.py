# -*- coding: utf-8 -*-
"""
Unit tests for endpoints in the main blueprint
"""
import pytest
from urllib.parse import urlparse
from flask import url_for

def test_index_route(test_client):
    """
    TEST the main route
    """
    res = test_client.get("/index", follow_redirects=False)
    assert res.status_code == 200
