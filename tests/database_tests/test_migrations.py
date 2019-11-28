# -*- coding: utf-8 -*-
"""
Tests for Database setups
"""
import pytest
import os
from alembic.command import upgrade
from alembic.config import Config as alem_Config
from app.models import Dataset, User, AffiliationType, Role, UsersRoles
import app.cli as cli


def test_db_migration(app, db, session):
    """
    TEST the current set of db migrations
    """
    ALEMBIC_CONFIG = os.path.join(app.root_path, "../migrations/alembic.ini")
    assert os.path.exists(ALEMBIC_CONFIG)

    config = alem_Config(ALEMBIC_CONFIG)
    config.set_main_option("script_location",
                           os.path.join(app.root_path,
                                        "../migrations"))
    db.drop_all()
    # if there is a problem, this will not be None
    is_success = True
    try:
        upgrade(config, 'head')
    except Exception as e:
        is_success = False
        # Need to reset so other tests are not effected
        # I am sure that I am doing this wrong.
        db.drop_all()
        db.create_all()
        print("Alembic Migraiton failed: {}".format(e))

    assert is_success


def test_seed_db_test(app, session, runner):
    """
    TEST to test the initialization of the database
    """
    cli.register(app)
    result = runner.invoke(args=["seed_test_db"])
    d = Dataset.query.filter(Dataset.dataset_id ==
                             "8de99b0e-5f94-11e9-9e05-52545e9add8e").first()
    assert d.name == "Multicenter Single Subject Human MRI Phantom"
    ats = AffiliationType.query.all()

    assert ats[0].name == "PI"
    assert ats[0].label == "Principal Investigator (Professor)"
    assert ats[-1].name == "OT"
    assert ats[-1].label == "Other"
    u = User.query.filter(User.full_name=="CONP Admin").first()
    print ("------- {}".format(u))
    assert u.full_name == "CONP Admin"
    assert u.email == app.config['ADMINS'][0]
    assert u.affiliation == 'CONP'
    assert u.affiliation_type_key() == "OT"

    session.query(User).delete()
    session.query(Role).delete()
    session.query(UsersRoles).delete()
    session.query(AffiliationType).delete()
    session.query(Dataset).delete()
    session.commit()


def test_seed_test_datasets_db(app,session,runner):
    cli.register(app)
    result = runner.invoke(args=["seed_test_datasets_db"])
    d = Dataset.query.filter(Dataset.dataset_id ==
                             "8de99b0e-5f94-11e9-9e05-52545e9add8e").first()
    assert d.name == "Multicenter Single Subject Human MRI Phantom"
    session.query(Dataset).delete()
    session.commit()

def test_seed_aff_type_db(app, session,runner):
    """
    TEST to test the initialization of the affiliation types
    """
    cli.register(app)
    result = runner.invoke(args=['seed_aff_types_db'])
    ats = AffiliationType.query.all()

    assert ats[0].name == "PI"
    assert ats[0].label == "Principal Investigator (Professor)"
    assert ats[-1].name == "OT"
    assert ats[-1].label == "Other"
    session.query(AffiliationType).delete()

def test_seed_admin_acct(app, session, runner):
    """
    TEST to test the initialization of the admin account
    """
    cli.register(app)
    result1 = runner.invoke(args=['seed_aff_types_db'])
    result2 = runner.invoke(args=['seed_admin_acct_db'])
    u = User.query.filter(User.full_name=="CONP Admin").first()
    print ("------- {}".format(u))
    assert u.full_name == "CONP Admin"
    assert u.email == app.config['ADMINS'][0]
    assert u.affiliation == 'CONP'
    assert u.affiliation_type_key() == "OT"
    session.query(User).delete()
    session.query(Role).delete()
    session.query(UsersRoles).delete()
    session.query(AffiliationType).delete()
    session.commit()

