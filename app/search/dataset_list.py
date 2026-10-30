"""The Data page (/search): one card per dataset, a filter sidebar and sort,
as server-rendered HTML (the 2026 redesign, option A of the Portal page
mockups; the Experiments list uses the same pattern).

The text search itself is the search index's (build_dataset_query, through
routes._dataset_elements); this module turns the matching datasets into
cards, applies the sidebar filters, sorts and pages them, and counts the
filter values over the matching set.
"""
import json
import os
import re
from html import unescape

from app.search.dataset_page import (
    RESTRICTED,
    clean_version,
    get_routes,
    repository_has_data,
    title_html,
)

# Filters in the sidebar: (GET parameter, heading, card field).
FACETS = (
    ('origin', 'Origin', 'origin_facet'),
    ('access', 'Access', 'access_facet'),
    ('get', 'How to get it', 'routes_facet'),
    ('modality', 'Modality', 'modality_facet'),
    ('format', 'Format', 'formats'),
    ('linked', 'Linked publication', 'linked_facet'),
    ('used', 'Used in research', 'used_facet'),
)
SORTS = (
    ('relevance', 'Best match'),
    ('added', 'Recently added'),
    ('updated', 'Recently updated'),
    ('name', 'Name A–Z'),
    ('subjects', 'Most subjects'),
    ('size', 'Largest'),
    ('evidence', 'Has an Evidence publication'),
    ('used', 'Most used in research'),
)
# 30 by default, as the Data page has shown since #1021; "All" shows every
# dataset on one page (the old list's max_per_page=All still works).
ALL = 'all'
PER_PAGE = (30, 50, 100, ALL)
# A facet shows this many values; the rest open with "More".
FACET_SHOWN = 8

ROUTE_DOWNLOAD = 'Download in the browser'
ROUTE_DATALAD = 'DataLad'
ROUTE_CBRAIN = 'On CBRAIN'
ROUTE_SOURCE = 'At the source'

_CASE = {'mri': 'MRI', 'fmri': 'fMRI', 'dmri': 'dMRI', 'eeg': 'EEG', 'meg': 'MEG', 'pet': 'PET', 'ieeg': 'iEEG',
         'ct': 'CT', 'dti': 'DTI', 'mrs': 'MRS', 'nirs': 'NIRS', 'fnirs': 'fNIRS', 'ecg': 'ECG', 'emg': 'EMG',
         'rna-seq': 'RNA-Seq', 'snp': 'SNP'}
_FORMAT_CASE = {'nifti': 'NIfTI', 'nii': 'NIfTI', 'niigz': 'NIfTI', 'nii.gz': 'NIfTI', 'gifti': 'GIfTI',
                'gii': 'GIfTI', 'bigwig': 'bigWig', 'rna-seq': 'RNA-Seq'}
_EVIDENCE_LABEL = {'re-executable': 'Re-executable publication', 'interactive': 'Interactive publication',
                   'wired': 'Evidence publication'}

# Values the records use for "no information", left out of chips and filters
# (a dataset with no real modality is counted under "Not stated").
_PLACEHOLDERS = {'', 'n/a', 'na', 'none', 'unknown', 'not specified', 'other', 'dataset', 'null', '-'}
NOT_STATED = 'Not stated'
USED = 'Cited or mentioned in papers'

_dats_cache = {}


def _listify(v):
    if v is None or v == '':
        return []
    if isinstance(v, (list, tuple)):
        return [x for x in v if x not in (None, '')]
    return [v]


def modality_label(m):
    s = str(m).strip()
    return _CASE.get(s.lower(), s[:1].upper() + s[1:])


def format_label(f):
    s = str(f).strip().lstrip('.')
    return _FORMAT_CASE.get(s.lower(), s.upper() if len(s) <= 6 else s)


