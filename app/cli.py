# -*- coding: utf-8 -*-
"""Command Line Interface Module

Module that contains the special command line tools

"""
import os
import uuid
import shutil
from datetime import datetime, timedelta
from typing import Type

from app import db
from app.models import Experiment as DBExperiment, Dataset as DBDataset
from app.threads import UpdatePipelineData

from . import config

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
    
    @app.cli.command("seed_test_experiments")
    def seed_test_experiments():
        _update_experiments(app)
    
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

    @app.cli.command('update_analytics')
    def update_analytics():
        """
        Wrapper to call the update of the analytics tables
        """
        _update_analytics(app)

    @app.cli.command('generate_missing_ark_ids')
    def generate_missing_ark_ids():
        """
        Wrapper to generate missing ARK identifiers
        """
        _generate_missing_ark_ids(app)


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

    _generate_missing_ark_ids(app)


def _update_datalad_objects(
        app,
        object_type: str,  # 'dataset' or 'experiment'
        repo_name: str,
        object_class: Type[db.Model]
    ):
    from app.models import ArkId
    from app.models import DatasetAncestry as DBDatasetAncestry
    from sqlalchemy import exc
    from datalad import api
    from datalad.api import Dataset as DataladDataset
    import fnmatch
    import json
    from pathlib import Path
    import git
    import traceback

    datasetsdir = Path(app.config['DATA_PATH']) / repo_name
    datasetsdir.mkdir(parents=True, exist_ok=True)

    # Initialize the git repository object
    try:
        repo = git.Repo(datasetsdir)
    except git.exc.InvalidGitRepositoryError:
        repo = git.Repo.clone_from(
            f'https://github.com/CONP-PCNO/{repo_name}',
            datasetsdir,
            branch='master'
        )

    # Update to latest commit
    origin = repo.remotes.origin
    origin.pull('master')
    repo.submodule_update(recursive=True, force_reset=True, force_remove=True, keep_going=True)

    d = DataladDataset(path=datasetsdir)
    if not d.is_installed():
        api.clone(
            source=f'https://github.com/CONP-PCNO/{repo_name}',
            path=datasetsdir
        )
        d = DataladDataset(path=datasetsdir)

    try:
        d.install(path='', recursive=True)
    except Exception as e:
        print("\033[91m")
        print("[ERROR  ] An exception occurred in datalad update.")
        print(e.args)
        print(traceback.format_exc())
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

        # The following relates to the DATS.json files
        # of the projects directory in the conp-dataset repo.
        # Skip directories that aren't projects.
        patterns = [app.config['DATA_PATH'] + f'/{repo_name}/projects/*']
        if not any(fnmatch.fnmatch(ds['path'], pattern) for pattern in patterns):
            print(f"[ERROR  ] No matching dataset found for {ds['path']}, {patterns}")
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
        dataset = object_class.query.filter_by(
            **{f"{object_type}_id": ds['gitmodule_name']}
        ).first()

        # pull the timestamp of the first commit in the git log for the dataset create date
        createDate = datetime.utcnow()
        try:
            createTimeStamp = os.popen(
                "git -C {} log --pretty=format:%ct --reverse | head -1".format(ds['path'])).read()
            createDate = datetime.fromtimestamp(int(createTimeStamp))
        except Exception:
            print("[ERROR  ] Create Date couldnt be read.")

        firstMergeDate = datetime.utcnow()
        try:
            firstMergeTimeStamp = os.popen(
                "git -C {} log --pretty=format:%ct --reverse {} | head -1".format(
                    app.config['DATA_PATH'] + f"/{repo_name}",
                    ds['path']
                )).read()
            firstMergeDate = datetime.fromtimestamp(int(firstMergeTimeStamp))
        except Exception:
            print("[ERROR  ] First merge date of the submodule dataset could not be read.")

        # last commit in the git log for the dataset update date
        updateDate = datetime.utcnow()
        try:
            createTimeStamp = os.popen(
                "git -C {} log --pretty=format:%ct | head -1".format(ds['path'])).read()
            updateDate = datetime.fromtimestamp(int(createTimeStamp))
        except Exception:
            print("[ERROR  ] Update Date couldnt be read.")

        # get the remote URL
        remoteUrl = None
        try:
            remoteUrl = os.popen(
                "git -C {} config --get remote.origin.url".format(ds['path'])).read()
        except Exception:
            print("[ERROR  ] Remote URL couldnt be read.")

        if dataset is None:
            dataset = object_class()
            setattr(dataset, f'{object_type}_id', ds['gitmodule_name'])
            dataset.date_created = createDate
            dataset.date_added_to_portal = firstMergeDate

        if dataset.date_created != createDate:
            dataset.date_created = createDate

        # check for dataset ancestry
        extraprops = dats.get('extraProperties', [])
        for prop in extraprops:
            if prop.get('category') == 'parent_dataset_id':
                for x in prop.get('values', []):
                    if x.get('value', None) is None:
                        continue
                    datasetAncestry = DBDatasetAncestry()
                    datasetAncestry.id = str(uuid.uuid4())
                    datasetAncestry.parent_dataset_id = 'projects/' + \
                        x.get('value', None)
                    datasetAncestry.child_dataset_id = dataset.dataset_id
                    try:
                        db.session.merge(datasetAncestry)
                        db.session.commit()
                    except exc.IntegrityError:
                        # we already have a record of this ancestry
                        db.session.rollback()

        if not dataset.date_added_to_portal:
            dataset.date_added_to_portal = firstMergeDate

        dataset.date_updated = updateDate
        dataset.fspath = ds['path']
        dataset.remoteUrl = remoteUrl
        dataset.description = dats.get(
            'description', 'No description in DATS.json')
        dataset.name = dats.get(
            'title',
            os.path.basename(getattr(dataset, f'{object_type}_id'))
        )

        db.session.merge(dataset)
        db.session.commit()

        # if the dataset does not have an ARK identifier yet, generate it
        dataset_with_ark_id_list = [row[0] for row in db.session.query(getattr(ArkId, f'{object_type}_id')).all()]
        if getattr(dataset, f"{object_type}_id") not in dataset_with_ark_id_list:
            new_ark_id = ark_id_minter(app, object_type)
            save_ark_id_in_database(app, object_type, new_ark_id, getattr(dataset, f'{object_type}_id'))
        print('[INFO   ] ' + ds['gitmodule_name'] + ' updated.')


