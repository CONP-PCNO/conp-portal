# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for the pipelines blueprint
"""
import json
import os
import time
import math
from app.threads import UpdatePipelineData
from flask import render_template, request, url_for
from flask_login import current_user
from app.pipelines import pipelines_bp


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
    max_per_page = int(request.args.get('max_per_page') or 10)
    search = request.args.get('search') or ""
    tags = request.args.get('tags') or ""

    return render_template('pipelines.html',
                           title='CONP | Tools & Pipelines',
                           page=page,
                           max_per_page=max_per_page,
                           search=search,
                           tags=tags)


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
    max_per_page = int(request.args.get("max_per_page") or 999999)
    page = int(request.args.get("page") or 1)
    cache_dir = os.path.join(os.path.expanduser(
        '~'), ".cache", "boutiques", "production")
    all_desc_path = os.path.join(cache_dir, "all_descriptors.json")
    all_detailed_desc_path = os.path.join(
        cache_dir, "detailed_all_descriptors.json")

    # fetch data from cache
    with open(all_desc_path, "r") as f:
        all_descriptors = json.load(f)

    with open(all_detailed_desc_path, "r") as f:
        detailed_all_descriptors = json.load(f)

    # search cache with search query else return everything
    if search_query not in ("", '', None):
        elements = [
            {**descriptor, **detailed_all_descriptors[d_index]}
            for d_index, descriptor in enumerate(all_descriptors)
            if search_query in (
                (str(descriptor.values())
                    + str(detailed_all_descriptors[d_index]["tags"].values())).lower()
                if "tags" in detailed_all_descriptors[d_index] else
                str(descriptor.values()).lower()
            )
        ]
    else:
        elements = [
            {**descriptor, **detailed_all_descriptors[d_index]}
            for d_index, descriptor in enumerate(all_descriptors)
        ]

    # filter out the deprecated pipelines
    elements = list(filter(lambda e: (not e["DEPRECATED"]), elements))

    # filter by tags
    if len(tags) > 0:
        elements = list(filter(lambda e: ("tags" in e and "domain" in e["tags"]), elements))
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

    if (real_key == 'title'):
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
    if len(elements) > max_per_page:
        start_index = (page-1)*max_per_page
        end_index = start_index + max_per_page
        if end_index > len(elements):
            end_index = len(elements)
        elements_on_page = elements[start_index:end_index]

    # if element has online platform url, retrieve the cbrain one,
    # else take the first one and set logo
    # TODO right now, this handles CBRAIN and one other platform

    for element in elements_on_page:
        element["platforms"] = [{} for x in range(0, 1)]
        element["platforms"][0]["img"] = url_for(
            'static', filename="img/run_on_cbrain_gray.png")
        element["platforms"][0]["uri"] = ""

        if "onlineplatformurls" in element:
            # Check CBRAIN
            for url in element["onlineplatformurls"]:
                if url.startswith('https://portal.cbrain.mcgill.ca'):
                    element["platforms"][0]["img"] = url_for(
                        'static', filename="img/run_on_cbrain_green.png")
                    element["platforms"][0]["uri"] = url
                else:
                    platform_dict = {"img": url_for('static', filename="img/globe-solid-green.png"),
                                     "uri": url}
                    element["platforms"].append(platform_dict)

    # construct payload
    payload = {
        "authorized": authorized,
        "total": len(elements),
        "page": page,
        'num_pages': math.ceil(len(elements)/max_per_page),
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

    # fetch data from cache
    cache_dir = os.path.join(os.path.expanduser(
        '~'), ".cache", "boutiques", "production")
    all_desc_path = os.path.join(cache_dir, "all_descriptors.json")
    all_detailed_desc_path = os.path.join(
        cache_dir, "detailed_all_descriptors.json")
    with open(all_desc_path, "r") as f:
        all_descriptors = json.load(f)

    with open(all_detailed_desc_path, "r") as f:
        detailed_all_descriptors = json.load(f)

    elements = [
        {**descriptor, **detailed_all_descriptors[d_index]}
        for d_index, descriptor in enumerate(all_descriptors)
    ]

    element = list(filter(lambda e: e['ID'] == pipeline_id, elements))[0]

    # make all keys lowercase
    element = {k.lower(): v for k, v in element.items()}

    element["platforms"] = [{} for x in range(0, 1)]
    element["platforms"][0]["img"] = url_for(
        'static', filename="img/run_on_cbrain_gray.png")
    element["platforms"][0]["uri"] = ""

    if "online-platform-urls" in element:
        # Check CBRAIN
        for url in element["online-platform-urls"]:
            if url.startswith('https://portal.cbrain.mcgill.ca'):
                element["platforms"][0]["img"] = url_for(
                    'static', filename="img/run_on_cbrain_green.png")
                element["platforms"][0]["uri"] = url
            else:
                platform_dict = {"img": url_for('static', filename="img/globe-solid-green.png"),
                                 "uri": url}
                element["platforms"].append(platform_dict)

    # make all keys lowercase and without spaces
    element =  {k.lower().replace(" ", ""): v for k, v in element.items()}

    return render_template(
        'pipeline.html',
        title='CONP | Pipeline',
        pipeline=element
    )
