# -*- coding: utf-8 -*-
"""Command Line Interface Module

Module that contains the special command line tools

"""
import os
import click
import csv
from datetime import datetime
from app.threads import UpdatePipelineData


def register(app):

    @app.cli.command("seed_test_db")
    def seed_test_db():
        from app import db
        from app.models import User, Dataset

        # create an admin user (Not useful now, but at least we will have a user)

        # import the current dataset information (to be replaced by dyanmic process)
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

            dataset_stats_csvfile = os.path.join(app.root_path, "../test/datasets_stats.csv")
            with open(dataset_stats_csvfile, 'r') as datastat_csv:
                csv_reader = csv.DictReader(datastat_csv)
                for row in csv_reader:
                    dataset = Dataset.query.filter_by(dataset_id=row['dataset_id']).first()
                    dataset.size=row['size']
                    dataset.files=row['files']
                    dataset.sources=row['sources']
                    dataset.num_subjects=row['num_subjects']
                    dataset.num_downloads=row['num_downloads']
                    dataset.num_likes=row['num_likes']
                    dataset.num_views=row['num_views']

                    db.session.commit()


    @app.cli.command('update_pipeline_data')
    def update_pipeline_data():
        thr = UpdatePipelineData(path=os.path.join(os.path.expanduser('-'),
                                 ".cache", "boutiques"))
        thr.start()
        thr.join()
