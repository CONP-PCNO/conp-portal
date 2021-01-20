# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes in search blueprint
"""
import json
import os
import re
from datetime import datetime, timedelta

import requests
from flask import Response, abort, render_template, request, url_for, current_app, send_from_directory
from flask_login import current_user
from sqlalchemy import func, or_

from app.models import Dataset, DatasetAncestry, User
from app.search import search_bp
from app.search.models import DATSDataset
from app.services import github


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
    formats = request.args.get('formats')
    search = request.args.get('search')
    tags = request.args.get('tags')
    sortComparitor = request.args.get('sortComparitor')
    sortKey = request.args.get('sortKey')
    max_per_page = request.args.get('max_per_page')
    page = request.args.get('page')

    filters = {
        "modalities": modalities,
        "formats": formats,
        "search": search,
        "tags": tags,
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

    # Build dataset response
    for d in datasets:
        try:
            datsdataset = DATSDataset(d.fspath)
        except Exception as e:
            # If the DATS file can't be laoded, skip this dataset.
            # There should be an error message in the logs/update_datsets.log
            continue

        # If search term exists filter results here
        if request.args.get('search'):
            searchTerm = request.args.get('search')
            with open(datsdataset.DatsFilepath, 'r') as dats:
                match = False
                for line in dats.readlines():
                    if searchTerm.lower() in line.lower():
                        match = True
                        break
                if(not match):
                    continue

        dataset = {
            "authorized": authorized,
            "id": d.dataset_id,
            "title": d.name.replace("'", ""),
            "isPrivate": d.is_private,
            "thumbnailURL": "/dataset_logo?id={}".format(d.dataset_id),
            "downloadPath": d.dataset_id,
            "URL": '?',
            "dateAdded": str(d.date_created.date()),
            "dateUpdated": str(d.date_updated.date()),
            "size": datsdataset.size,
            "files": datsdataset.fileCount,
            "subjects": datsdataset.subjectCount,
            "format": datsdataset.formats,
            "modalities": datsdataset.modalities,
            "sources": datsdataset.sources,
            "conpStatus": datsdataset.conpStatus,
            "authorizations": datsdataset.authorizations,
            "principalInvestigators": datsdataset.principalInvestigators,
            "primaryPublications": datsdataset.primaryPublications,
            "logoFilepath": datsdataset.LogoFilepath,
            "status": datsdataset.status,
        }

        elements.append(dataset)

    modalities = []
    for e in elements:
        if e['modalities'] is None:
            continue
        for m in e['modalities'].split(", "):
            modalities.append(m.lower())
    modalities = list(set(modalities))

    formats = []
    # by default, formats should be represented in upper case
    # except for NIfTI, BigWig and RNA-Seq
    for e in elements:
        if e['format'] is None:
            continue
        for m in e['format'].split(", "):
            formatted_string = re.sub(r'\.', '', m)
            if formatted_string.lower() in ['nifti', 'nii', 'niigz']:
                formats.append('NIfTI')
            elif formatted_string.lower() == 'bigwig':
                formats.append('BigWig')
            elif formatted_string.lower() == 'rna-seq':
                formats.append('RNA-Seq')
            else:
                formats.append(formatted_string.upper())
    formats = sorted(list(set(formats)))

    queryAll = bool(request.args.get('elements') == 'all')
    if(not queryAll):

        if request.args.get('modalities'):
            filterModalities = request.args.get('modalities').split(",")
            elements = list(
                filter(lambda e: e['modalities'] is not None, elements))
            elements = list(filter(lambda e: all(item in (m.lower(
            ) for m in e['modalities'].split(", ")) for item in filterModalities), elements))
        if request.args.get('formats'):
            filterFormats = request.args.get('formats').split(",")
            elements = list(
                filter(lambda e: e['format'] is not None, elements)
            )
            elements = list(filter(lambda e: all(item.lower() in (
                f.lower() for f in e['format'].split(", ")) for item in filterFormats), elements)
            )

        cursor = None
        limit = None
        if(request.args.get('max_per_page') != 'All'):
            delta = int(request.args.get('max_per_page', 10)) * \
                (int(request.args.get('page', 1)) - 1)
            cursor = max(
                min(int(request.args.get('cursor') or 0), 0), 0) + delta
            limit = int(request.args.get('limit') or 10)

        sort_key = request.args.get('sortKey') or "conpStatus"
        paginated = elements

        if(sort_key == "conpStatus"):
            order = {'conp': 0, 'canadian': 1, 'external': 2}
            paginated.sort(key=lambda o: (
                o[sort_key].lower() not in order, order.get(o[sort_key].lower(), None)))

        elif(sort_key == "title"):
            paginated.sort(key=lambda o: o[sort_key].lower())

        elif(sort_key == "sizeDes" or sort_key == "sizeAsc"):

            def getAbsoluteSize(e):
                if not e["size"]:
                    return 0.0

                units = ["KB", "MB", "GB", "TB"]
                unitScales = [1000, 1000**2, 1000**3, 1000**4]
                size = e["size"].split(" ")
                absoluteSize = size[0]
                if(size[1] in units):
                    absoluteSize = float(size[0]) * \
                        unitScales[units.index(size[1])]
                return absoluteSize

            reverse = (sort_key == 'sizeDes')
            paginated.sort(key=lambda o: getAbsoluteSize(o), reverse=reverse)

        elif(sort_key == "filesDes" or sort_key == "filesAsc"):

            def getNumberOfFiles(e):
                if not e["files"]:
                    return 0

                return int(e["files"])

            reverse = (sort_key == 'filesDes')
            paginated.sort(key=lambda o: getNumberOfFiles(o), reverse=reverse)

        elif(sort_key == "subjectsDes" or sort_key == "subjectsAsc"):

            def getNumberOfSubjects(e):
                if not e["subjects"]:
                    return 0

                return int(e["subjects"])
            reverse = (sort_key == 'subjectsDes')
            paginated.sort(key=lambda o: getNumberOfSubjects(o),
                           reverse=reverse)

        elif(sort_key == "dateAddedDesc" or sort_key == "dateAddedAsc"):

            reverse = (sort_key == 'dateAddedAsc')
            paginated.sort(key=lambda o: (
                o["dateAdded"] is None, o["dateAdded"]), reverse=reverse)

        elif(sort_key == "dateUpdatedDesc" or sort_key == "dateUpdatedAsc"):

            reverse = (sort_key == 'dateUpdatedAsc')
            paginated.sort(key=lambda o: (
                o["dateUpdated"] is None, o["dateUpdated"]), reverse=reverse)

        else:
            paginated.sort(key=lambda o: (o[sort_key] is None, o[sort_key]))

        if(cursor is not None and limit is not None):
            paginated = paginated[(cursor):(cursor + limit)]
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

    dataset = {
        "authorized": authorized,
        "name": datsdataset.name,
        "id": d.dataset_id,
        "title": d.name.replace("'", ""),
        "isPrivate": d.is_private,
        "thumbnailURL": "/dataset_logo?id={}".format(d.dataset_id),
        "imagePath": "static/img/",
        "downloadPath": d.dataset_id,
        "URL": 'raw_data_url',
        "downloads": "0",
        "views": "0",
        "likes": "0",
        "dateAdded": str(d.date_created.date()),
        "dateUpdated": str(d.date_updated.date()),
        "size": datsdataset.size,
        "files": datsdataset.fileCount,
        "subjects": datsdataset.subjectCount,
        "format": datsdataset.formats,
        "modalities": datsdataset.modalities,
        "sources": datsdataset.sources,
        "conpStatus": datsdataset.conpStatus,
        "authorizations": datsdataset.authorizations,
        "principalInvestigators": datsdataset.principalInvestigators,
        "primaryPublications": datsdataset.primaryPublications,
        "logoFilepath": datsdataset.LogoFilepath,
        "status": datsdataset.status,
    }

    metadata = get_dataset_metadata_information(d)

    readme = get_dataset_readme(d.dataset_id)

    if dataset["status"] == "Working":
        color = "success"
    elif dataset["status"] == "Unknown":
        color = "lightgrey"
    else:
        color = "critical"

    ciBadgeUrl = "https://img.shields.io/badge/circleci-" + \
        dataset["status"] + "-" + color + "?style=flat-square&logo=circleci"

    return render_template(
        'dataset.html',
        title='CONP | Dataset',
        data=dataset,
        metadata=metadata,
        readme=readme,
        ciBadgeUrl=ciBadgeUrl,
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
    childDatasets = []
    datasetAncestries = DatasetAncestry.query.all()
    for da in datasetAncestries:
        if da.parent_dataset_id == dataset.dataset_id:
            name = da.child_dataset_id[9:]
            childDataset = {
                "child_dataset_id": da.child_dataset_id,
                "name": name
            }
            childDatasets.append(childDataset)

    return {
        "schema_org_metadata": datsdataset.schema_org_metadata,
        "authors": datsdataset.authors,
        "description": datsdataset.description,
        "contact": datsdataset.contacts,
        "version": datsdataset.version,
        "licenses": datsdataset.licenses,
        "sources": datsdataset.sources,
        "parentDatasets": datsdataset.parentDatasetId,
        "primaryPublications": datsdataset.primaryPublications,
        "childDatasets": childDatasets
    }


def get_dataset_readme(dataset_id):

    dataset = Dataset.query.filter_by(dataset_id=dataset_id).first()
    if dataset is None:
        return 'Dataset Not Found', 404

    datsdataset = DATSDataset(dataset.fspath)

    readmeFilepath = datsdataset.ReadmeFilepath

    f = open(readmeFilepath, 'r')
    if f.mode != 'r':
        return 'Readme Not Found', 404

    readme = f.read()

    content = github.render_content(readme)

    return content
