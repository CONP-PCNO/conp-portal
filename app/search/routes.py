""" Routes Module

    Currently this module contains all of the routes in search blueprint
"""
import json
import os
import re

from flask import (
    abort,
    current_app,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    url_for,
)
from flask_login import current_user
from sqlalchemy import func

from app.analytics.routes import datasets_downloads, datasets_views
from app.dats import DEFAULT_LOGO, load_dataset_logos, load_remote_logo_copies, resolve_dataset_logo
from app.models import ArkId, Dataset, DatasetAncestry
from app.models import MatomoDailyGetDatasetPageViewsSummary
from app.search import search_bp
from app.search.dataset_query import matches_suggestion, suggest_correction, vocabulary
from app.search.text_match import rank, score as match_score
from app.search.dataset_page import (
    access_context,
    as_url,
    citation_bibtex,
    citation_key,
    citation_ris,
    citation_text,
    clean_version,
    created_year,
    dataset_doi,
    dats_record_html,
    direct_download,
    fix_readme_links,
    get_routes,
    publication_citations,
    title_html,
    licence_badges,
    strip_title_heading,
)
from app.search.models import DatasetCache, DATSDataset
from app.search.queries import (
    example_query_1,
    example_query_2,
    example_query_3,
    example_query_4,
    example_query_5,
)
from app.services import github
from config import Config


@search_bp.app_template_filter('as_url')
def _as_url_filter(value):
    return as_url(value)


@search_bp.app_template_global('dataset_routes')
def _dataset_routes_global(*args, **kwargs):
    """get_routes for templates rendered without page.routes (tests, older callers)."""
    return get_routes(*args, **kwargs)


@search_bp.route('/search')
def search():
    """ The Data page: datasets as cards with a filter sidebar, sort and
        pages, all plain GET parameters (search, origin, access, get,
        modality, format, linked, sort, show, page), so every view has its
        own address. The Data page's earlier parameters (modalities,
        formats, authorizations, cbrain, sortKey, max_per_page) still work.
    """
    from app.search.dataset_list import (
        FACETS,
        PER_PAGE,
        SORTS,
        chosen_per_page,
        chosen_sort,
        dataset_card,
        filter_cards,
        page_links,
        page_of,
        selected_filters,
        sort_options,
    )

    query = (request.args.get('search') or request.args.get('q') or '').strip()
    selected = selected_filters(request.args)
    sort = chosen_sort(request.args, query)
    default_sort = 'relevance' if query else 'added'
    per_page = chosen_per_page(request.args)

    cards = []
    for e in _dataset_elements(query or None, bool(current_user.is_authenticated)):
        try:
            cards.append(dataset_card(e))
        except Exception:  # one odd record must not take the Data page down
            current_app.logger.exception("Skipping dataset %s on the Data page", e.get('id'))
    total = Dataset.query.count() or len(cards)
    shown, facets = filter_cards(cards, selected, sort)
    on_page, page, pages = page_of(shown, request.args.get('page'), per_page)

    def link(**changes):
        """This page's address with some parameters changed (None drops one)."""
        args = {'search': query or None, 'sort': sort if sort != default_sort else None,
                'show': per_page if per_page != PER_PAGE[0] else None}
        for key, _label, _field in FACETS:
            args[key] = selected.get(key) or None
        args.update(changes)
        return url_for('search.search', **{k: v for k, v in args.items() if v not in (None, [], '')})

    suggestion = None
    if query and not shown:
        suggestion = _did_you_mean(query)
    return render_template('search.html', title='CONP | Data', user=current_user,
                           query=query, cards=on_page, matching=len(shown), total=total, suggestion=suggestion,
                           facets=facets, sort='' if sort == default_sort else sort,
                           sorts=sort_options(SORTS, query, 'added'), per_page=per_page,
                           per_page_options=PER_PAGE, page=page, pages=pages,
                           page_links=page_links(page, pages), link=link,
                           filtered=bool(query or any(selected.values())))


def _did_you_mean(query):
    """A corrected search for one that found nothing, from the words of the
    titles, keywords, modalities, tools and experiments the Portal lists."""
    texts = []
    try:
        ix = _ensure_search_index()
        with ix.searcher() as searcher:
            for d in searcher.documents():
                texts.extend([d.get('title'), d.get('keywords'), d.get('modalities'), d.get('formats')])
    except Exception:
        pass
    try:
        from app.pipelines.routes import _tool_elements
        texts.extend(e.get('title') or e.get('name') for e in _tool_elements())
    except Exception:
        pass
    return suggest_correction(query, vocabulary(texts))