def _update_datasets(app):
    """
    Updates from conp-datasets
    """
    _update_datalad_objects(app, "dataset", "conp-dataset", DBDataset)


def _update_experiments(app):
    """
    Updates from conp-datasets
    """
    _update_datalad_objects(app, "experiment", "conp-experiments", DBExperiment)


def _update_analytics(app):
    """
    Updates analytics table using Matomo API endpoints
    """

    matomo_server_url = app.config['MATOMO_SERVER_URL']
    matomo_site_id = app.config['MATOMO_SITE_ID']
    matomo_token_auth = app.config['MATOMO_TOKEN_AUTH']

    matomo_api_baseurl = f"https://{matomo_server_url}/?module=API" \
                         f"&idSite={matomo_site_id}" \
                         f"&token_auth={matomo_token_auth}" \
                         f"&format=json" \
                         f"&filter_limit=-1"

    _update_analytics_matomo_visits_summary(app, matomo_api_baseurl)

    _update_analytics_matomo_get_page_urls_summary(app, matomo_api_baseurl)

    _update_analytics_matomo_get_daily_dataset_views_summary(app, matomo_api_baseurl)

    _update_analytics_matomo_get_daily_keyword_searches_summary(app, matomo_api_baseurl)

    _update_analytics_matomo_get_daily_portal_download_summary(app, matomo_api_baseurl)

    _update_github_traffic_counts(app)


