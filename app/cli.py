# -*- coding: utf-8 -*-
"""Command Line Interface Module

Module that contains the special command line tools

"""
import os
import click
import csv
from datetime import datetime, timedelta
from pytz import timezone
from app.threads import UpdatePipelineData


def register(app):
    @app.cli.command('seed_aff_types_db')
    def seed_aff_types_db():
        """
        Wrapper to call seeding the affiliation types
        """
        _seed_aff_types_db(app)

    @app.cli.command('seed_admin_acct_db')
    def seed_admin_acct_db():
        """
        Wrapper to call seeding the administration account
        """
        _seed_admin_acct_db(app)

    @app.cli.command("seed_test_datasets_db")
    def seed_test_datasets_db():
        """
        Wrapper to call the seeding of static test datasets
        """
        _seed_test_datasets_db(app)

    @app.cli.command("seed_test_db")
    def seed_test_db():
        """
        Wrapper to call the seeding of the test database
        """
        _seed_aff_types_db(app)
        _seed_admin_acct_db(app)
        _seed_test_datasets_db(app)

    @app.cli.command('update_pipeline_data')
    def update_pipeline_data():
        """
        Wrapper to call the updating to the pipeline data
        """
        _update_pipeline_data(app)

    @app.cli.command('update_datasets_metadata')
    def update_datasets_metadata():
        """
        Wrapper to call the updating to the datasets metadata
        """
        _update_datasets_metadata(app)

def _seed_aff_types_db(app):
    """
    Seeds the inital affiliation types
    """
    from app import db
    from app.models import AffiliationType

    for x, y in [
        ("PI", "Principal Investigator (Professor)"),
        ("RA", "Research Associate"),
        ("PD", "Post-Doctoral Fellow"),
        ("PS", "PhD Candidate"),
        ("MS", "Masters Student"),
        ("US", "Undergraduate Student"),
        ("IS", "Informatics Specialist"),
        ("CO", "Commercial Company"),
        ("OT", "Other")
    ]:
        # Check if already there
        if len(AffiliationType.query.filter(AffiliationType.name == x,
                                            AffiliationType.label == y).all()) == 0:
            at = AffiliationType(name=x, label=y)
            db.session.add(at)

    db.session.commit()


def _seed_admin_acct_db(app):
    """
    Seeds an administrator account
    Uses Config Paramters for determining Admin account
    """
    from app import db
    from app.models import User, Role, AffiliationType

    # Do not perform is the user already exists
    if len(User.query.filter(User.full_name == "CONP Admin").all()) == 0:
        print("Creating Admin User")
        # create an admin user (Not useful now, but at least we will have a user)
        user = User(
            email=app.config['ADMINS'][0],
            email_confirmed_at=datetime.utcnow(),
            password=app.user_manager.hash_password('TestPW!'),
            active=True,
            full_name='CONP Admin',
            affiliation='CONP',
            expiration=datetime.utcnow() + timedelta(days=365),
            date_created=datetime.utcnow(),
            date_updated=datetime.utcnow()
        )
        user.affiliation_type = AffiliationType.query.filter(
            AffiliationType.name == "OT").first()

        user.roles.append(Role(name='admin'))
        user.roles.append(Role(name='member'))

        db.session.add(user)
        db.session.commit()


def _seed_test_datasets_db(app):
    """
    Seeds a set of test datasets populated from a static csv file
    """
    _update_datasets_metadata(app)

def _update_pipeline_data(app):
    """
    Updates from Zenodo the available pipelines
    """
    thr = UpdatePipelineData(path=os.path.join(os.path.expanduser('~'),
                                               ".cache", "boutiques"))
    thr.start()
    thr.join()

def _update_datasets_metadata(app):
    """
    Updates from Zenodo the available pipelines
    """
    from app import db, config
    from app.models import Dataset as DBDataset
    from datalad import api
    from datalad.api import Dataset as DataladDataset
    import fnmatch
    import json

    datasetspath = app.config['DATA_PATH']

    d = DataladDataset(path=datasetspath + '/conp-dataset')
    if not d.is_installed():
        api.clone(source='http://github.com/CONP-PCNO/conp-dataset', path=datasetspath + '/conp-dataset')
        d = DataladDataset(path=datasetspath + '/conp-dataset')
        d.install(path='', recursive=True)
    
    try:
       d.update(path='')
    except Exception as e:
       print("An exception occurred in datalad update")
       print(e.args)
       
    
    for ds in d.subdatasets():
        subdataset = DataladDataset(path=ds['path'])
        if not subdataset.is_installed():
            subdataset.install(path='')

        dirs = os.listdir(ds['path'])
        descriptor = ''
        for file in dirs:
            if fnmatch.fnmatch(file.lower(), 'dats.json'):
                descriptor = file
        if descriptor == '':
            print('DATS.json file can`t be found in ' + ds['path'])
            continue

        with open(ds['path'] + '/' + descriptor, 'r') as f:
            dats = json.load(f)

        # use dats.json data to fill the datasets table
        # avoid duplication / REPLACE instead of insert
        dataset = DBDataset.query.filter_by(dataset_id=ds['gitmodule_name']).first()
        if dataset is None:
            dataset = DBDataset()
            dataset.date_created = datetime.utcnow()

        print(ds)
        dataset.dataset_id = ds.id
        dataset.download_path = ds['path'] + '/' + descriptor
        dataset.date_updated = datetime.utcnow()
        dataset.description = dats['description']
        dataset.name = dats['title']
        dataset.raw_data_url = ds['path'] 
        
        db.session.merge(dataset)
        print(ds['gitmodule_name'] + ' updated.')

    db.session.commit()
