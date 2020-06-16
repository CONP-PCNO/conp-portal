# -*- coding: utf-8 -*-
"""
Unit tests for endpoints in the pipelines blueprint
"""
import pytest
import app.cli as cli
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


def test_pipeline_search_route(session, new_pipeline, test_client, app, runner):
    """
    GIVEN calling the route "/pipeline-search"
    WHEN no user is logged in
    AND no filter is used
    THEN should return success code and all pipelines
    """

    session.add(new_pipeline)
    session.commit()

    cli.register(app)
    result = runner.invoke(args=["update_pipeline_data"])

    headers = {'Content-Type': 'application/json'}
    res = test_client.get("/pipeline-search", headers = headers)
    assert res.status_code == 200

    body = res.get_json(force=True)

    assert type(body) != type(None)
    assert body["authorized"] == False
    assert type(body["elements"]) != type(None)
    assert body["total"] > 0

def test_pipeline_search_route_with_filter(session, new_pipeline, test_client):
    """
    GIVEN calling the route "/pipeline-search"
    WHEN no user is logged in
    AND a filter is used
    THEN should return success code and filtered pipelines
    """

    session.add(new_pipeline)
    session.commit()

    query = {'search': 'RandomSearchTerm'}
    headers = {'Content-Type': 'application/json'}
    res = test_client.get("/pipeline-search", headers = headers, query_string = query)
    assert res.status_code == 200

    body = res.get_json(force=True)

    assert type(body) != type(None)
    assert body["authorized"] == False
    assert type(body["elements"]) != type(None)
    assert body["total"] == 0


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