@search_bp.route('/find')
def find():
    """One search across the Portal (the home page's search box): the
    datasets, tools and experiments that match, a few of each, with a link
    to the full list in each section."""
    from app.experiments.experiment_page import filter_cards as experiment_filter
    from app.experiments.routes import experiment_cards
    from app.pipelines.routes import _tool_elements, get_cbrain_availability, get_tool_icons, tool_icon
    from app.pipelines.tool_list import filter_cards as tool_filter, group_related, tool_card
    from app.search.dataset_list import dataset_card, filter_cards as dataset_filter

    query = (request.args.get('q') or request.args.get('search') or '').strip()
    if not query:
        return redirect(url_for('main.index'))
    shown = 5

    datasets = []
    for e in _dataset_elements(query, bool(current_user.is_authenticated)):
        try:
            datasets.append(dataset_card(e))
        except Exception:
            current_app.logger.exception("Skipping dataset %s on /find", e.get('id'))
    datasets, _ = dataset_filter(datasets, {}, 'relevance')    # best match first, as on the Data page

    try:
        # The same cards as the Tools & Pipelines list (CBRAIN launch links included).
        with open(os.path.join(os.getcwd(), "app/static/pipelines/cbrain-conp-pipeline.json")) as f:
            launch_ids = set(json.load(f).keys())
        availability = get_cbrain_availability()
        icons, default_icon = get_tool_icons()
        tool_cards = [tool_card(e, availability.get(e.get('id')), launch_ids | set(availability), launch_ids,
                                tool_icon(e.get('id'), icons, default_icon)) for e in _tool_elements()]
        tools, _ = tool_filter(tool_cards, query, {}, 'relevance')
        tool_count = len(tools)
        order = {c['id']: i for i, c in enumerate(tools)}
        tools = sorted(group_related(tools), key=lambda c: order[c['id']])
    except Exception:
        current_app.logger.exception("Tools unavailable on /find")
        tools, tool_count = [], 0

    try:
        experiments, _ = experiment_filter(experiment_cards(), query, {}, 'relevance')
    except Exception:
        current_app.logger.exception("Experiments unavailable on /find")
        experiments = []

    found = bool(datasets or tools or experiments)
    return render_template(
        'find.html', title='CONP | Search', user=current_user, query=query,
        datasets=datasets[:shown], dataset_count=len(datasets),
        tools=tools[:shown], tool_count=tool_count,
        experiments=experiments[:shown], experiment_count=len(experiments),
        suggestion=None if found else _did_you_mean(query))


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
    # @todo:ant: add to config
    logopath = DEFAULT_LOGO

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

    logopath = DATSDataset(datasetrootdir, dataset_id=dataset.dataset_id).LogoFilepath

    # A logo given as a URL (in DATS.json or in dataset-logos.json) is not a
    # file on this server: send the browser there instead.
    if logopath.lower().startswith("http"):
        return redirect(logopath)

    # send_file sets the image type from the file name: the bytes alone were
    # sent as text/html, which browsers tolerate for PNG/JPEG but not for SVG.
    return send_file(os.path.abspath(logopath))


def _ensure_search_index():
    """Open the Whoosh index, creating and populating it when needed.

    Python 3.14 / Flask 3.x compatibility: This function ensures that the
    Whoosh search index exists and is populated before search routes attempt
    to use it. The old code assumed the index was always pre-populated via
    `flask update_index` during setup, which caused EmptyIndexError in test
    environments and fresh deployments.

    Behavior:
    1. Create the index directory if it doesn't exist
    2. Try to open an existing index; if it doesn't exist (EmptyIndexError),
       create a new empty one with the correct schema
    3. If the index is empty (0 documents), check if there are datasets in
       the database and populate the index from them
    4. Return the ready-to-use index

    This lazy-loading approach makes the app resilient to missing indexes
    while avoiding expensive re-indexing on every request by checking the
    document count only on the first call per request lifecycle.
    """
    from whoosh import index
    from whoosh.index import EmptyIndexError

    index_path = os.path.join(os.getcwd(), "index")
    os.makedirs(index_path, exist_ok=True)

    try:
        ix = index.open_dir(index_path)
    except EmptyIndexError:
        # Index directory exists but is empty or not yet initialized.
        # Create schema and initialize index.
        from app.cli import _update_schema
        ix = _update_schema(current_app)

    if ix.doc_count_all() == 0:
        # Index exists but has no documents. Check if we have datasets in
        # the database and populate the index from them. This handles the
        # case where the app was started before CLI setup commands ran.
        from app.cli import _update_index
        from app.models import Dataset as DBDataset

        if DBDataset.query.count() > 0:
            _update_index(current_app, DBDataset, False)
            ix = index.open_dir(index_path)

    return ix


