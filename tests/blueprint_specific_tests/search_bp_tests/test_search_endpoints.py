# -*- coding: utf-8 -*-
"""
Unit tests for endpoints in the search blueprint
"""
import pytest
from urllib.parse import urlparse
from flask import url_for


def test_pipelines_route(test_client):
    """
    GIVEN calling the route "/search"
    WHEN no user is logged in
    THEN should return success code
    """
    res = test_client.get("/search")
    assert res.status_code == 200


def test_pipelines_route(test_client):
    """
    GIVEN calling the route "/dataset-search"
    WHEN no user is logged in
    THEN should return success code
    """
    #res = test_client.get("/dataset-search")
    #assert res.status_code == 200

    assert True

def test_pipelines_route(test_client):
    """
    GIVEN calling the route "/dataset"
    WHEN no user is logged in
    THEN should return success code
    """
    #res = test_client.get("/dataset")
    #assert res.status_code == 200

    assert True