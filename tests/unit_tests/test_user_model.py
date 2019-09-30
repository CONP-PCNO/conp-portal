# -*- coding: utf-8 -*-
import pytest
from app.models import User, Role,UsersRoles
from datetime import datetime, timedelta

@pytest.fixture(scope='function')
def test_new_user(new_user):
    """
    GIVEN a User Model
    WHEN a new User is created
    THEN check the characteristics
    """
    assert new_user.email == "example@mailinator.com"
    assert new_user.full_name=="Example User"
    assert new_user.password != "THISPassword"
    assert new_user.affiliation == "CONP"
    assert app.user_manager.verify_password("ThisPassword",new_user.password)

def test_user_db_model(session, new_user):
    """
    GIVEN a User Model
    WHEN a new User is created and injested into DB
    THEN check that the database user is the same
    AND the default values are set correctly
    """
    session.add(new_user)
    ## have to mock the event.listener which won't get called here
    new_user.before_commit(session)
    session.commit()
    u = User.query.filter(User.id == new_user.id).first()
    assert new_user.id > 0
    assert u.full_name == new_user.full_name
    assert u.affiliation == new_user.affiliation
    assert u.has_role("member")
    session.delete(u)
    session.commit()
    u2 = User.query.filter(User.id == new_user.id).first()
    assert u2 is None
