# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes in search blueprint
"""
import json
import os
import re

from flask import (
    render_template,
    request,
    current_app,
    send_from_directory,
    url_for,
)
from flask_login import current_user

from app.models import ArkId
from app.models import Dataset, DatasetAncestry
from app.search import search_bp
from app.search.models import DATSDataset, DatasetCache
from app.search.queries import (
    example_query_1, example_query_2, example_query_3, example_query_4, example_query_5
)
from app.analytics.routes import datasets_views, datasets_downloads
from app.services import github
from config import Config


@search_bp.route('/search')
def search():
    """ Dataset Search Route

        This route executes a dataset search

        Args:
            search is the search term in the GET Request

        Retuns:
            JSON containing the matching datasets
    """

    modalities = request.args.get('modalities')
    if modalities is not None:
        modalities = modalities.split(",")

    formats = request.args.get('formats')
    if formats is not None:
        formats = formats.split(",")

    authorizations = request.args.get('authorizations')
    if authorizations is not None:
        authorizations = authorizations.split(",")

    cbrain = request.args.get('cbrain')
    search = request.args.get('search')
    sortComparitor = request.args.get('sortComparitor')
    sortKey = request.args.get('sortKey')
    max_per_page = request.args.get('max_per_page')
    page = request.args.get('page')

    filters = {
        "modalities": modalities,
        "formats": formats,
        "authorizations": authorizations,
        "cbrain": cbrain,
        "search": search,
        "sortComparitor": sortComparitor,
        "sortKey": sortKey,
        "max_per_page": max_per_page,
        "page": page
    }

    return render_template('search.html', title='CONP | Search', user=current_user, filters=filters)


@search_bp.route('/dataset_logo')
def get_dataset_logo():
    """
        Gets data set logos that are statically stored in the portal
        TODO: This should not be static, should be a fucntion the dataset in the database

        Args:
            dataset_id: the unique identifier of the dataset

        Returns:
            path to the png file for the logo
    """
    logopath = "app/static/img/default_dataset.jpeg"

    dataset_id = request.args.get('id', '')
    dataset = Dataset.query.filter_by(dataset_id=dataset_id).first()
    if dataset is None:
        # This shoud return a 404 not found
        return 'Not Found', 400

    datasetrootdir = os.path.join(
        current_app.config['DATA_PATH'],
        'conp-dataset',
        dataset.fspath
    )

    logopath = DATSDataset(datasetrootdir).LogoFilepath

    with open(logopath, 'rb') as logofile:
        return logofile.read()


@search_bp.route('/dataset-search', methods=['GET'])
def dataset_search():
    """ Dataset Search Route

        This route executes a dataset search

        Args:
            search is the search term in the GET Request

        Retuns:
            JSON containing the matching datasets
    """
    datasets = []

    if current_user.is_authenticated:
        authorized = True
    else:
        authorized = False

    if request.args.get('id'):
        # Query datasets
        datasets = Dataset.query.filter_by(
            dataset_id=request.args.get('id')).all()

    else:
        # Query datasets
        datasets = Dataset.query.order_by(Dataset.id).all()

    # Element input for payload
    elements = []

    with open(os.path.join(os.getcwd(), "app/static/datasets/dataset-cbrain-ids.json"), "r") as f:
        cbrain_dataset_ids = json.load(f)
        f.close()

    # Get the number of views of datasets
    views = json.loads(datasets_views())
    downloads = json.loads(datasets_downloads())

    # Build dataset response
    for d in datasets:
        try:
            datsdataset = DATSDataset(d.fspath)
        except Exception:
            # If the DATS file can't be laoded, skip this dataset.
            # There should be an error message in the logs/update_datsets.log
            continue

        # If search term exists filter results here
        if request.args.get('search'):
            search_term = request.args.get('search')
            with open(datsdataset.DatsFilepath, 'r') as dats:
                match = False
                for line in dats.readlines():
                    if search_term.lower() in line.lower():
                        match = True
                        break
                if not match:
                    continue

        datasetTitle = d.name.replace("'", "")
        if datasetTitle in cbrain_dataset_ids.keys():
            dataset_cbrain_id = cbrain_dataset_ids[datasetTitle]
        else:
            dataset_cbrain_id = ""

        views_nb = [v["nb_hits"] for v in views if v["dataset_id"] == d.dataset_id]
        download_id = os.path.basename(d.fspath) + "_version"
        downloads_nb = [
            e["nb_hits"] for e in downloads if e["dataset_id"].startswith(download_id)
        ]

        ark_id_row = ArkId.query.filter_by(dataset_id=d.dataset_id).first()

        try:
            zipped = DatasetCache(current_app).getZipLocation(d)
        except IOError:
            zipped = None

        show_download_button = zipped is not None
        zip_location = '/data/{0}'.format(os.path.basename(zipped or ''))

        dataset = {
            "authorized": authorized,
            "ark_id": 'https://n2t.net/' + ark_id_row.ark_id,
            "id": d.dataset_id,
            "title": d.name.replace("'", "\'"),
            "remoteUrl": d.remoteUrl,
            "isPrivate": d.is_private,
            "thumbnailURL": "/dataset_logo?id={}".format(d.dataset_id),
            "downloadPath": d.dataset_id,
            "URL": '?',
            "downloads": downloads_nb,
            "views": views_nb,
            "dateAdded": str(d.date_added_to_portal.date()) if d.date_added_to_portal else None,
            "dateUpdated": str(d.date_updated.date()),
            "creators": datsdataset.creators,
            "origin": datsdataset.origin,
            "size": datsdataset.size,
            "files": datsdataset.fileCount,
            "subjects": datsdataset.subjectCount,
            "formats": datsdataset.formats,
            "modalities": datsdataset.modalities,
            "licenses": datsdataset.licenses,
            "version": datsdataset.version,
            "sources": datsdataset.sources,
            "conpStatus": datsdataset.conpStatus,
            "authorizations": datsdataset.authorizations,
            "principalInvestigators": datsdataset.principalInvestigators,
            "primaryPublications": datsdataset.primaryPublications,
            "logoFilepath": datsdataset.LogoFilepath,
            "status": datsdataset.status,
            "cbrain_id": url_for(
                "main.redirect_to_cbrain", cbrainurl=dataset_cbrain_id
            )
            if dataset_cbrain_id
            else dataset_cbrain_id,
            "showDownloadButton": show_download_button,
            "zipLocation": zip_location
        }

        elements.append(dataset)

    modalities = []
    for e in elements:
        if e['modalities'] is None or e['modalities'] == '':
            continue
        for m in e['modalities']:
            modalities.append(m.lower())
    modalities = sorted(list(set(modalities)))

    formats = []
    # by default, formats should be represented in upper case
    # except for NIfTI, bigWig and RNA-Seq
    for e in elements:
        if e['formats'] is None or e['formats'] == []:
            continue
        for m in e['formats']:
            if m.lower() in ['nifti', 'nii', 'niigz']:
                formats.append('NIfTI')
            elif m.lower() in ['gifti', 'gii']:
                formats.append('GIfTI')
            elif m.lower() == 'bigwig':
                formats.append('bigWig')
            elif m.lower() == 'rna-seq':
                formats.append('RNA-Seq')
            else:
                formats.append(m.upper())
    formats = sorted(list(set(formats)), key=str.casefold)

    authorizations = ['Yes', 'No']

    query_all = bool(request.args.get('elements') == 'all')
    if not query_all:

        if request.args.get('modalities'):
            filter_modalities = request.args.get('modalities').split(",")
            elements = list(
                filter(lambda e: e['modalities'] is not None, elements))
            elements = list(filter(lambda e: all(item in (m.lower(
            ) for m in e['modalities']) for item in filter_modalities), elements))
        if request.args.get('formats'):
            filter_formats = request.args.get('formats').split(",")
            elements = list(
                filter(lambda e: e['formats'] is not None, elements)
            )
            elements = list(filter(lambda e: all(item.lower() in (
                f.lower() for f in e['formats']) for item in filter_formats), elements)
            )
        if request.args.get('authorizations'):
            filter_auth = request.args.get('authorizations').split(',')
            elements = list(filter(lambda e: e['authorizations'] is not None, elements))
            for item in filter_auth:
                if item == "Yes":
                    elements = list(filter(lambda e: e['authorizations'] in ['private', 'registered'], elements))
                if item == "No":
                    elements = list(filter(lambda e: e['authorizations'] not in ['private', 'registered'], elements))

        if request.args.get('cbrain'):
            elements = list(
                filter(lambda e: e['cbrain_id'] != '', elements)
            )

        cursor = None
        limit = None
        if request.args.get('max_per_page') != 'All':
            delta = int(request.args.get('max_per_page', 10)) * \
                (int(request.args.get('page', 1)) - 1)
            cursor = max(
                min(int(request.args.get('cursor') or 0), 0), 0) + delta
            limit = int(request.args.get('limit') or 10)

        sort_key = request.args.get('sortKey') or "conpStatus"
        paginated = elements

        if sort_key == "conpStatus":
            order = {'conp': 0, 'canadian': 1, 'external': 2}
            paginated.sort(key=lambda o: (
                o[sort_key].lower() not in order, order.get(o[sort_key].lower(), None)))

        elif sort_key == "title":
            paginated.sort(key=lambda o: o[sort_key].lower())

        elif sort_key == "sizeDes" or sort_key == "sizeAsc":

            def get_absolute_size(o):
                if not o["size"]:
                    return 0.0

                units = ["KB", "MB", "GB", "TB"]
                unit_scales = [1000, 1000**2, 1000**3, 1000**4]
                size = o["size"].split(" ")
                absolute_size = size[0]
                if size[1] in units:
                    absolute_size = float(size[0]) * \
                        unit_scales[units.index(size[1])]
                return absolute_size

            reverse = (sort_key == 'sizeDes')
            paginated.sort(key=lambda o: get_absolute_size(o), reverse=reverse)

        elif sort_key == "filesDes" or sort_key == "filesAsc":

            def get_number_of_files(o):
                if not o["files"]:
                    return 0

                return int(o["files"])

            reverse = (sort_key == 'filesDes')
            paginated.sort(key=lambda o: get_number_of_files(o),
                           reverse=reverse)

        elif sort_key == "subjectsDes" or sort_key == "subjectsAsc":

            def get_number_of_subjects(o):
                if not o["subjects"]:
                    return 0

                return int(o["subjects"])

            reverse = (sort_key == 'subjectsDes')
            paginated.sort(key=lambda o: get_number_of_subjects(o),
                           reverse=reverse)

        elif sort_key == "dateAddedDesc" or sort_key == "dateAddedAsc":

            reverse = (sort_key == 'dateAddedAsc')
            paginated.sort(key=lambda o: (
                o["dateAdded"] is None, o["dateAdded"]), reverse=reverse)

        elif sort_key == "dateUpdatedDesc" or sort_key == "dateUpdatedAsc":

            reverse = (sort_key == 'dateUpdatedAsc')
            paginated.sort(key=lambda o: (
                o["dateUpdated"] is None, o["dateUpdated"]), reverse=reverse)

        elif sort_key == "viewsDes" or sort_key == "viewsAsc":

            reverse = (sort_key == "viewsDes")
            paginated.sort(key=lambda o: (
                o["views"] is None, o["views"]), reverse=reverse)

        elif sort_key == "downloadsDes" or sort_key == "downloadsAsc":

            reverse = (sort_key == "downloadsDes")
            paginated.sort(key=lambda o: (
                o["downloads"] is None, o["downloads"]), reverse=reverse)

        else:
            paginated.sort(key=lambda o: (o[sort_key] is None, o[sort_key]))

        if cursor is not None and limit is not None:
            paginated = paginated[cursor:(cursor + limit)]
    else:
        paginated = elements

    # Construct payload
    payload = {
        "authorized": authorized,
        "total": len(elements),
        "sortKeys": [
            {
                "key": "conpStatus",
                "label": "Origin"
            },
            {
                "key": "title",
                "label": "Dataset Name"
            },
            {
                "key": "dateAddedAsc",
                "label": "Date Added (Newest FIrst)"
            },
            {
                "key": "dateAddedDesc",
                "label": "Date Added (Oldest First)"
            },
            {
                "key": "dateUpdatedAsc",
                "label": "Date Updated (Newest First)"
            },
            {
                "key": "dateUpdatedDesc",
                "label": "Date Updated (Oldest First)"
            },
            {
                "key": "sizeDes",
                "label": "Disk Space Usage (Largest First)"
            },
            {
                "key": "sizeAsc",
                "label": "Disk Space Usage (Smallest First)"
            },
            {
                "key": "filesDes",
                "label": "Number of Files (Largest First)"
            },
            {
                "key": "filesAsc",
                "label": "Number of Files (Smallest First)"
            },
            {
                "key": "subjectsDes",
                "label": "Number of Subjects (Largest First)"
            },
            {
                "key": "subjectsAsc",
                "label": "Number of Subjects (Smallest First)"
            },
            {
                "key": "viewsDes",
                "label": "Number of Views (Largest First)"
            },
            {
                "key": "viewsAsc",
                "label": "Number of Views (Smallest First)"
            },
            {
                "key": "downloadsDes",
                "label": "Number of Direct Downloads (Largest First)"
            },
            {
                "key": "downloadsAsc",
                "label": "Number of Direct Downloads (Smallest First)"
            }
        ],
        "filterKeys": [
            {
                "key": "modalities",
                "values": modalities
            },
            {
                "key": "formats",
                "values": formats
            },
            {
                "key": "authorizations",
                "values": authorizations
            }
        ],
        "elements": paginated
    }

    return json.dumps(payload)


@search_bp.route('/dataset', methods=['GET'])
def dataset_info():
    """ Dataset Route

        Route to get the page for one dataset

        Args:
            id (REQ ARG): the id of the dataset to display

        Returns:
            rendered dataset.html for the dataset

    """

    dataset_id = request.args.get('id')

    # Query dataset
    d = Dataset.query.filter_by(dataset_id=dataset_id).first()
    datsdataset = DATSDataset(d.fspath)

    if current_user.is_authenticated:
        authorized = True
    else:
        authorized = False

    with open(os.path.join(os.getcwd(), "app/static/datasets/dataset-cbrain-ids.json"), "r") as f:
        cbrain_dataset_ids = json.load(f)
        f.close()

    datasetTitle = d.name.replace("'", "")
    if datasetTitle in cbrain_dataset_ids.keys():
        dataset_cbrain_id = cbrain_dataset_ids[datasetTitle]
    else:
        dataset_cbrain_id = ""

    ark_id_row = ArkId.query.filter_by(dataset_id=d.dataset_id).first()

    try:
        zipped = DatasetCache(current_app).getZipLocation(d)
    except IOError:
        zipped = None

    show_download_button = zipped is not None
    zip_location = '/data/{0}'.format(os.path.basename(zipped or ''))

    dataset = {
        "authorized": authorized,
        "ark_id": 'https://n2t.net/' + ark_id_row.ark_id,
        "name": datsdataset.name,
        "id": d.dataset_id,
        "title": d.name.replace("'", "\'"),
        "remoteUrl": d.remoteUrl,
        "isPrivate": d.is_private,
        "thumbnailURL": "/dataset_logo?id={}".format(d.dataset_id),
        "imagePath": "static/img/",
        "downloadPath": d.dataset_id,
        "URL": 'raw_data_url',
        "downloads": "0",
        "views": "0",
        "likes": "0",
        "dateAdded": str(d.date_added_to_portal.date()) if d.date_added_to_portal else None,
        "dateUpdated": str(d.date_updated.date()),
        "creators": datsdataset.creators,
        "origin": datsdataset.origin,
        "size": datsdataset.size,
        "files": datsdataset.fileCount,
        "subjects": datsdataset.subjectCount,
        "formats": datsdataset.formats,
        "modalities": datsdataset.modalities,
        "licenses": datsdataset.licenses,
        "version": datsdataset.version,
        "sources": datsdataset.sources,
        "conpStatus": datsdataset.conpStatus,
        "authorizations": datsdataset.authorizations,
        "principalInvestigators": datsdataset.principalInvestigators,
        "primaryPublications": datsdataset.primaryPublications,
        "logoFilepath": datsdataset.LogoFilepath,
        "status": datsdataset.status,
        "cbrain_id": dataset_cbrain_id,
        "zipLocation": zip_location,
        "showDownloadButton": show_download_button
    }

    metadata = get_dataset_metadata_information(d)

    readme = get_dataset_readme(d.dataset_id)

    if dataset["status"] == "Working":
        color = "success"
    elif dataset["status"] == "Unknown":
        color = "lightgrey"
    else:
        color = "critical"

    ci_badge_url = "https://img.shields.io/badge/circleci-" + \
        dataset["status"] + "-" + color + "?style=flat-square&logo=circleci"

    return render_template(
        'dataset.html',
        title='CONP | Dataset',
        data=dataset,
        metadata=metadata,
        readme=readme,
        ciBadgeUrl=ci_badge_url,
        user=current_user
    )


@search_bp.route('/download_metadata', methods=['GET'])
def download_metadata():
    """ Download Metadata Route

        route to allow downloading the metadata for a dataset

        Args:
            dataset (REQ ARG): the dataset

        Returns:
            Response to the zipped metadata for the browser to download

        Raises:
            HTML error if this fails
    """
    dataset_id = request.args.get('dataset', '')
    dataset = Dataset.query.filter_by(dataset_id=dataset_id).first()
    if dataset is None:
        # This shoud return a 404 not found
        return 'Not Found', 400

    datasetrootdir = os.path.join(
        current_app.config['DATA_PATH'],
        'conp-dataset',
        dataset.fspath
    )

    datspath = DATSDataset(datasetrootdir).DatsFilepath
    return send_from_directory(
        os.path.dirname(datspath),
        os.path.basename(datspath),
        as_attachment=True,
        attachment_filename=os.path.join(
            dataset.name.replace(' ', '_'), '.dats.json'),
        mimetype='application/json'
    )


@search_bp.route('/sparql')
def sparql():
    """
        Route for the SPARQL interface provided by YASGUI
    """

    sparql_endpoint = Config.NEXUS_SPARQL_ENDPOINT
    queries = {
        "Example 1": example_query_1,
        "Example 2": example_query_2,
        "Example 3": example_query_3,
        "Example 4": example_query_4,
        "Example 5": example_query_5
    }

    return render_template('sparql.html', title='CONP | SPARQL', user=current_user,
                           sparql_endpoint=sparql_endpoint, queries=queries)


def get_dataset_metadata_information(dataset):
    """
        returns the datasets metadata

        Args:
            dataset: dictionary for the dataset

        Returns
            payload containing the datasets metadata

    """

    datsdataset = DATSDataset(dataset.fspath)

    # check for child datasets
    child_datasets = []
    dataset_ancestries = DatasetAncestry.query.all()
    for da in dataset_ancestries:
        if da.parent_dataset_id == dataset.dataset_id:
            name = da.child_dataset_id[9:]
            child_dataset = {
                "child_dataset_id": da.child_dataset_id,
                "name": name
            }
            child_datasets.append(child_dataset)

    return {
        "schema_org_metadata": datsdataset.schema_org_metadata,
        "creators": datsdataset.creators,
        "description": datsdataset.description,
        "contact": datsdataset.contacts,
        "version": datsdataset.version,
        "licenses": datsdataset.licenses,
        "sources": datsdataset.sources,
        "keywords": datsdataset.keywords,
        "parentDatasets": datsdataset.parentDatasetId,
        "primaryPublications": datsdataset.primaryPublications,
        "childDatasets": child_datasets,
        "dimensions": datsdataset.dimensions,
        "producedBy": datsdataset.producedBy,
        "isAbout": datsdataset.isAbout,
        "acknowledges": datsdataset.acknowledges,
        "spatialCoverage": datsdataset.spatialCoverage,
        "dates": datsdataset.dates,
        "remoteUrl": dataset.remoteUrl,
    }


def get_dataset_readme(dataset_id):

    dataset = Dataset.query.filter_by(dataset_id=dataset_id).first()
    if dataset is None:
        return 'Dataset Not Found', 404

    datsdataset = DATSDataset(dataset.fspath)

    readme_filepath = datsdataset.ReadmeFilepath

    f = open(readme_filepath, 'r')
    if f.mode != 'r':
        return 'Readme Not Found', 404

    readme = f.read()

    content = github.render_content(readme)

    return content
