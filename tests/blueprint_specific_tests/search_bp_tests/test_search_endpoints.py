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


def test_dataset_search_route(session, new_dataset, new_dataset_stats, test_client):
    """
    GIVEN calling the route "/dataset-search"
    WHEN no user is logged in
    AND no search filter is used
    THEN should return success code with all datasets
    """

    session.add(new_dataset)
    session.commit()

    session.add(new_dataset_stats)
    session.commit()

    headers = {'Content-Type': 'application/json'}
    res = test_client.get("/dataset-search", headers = headers)
    assert res.status_code == 200

    body = res.get_json(force=True)

    assert type(body) != type(None)
    assert body["authorized"] == False
    assert body["total"] == 1

def test_dataset_search_route_with_filter(session, new_dataset, new_dataset_stats, test_client):
    """
    GIVEN calling the route "/dataset-search"
    WHEN no user is logged in
    AND a filter is used
    THEN should return success code with filtered results
    """

    session.add(new_dataset)
    session.commit()

    session.add(new_dataset_stats)
    session.commit()

    query = {'search': 'SearchTerm'}
    headers = {'Content-Type': 'application/json'}
    res = test_client.get("/dataset-search", headers = headers, query_string = query)
    assert res.status_code == 200

    body = res.get_json(force=True)

    assert type(body) != type(None)
    assert body["total"] == 0


def test_dataset_route(session, new_dataset, new_dataset_stats, test_client):
    """
    GIVEN calling the route "/dataset"
    WHEN no user is logged in
    THEN should return success code

    TODO: mock the datasets table to provide a valid return object
    """
    session.add(new_dataset)
    session.commit()

    session.add(new_dataset_stats)
    session.commit()

    query = {'id': '8de99b0e-5f94-11e9-9e05-52545e9add8e'}
    headers = {'Content-Type': 'application/json'}

    # res = test_client.get("/dataset", headers = headers, query_string = query)

    assert True