def _update_analytics_matomo_visits_summary(app, matomo_api_baseurl):
    """
    Function to update specifically the Matomo visits summary
    queried from the Matomo API endpoint VisitsSummary.

    Note: gather stats only until the day before the current
    day since stats are still being gathered by Matomo for the
    current day.
    """

    from app import db
    from app.models import MatomoDailyVisitsSummary
    import requests

    # grep the dates already inserted into the database
    db_results = db.session.query(MatomoDailyVisitsSummary.date).all()
    dates_in_database = [row[0] for row in db_results]

    # determines which dates are missing from the database and could be queried on Matomo
    dates_to_process = determine_dates_to_query_on_matomo(dates_in_database)

    # for each date to process, query Matomo and insert response into the database
    for date in dates_to_process:
        matomo_query = f"{matomo_api_baseurl}" \
                       f"&method=VisitsSummary.get" \
                       f"&period=day" \
                       f"&date={date}"
        response = requests.get(matomo_query).json()

        if not response:
            continue

        visits_summary = MatomoDailyVisitsSummary()
        visits_summary.date = date
        visits_summary.avg_time_on_site = response['avg_time_on_site']
        visits_summary.bounce_count = response['bounce_count']
        visits_summary.max_actions = response['max_actions']
        visits_summary.nb_actions = response['nb_actions']
        visits_summary.nb_actions_per_visit = response['nb_actions_per_visit']
        visits_summary.nb_uniq_visitors = response['nb_uniq_visitors']
        visits_summary.nb_users = response['nb_users']
        visits_summary.nb_visits = response['nb_visits']
        visits_summary.nb_visits_converted = response['nb_visits_converted']
        visits_summary.sum_visit_length = response['sum_visit_length']

        db.session.merge(visits_summary)
        db.session.commit()
        print(f'[INFO   ] Inserted Matomo visits summary for {date}')


def _update_analytics_matomo_get_page_urls_summary(app, matomo_api_baseurl):
    """
    Function to update specifically the Matomo visited page URLs summary
    queried from the Matomo API endpoint Actions.getPageUrls.

    This will get the URLs for all pages except for the dataset specific
    pages. This will be done by a different function in a different table...

    Note: gather stats only until the day before the current
    day since stats are still being gathered by Matomo for the
    current day.
    """

    from app import db
    from app.models import MatomoDailyGetPageUrlsSummary
    import requests

    # grep the dates already inserted into the database
    date_field = MatomoDailyGetPageUrlsSummary.date
    db_results = db.session.query(date_field).distinct(date_field).all()
    dates_in_database = [row[0] for row in db_results]

    # determines which dates are missing from the database and could be queried on Matomo
    dates_to_process = determine_dates_to_query_on_matomo(dates_in_database)

    # for each date to process, query Matomo API and insert response into the database
    for date in dates_to_process:
        matomo_query = f"{matomo_api_baseurl}" \
                       f"&method=Actions.getPageUrls" \
                       f"&period=day" \
                       f"&date={date}"
        response = requests.get(matomo_query).json()

        if not response:
            # if no response, then there are no stats for that date.
            # enter the date in the table so that this date is not
            # reprocessed at the next run of analytics updates
            page_summary = MatomoDailyGetPageUrlsSummary()
            page_summary.date = date
            db.session.merge(page_summary)
            db.session.commit()
            continue

        for page in response:
            url = page['url'] if 'url' in page.keys() else None
            uniq_visitors = page['nb_uniq_visitors'] if 'nb_uniq_visitors' in page.keys() else None
            page_summary = MatomoDailyGetPageUrlsSummary()
            page_summary.date = date
            page_summary.url = url
            page_summary.label = page['label']
            page_summary.nb_hits = page['nb_hits']
            page_summary.nb_visits = page['nb_visits']
            page_summary.nb_uniq_visitors = uniq_visitors
            page_summary.sum_time_spent = page['sum_time_spent']
            page_summary.avg_time_on_page = page['avg_time_on_page']

            db.session.merge(page_summary)
            db.session.commit()

        print(f'[INFO   ] Inserted Matomo visits per page URL for {date}')


