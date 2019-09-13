# -*- coding: utf-8 -*-
"""Command Line Interface Module

Module that contains the special command line tools

"""
import os
import click
import csv
import configparser
import json
import logging
from pathlib import Path
from datetime import datetime
from app.threads import UpdatePipelineData

logging.basicConfig(format="%(name)s [%(levelname)s]: %(message)s")
logger = logging.getLogger(os.path.basename(__file__))


def register(app):

    @app.cli.command("seed_test_db")
    def seed_test_db():
        from app import db
        from app.models import User, Dataset, DatasetStats

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

            dataset_stats_csvfile = os.path.join(app.root_path, "../test/datasets_stats.csv")
            with open(dataset_stats_csvfile, 'r') as datastat_csv:
                csv_reader = csv.DictReader(datastat_csv)
                for row in csv_reader:
                    dataset_stat = DatasetStats(
                                                dataset_id=row['dataset_id'],
                                                size=row['size'],
                                                files=row['files'],
                                                sources=row['sources'],
                                                num_subjects=row['num_subjects'],
                                                num_downloads=row['num_downloads'],
                                                num_likes=row['num_likes'],
                                                num_views=row['num_views'],
                                                date_updated=datetime.utcnow()
                                                )
                    db.session.add(dataset_stat)

            db.session.commit()

    @app.cli.command("update_datasets")
    def update_datasets():
        from app import db
        from app.models import Dataset
        from sqlalchemy.exc import IntegrityError

        logger.setLevel(app.logger.getEffectiveLevel())

        data_path = app.config.get("DATA_PATH", "static/data/projects").lstrip("/")
        search_path = Path(app.root_path).joinpath(data_path)

        for project in search_path.glob("*"):
            if not project.is_dir():
                continue

            datalad_conf = project.joinpath(".datalad/config")
            dataset_id = _read_config(datalad_conf, "datalad \"dataset\"",
                                      "id")

            git_conf = project.joinpath(".git/config")
            annex_uuid = _read_config(git_conf, "annex", "uuid")

            model = _get_dats_model(project)
            if model:
                description = model.get("description")
                try:
                    download_path = model.get("storedIn").get("name")
                except AttributeError:
                    download_path = None
                name = model.get('title')
                if model.get("types"):
                    modality = ",".join([item.get("value").lower()
                                        for item in model.get("types")
                                        if item.get("value")])
                else:
                    modality = None
                version = model.get("version")
                try:
                    raw_data_url = model.get("distributions").get("access").get(
                            "landingPage")
                except AttributeError:
                    raw_data_url = None
                data_format = _get_formats(model)
                private = model.get("privacy") == "Open Access"
            else:
                description = None
                download_path = None
                raw_data_url = None
                name = None
                modality = None
                version = None
                data_format = None
                is_private = None

            record = Dataset(dataset_id=dataset_id,
                             annex_uuid=annex_uuid,
                             description=description,
                             owner_id=None,
                             download_path=download_path,
                             raw_data_url=raw_data_url,
                             image=None,
                             name=name,
                             modality=modality,
                             version=version,
                             format=data_format,
                             category=None,
                             is_private=private)

            try:
                db.session.add(record)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                query = Dataset.query
                if dataset_id:
                    query = query.filter(Dataset.dataset_id == dataset_id)
                if annex_uuid:
                    query = query.filter(Dataset.annex_uuid == annex_uuid)
                found = query.first()
                found.description = description
                found.download_path = download_path
                found.raw_data_url = raw_data_url
                found.name = name
                found.modality = modality
                found.version = version
                found.format = data_format
                found.is_private = private
                found.date_updated = datetime.utcnow()
                db.session.add(found)
                db.session.commit()

    @app.cli.command('update_pipeline_data')
    def update_pipeline_data():
        thr = UpdatePipelineData(path=os.path.join(os.path.expanduser('-'),
                                 ".cache", "boutiques"))
        thr.start()
        thr.join()


def _read_config(file_path, section, key):
    parser = configparser.ConfigParser(strict=False)
    try:
        parser.read(file_path)
        value = parser[section][key]
    except Exception as e:
        logger.info("Couldnt parse {}.{} from {}. Reason - {} {}".format(
                section, key, file_path, type(e).__name__, e))
        return None
    return value


def _get_dats_model(project):
    dats_file = project.joinpath("DATS.json")
    if not dats_file.is_file():
        dats_file = project.joinpath("dats.json")

    try:
        with dats_file.open() as df:
            model = json.load(df)
    except Exception as e:
        logger.error("Couldnt parse dats model for {}. Reason - {} {}".format(
                project, type(e).__name__, e))
        return None
    return model


def _get_formats(model):
    dists = model.get("distributions")
    if not dists:
        return None

    if type(dists) == list:
        dists = dists[0]

    if not dists.get("formats"):
        return None

    try:
        data_format = ",".join(dists["formats"])
    except TypeError:
        data_format = ",".join([item.get("description") for item in dists["formats"]])

    return data_format
