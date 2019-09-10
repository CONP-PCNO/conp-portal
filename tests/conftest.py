# -*- coding: utf-8 -*-
"""
This is the initial module that contains the pytest configuration fixtures
"""
import pytest
import os
from app import create_app
from app import db as _db
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from config import TestingConfig

@pytest.fixture(scope='session')
def app(request):
  """
  This is creates the mock app for testing, it uses the
  TestingConfig in Config.py
  """
  app = create_app(config_settings=TestingConfig)
  ctx = app.app_context()
  ctx.push()

  def teardown():
    ctx.pop()

  request.addfinalizer(teardown)
  return app

@pytest.fixture(scope='session')
def db(app, request):
  """
  This is creates the test db
  """
  test_db_file = app.config['SQLALCHEMY_DATABASE_URI'].split(":///")[1]

  if os.path.exists(test_db_file):
    os.unlink(test_db_file)

  def teardown():
    _db.drop_all()
    os.unlink(test_db_file)

  _db.app = app
  _db.create_all()

  request.addfinalizer(teardown)
  return _db

@pytest.fixture(scope='function')
def session(db, request):
  """
  This creates a mock session
  """
  connection = db.engine.connect()
  transaction = connection.begin()

  options = dict(bind=connection)
  session = db.create_scoped_session(options=options)

  db.session = session

  def teardown():
    session.close()
    transaction.rollback()
    connection.close()

  request.addfinalizer(teardown)
  return session

@pytest.fixture(scope='function')
def test_client(app):
  return app.test_client()

@pytest.fixture()
def runner(app):
  return app.test_cli_runner()