def _update_analytics_matomo_get_daily_dataset_views_summary(app, matomo_api_baseurl):
    """
    Function to update specifically the Matomo daily dataset views summary
    queried from the Matomo API endpoint Actions.getPageUrl for each dataset_id.

    Note: gather stats only until the day before the current
    day since stats are still being gathered by Matomo for the
    current day.
    """
    from app import db
    from app.models import MatomoDailyGetDatasetPageViewsSummary
    from app.models import Dataset as DBDataset
    import requests

    # grep the dates already inserted into the database
    date_field = MatomoDailyGetDatasetPageViewsSummary.date
    db_results = db.session.query(date_field).distinct(date_field).all()
    dates_in_database = [row[0] for row in db_results]

    # determines which dates are missing from the database and could be queried on Matomo
    dates_to_process = determine_dates_to_query_on_matomo(dates_in_database)

    # get the list of dataset_id_list to process
    dataset_id_list = [row[0] for row in db.session.query(DBDataset.dataset_id).all()]

    # for each date and each dataset, query Matomo for the view stats
    for date in dates_to_process:
        date_inserted = False
        for dataset_id in dataset_id_list:
            page_url = f"https://portal.conp.ca/dataset?id={dataset_id}"
            matomo_query = f"{matomo_api_baseurl}" \
                           f"&method=Actions.getPageUrl" \
                           f"&period=day" \
                           f"&date={date}" \
                           f"&pageUrl={page_url}"
            response = requests.get(matomo_query).json()

            if not response:
                continue

            views_summary = MatomoDailyGetDatasetPageViewsSummary()
            views_summary.date = date
            views_summary.dataset_id = dataset_id
            views_summary.url = response[0]['url']
            views_summary.label = response[0]['label']
            views_summary.nb_hits = response[0]['nb_hits']
            views_summary.nb_visits = response[0]['nb_visits']
            views_summary.nb_uniq_visitors = response[0]['nb_uniq_visitors']
            views_summary.sum_time_spent = response[0]['sum_time_spent']
            views_summary.avg_time_on_page = response[0]['avg_time_on_page']

            db.session.merge(views_summary)
            db.session.commit()

            date_inserted = True
            print(f'[INFO   ] Inserted Matomo number of views for {dataset_id} on {date}')

        # if no stats existed for that date, then add a row to the table
        # with empty values so that the script does not reprocess that date
        if not date_inserted:
            views_summary = MatomoDailyGetDatasetPageViewsSummary()
            views_summary.date = date
            db.session.merge(views_summary)
            db.session.commit()


def _update_analytics_matomo_get_daily_portal_download_summary(app, matomo_api_baseurl):
    """
    Function to update specifically the Matomo daily download summary
    queried from the Matomo API endpoint Actions.getDownloads.

    Note: gather stats only until the day before the current
    day since stats are still being gathered by Matomo for the
    current day.
    """
    from app import db
    from app.models import MatomoDailyGetPortalDownloadSummary
    import requests

    # grep the dates already inserted into the database
    date_field = MatomoDailyGetPortalDownloadSummary.date
    db_results = db.session.query(date_field).distinct(date_field).all()
    dates_in_database = [row[0] for row in db_results]

    # determines which dates are missing from the database and could be queried on Matomo
    dates_to_process = determine_dates_to_query_on_matomo(dates_in_database)

    # for each date query Matomo for the download stats
    for date in dates_to_process:
        matomo_query = f"{matomo_api_baseurl}" \
                       f"&method=Actions.getDownloads" \
                       f"&period=day" \
                       f"&date={date}" \
                       f"&expanded=1"
        response = requests.get(matomo_query).json()

        if not response:
            download_summary = MatomoDailyGetPortalDownloadSummary()
            download_summary.date = date
            db.session.merge(download_summary)
            db.session.commit()
            continue

        for category in response:
            for downloaded_item in category['subtable']:
                download_summary = MatomoDailyGetPortalDownloadSummary()
                download_summary.date = date
                download_summary.url = downloaded_item['url']
                download_summary.label = downloaded_item['label']
                download_summary.nb_hits = downloaded_item['nb_hits']
                download_summary.nb_visits = downloaded_item['nb_visits']
                download_summary.nb_uniq_visitors = downloaded_item['nb_uniq_visitors']
                download_summary.sum_time_spent = downloaded_item['sum_time_spent']
                download_summary.segment = downloaded_item['segment']

                db.session.merge(download_summary)
                db.session.commit()

                label = downloaded_item['label']
                print(f'[INFO   ] Inserted Matomo number of portal downloads for {label} on {date}')


