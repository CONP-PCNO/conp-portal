""" Routes Module

    Currently this module contains all of the routes for the pipelines blueprint
"""
import json
import os

from flask import render_template, request, url_for
from flask_login import current_user

from app.models import ArkId
from app.pipelines import pipelines as pipelines_utils
from app.pipelines import pipelines_bp
from app.pipelines.tool_page import tool_page_context


def get_cbrain_availability():
    """ Map Zenodo ids of tools that run on CBRAIN (in some version) to the
        CBRAIN tool and the underlying software versions CBRAIN offers.

        Returns:
            dict: {zenodo_id: {"tool": str, "software": str, "versions": [str]}}
    """
    with open(os.path.join(os.getcwd(), "app/static/pipelines/cbrain-available-pipeline.json")) as f:
        data = json.load(f)
    tools = data.get("tools", {})
    availability = {}
    for zenodo_id, tool in data.get("pipelines", {}).items():
        info = tools.get(tool, {})
        availability[zenodo_id] = {
            "tool": tool,
            "software": info.get("software", tool),
            "versions": info.get("versions", []),
        }
    return availability


def get_tool_icons():
    """ Map Zenodo ids of tools to the icon shown on their card: the logo of
        the software the tool is (FreeSurfer, FSL, ...), read from
        app/static/pipelines/tool-icons.json. Tools that are not mapped to a
        family get the file's "default" entry, the CONP generic tool icon.

        Returns:
            tuple: ({zenodo_id: {"src": str, "label": str}},
                    {"src": str, "label": str, "generic": True} or None when
                    the file has no "default" entry)
    """
    with open(os.path.join(os.getcwd(), "app/static/pipelines/tool-icons.json")) as f:
        data = json.load(f)
    families = data.get("families", {})
    icons = {}
    for zenodo_id, family in data.get("pipelines", {}).items():
        info = families.get(family)
        if not info or not info.get("img"):
            continue
        icons[zenodo_id] = {
            "src": url_for('static', filename=info["img"]),
            "label": info.get("label", family),
        }
    default = data.get("default") or {}
    default_icon = None
    if default.get("img"):
        default_icon = {
            "src": url_for('static', filename=default["img"]),
            "label": default.get("label", "Tool"),
            "generic": True,
        }
    return icons, default_icon


def tool_icon(zenodo_id, icons, default_icon):
    """ The icon for one tool: its family's logo, else the generic icon. """
    icon = icons.get(zenodo_id) or default_icon
    return dict(icon) if icon else None


def _tool_elements():
    """Every tool the Portal lists (the Boutiques cache without deprecated
    or blocked descriptors), keys lower-cased without hyphens or spaces, as
    pipeline_search builds them."""
    elements = pipelines_utils.get_pipelines_from_cache(None)
    elements = [e for e in elements if not e.get("DEPRECATED", None)]
    with open(os.path.join(os.getcwd(), "app/static/pipelines/block-list-pipeline.json")) as f:
        blocked = set(json.load(f))
    elements = [e for e in elements if e.get('ID') not in blocked]
    return [{k.lower().replace("-", "").replace(" ", ""): v for k, v in e.items()} for e in elements]


