"""
Unit tests for endpoints in the main blueprint
"""

def test_index_route(test_client):
    """
    TEST the main route
    """
    res = test_client.get("/index", follow_redirects=False)
    assert res.status_code == 200