def _update_analytics_matomo_get_daily_keyword_searches_summary(app, matomo_api_baseurl):
    """
    Function to update specifically the Matomo daily keyword search summary
    queried from the Matomo API endpoint Actions.getSiteSearchKeywords.

    Note: gather stats only until the day before the current
    day since stats are still being gathered by Matomo for the
    current day.
    """
    from app import db
    from app.models import MatomoDailyGetSiteSearchKeywords
    import requests

    # grep the dates already inserted into the database
    date_field = MatomoDailyGetSiteSearchKeywords.date
    db_results = db.session.query(date_field).distinct(date_field).all()
    dates_in_database = [row[0] for row in db_results]

    # determines which dates are missing from the database and could be queried on Matomo
    dates_to_process = determine_dates_to_query_on_matomo(dates_in_database)

    # for each date to process, query Matomo API and insert response into the database
    for date in dates_to_process:
        matomo_query = f"{matomo_api_baseurl}" \
                       f"&method=Actions.getSiteSearchKeywords" \
                       f"&period=day" \
                       f"&date={date}"
        response = requests.get(matomo_query).json()

        if not response:
            # if no response, then there are no stats for that date.
            # enter the date in the table so that this date is not
            # reprocessed at the next run of analytics updates
            keyword_summary = MatomoDailyGetSiteSearchKeywords()
            keyword_summary.date = date
            db.session.merge(keyword_summary)
            db.session.commit()

        for keyword in response:
            exit_nb_visits = keyword['exit_nb_visits'] \
                if 'exit_nb_visits' in keyword.keys() else None
            keyword_summary = MatomoDailyGetSiteSearchKeywords()
            keyword_summary.date = date
            keyword_summary.avg_time_on_page = keyword['avg_time_on_page']
            keyword_summary.bounce_rate = keyword['bounce_rate']
            keyword_summary.exit_nb_visits = exit_nb_visits
            keyword_summary.exit_rate = keyword['exit_rate']
            keyword_summary.label = keyword['label']
            keyword_summary.nb_hits = keyword['nb_hits']
            keyword_summary.nb_pages_per_search = keyword['nb_pages_per_search']
            keyword_summary.nb_visits = keyword['nb_visits']
            keyword_summary.segment = keyword['segment']
            keyword_summary.sum_time_spent = keyword['sum_time_spent']

            db.session.merge(keyword_summary)
            db.session.commit()

        print(f'[INFO   ] Inserted Matomo search keywords summary for {date}')


def determine_dates_to_query_on_matomo(dates_in_database):
    """
    Determines which dates need to be queried on Matomo to update the dataset.
    """

    from datetime import datetime, timedelta

    # determines which dates are missing from the database and could be queried on Matomo
    # NOTE: start date was set to 2020-05-01 as May is when the portal started to be live
    start_date = datetime.strptime('2020-05-01', '%Y-%m-%d').date()
    end_date = (datetime.today() - timedelta(1)).date()
    delta = timedelta(days=1)
    dates_to_process = []
    while start_date <= end_date:
        if str(start_date) not in dates_in_database:
            dates_to_process.append(str(start_date))
        start_date += delta

    return dates_to_process