def size_bytes(size):
    """"8.4 GB" -> 8.4e9 (0 when unknown), for sorting by size."""
    m = re.match(r'^\s*([\d.]+)\s*([KMGTP]?B)\b', str(size or ''), re.I)
    if not m:
        return 0.0
    scale = {'B': 1, 'KB': 1e3, 'MB': 1e6, 'GB': 1e9, 'TB': 1e12, 'PB': 1e15}[m.group(2).upper()]
    return float(m.group(1)) * scale


def _int(v):
    try:
        return int(str(v).replace(',', '').strip())
    except (TypeError, ValueError):
        return None


def _descriptor(fspath):
    """The dataset's DATS record (cached until the file changes), {} if none."""
    if not fspath or not os.path.isdir(fspath):
        return {}
    for name in os.listdir(fspath):
        if name.lower() == 'dats.json':
            path = os.path.join(fspath, name)
            try:
                mtime = os.path.getmtime(path)
                hit = _dats_cache.get(path)
                if hit and hit[0] == mtime:
                    return hit[1]
                with open(path) as f:
                    descriptor = json.load(f)
                _dats_cache[path] = (mtime, descriptor)
                return descriptor
            except (OSError, ValueError):
                return {}
    return {}


def _creators(element):
    names = []
    for c in _listify(element.get('creators')):
        if isinstance(c, dict):
            c = c.get('name') or c.get('fullName') or ' '.join(
                x for x in (c.get('firstName'), c.get('lastName')) if x)
        if c:
            names.append(str(c))
    return names


def _paper_count(dataset_id):
    """Papers that cite or name the dataset, from `flask update_research_use`
    (DATA_PATH/research_use/latest.json); 0 without that file."""
    try:
        from flask import current_app

        from app.research_use import paper_count
        return paper_count(current_app.config.get('DATA_PATH'), dataset_id)
    except Exception:   # outside an app, or an unreadable file: no chip
        return 0


