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
    from app import db
    from app.models import User, Dataset, DatasetStats

    dataset_csvfile = os.path.join(app.root_path, "../test/datasets.csv")
    with open(dataset_csvfile, 'r') as data_csv:
        csv_reader = csv.DictReader(data_csv)
        for row in csv_reader:
            dataset = Dataset(
                dataset_id=row['dataset_id'],
                annex_uuid=row['annex_uuid'],
                description=row['description'],
                owner_id=row['owner_id'],
                download_path=row['download_path'],
                raw_data_url=row['raw_data_url'],
                name=row['name'],
                modality=row['modality'],
                version=row['version'],
                format=row['format'],
                category=row['category'],
                date_created=datetime.utcnow(),
                date_updated=datetime.utcnow(),
                is_private=row['is_private'] == 'True'
            )

            db.session.add(dataset)
        db.session.commit()

        dataset_stats_csvfile = os.path.join(
            app.root_path, "../test/datasets_stats.csv")
        with open(dataset_stats_csvfile, 'r') as datastat_csv:
            csv_reader = csv.DictReader(datastat_csv)
            for row in csv_reader:
                dataset_id = Dataset.query.filter_by(dataset_id=row['dataset_id']).first().id
                dataset_stat = DatasetStats(
                    dataset_id=row['dataset_id'],
                    size=row['size'],
                    files=row['files'],
                    sources=row['sources'],
                    num_subjects=row['num_subjects'],
                    num_downloads=row['num_downloads'],
                    num_likes=row['num_likes'],
                    num_views=row['num_views'],
                    date_updated=datetime.utcnow(),
                    fk_dataset_id=dataset_id
                )
                db.session.add(dataset_stat)

        db.session.commit()


def _update_pipeline_data(app):
    """
    Updates from Zenodo the available pipelines
    """
    thr = UpdatePipelineData(path=os.path.join(os.path.expanduser('-'),
                                               ".cache", "boutiques"))
    thr.start()
    thr.join()