@search_bp.route('/dataset-search-suggestions', methods=['GET'])
def dataset_search_suggestions():
    """ Dataset Search Keyword Route

        This route collects the dataset search autocomplete keywords

        Args:
            search is the search term in the GET Request

        Retuns:
            JSON containing the matching keywords
    """

    search_term = request.args.get('search').lower()
    if not search_term:
        return json.dumps([])
    else:
        # @todo:ant: add to config
        with open(os.path.join(os.getcwd(), "app/static/datasets/dataset-terms-mapping.json")) as f:
            dataset_terms_mapping = json.load(f)
            f.close()

        ix = _ensure_search_index()
        with ix.reader() as r:
            fields = [field for field in ix.schema.scorable_names() if field not in ['name', 'title']]
            suggestions = set()
            datasets = set()
            for field in fields:
                for f in r.iter_field(field):
                    s = f[0].decode("utf-8")
                    if matches_suggestion(search_term, s):
                        suggestions.add(s)

            for f in r.iter_field('title'):
                s = f[0].decode("utf-8")
                if matches_suggestion(search_term, s):
                    datasets.add(s)

            # Adding mapping terms
            for t in dataset_terms_mapping:
                if matches_suggestion(search_term, t):
                    suggestions.add(t)

            suggestions = list(suggestions)
            suggestions.sort()

            datasets = list(datasets)
            datasets.sort()

            return json.dumps(
                {
                    'suggestions': suggestions,
                    'datasets': datasets,
                }
            )


def _dataset_page_views(dataset_id):
    """Matomo page views of this dataset's page, summed over the daily
    summaries (collected since January 2021). 0 when none are recorded."""
    try:
        total = (MatomoDailyGetDatasetPageViewsSummary.query
                 .with_entities(func.sum(MatomoDailyGetDatasetPageViewsSummary.nb_hits))
                 .filter_by(dataset_id=dataset_id).scalar())
    except Exception:  # analytics must never break the page
        return 0
    return int(total or 0)


def _evidence_publication_types():
    """Provisional NeuroLibre/Evidence publication types keyed by publication
    DOI (lowercased).

    Superseded by explicit type metadata from the Evidence side when it
    becomes available. Returns an empty mapping if the file is missing or
    malformed, so a bad file degrades to "no badge" rather than an error.
    """
    try:
        with open(os.path.join(
                os.getcwd(),
                # @todo:ant: add to config
                "app/static/datasets/evidence-publication-types.json")) as epf:
            return {k.lower(): v for k, v in json.load(epf).items()}
    except (OSError, ValueError):
        return {}


