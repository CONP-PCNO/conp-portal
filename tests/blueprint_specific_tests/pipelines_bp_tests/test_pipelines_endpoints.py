# -*- coding: utf-8 -*-
"""
Unit tests for endpoints in the pipelines blueprint
"""
import pytest
from urllib.parse import urlparse
from flask import url_for


def test_pipelines_route(test_client):
    """
    GIVEN calling the route "/pipelines"
    WHEN no user is logged in
    THEN should return success code
    """
    res = test_client.get("/pipelines")
    assert res.status_code == 200


def test_pipeline_search_route(test_client):
    """
    GIVEN calling the route "/pipeline-search"
    WHEN no user is logged in
    THEN should return success code
    """
    res = test_client.get("/pipeline-search")
    assert res.status_code == 200


def test_share_route(test_client):
    """
    GIVEN calling the route "/share"
    WHEN no user is logged in
    THEN should return success code
    """
    res = test_client.get("/share")
    assert res.status_code == 200

def test_tools_route(test_client):
    """
    GIVEN calling the route "/tools"
    WHEN no user is logged in
    THEN should return success code
    """
    res = test_client.get("/tools")
    assert res.status_code == 200