@pipelines_bp.route('/pipelines', methods=['GET'])
def pipelines():
    """ The Tools & Pipelines list: one card per tool (related descriptors
        grouped), a filter sidebar (runs on, software, domain, container),
        sort and pages; plain GET parameters (search, runs, software,
        domain, container, sort, show, page, separate). The old list's
        parameters (tags, cbrain, sortKey, max_per_page) still work.
    """
    from app.pipelines.tool_list import (
        FACETS,
        PER_PAGE,
        SORTS,
        chosen_per_page,
        chosen_sort,
        filter_cards,
        group_related,
        selected_filters,
        tool_card,
    )
    from app.search.dataset_list import page_links, page_of

    query = (request.args.get('search') or '').strip()
    selected = selected_filters(request.args)
    sort = chosen_sort(request.args)
    per_page = chosen_per_page(request.args)
    separate = request.args.get('separate') in ('1', 'true', 'on')

    with open(os.path.join(os.getcwd(), "app/static/pipelines/cbrain-conp-pipeline.json")) as f:
        launch_ids = set(json.load(f).keys())
    availability = get_cbrain_availability()
    on_cbrain = launch_ids | set(availability.keys())
    icons, default_icon = get_tool_icons()

    cards = [tool_card(e, availability.get(e.get('id')), on_cbrain, launch_ids,
                       tool_icon(e.get('id'), icons, default_icon))
             for e in _tool_elements()]
    shown, facets = filter_cards(cards, query, selected, sort)
    matching = len(shown)
    # Type-ahead terms for the search box: tool names, software, domains.
    suggest_terms = sorted({c['title'] for c in cards} | {c['family'] for c in cards if c['family']}
                           | {d for c in cards for d in c['domains']}, key=str.lower)
    if not separate:
        order = {c['id']: i for i, c in enumerate(shown)}
        shown = sorted(group_related(shown), key=lambda c: order[c['id']])
    on_page, page, pages = page_of(shown, request.args.get('page'), per_page)

    def link(**changes):
        args = {'search': query or None, 'sort': sort if sort != 'downloads' else None,
                'show': per_page if per_page != PER_PAGE[0] else None, 'separate': '1' if separate else None}
        for key, _label, _field in FACETS:
            args[key] = selected.get(key) or None
        args.update(changes)
        return url_for('pipelines.pipelines', **{k: v for k, v in args.items() if v not in (None, [], '')})

    return render_template('pipelines.html', title='CONP | Tools & Pipelines', user=current_user,
                           query=query, cards=on_page, matching=matching, entries=len(shown), total=len(cards),
                           facets=facets, sort=sort, sorts=SORTS, per_page=per_page, per_page_options=PER_PAGE,
                           page=page, pages=pages, page_links=page_links(page, pages), link=link,
                           separate=separate, suggest_terms=suggest_terms,
                           filtered=bool(query or any(selected.values())))


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
        # "Available on CBRAIN": the tool runs on CBRAIN in some version, whether
        # or not the Portal has a launch link for it yet
        with open(os.path.join(os.getcwd(), "app/static/pipelines/cbrain-conp-pipeline.json")) as f:
            on_cbrain = set(json.load(f).keys())
        on_cbrain |= set(get_cbrain_availability().keys())
        elements = list(
            filter(lambda e: e["ID"] in on_cbrain, elements)
        )

    blocked_pipelines_ids = list()
    with open(os.path.join(os.getcwd(), "app/static/pipelines/block-list-pipeline.json")) as f:
        blocked_pipelines_ids = json.load(f)
    blocked_pipelines_indexes = list()
    for index, element in enumerate(elements):
        if element['ID'] in blocked_pipelines_ids:
            blocked_pipelines_indexes += [index]
        ark_id_row = ArkId.query.filter_by(pipeline_id=element['ID']).first()
        element['ark_id'] = ('https://n2t.net/' + ark_id_row.ark_id) if ark_id_row is not None else ''
    for index in reversed(blocked_pipelines_indexes):
        elements.pop(index)

    # filter by tags
    if len(tags) > 0:
        elements = list(
            filter(lambda e: ("tags" in e and "domain" in e["tags"]), elements))
        elements = list(filter(lambda e: all(
            t.lower() in map(str.lower, e["tags"]["domain"]) for t in tags), elements))

    # sort, make all keys lowercase and without hyphens or spaces
    elements = [{k.lower().replace("-", "").replace(" ", ""): v for k, v in element.items()}
                for element in elements]

    if sort_key == 'conpStatus':
        sort_key = 'publicationdate-desc'

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
            end_index = min(end_index, len(elements))
            elements_on_page = elements[start_index:end_index]

    # if element has online platform url, retrieve the cbrain one,
    # else take the first one and set logo
    # TODO right now, this handles CBRAIN and one other platform

    with open(os.path.join(os.getcwd(), "app/static/pipelines/cbrain-conp-pipeline.json")) as f:
        zenodo_urls = json.load(f)
    cbrain_availability = get_cbrain_availability()
    tool_icons, default_tool_icon = get_tool_icons()

    for element in elements_on_page:
        element["cbrain"] = cbrain_availability.get(element["id"])
        element["icon"] = tool_icon(element["id"], tool_icons, default_tool_icon)
        element["platforms"] = [{} for x in range(1)]
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

    tags = []
    for e in elements:
        if isinstance(e['tags'], str) and e['tags']:
            tags.append(e['tags'].lower())
        if isinstance(e['tags'], dict) and e['tags'].get('domain'):
            if isinstance(e['tags']['domain'], str):
                tags.append(e['tags']['domain'])
            else:
                for t in e['tags']['domain']:
                    tags.append(t.lower())
        else:
            continue

    tags = sorted(list(set(tags)))

    # construct payload
    payload = {
        "authorized": authorized,
        "total": len(elements),
        "sortKeys": [
            {
                "key": "publicationdate-desc",
                "label": "Publication date (Newest First)"
            },
            {
                "key": "publicationdate-asc",
                "label": "Publication date (Oldest First)"
            },
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
        "filterKeys": [
            {
                "key": "tags",
                "values": tags
            },
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

    element["platforms"] = [{} for x in range(1)]
    element["platforms"][0]["img"] = url_for(
        'static', filename="img/run_on_cbrain_gray.png")
    element["platforms"][0]["uri"] = ""

    with open(os.path.join(os.getcwd(), "app/static/pipelines/cbrain-conp-pipeline.json")) as f:
        zenodo_urls = json.load(f)

    element["cbrain"] = get_cbrain_availability().get(element["id"])
    element["icon"] = tool_icon(element["id"], *get_tool_icons())

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
        pipeline=element,
        page=tool_page_context(element),
    )