def _dataset_elements(search_term, authorized):
    """Every dataset matching search_term (all of them when it is empty),
    as the dicts /dataset-search returns and the Data page lists."""
    import logging

    logger = logging.getLogger(__name__)
    elements = []
    # @todo:ant: add to config
    with open(os.path.join(os.getcwd(), "app/static/datasets/dataset-terms-mapping.json")) as f:
        dataset_terms_mapping = json.load(f)
        f.close()

    # Query datasets
    datasets = []
    scores = {}
    ix = _ensure_search_index()
    # Element input for payload
    with ix.searcher() as searcher:
        # If search term exists filter results here
        if search_term:
            # Every typed word must start a word in some searchable field
            # (folded spellings, hyphenated words also joined; see text_match),
            # scored for the "Best match" order.
            fields = [f for f in ix.schema.scorable_names() if f in ix.schema.names()]
            _datasets = []
            for d in searcher.documents():
                try:
                    s = match_score({f: d.get(f) for f in fields}, search_term, dataset_terms_mapping)
                except Exception as e:  # never a server error for a search
                    logger.warning("Search failed for %r on %s: %s", search_term, d.get('id'), e)
                    s = 0
                if s:
                    scores[d['id']] = s
                    _datasets.append(d)

            ds = set()
            ds_add = ds.add
            datasets = [d for d in _datasets if not (d['title'] in ds or ds_add(d['title']))]
        else:
            datasets = searcher.documents()

        evidence_publication_types = _evidence_publication_types()
        dataset_logos = load_dataset_logos()
        remote_logo_copies = load_remote_logo_copies()

        # Get the number of views of datasets
        views = json.loads(datasets_views())
        downloads = json.loads(datasets_downloads())

        for d in datasets:
            dataset_metadata = Dataset.query.filter_by(dataset_id=d['id']).first()
            if dataset_metadata is None:
                # In the search index but not in the database (an index older
                # than the last update): skip it rather than fail the list.
                continue

            views_nb = [v["nb_hits"] for v in views if v["dataset_id"] == d['id']]
            download_id = os.path.basename(d['datasetPath']) + "_version"
            downloads_nb = [
                e["nb_hits"] for e in downloads if e["dataset_id"].startswith(download_id)
            ]

            ark_id_row = ArkId.query.filter_by(dataset_id=d['id']).first()
            # Python 3.14 compatibility: ArkId rows may not exist for all
            # datasets if they were added before the ARK ID generation CLI
            # command ran. Guard against AttributeError by checking if the
            # row exists before accessing its ark_id field.
            ark_id = 'https://n2t.net/' + ark_id_row.ark_id if ark_id_row else None

            try:
                zipped = DatasetCache(current_app).getZipLocation(d['datasetPath'])
            except OSError:
                zipped = None

            show_download_button = zipped is not None
            # @todo:ant: add to config
            # @todo: /data/ Should not be hard-coded. This is a temporary solution to get the zip location. The zip location should be stored in the database and retrieved from there.
            zip_location = '/data/{}'.format(os.path.basename(zipped or ''))

            dataset = {
                "authorized": authorized,
                "ark_id": ark_id,
                "id": d['id'],
                # the database keeps the title as written; the index strips quotes
                "title": dataset_metadata.name or d['title'],
                "remoteUrl": dataset_metadata.remoteUrl,
                "isPrivate": dataset_metadata.is_private,
                "thumbnailURL": "/dataset_logo?id={}".format(d['id']),
                "downloadPath": d['id'],
                "URL": '?',
                "downloads": downloads_nb,
                "views": views_nb,
                "dateAdded": str(dataset_metadata.date_added_to_portal.date()) if dataset_metadata.date_added_to_portal else None,
                "dateUpdated": str(dataset_metadata.date_updated.date()),
                "creators": parse_field(d.get('creators')),
                "origin": d.get('origin'),
                "size": d.get('size'),
                "files": d.get('fileCount'),
                "subjects": d.get('subjectCount'),
                "formats": parse_field(d.get('formats')),
                "modalities": parse_field(d.get('modalities')),
                "licenses": parse_field(d.get('licenses')),
                "version": d.get('version'),
                "sources": parse_field(d.get('sources')),
                "conpStatus": d.get('conpStatus'),
                "authorizations": d.get('authorizations'),
                "privacy": d.get('privacy'),
                "principalInvestigators": parse_field(d.get('principalInvestigators')),
                "primaryPublications": parse_field(d.get('primaryPublications')),
                # The index stores the logo found when it was built; a
                # dataset with none there gets its dataset-logos.json entry,
                # and a logo URL with a local copy gets the copy.
                "logoFilepath": resolve_dataset_logo(
                    d['id'], d.get('logoFilePath'), dataset_logos, remote_logo_copies
                ),
                "status": d.get('status'),
                "cbrain_id": url_for(
                    "main.redirect_to_cbrain", cbrainurl=d.get('cBrainId')
                )
                if d.get('cBrainId')
                else None,
                "showDownloadButton": show_download_button,
                "zipLocation": zip_location,
                "downloadOptions": d.get('downloadOptions'),
                "registrationPage": d.get('registrationPage'),
                "evidencePublication": d.get('evidencePublication'),
                "evidencePublicationType": evidence_publication_types.get(
                    (d.get('evidencePublication') or '').lower()
                ),
                # For the Data page only (server paths, never sent as JSON;
                # see _public): the folder and the text it searches/lists.
                "_fspath": d.get('datasetPath'),
                "_description": d.get('description'),
                "_keywords": parse_field(d.get('keywords')),
                "_creators_text": d.get('creators'),
                "_score": scores.get(d['id'], 0),
            }
            elements.append(dataset)
    if search_term:
        # Best match first (as the index's own ranking did for /dataset-search).
        elements = rank(elements, key='_score')
    return elements


