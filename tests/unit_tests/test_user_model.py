# -*- coding: utf-8 -*-
import pytest
from app.models import User, Role,UsersRoles, AffiliationType
from datetime import datetime, timedelta

def test_new_user(session, new_user, new_affiliation_type, app):
    """
    GIVEN a User Model
    WHEN a new User is created
    THEN check the characteristics
    """
    assert new_user.email == "example@mailinator.com"
    assert new_user.full_name=="Example User"
    assert new_user.password != "THISPassword"
    assert new_user.affiliation == "CONP"
    assert new_user.affiliation_type is not None
    assert new_user.affiliation_type == new_affiliation_type
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
    assert u.affiliation_type is not None
    assert u.affiliation_type == AffiliationType.query.filter(
                                 AffiliationType.name == "PR").first()

    assert u.has_role("member")
    session.delete(u)
    session.commit()
    u2 = User.query.filter(User.id == new_user.id).first()
    assert u2 is None