def _generate_missing_ark_ids(app):
    """
    Generates ARK identifiers for datasets that do not have yet an ARK ID.
    """

    from app import db
    from app.models import ArkId
    from app.models import Dataset as DBDataset
    from app.pipelines.pipelines import get_pipelines_from_cache

    pipelines = get_pipelines_from_cache()

    dataset_id_list = [row[0] for row in db.session.query(DBDataset.dataset_id).all()]
    dataset_with_ark_id_list = [row[0] for row in db.session.query(ArkId.dataset_id).all()]
    pipeline_id_list = [row['ID'] for row in pipelines]
    pipeline_with_ark_id_list = [row[0] for row in db.session.query(ArkId.pipeline_id).all()]

    for dataset_id in dataset_id_list:
        if dataset_id not in dataset_with_ark_id_list:
            new_ark_id = ark_id_minter(app, 'dataset')
            save_ark_id_in_database(app, 'dataset', new_ark_id, dataset_id)

    for pipeline_id in pipeline_id_list:
        if pipeline_id not in pipeline_with_ark_id_list:
            new_ark_id = ark_id_minter(app, 'pipeline')
            save_ark_id_in_database(app, 'pipeline', new_ark_id, pipeline_id)


def ark_id_minter(
        app,
        ark_id_type: str  # 'dataset', 'pipeline', or 'experiment'
    ):
    """
    Generates ARK identifiers for datasets and pipelines that do not have yet an ARK ID.

    :param ark_id_type: "dataset", "pipeline", or "experiment"
     :type ark_id_type: str

    :return: a new minted ARK identifier
    """

    from app import db
    from app.models import ArkId
    from app.services.pynoid import mint

    # arkid shoulder will be d7 for datasets and p7 for pipelines
    template = 'd7.reeeeeeedeeedeeek' if ark_id_type == 'dataset' else ('p7.reeeeeeedeeedeeek' if ark_id_type == 'pipeline' else 'e7.reeeeeeedeeedeeek')
    new_ark_id = mint(
        template=template,
        scheme='ark:/',
        naa=app.config["ARK_CONP_NAAN"]
    )

    # remint ARK ID until we get an ARK ID not already present in `ark_id` table
    # get the list of existing ARK IDs
    already_used_ark_id_list = [row[0] for row in db.session.query(ArkId.ark_id).all()]
    while new_ark_id in already_used_ark_id_list:
        new_ark_id = ark_id_minter(app, ark_id_type)

    return new_ark_id


def save_ark_id_in_database(app, ark_id_type, new_ark_id, source_id):

    from app import db
    from app.models import ArkId

    # get the list of existing ARK IDs
    already_used_ark_id_list = [row[0] for row in db.session.query(ArkId.ark_id).all()]

    # if the new ARK identifier does not already exist, add an entry in the ark_id table
    if new_ark_id not in already_used_ark_id_list:
        ark_id_summary = ArkId()
        ark_id_summary.ark_id = new_ark_id
        ark_id_summary.dataset_id = source_id if ark_id_type == "dataset" else None
        ark_id_summary.pipeline_id = source_id if ark_id_type == "pipeline" else None
        ark_id_summary.experiment_id = source_id if ark_id_type == "experiment" else None

        db.session.merge(ark_id_summary)
        db.session.commit()
        print(f'[INFO   ] Created ARK ID {new_ark_id} for {ark_id_type} {source_id}')