def dataset_card(e):
    """What the Data page shows (and filters on) for one dataset, from a
    routes._dataset_elements dict."""
    fspath = e.get('_fspath')
    auth = str(e.get('authorizations') or '').strip().lower()
    restricted = auth in RESTRICTED
    open_ = auth in ('public', 'open')
    has_data = repository_has_data(fspath)
    has_data = True if has_data is None else has_data
    sources = _listify(e.get('sources'))
    landing = sources[0] if sources and str(sources[0]).startswith('http') else None
    registration = e.get('registrationPage')

    # Same decision as the dataset page's "Get the data" tab, so every "Get it"
    # item lands on a way the page actually shows.
    r = get_routes(e.get('authorizations'), e.get('downloadOptions'), registration, landing, fspath,
                   descriptor=_descriptor(fspath), archive=bool(e.get('showDownloadButton')),
                   cbrain=bool(e.get('cbrain_id')), has_data=has_data)
    download = r['browser'] not in (None, 'too_large')   # too large: no browser download
    datalad = r['datalad']
    at_source = r['source'] or r['source_contact']   # the page has a "Download at the source" step
    host = r['host']
    request = ('Request access at {}'.format(host) if host else 'Request access') if r['request'] else None

    routes = []
    if download:
        routes.append(ROUTE_DOWNLOAD)
    if datalad:
        routes.append(ROUTE_DATALAD)
    if r['cbrain']:
        routes.append(ROUTE_CBRAIN)
    if r['offsite_branch']:   # got from the host, after a request step or not
        routes.append(ROUTE_SOURCE)

    status = str(e.get('conpStatus') or '').strip().lower()
    canadian = status in ('conp', 'canadian')
    origin = 'Canadian dataset' if canadian else ('International' if status == 'external' else None)

    modalities = sorted({modality_label(m) for m in _listify(e.get('modalities'))
                         if str(m).strip().lower() not in _PLACEHOLDERS}, key=str.lower)
    formats = sorted({format_label(f) for f in _listify(e.get('formats'))
                      if str(f).strip().lower().lstrip('.') not in _PLACEHOLDERS}, key=str.lower)
    licences = [str(x.get('name') if isinstance(x, dict) else x) for x in _listify(e.get('licenses'))]
    licences = [x for x in licences if x and x.lower() not in ('none', 'other')] or []
    subjects = _int(e.get('subjects'))
    evidence_type = str(e.get('evidencePublicationType') or '').lower()
    evidence = _EVIDENCE_LABEL.get(evidence_type, 'Evidence publication') if e.get('evidencePublication') else None
    views = sum(v for v in _listify(e.get('views')) if isinstance(v, (int, float)))
    description = re.sub(r'<[^>]+>', ' ', str(e.get('_description') or ''))
    description = re.sub(r'\s+', ' ', unescape(unescape(description))).strip()
    papers = _paper_count(e['id'])

    return {
        'id': e['id'],
        'url': '/dataset?id={}'.format(e['id']),
        'score': e.get('_score') or 0,
        'title': e.get('title') or e['id'],
        'title_html': title_html(e.get('title') or e['id']),
        'logo': e['logoFilepath'] if str(e.get('logoFilepath') or '').startswith('http') else e.get('thumbnailURL'),
        'origin': origin,
        'open': open_,
        'restricted': restricted,
        'creators': _creators(e),
        'added': e.get('dateAdded'),
        'updated': e.get('dateUpdated'),
        'year': (e.get('dateAdded') or '')[:4] or None,
        'version': clean_version(e.get('version')),
        'description': description,
        'keywords': [str(k.get('value') if isinstance(k, dict) else k) for k in _listify(e.get('_keywords'))],
        'size': e.get('size') or None,
        'size_bytes': size_bytes(e.get('size')),
        'subjects': subjects,
        'subjects_label': ('{} subject{}'.format(subjects, '' if subjects == 1 else 's') if subjects else None),
        'modalities': modalities,
        'modality_facet': modalities or [NOT_STATED],
        'formats': formats,
        'licence': ', '.join(licences[:2]) or None,
        'download': download,
        'datalad': datalad,
        'cbrain': r['cbrain'],
        'at_source': at_source,
        'request': request,
        'evidence': evidence,
        'views': views,
        'papers': papers,
        # facet values
        'origin_facet': [origin] if origin else [],
        'access_facet': ['Open'] if open_ else (['Account needed'] if restricted else ['Not stated']),
        'routes_facet': routes,
        'linked_facet': ['Evidence publication'] if evidence else [],
        'used_facet': [USED] if papers else [],
    }


def selected_filters(args):
    """The sidebar's checked values from the query string, plus the Data
    page's old parameters (modalities=, formats=, authorizations=Yes|No,
    cbrain=) so earlier links keep their filters."""
    selected = {key: [v for v in args.getlist(key) if v] for key, _label, _field in FACETS}

    def csv(name):
        return [v.strip() for v in (args.get(name) or '').split(',') if v.strip()]

    selected['modality'] += [modality_label(m) for m in csv('modalities')]
    selected['format'] += [format_label(f) for f in csv('formats')]
    for v in csv('authorizations'):
        selected['access'].append('Account needed' if v.lower() == 'yes' else 'Open')
    if (args.get('cbrain') or '').lower() in ('true', '1', 'yes', 'on'):
        selected['get'].append(ROUTE_CBRAIN)
    return {k: list(dict.fromkeys(v)) for k, v in selected.items()}


_OLD_SORTS = {'title': 'name', 'dateAddedDesc': 'added', 'dateUpdatedDesc': 'updated', 'subjectsDes': 'subjects',
              'sizeDes': 'size', 'evidencePublication': 'evidence'}


def chosen_sort(args, query=None):
    """The sort asked for, or the default: best match when there is a search,
    newest first otherwise."""
    sort = args.get('sort') or _OLD_SORTS.get(args.get('sortKey') or '')
    if sort in dict(SORTS) and (sort != 'relevance' or query):
        return sort
    return 'relevance' if query else 'added'


