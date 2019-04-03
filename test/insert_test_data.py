import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


import csv
from datetime import datetime, timedelta
from app.models import User, Dataset, DatasetStats, Pipeline
from app import db

class InsertTestDataset(object):

    def __init__(self):
        self.users_file = 'users.csv'
        self.datasets_file = 'datasets.csv'
        self.datasets_stats_file = 'datasets_stats.csv'
        self.pipelines_file = 'pipelines.csv'

    def insert_sample_users(self):

        with open(self.users_file, 'r') as users_file:

            reader = csv.reader(users_file)
            next(reader)

            for row in reader:
                user = User(
                    id = row[0],
                    oauth_id = row[1],
                    username = row[2],
                    email = row[3],
                    is_whitelisted = row[4] == 'True',
                    is_pi = row[5] == 'True',
                    is_account_expired = row[6] == 'True',
                    affiliation = row[7],
                    expiration = datetime.now() + timedelta(6*365/12), # 6 months
                    date_created = datetime.now(),
                    date_updated = datetime.now()
                )
                user.set_password('p4ssword')
                db.session.add(user)
        db.session.commit()
        users_file.close()


    def insert_sample_datasets(self):

        with open(self.datasets_file, 'r') as dataset_file:
            reader = csv.reader(dataset_file)
            next(reader)

            for row in reader:
                dataset = Dataset(
                    id = row[0],
                    dataset_id = row[1],
                    owner_id = row[2],
                    name = row[3],
                    modality = row[4],
                    version = row[5],
                    format = row[6],
                    category = row[7],
                    date_created = datetime.now(),
                    date_updated = datetime.now(),
                    is_private = row[8] == 'True'
                )
                db.session.add(dataset)
        db.session.commit()
        dataset_file.close()

    def insert_sample_datasets_stats(self):

        with open(self.datasets_stats_file, 'r') as dataset_stats_file:

            reader = csv.reader(dataset_stats_file)
            next(reader)

            for row in reader:
                stat = DatasetStats(
                    id = row[0],
                    dataset_id = row[1],
                    size = row[2],
                    files = row[3],
                    sources = row[4],
                    num_subjects = row[5],
                    num_downloads = row[6],
                    num_likes = row[7],
                    num_views = row[8],
                    date_updated = datetime.now()
                )
                db.session.add(stat)
        db.session.commit()
        dataset_stats_file.close()

    def insert_sample_pipelines(self):

        with open(self.pipelines_file, 'r') as pipelines_file:

            reader = csv.reader(pipelines_file)
            next(reader)

            for row in reader:
                pipeline = Pipeline(
                    id = row[0],
                    pipeline_id = row[1],
                    owner_id = row[2],
                    name = row[3],
                    version = row[4],
                    is_private = row[5] == 'True',
                    date_created = datetime.now(),
                    date_updated = datetime.now()
                )
                db.session.add(pipeline)
        db.session.commit()
        pipelines_file.close()



test_dataset = InsertTestDataset()
#test_dataset.insert_sample_users()
#test_dataset.insert_sample_datasets()
#test_dataset.insert_sample_datasets_stats()
test_dataset.insert_sample_pipelines()