@search_bp.route('/dataset-search', methods=['GET'])
def dataset_search():
    """ Dataset Search Route

        This route executes a dataset search

        Args:
            search is the search term in the GET Request

        Retuns:
            JSON containing the matching datasets
    """
    authorized = bool(current_user.is_authenticated)

    if request.args.get('id'):
        # One dataset (it raised a NameError here before: no elements built)
        elements = [e for e in _dataset_elements(None, authorized) if e['id'] == request.args.get('id')]
    else:
        elements = _dataset_elements(request.args.get('search'), authorized)

    modalities = []
    for e in elements:
        if e['modalities'] is None or e['modalities'] == '':
            continue
        for m in e['modalities']:
            modalities.append(m.lower())
    modalities = sorted(set(modalities))

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
    formats = sorted(set(formats), key=str.casefold)

    authorizations = ['Yes', 'No']

    query_all = bool(request.args.get('elements') == 'all')
    if not query_all:

        if request.args.get('modalities'):
            filter_modalities = request.args.get('modalities').split(",")
            elements = list(
                filter(lambda e: e['modalities'] is not None, elements)
            )
            elements = list(filter(lambda e: any(
                item.lower() in (
                    m.lower() for m in e['modalities']
                ) for item in filter_modalities
            ), elements))
        if request.args.get('formats'):
            filter_formats = request.args.get('formats').split(",")
            elements = list(
                filter(lambda e: e['formats'] is not None, elements)
            )
            elements = list(filter(lambda e: any(
                item.lower() in (
                    f.lower() for f in e['formats']
                ) for item in filter_formats
            ), elements))
        if request.args.get('authorizations'):
            filter_auth = request.args.get('authorizations').split(',')
            elements = list(filter(lambda e: e['authorizations'] is not None, elements))
            for item in filter_auth:
                if item == "Yes":
                    elements = list(filter(lambda e: e['authorizations'] in ['private', 'registered', 'controlled'], elements))
                if item == "No":
                    elements = list(filter(lambda e: e['authorizations'] not in ['private', 'registered', 'controlled'], elements))

        if request.args.get('cbrain'):
            elements = list(
                filter(lambda e: e['cbrain_id'], elements)
            )

        cursor = None
        limit = None
        if request.args.get('max_per_page') != 'All':
            delta = int(request.args.get('max_per_page', 20)) * \
                (int(request.args.get('page', 1)) - 1)
            cursor = max(
                min(int(request.args.get('cursor') or 0), 0), 0) + delta
            limit = int(request.args.get('limit') or 20)

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

        elif sort_key == "evidencePublication":
            # Datasets with a linked NeuroLibre/Evidence publication first,
            # then by title.
            paginated.sort(key=lambda o: (
                o.get("evidencePublication") is None, o["title"].lower()))

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
                "label": "Date Added (Newest First)"
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
            },
            {
                "key": "evidencePublication",
                "label": "Has NeuroLibre/Evidence Publication first"
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
        "elements": [_public(e) for e in paginated]
    }

    return json.dumps(payload)


def _public(element):
    """A dataset dict without its private keys (server paths)."""
    return {k: v for k, v in element.items() if not k.startswith('_')}


def _retired_dataset_page(dataset_id):
    """The page for a dataset removed from the catalogue (flask
    prune_datasets), with HTTP 410 Gone, or None when it never existed."""
    from app.models import ArkId, RetiredDataset

    if not dataset_id:
        return None
    retired = RetiredDataset.query.filter_by(dataset_id=dataset_id).first()
    if retired is None:
        return None
    ark = ArkId.query.filter_by(dataset_id=dataset_id).first()
    name = retired.name or dataset_id.split('/')[-1]
    successor = Dataset.query.filter_by(dataset_id=retired.replaced_by).first() if retired.replaced_by else None
    return render_template('retired_dataset.html', title='CONP | Dataset removed', user=current_user,
                           name=name, retired=retired, ark_id=ark.ark_id if ark else None,
                           successor=successor), 410


