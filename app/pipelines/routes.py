# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for the pipelines blueprint
"""
import json
import os
from flask import render_template, request, url_for
from flask_login import current_user
from app.pipelines import pipelines_bp, pipelines as pipelines_utils
from app.models import ArkId


@pipelines_bp.route('/pipelines', methods=['GET'])
def pipelines():
    """ Pipelines Route

        The route that leads to the pipelines page

        Args:
            page: the page that you want to display (default: 1)
            max_per_page: the number of items per page (default: 10)

        Returns:
            Rendered template for pipelines.html
    """
    page = int(request.args.get('page') or 1)
    max_per_page = request.args.get('max_per_page') or 10
    if max_per_page != 'All':
        max_per_page = int(max_per_page)
    cbrain = request.args.get('cbrain')
    search = request.args.get('search') or ""
    tags = request.args.get('tags') or ""
    sortComparitor = request.args.get('sortComparitor')
    sortKey = request.args.get('sortKey')

    filters = {
        "page": page,
        "max_per_page": max_per_page,
        "cbrain": cbrain,
        "search": search,
        "tags": tags,
        "sortComparitor": sortComparitor,
        "sortKey": sortKey,
    }

    return render_template('pipelines.html',
                           title='CONP | Tools & Pipelines',
                           filters=filters)


@pipelines_bp.route('/pipeline-search', methods=['GET'])
def pipeline_search():
    """ Pipeline Search Route

        This route is for searching the set of pipelines in the Portal

        Args:
            search (REQ ARG): search term

        Returns:
            JSON of the applicable pipelines
    """

    authorized = True if current_user.is_authenticated else False

    # get request variables
    search_query = request.args.get(
        "search").lower() if request.args.get("search") else ''
    tags = request.args.get(
        "tags").lower().split(',') if request.args.get("tags") else []
    sort_key = request.args.get("sortKey") or "downloads-desc"

    max_per_page = None
    if request.args.get('max_per_page') != 'All':
        max_per_page = int(request.args.get("max_per_page") or 999999)

    page = int(request.args.get("page") or 1)

    elements = pipelines_utils.get_pipelines_from_cache(search_query)

    # filter out the deprecated pipelines
    elements = list(
        filter(lambda e: (not e.get("DEPRECATED", None)), elements))

    if request.args.get('cbrain'):
        with open(os.path.join(os.getcwd(), "app/static/pipelines/cbrain-conp-pipeline.json"), "r") as f:
            zenodo_urls = json.load(f)
        print(zenodo_urls.keys())
        elements = list(
            filter(lambda e: e["ID"] in zenodo_urls.keys(), elements)
        )

    blocked_pipelines_ids = list()
    with open(os.path.join(os.getcwd(), "app/static/pipelines/block-list-pipeline.json"), "r") as f:
        blocked_pipelines_ids = json.load(f)
    blocked_pipelines_indexes = list()
    for index, element in enumerate(elements):
        if element['ID'] in blocked_pipelines_ids:
            blocked_pipelines_indexes += [index]
        ark_id_row = ArkId.query.filter_by(pipeline_id=element['ID']).first()
        element['ark_id'] = 'https://n2t.net/' + ark_id_row.ark_id
    for index in reversed(blocked_pipelines_indexes):
        elements.pop(index)

    # filter by tags
    if len(tags) > 0:
        elements = list(
            filter(lambda e: ("tags" in e and "domain" in e["tags"]), elements))
        elements = list(filter(lambda e: all(
            t in e["tags"]["domain"] for t in tags), elements))

    # sort, make all keys lowercase and without hyphens or spaces
    elements = [{k.lower().replace("-", "").replace(" ", ""): v for k, v in element.items()}
                for element in elements]

    if sort_key == 'conpStatus':
        sort_key = 'downloads-desc'

    real_key = sort_key
    if sort_key.endswith("-desc"):
        real_key = sort_key[:-5]
    elif sort_key.endswith("-asc"):
        real_key = sort_key[:-4]
    reverse = sort_key.endswith("-desc")

    if real_key == 'title':
        elements.sort(
            key=lambda x: (x[real_key] is None, x[real_key].lower()),
            reverse=reverse
        )
    else:
        elements.sort(
            key=lambda x: (x[real_key] is None, x[real_key]),
            reverse=reverse
        )

    # extract the appropriate page
    elements_on_page = elements
    if max_per_page is not None:
        if len(elements) > max_per_page:
            start_index = (page - 1) * max_per_page
            end_index = start_index + max_per_page
            if end_index > len(elements):
                end_index = len(elements)
            elements_on_page = elements[start_index:end_index]

    # if element has online platform url, retrieve the cbrain one,
    # else take the first one and set logo
    # TODO right now, this handles CBRAIN and one other platform

    with open(os.path.join(os.getcwd(), "app/static/pipelines/cbrain-conp-pipeline.json"), "r") as f:
        zenodo_urls = json.load(f)

    for element in elements_on_page:
        element["platforms"] = [{} for x in range(0, 1)]
        element["platforms"][0]["img"] = url_for(
            'static', filename="img/run_on_cbrain_gray.png")
        element["platforms"][0]["uri"] = ""

        if element["id"] in zenodo_urls.keys():
            element["platforms"][0]["img"] = url_for(
                'static', filename="img/run_on_cbrain_green.png")
            element["platforms"][0]["uri"] = url_for(
                "main.redirect_to_cbrain", cbrainurl=zenodo_urls[element["id"]]
            )
        else:
            element["platforms"][0]["img"] = url_for(
                'static', filename="img/run_on_cbrain_gray.png")
            element["platforms"][0]["uri"] = ""

    # construct payload
    payload = {
        "authorized": authorized,
        "total": len(elements),
        "sortKeys": [
            {
                "key": "downloads-desc",
                "label": "Downloads (High to Low)"
            },
            {
                "key": "downloads-asc",
                "label": "Downloads (Low to High)"
            },
            {
                "key": "title-asc",
                "label": "Title (Ascending)"
            },
            {
                "key": "title-desc",
                "label": "Title (Descending)"
            },
            {
                "key": "id-asc",
                "label": "Pipeline ID (Ascending)"
            },
            {
                "key": "id-desc",
                "label": "Pipeline ID (Descending)"
            }
        ],
        "elements": elements_on_page
    }

    return json.dumps(payload)


@pipelines_bp.route('/tools')
def tools():
    """ Tools Route

        Route to lead to the tools page

        Args:
            None

        Returns:
            rendered template for tools.html for current_user
    """
    return render_template('tools.html', title='CONP | Tools & Pipelines', user=current_user)


@pipelines_bp.route('/pipeline', methods=['GET'])
def pipeline_info():
    """ Pipeline Route

        Route to get the page for one pipeline

        Args:
            id (REQ ARG): the id of the pipeline to display

        Returns:
            rendered pipeline.html for the pipeline

    """

    pipeline_id = request.args.get('id')

    pipelines = pipelines_utils.get_pipelines_from_cache()

    element = list(filter(lambda e: e['ID'] == pipeline_id, pipelines))[0]

    # make all keys lowercase
    element = {k.lower(): v for k, v in element.items()}

    element["platforms"] = [{} for x in range(0, 1)]
    element["platforms"][0]["img"] = url_for(
        'static', filename="img/run_on_cbrain_gray.png")
    element["platforms"][0]["uri"] = ""

    with open(os.path.join(os.getcwd(), "app/static/pipelines/cbrain-conp-pipeline.json"), "r") as f:
        zenodo_urls = json.load(f)

    if element["id"] in zenodo_urls.keys():
        element["platforms"][0]["img"] = url_for(
            'static', filename="img/run_on_cbrain_green.png")
        element["platforms"][0]["uri"] = zenodo_urls[element["id"]]
    else:
        element["platforms"][0]["img"] = url_for(
            'static', filename="img/run_on_cbrain_gray.png")
        element["platforms"][0]["uri"] = ""

    # get pipeline ARK ID
    ark_id_row = ArkId.query.filter_by(pipeline_id=element['id']).first()
    element['ark_id'] = 'https://n2t.net/' + ark_id_row.ark_id

    # make all keys lowercase and without spaces
    element = {k.lower().replace(" ", ""): v for k, v in element.items()}

    return render_template(
        'pipeline.html',
        title='CONP | Pipeline',
        pipeline=element
    )
