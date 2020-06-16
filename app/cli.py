# -*- coding: utf-8 -*-
"""Command Line Interface Module

Module that contains the special command line tools

"""
import os
import click
import csv
import uuid
from datetime import datetime, timedelta
from pytz import timezone
from app.threads import UpdatePipelineData
from app.search.models import DATSDataset


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

    @app.cli.command('update_datasets')
    def update_datasets():
        """
        Wrapper to call the updating to the datasets metadata
        """
        _update_datasets(app)


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
    _update_datasets(app)


def _update_pipeline_data(app):
    """
    Updates from Zenodo the available pipelines
    """
    t = UpdatePipelineData()
    t.start()
    t.join()


def _update_datasets(app):
    """
    Updates from conp-datasets
    """
    from app import db, config
    from app.models import Dataset as DBDataset
    from app.models import DatasetAncestry as DBDatasetAncestry
    from datalad import api
    from datalad.api import Dataset as DataladDataset
    import fnmatch
    import json
    from pathlib import Path
    import git

    datasetsdir = Path(app.config['DATA_PATH']) / 'conp-dataset'
    datasetsdir.mkdir(parents=True, exist_ok=True)

    # Initialize the git repository object
    try:
        repo = git.Repo(datasetsdir)
    except git.exc.InvalidGitRepositoryError as e:
        repo = git.Repo.clone_from(
            'https://github.com/CONP-PCNO/conp-dataset',
            datasetsdir,
            branch='master'
        )

    # Update to latest commit
    origin = repo.remotes.origin
    origin.pull('master')
    repo.submodule_update(recursive=False, keep_going=True)

    d = DataladDataset(path=datasetsdir)
    if not d.is_installed():
        api.clone(
            source='https://github.com/CONP-PCNO/conp-dataset',
            path=datasetsdir
        )
        d = DataladDataset(path=datasetsdir)

    try:
        d.install(path='', recursive=True)
    except Exception as e:
        print("\033[91m")
        print("[ERROR  ] An exception occurred in datalad update.")
        print(e.args)
        print("\033[0m")
        return

    print('[INFO   ] conp-dataset update complete')
    print('[INFO   ] Updating subdatasets')

    for ds in d.subdatasets():
        print('[INFO   ] Updating ' + ds['gitmodule_url'])
        subdataset = DataladDataset(path=ds['path'])
        if not subdataset.is_installed():
            try:
                api.clone(
                    source=ds['gitmodule_url'],
                    path=ds['path']
                )
                subdataset = DataladDataset(path=ds['path'])
                subdataset.install(path='')
            except Exception as e:
                print("\033[91m")
                print(
                    "[ERROR  ] An exception occurred in datalad install for " + str(ds) + ".")
                print(e.args)
                print("\033[0m")
                continue

        dirs = os.listdir(ds['path'])
        descriptor = ''
        for file in dirs:
            if fnmatch.fnmatch(file.lower(), 'dats.json'):
                descriptor = file

        if descriptor == '':
            print("\033[91m")
            print('[ERROR  ] DATS.json file can`t be found in ' + ds['path'] + ".")
            print("\033[0m")
            continue

        try:
            with open(os.path.join(ds['path'], descriptor), 'r') as f:
                dats = json.load(f)
        except Exception as e:
            print("\033[91m")
            print("[ERROR  ] Descriptor file can't be read.")
            print(e.args)
            print("\033[0m")
            continue

        # use dats.json data to fill the datasets table
        # avoid duplication / REPLACE instead of insert
        dataset = DBDataset.query.filter_by(
            dataset_id=ds['gitmodule_name']).first()

        # pull the timestamp of the first commit in the git log for the dataset
        createTimeStamp = os.popen(
            "git -C {} log --pretty=format:%ct --reverse | head -1".format(ds['path'])).read()
        try:
            createDate = datetime.fromtimestamp(int(createTimeStamp))
        except ValueError:
            createDate = datetime.utcnow()

        if dataset is None:
            dataset = DBDataset()
            dataset.dataset_id = ds['gitmodule_name']
            dataset.date_created = createDate

        if(dataset.date_created != createDate):
            dataset.date_created = createDate

        # check for dataset ancestry
        extraprops = dats.get('extraProperties', [])
        for prop in extraprops:
            if prop.get('category') == 'derivedFrom':
                for x in prop.get('values', []):
                    if x.get('parent_dataset_id', None) is None:
                        continue
                    datasetAncestry = DBDatasetAncestry()
                    datasetAncestry.id = str(uuid.uuid4())
                    datasetAncestry.parent_dataset_id = 'projects/' + x.get('parent_dataset_id', None)
                    datasetAncestry.child_dataset_id = dataset.dataset_id
                    db.session.merge(datasetAncestry)

        dataset.date_updated = datetime.utcnow()
        dataset.fspath = ds['path']
        dataset.description = dats.get(
            'description', 'No description in DATS.json')
        dataset.name = dats.get(
            'title',
            os.path.basename(dataset.dataset_id)
        )

        db.session.merge(dataset)
        db.session.commit()
        print('[INFO   ] ' + ds['gitmodule_name'] + ' updated.')
