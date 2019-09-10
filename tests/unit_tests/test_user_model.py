# -*- coding: utf-8 -*-
import pytest
from app.models import User
from datetime import datetime, timedelta


@pytest.fixture(scope='module')
def new_user():
    """
    Creates a new mock user for us to test things
    """
    user = User(
                oauth_id="0000-0000-0000-0000",
                username="testuser",
                email="example@mailinator.com",
                affiliation="CONP",
                expiration=datetime.utcnow() + timedelta(days=30)
            )
    user.set_password("ThisPassword")
    return user


def test_new_user(new_user):
    """
    GIVEN a User Model
    WHEN a new User is created
    THEN check the characteristics
    """
    assert new_user.email == "example@mailinator.com"
    assert new_user.username == "testuser"
    assert new_user.password_hash != "THISPassword"
    assert new_user.affiliation == "CONP"


def test_set_password(new_user):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly. and not as plaintext
    """
    new_user.set_password("HorseFeathers")
    assert new_user.password_hash != "HorseFeathers"
    assert new_user.check_password("HorseFeathers")
    assert not new_user.check_password("HorseFeathers2")
    assert not new_user.check_password("THISPassword")


def test_user_db_model(session, new_user):
    """
    GIVEN a User Model
    WHEN a new User is created and injested into DB
    THEN check that the database user is the same
    AND the default values are set correctly
    """
    session.add(new_user)
    session.commit()
    u = User.query.filter(User.id == new_user.id).first()
    assert new_user.id > 0
    assert u == new_user
    # Test that defaults get set now
    assert not u.is_whitelisted
    assert not u.is_pi
    assert not u.is_account_expired
    test_set_password(u)
    session.delete(u)
    session.commit()
    u2 = User.query.filter(User.id == new_user.id).first()
    assert u2 is None
