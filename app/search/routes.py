# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes in search blueprint
"""
import json
import os
from datetime import datetime, timedelta

import requests
from flask import Response, abort, render_template, request, current_app, send_from_directory
from flask_login import current_user
from sqlalchemy import func, or_

from app.models import Dataset, User
from app.search import search_bp
from app.search.models import DATSDataset


@search_bp.route('/search')
def search():
    """ Dataset Search Route

        This route executes a dataset search

        Args:
            search is the search term in the GET Request

        Retuns:
            JSON containing the matching datasets
    """
    return render_template('search.html', title='CONP | Search', user=current_user)


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

    if request.args.get('search'):
        term = '%' + request.args.get('search') + '%'
        # Query datasets
        datasets = Dataset.query.filter(
            or_(func.lower(Dataset.name)
                .like(func.lower(term)),
                func.lower(Dataset.description)
                .like(func.lower(term)))
        )

    elif request.args.get('id'):
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
            "authorizations": datsdataset.authorizations
        }
        elements.append(dataset)

    queryAll = bool(request.args.get('elements') == 'all')

    if(not queryAll):

        if request.args.get('modalities'):
            filterModalities = request.args.get('modalities').split(",")
            elements = list(filter(lambda e: e['modalities'] is not None, elements))
            elements = list(filter(lambda e: all(item in e['modalities'].lower() for item in filterModalities), elements))
            print(elements)
        if request.args.get('formats'):
            filterFormats = request.args.get('formats')
            elements = list(filter(lambda e: e['format'] is not None, elements))
            elements = list(filter(lambda e: all(item in e['format'].lower() for item in filterFormats), elements))

        delta = int(request.args.get('max_per_page', 10)) * \
                    (int(request.args.get('page', 1)) - 1)
        cursor = max(min(int(request.args.get('cursor') or 0), 0), 0) + delta
        limit = max(min(int(request.args.get('limit') or 10), 10), 0)
        sort_key = request.args.get('sortKey') or "conpStatus"
        paginated = elements

        if(sort_key == "conpStatus"):
            order = {'conp': 0, 'canadian': 1, 'external': 2}
            paginated.sort(key=lambda o: order[o[sort_key].lower()])

        elif(sort_key == "title"):
            paginated.sort(key=lambda o: o[sort_key].lower())

        elif(sort_key == "size"):
            paginated.sort(key=lambda o: o[sort_key])

        else:
            paginated.sort(key=lambda o: (o[sort_key] is None, o[sort_key]))

        paginated=paginated[(cursor):(cursor + limit)]
    else:
        paginated=elements

    # Construct payload
    payload={
        "authorized": authorized,
        "total": len(elements),
        "sortKeys": [
            {
                "key": "conpStatus",
                "label": "Origin"
            },
            {
                "key": "title",
                "label": "Title"
            },
            {
                "key": "dateAdded",
                "label": "Date Added"
            },
            {
                "key": "dateUpdated",
                "label": "Date Updated"
            },
            {
                "key": "size",
                "label": "Size"
            },
            {
                "key": "files",
                "label": "Files"
            },
            {
                "key": "subjects",
                "label": "Subjects"
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

    dataset_id=request.args.get('id')

    # Query dataset
    d=Dataset.query.filter_by(dataset_id=dataset_id).first()
    datsdataset=DATSDataset(d.fspath)

    if current_user.is_authenticated:
        authorized=True
    else:
        authorized=False

    dataset={
        "authorized": authorized,

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
        "authorizations": datsdataset.authorizations
    }

    metadata=get_dataset_metadata_information(d)

    return render_template(
        'dataset.html',
         title='CONP | Dataset',
         data=dataset,
         metadata=metadata,
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
    dataset_id=request.args.get('dataset', '')
    dataset=Dataset.query.filter_by(dataset_id=dataset_id).first()
    if dataset is None:
        # This shoud return a 404 not found
        return 'Not Found', 400

    datasetrootdir=os.path.join(
        current_app.config['DATA_PATH'],
        'conp-dataset',
        dataset.fspath
    )

    datspath=DATSDataset(datasetrootdir).DatsFilepath
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

    datsdataset=DATSDataset(dataset.fspath)

    return {
        "authors": datsdataset.authors,
        "description": datsdataset.description,
        "contact": datsdataset.contacts,
        "version": datsdataset.version,
        "licenses": datsdataset.licenses,
        "sources": datsdataset.sources
    }