def sort_options(sorts, query, default_without_query):
    """The Sort menu as (value, label) pairs. The default has an empty
    value, so a new search submitted from the form gets its own default (best
    match) instead of the order the previous page happened to show. Without a
    search there is no "Best match"."""
    if query:
        return [('' if v == 'relevance' else v, label) for v, label in sorts]
    return [('' if v == default_without_query else v, label) for v, label in sorts if v != 'relevance']


def chosen_per_page(args):
    raw = str(args.get('show') or args.get('max_per_page') or '').strip().lower()
    if raw == ALL:
        return ALL
    n = _int(raw)
    return n if n in PER_PAGE else PER_PAGE[0]


def sort_title(title):
    """Sort key for a title: case-insensitive, without a leading "(Dataset)" or
    similar bracketed label the Zenodo crawler keeps, and without markup."""
    t = re.sub(r'<[^>]+>', '', str(title or ''))
    t = re.sub(r'^\s*[\(\[][^\)\]]{1,20}[\)\]]\s*', '', t)
    return t.strip().lower()


def filter_cards(cards, selected, sort):
    """Facet filters (any value within a facet, all facets together), sort,
    and the counts of each filter value over the matching set."""
    def keep(card, skip=None):
        for key, _label, field in FACETS:
            if key == skip:
                continue
            want = selected.get(key) or []
            if want and not set(want) & set(card[field]):
                return False
        return True

    shown = [c for c in cards if keep(c)]
    if sort == 'relevance':
        # Ties: newest first, as without a search.
        shown.sort(key=lambda c: c['added'] or '', reverse=True)
        shown.sort(key=lambda c: -(c.get('score') or 0))
    elif sort == 'name':
        shown.sort(key=lambda c: sort_title(c['title']))
    elif sort == 'updated':
        shown.sort(key=lambda c: c['updated'] or '', reverse=True)
    elif sort == 'subjects':
        shown.sort(key=lambda c: (-(c['subjects'] or 0), c['title'].lower()))
    elif sort == 'size':
        shown.sort(key=lambda c: (-c['size_bytes'], c['title'].lower()))
    elif sort == 'evidence':
        shown.sort(key=lambda c: (c['evidence'] is None, c['title'].lower()))
    elif sort == 'used':
        shown.sort(key=lambda c: (-(c.get('papers') or 0), c['title'].lower()))
    else:
        shown.sort(key=lambda c: c['added'] or '', reverse=True)

    facets = []
    for key, label, field in FACETS:
        # Counts within a facet ignore that facet's own selection, so ticking
        # "MRI" still shows how many EEG datasets there are.
        counts = {}
        for c in cards:
            if keep(c, skip=key):
                for v in set(c[field]):
                    counts[v] = counts.get(v, 0) + 1
        for v in selected.get(key) or []:
            counts.setdefault(v, 0)
        items = [{'value': v, 'count': n, 'checked': v in (selected.get(key) or [])}
                 for v, n in sorted(counts.items(), key=lambda kv: (kv[0] == NOT_STATED, -kv[1], kv[0].lower()))]
        if items:
            # Checked values always show, even past the first few.
            head = items[:FACET_SHOWN]
            more = [i for i in items[FACET_SHOWN:]]
            head += [i for i in more if i['checked']]
            more = [i for i in more if not i['checked']]
            facets.append({'key': key, 'label': label, 'items': head, 'more': more})
    return shown, facets


def page_of(items, page, per_page):
    """(the items on that page, page, number of pages)."""
    if per_page == ALL:
        return items, 1, 1
    pages = max(1, -(-len(items) // per_page))
    page = min(max(1, _int(page) or 1), pages)
    start = (page - 1) * per_page
    return items[start:start + per_page], page, pages


def page_links(page, pages):
    """Page numbers to show, with None for a gap: 1 2 3 … 10."""
    wanted = {1, pages, page - 1, page, page + 1}
    if page <= 3:
        wanted |= {2, 3}
    out, last = [], 0
    for n in sorted(x for x in wanted if 1 <= x <= pages):
        if n - last > 1:
            out.append(None)
        out.append(n)
        last = n
    return out
