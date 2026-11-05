"""
Unit tests for endpoints in the auth blueprint
"""
import re
from urllib.parse import urlparse

from flask import url_for
from flask_security import verify_password
import pytest

from app.models import AffiliationType, User


@pytest.mark.parametrize("security_salt", ["", "production-secret-key"])
def test_production_requires_distinct_security_salt(security_salt):
    """
    GIVEN production configuration without a dedicated password salt
    WHEN the application is created
    THEN startup fails instead of reusing SECRET_KEY
    """
    from app import create_app
    from config import ProductionConfig

    class MissingPasswordSaltConfig(ProductionConfig):
        SECRET_KEY = "production-secret-key"
        SECURITY_PASSWORD_SALT = security_salt

    with pytest.raises(RuntimeError, match="distinct from SECRET_KEY"):
        create_app(config_settings=MissingPasswordSaltConfig)


def test_login_route(app, test_client):
    """
    GIVEN calling the route "/login"
    WHEN no user is logged in
    THEN should return success code
    """
    with app.test_request_context():
        login_url = url_for('user.login')
    res = test_client.get(login_url)
    assert res.status_code == 200


def test_registration_route(db, test_client):
    """
    GIVEN an unregistered visitor
    WHEN they open the registration page
    THEN the custom account fields are rendered
    """
    response = test_client.get(url_for('user.register'))
    forgot_password = test_client.get(url_for('user.forgot_password'))
    resend_confirmation = test_client.get(url_for('user.send_confirmation'))

    assert response.status_code == 200
    assert forgot_password.status_code == 200
    assert resend_confirmation.status_code == 200
    assert b'name="full_name"' in response.data
    assert b'name="affiliation_type"' in response.data
    assert b'name="password_confirm"' in response.data
    assert b'name="agreeToTerms"' in response.data


def test_registration_confirmation_and_password_reset(app, db, test_client, monkeypatch):
    """
    GIVEN a visitor registering for an account
    WHEN they confirm their email and request a password reset
    THEN confirmation and reset messages contain working tokens
    """
    monkeypatch.setitem(app.config, "WTF_CSRF_ENABLED", False)
    affiliation_type = AffiliationType(name="AUTH-TEST", label="Auth test")
    db.session.add(affiliation_type)
    db.session.commit()

    mail = app.extensions["mail"]
    with mail.record_messages() as outbox:
        registration = test_client.post(
            url_for("user.register"),
            data={
                "email": "security-migration@example.com",
                "full_name": "Security Migration",
                "affiliation": "CONP",
                "affiliation_type": affiliation_type.id,
                "password": "InitialPassword123!",
                "password_confirm": "InitialPassword123!",
                "agreeToTerms": "y",
            },
        )
        assert registration.status_code == 302
        assert registration.headers["Location"].endswith("/user/confirmation_sent")
        user = User.query.filter_by(
            email="security-migration@example.com"
        ).one()
        assert user.confirmed_at is None
        assert user.has_role("member")
        assert len(outbox) == 1
        confirmation_url = re.search(
            r"https?://[^\s<>]+/confirm/[^\s<>]+", outbox[0].body
        ).group().rstrip(").,")

        confirmation = test_client.get(urlparse(confirmation_url).path)
        assert confirmation.status_code == 302
        assert user.confirmed_at is not None

        reset_request = test_client.post(
            url_for("user.forgot_password"),
            data={"email": "security-migration@example.com"},
        )
        assert reset_request.status_code == 200
        assert len(outbox) == 2
        reset_url = re.search(
            r"https?://[^\s<>]+/reset/[^\s<>]+", outbox[1].body
        ).group().rstrip(").,")

        reset_form = test_client.get(urlparse(reset_url).path)
        assert reset_form.status_code == 200
        assert b'name="password_confirm"' in reset_form.data
        password_reset = test_client.post(
            urlparse(reset_url).path,
            data={
                "password": "ReplacementPassword456!",
                "password_confirm": "ReplacementPassword456!",
            },
        )
        assert password_reset.status_code == 302
        assert verify_password("ReplacementPassword456!", user.password)

    test_client.post(url_for("user.logout"))
    db.session.delete(user)
    db.session.delete(affiliation_type)
    db.session.commit()