def _update_github_traffic_counts(app):
    """
    Logic to update the GitHub traffic count tables of the portal to save
    traffic information in our local database (clone and view counts).

    Updates the following two tables based on GitHub API calls:
      - github_daily_views_count
      - github_daily_clones_count (a.k.a. DataLad download count estimation)

    Warnings on major confounding factors in the number of dataset clones:
      - the daily tests run on Circle CI create multiple clones per day (which
      explains why there is always at least 1 unique clone counted per dataset
      every day)
      - the archiver and other automated script run by CONP contributes to the
      number of clones every time a dataset is updated (including DATS and
      README updates)
      - CONP developers also contribute to the number of clones when testing,
      updating or downloading datasets
    """

    from app import db
    from app.models import GithubDailyClonesCount, GithubDailyViewsCount
    from pathlib import Path
    import git

    datasetsdir = Path(app.config['DATA_PATH']) / 'conp-dataset'
    try:
        repo = git.Repo(datasetsdir)
    except git.exc.InvalidGitRepositoryError:
        repo = git.Repo.clone_from(
            'https://github.com/CONP-PCNO/conp-dataset',
            datasetsdir,
            branch='master'
        )

    # loop through the list of submodules present in CONP-PCNO/conp-dataset.git
    for submodule in repo.submodules:
        sub_repo = submodule.url.replace('https://github.com/', '').replace('.git', '')
        if sub_repo.startswith('CONP-PCNO/'):
            # skip the repos under the CONP-PCNO organization as they are not datasets
            continue

        # query the GitHub analytics API for number of clones and views
        daily_stat_dict = _get_repo_analytics(app, sub_repo)
        if not daily_stat_dict:
            continue

        # get the list of dates already in the database for this repo
        dates_in_db_dict = {}
        db_clones_results = db.session.query(GithubDailyClonesCount.date).filter_by(repo=sub_repo).all()
        dates_in_db_dict['clones'] = [row[0] for row in db_clones_results]
        db_views_results = db.session.query(GithubDailyViewsCount.date).filter_by(repo=sub_repo).all()
        dates_in_db_dict['views'] = [row[0] for row in db_views_results]

        # loop through results returned by GitHub API calls and insert
        # new data in the proper database table
        for analytic_type in daily_stat_dict:
            if not daily_stat_dict[analytic_type]:
                continue

            for date in daily_stat_dict[analytic_type]:
                if date in dates_in_db_dict[analytic_type]:
                    # go to next date if there is already an entry for the date
                    # for that repo in the database table
                    continue

                analytics_summary = None
                if analytic_type == 'clones':
                    analytics_summary = GithubDailyClonesCount()
                elif analytic_type == 'views':
                    analytics_summary = GithubDailyViewsCount()
                else:
                    print("GitHub analytic type is neither 'clones' nor 'views'")

                if analytics_summary:
                    analytics_summary.date = date
                    analytics_summary.repo = sub_repo
                    analytics_summary.timestamp = daily_stat_dict[analytic_type][date]['timestamp']
                    analytics_summary.count = daily_stat_dict[analytic_type][date]['count']
                    analytics_summary.unique_count = daily_stat_dict[analytic_type][date]['unique_count']

                    db.session.merge(analytics_summary)
                    db.session.commit()


def _get_repo_analytics(app, repo):
    """
    Queries the GitHub API for views and clones traffic information and returns
    a dictionary with the API response information.

    Structure of the returned dictionary:
        {
            "clones": {
                "2022-02-28": {
                    "timestamp": "2022-02-28 00:00:00",
                    "date": "2022-02-28",
                    "count": "5",
                    "unique_count": "1"
                },
                "2022-03-01": {
                    "timestamp": "2022-03-01 00:00:00",
                    "date": "2022-03-01",
                    "count": "6",
                    "unique_count": "2"
                },
                ...
            },
            "views": {
                "2022-02-28": {
                    "timestamp": "2022-02-28 00:00:00",
                    "date": "2022-02-28",
                    "count": "3",
                    "unique_count": "1"
                },
                ...
            }
        }
    """

    from github import Github

    token = app.config['GITHUB_PAT']
    g = Github(token)

    g_analytics = {}
    try:
        g_analytics['clones'] = g.get_repo(repo).get_clones_traffic(per='day')
        g_analytics['views'] = g.get_repo(repo).get_views_traffic(per='day')
    except Exception as e:
        g_analytics['clones'] = {}
        g_analytics['views'] = {}
        print(f"Error while fetching GitHub analytics for {repo}:\n\t{e}")

    daily_stat_dict = {
        'clones': {},
        'views': {}
    }
    for analytic_type in g_analytics:
        if g_analytics[analytic_type]:
            for day_data in g_analytics[analytic_type][analytic_type]:
                timestamp = day_data.timestamp
                date = timestamp.strftime('%Y-%m-%d')
                daily_stat_dict[analytic_type][date] = {
                    "timestamp": timestamp,
                    "date": date,
                    "count": day_data.count,
                    "unique_count": day_data.uniques
                }

    return daily_stat_dict