def _research_use_view(dataset_id):
    """The "Used in research" tab (papers from `flask update_research_use`),
    or None: no paper found, no data file yet, or an unreadable one."""
    from app.research_use import dataset_view
    try:
        return dataset_view(current_app.config.get('DATA_PATH'), dataset_id)
    except Exception:
        current_app.logger.exception("Research use of %s can't be shown", dataset_id)
        return None


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
    if d is None:
        retired = _retired_dataset_page(dataset_id)
        if retired is not None:
            return retired
        abort(404)  # an unknown id (old link, typo) is not found, not a server error
    try:
        datsdataset = DATSDataset(d.fspath, dataset_id=d.dataset_id)
        datsdataset.descriptor  # read now, so a missing folder or record fails here
    except (OSError, RuntimeError, ValueError, TypeError, KeyError) as e:
        # The row exists but its folder or DATS.json can't be read (a failed
        # checkout, or a dataset removed from conp-dataset but not yet pruned):
        # say so instead of a server error.
        current_app.logger.warning("Dataset %s can't be read from %s: %s", d.dataset_id, d.fspath, e)
        abort(503, description="This dataset's record can't be read at the moment. Please try again later.")

    if current_user.is_authenticated:
        authorized = True
    else:
        authorized = False

    # @todo:ant: add to config
    with open(os.path.join(os.getcwd(), "app/static/datasets/dataset-cbrain-ids.json")) as f:
        cbrain_dataset_ids = json.load(f)
        f.close()

    datasetTitle = d.name.replace("'", "")
    if datasetTitle in cbrain_dataset_ids:
        dataset_cbrain_id = cbrain_dataset_ids[datasetTitle]
    else:
        dataset_cbrain_id = ""

    ark_id_row = ArkId.query.filter_by(dataset_id=d.dataset_id).first()

    try:
        zipped = DatasetCache(current_app).getZipLocation(d.fspath)
    except OSError:
        zipped = None

    show_download_button = zipped is not None
    # @todo:ant: add to config
    # @todo: This is a temporary solution to get the zip location. The zip location should be stored in the database and retrieved from there.
    zip_location = '/data/{}'.format(os.path.basename(zipped or ''))

    dataset = {
        "authorized": authorized,
        "ark_id": 'https://n2t.net/' + ark_id_row.ark_id,
        "name": datsdataset.name,
        "id": d.dataset_id,
        "title": d.name.replace("'", "\'"),
        "remoteUrl": d.remoteUrl,
        "isPrivate": d.is_private,
        "thumbnailURL": f"/dataset_logo?id={d.dataset_id}",
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
        "version": clean_version(datsdataset.version),
        "sources": datsdataset.sources,
        "conpStatus": datsdataset.conpStatus,
        "authorizations": datsdataset.authorizations,
        "principalInvestigators": datsdataset.principalInvestigators,
        "primaryPublications": datsdataset.primaryPublications,
        "registrationPage": datsdataset.registrationPage,
        "downloadOptions": datsdataset.downloadOptions,
        "logoFilepath": datsdataset.LogoFilepath,
        "status": datsdataset.status,
        "cbrain_id": dataset_cbrain_id,
        "zipLocation": zip_location,
        "showDownloadButton": show_download_button,
        "evidencePublication": datsdataset.evidencePublication,
        "evidencePublicationType": _evidence_publication_types().get(
            (datsdataset.evidencePublication or '').lower()
        ),
    }

    metadata = get_dataset_metadata_information(d)

    readme = fix_readme_links(strip_title_heading(get_dataset_readme(d.dataset_id), dataset["title"]),
                              d.remoteUrl)

    # Dataset landing page (option B of the 2026 page review): short licence
    # badges, a ready-made citation and the year the dataset was added.
    year_added = (dataset["dateAdded"] or "")[:4] or None
    descriptor = datsdataset.descriptor
    # A dataset with its own DOI (Zenodo, OSF, ...) is cited by that DOI; the
    # others by the Portal's ARK. Titles may carry HTML (e.g. T<sub>1</sub>).
    doi, doi_publisher = dataset_doi(descriptor)
    cite_year = (created_year(descriptor) or year_added) if doi else year_added
    cite_title = re.sub(r'<[^>]+>', '', dataset["title"] or '')
    cite_args = (datsdataset.creators, cite_year, cite_title, dataset["version"], dataset["ark_id"])
    parents = []
    for parent_id in (datsdataset.parentDatasetId or []):
        pid = parent_id if parent_id.startswith('projects/') else 'projects/' + parent_id
        row = None if parent_id.startswith('http') else Dataset.query.filter_by(dataset_id=pid).first()
        parents.append({
            "url": parent_id if parent_id.startswith('http') else '/dataset?id=' + pid,
            "title": row.name if row is not None else parent_id,
        })
    page = {
        "licences": licence_badges(datsdataset.licenses),
        "citation": citation_text(*cite_args, doi=doi, publisher=doi_publisher),
        "citation_bibtex": citation_bibtex(*cite_args, dataset["id"], doi=doi, publisher=doi_publisher),
        "citation_ris": citation_ris(*cite_args, doi=doi, publisher=doi_publisher),
        "citation_key": citation_key(dataset["id"], cite_year),
        "doi": doi,
        "publications": publication_citations(descriptor),
        "direct_download": direct_download(descriptor, d.fspath),
        "dats_html": dats_record_html(descriptor),
        "parents": parents,
        "access": access_context(
            dataset["authorizations"], datsdataset.registrationPage, datsdataset.sources, d.fspath),
        "routes": get_routes(
            dataset["authorizations"], datsdataset.downloadOptions, datsdataset.registrationPage,
            datsdataset.sources, d.fspath, descriptor=descriptor, archive=show_download_button,
            cbrain=bool(dataset_cbrain_id)),
        "title_html": title_html(dataset["title"]),
        "cbrainPipelinesUrl": url_for('pipelines.pipeline_search'),
        "views": _dataset_page_views(d.dataset_id),
        "research": _research_use_view(d.dataset_id),
    }

    # The CircleCI test badge is gone: the dataset tests stopped running on
    # 1 Oct 2026 and every page showed "Test status: Unknown".
    return render_template(
        'dataset.html',
        title='CONP | Dataset',
        data=dataset,
        metadata=metadata,
        readme=readme,
        page=page,
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
    from unidecode import unidecode

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
        download_name=unidecode(dataset.name.replace(' ', '_') + '.dats.json'),
        mimetype='application/json'
    )


