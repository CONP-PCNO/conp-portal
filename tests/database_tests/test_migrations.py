# -*- coding: utf-8 -*-
"""
Tests for Database setups
"""
import pytest
import os
from app import db,cli
from alembic.command import upgrade
from alembic.config import Config as alem_Config
from app.models import Dataset


def test_db_migration(app,db):
  """
  TEST the current set of db migrations
  """
  ALEMBIC_CONFIG = os.path.join(app.root_path,"../migrations/alembic.ini")
  assert os.path.exists(ALEMBIC_CONFIG)

  config = alem_Config(ALEMBIC_CONFIG)
  config.set_main_option("script_location",
                         os.path.join(app.root_path,
                                      "../migrations"))
  db.drop_all()
  ## if there is a problem, this will not be None
  is_success = True
  try:
    upgrade(config,'head')
  except Exception as e:
    is_success = False
    ### Need to reset so other tests are not effected
    ### I am sure that I am doing this wrong.
    db.drop_all()
    db.create_all()
    print("Alembic Migraiton failed: {}".format(e))

  assert is_success == True

def test_seed_db_test(app,session,runner):
  """
  TEST to test the initialization of the database
  """
  cli.register(app)
  result = runner.invoke(args=["seed_test_db"])
  d = Dataset.query.filter(Dataset.dataset_id=="8de99b0e-5f94-11e9-9e05-52545e9add8e").first()
  assert d.name == "Multicenter Single Subject Human MRI Phantom"
  #assert False
