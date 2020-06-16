# -*- coding: utf-8 -*-
import pytest
from app.models import Dataset
from datetime import datetime, timedelta


def test_new_dataset(new_dataset):
    """
    GIVEN a Dataset Model
    WHEN a new Dataset is create
    THEN check the characteristics
    """
    assert new_dataset.dataset_id == "8de99b0e-5f94-11e9-9e05-52545e9add8e"
    assert new_dataset.description == "Human Brain phantom scans, Multiple MRI"\
                                      " scans of a single human phantom over 11"\
                                      " years, T1 weighted images and others on"\
                                      " 13 scanner in 6 sites accross North America."\
                                      " The data are available in minc format"
    assert new_dataset.name == "Multicenter Single Subject Human MRI Phantom"
    assert new_dataset.version == "1.0"
    assert not new_dataset.is_private
    assert new_dataset.fspath == './test/test_dataset'


def test_dataset_db_model(session, new_dataset):
    """
    GIVEN a Dataset Model
    WHEN a new Dataset is created and injested into DB
    THEN check that the database dataset is the same
    AND the default values are set correctly
    """
    session.add(new_dataset)
    session.commit()
    assert new_dataset.id > 0
    d = Dataset.query.filter(Dataset.id == new_dataset.id).first()
    assert d == new_dataset
    # Also test defaults
    assert (datetime.now() - d.date_created).total_seconds() < 3600
    assert (datetime.now() - d.date_updated).total_seconds() < 3600
    session.delete(d)
    session.commit()
    d2 = Dataset.query.filter(Dataset.id == new_dataset.id).first()
    assert d2 is None