@search_bp.route('/download_metadata_experiment', methods=['GET'])
def download_metadata_experiment():
    """ Download Metadata Route for Experiments

        This route allows downloading the metadata for an experiment.

        Args:
            experiment (REQ ARG): the experiment

        Returns:
            Response to the JSON metadata file for the browser to download.

        Raises:
            400 if experiment not found.
    """
    from unidecode import unidecode

    from app.experiments.routes import find_experiment
    experiment = find_experiment(request.args.get('experiment', ''))

    if experiment is None:
        return 'Experiment Not Found', 400

    # Construire le chemin du dossier contenant les fichiers DATS.json
    experiment_root_dir = os.path.join(
        current_app.config['DATA_PATH'],
        'conp-experiments',
        experiment.fspath
    )

    dats_path = os.path.join(experiment_root_dir, 'DATS.json')

    if not os.path.exists(dats_path):
        return 'File Not Found', 400

    # Nettoyer le nom du fichier avec `unidecode`
    safe_filename = unidecode(experiment.name.replace(" ", "_")) + '.dats.json'

    return send_from_directory(
        os.path.dirname(dats_path),
        os.path.basename(dats_path),
        as_attachment=True,
        download_name=safe_filename,   # Flask 2.2+: attachment_filename was removed (500 error)
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
        "registrationPage": datsdataset.registrationPage,
        "downloadOptions": datsdataset.downloadOptions,
        "registrationEmail": bool(datsdataset.registrationPage and re.match(r"[^@]+@[^@]+\.[^@]+", datsdataset.registrationPage))
    }


def parse_field(field):
    try:
        return json.loads(field)
    except (json.JSONDecodeError, TypeError):
        return field


def get_dataset_readme(dataset_id):

    dataset = Dataset.query.filter_by(dataset_id=dataset_id).first()
    if dataset is None:
        return 'Dataset Not Found', 404

    datsdataset = DATSDataset(dataset.fspath)

    readme_filepath = datsdataset.ReadmeFilepath

    try:
        with open(readme_filepath) as f:
            readme = f.read()
            content = github.render_content(readme)
            return content
    except FileNotFoundError:
        return 'Readme Not Found', 404
