"""
Unit tests for endpoints in the profile blueprint
"""
from datetime import datetime
from urllib.parse import urlparse

from flask import render_template, url_for
from flask_login import login_user
from flask_security import hash_password

from app.models import Role, User


def test_pipelines_route(app, test_client):
    """
    GIVEN calling the route "/profile"
    WHEN no user is logged in
    THEN should return success code
    """
    with app.test_request_context():
        profile_url = url_for('profile.current_user_profile_page')
        login_url = url_for("user.login")

    res = test_client.get(profile_url, follow_redirects=False)
    assert res.status_code == 302
    assert urlparse(res.location).path == urlparse(login_url).path

    res = test_client.get(profile_url, follow_redirects=True)
    assert res.status_code==200


def test_admin_edit_user_profile_redirects_when_user_id_is_missing(
    app, test_client, session, monkeypatch
):
    monkeypatch.setitem(app.config, "WTF_CSRF_ENABLED", False)
    admin = User(
        email="admin-profile-test@example.com",
        password=hash_password("test-password"),
        active=True,
        email_confirmed_at=datetime.now(),
        full_name="Profile Test Admin",
    )
    admin.roles.append(Role(name="admin"))
    session.add(admin)
    session.commit()

    login = test_client.post(
        url_for("user.login"),
        data={"email": admin.email, "password": "test-password"},
    )
    assert login.status_code == 302

    response = test_client.get(
        url_for("profile.admin_user_profile_page"),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert urlparse(response.location).path == urlparse(url_for("main.index")).path


def test_navigation_has_csrf_protected_logout_for_authenticated_user(app, session):
    admin = User(
        email="navigation-logout-test@example.com",
        password=hash_password("test-password"),
        active=True,
        full_name="Navigation Test User",
    )
    session.add(admin)
    session.commit()

    with app.test_request_context("/"):
        login_user(admin)
        html = render_template("fragments/navigation_bar.html")

    assert 'action="/logout"' in html
    assert 'name="csrf_token"' in html
    assert ">Logout</button>" in "".join(html.split())
