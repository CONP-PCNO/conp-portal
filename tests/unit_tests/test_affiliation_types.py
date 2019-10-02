# -*- coding: utf-8 -*-
import pytest
from app.models import User, AffiliationType
from datetime import datetime, timedelta

def test_new_affiliation_type(new_affiliation_type):
    """
    GIVEN an AffiliationType model
    WHEN a new AffiliationType is created
    THEN check the characteristics
    """

    assert new_affiliation_type.name == "PR"
    assert new_affiliation_type.label == "Professor"

def test_affiliation_type_db_model(session, new_affiliation_type):
    """
    GIVEN an AffiliationType model
    WHEN a new AffiliationType is created and injested
    THEN check the characteristics
    """
    session.add(new_affiliation_type)
    session.commit()

    aft = AffiliationType.query.filter(AffiliationType.id == new_affiliation_type.id).first()
    assert new_affiliation_type.id > 0
    assert aft.name == "PR"
    assert aft.label == "Professor"
    session.delete(aft)
    session.commit()
    aft2 = AffiliationType.query.filter(AffiliationType.id == new_affiliation_type.id).first()
    assert aft2 is None
