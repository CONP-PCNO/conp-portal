"""Helpers for the dataset landing page (dataset.html).

Everything here is derived from the dataset's own records (DATS.json,
README, the Portal database); nothing is written per dataset.
"""
import json
import re
from html import unescape

# --------------------------------------------------------------------------
# Licence badge
# --------------------------------------------------------------------------
CC_BASE = 'https://creativecommons.org/licenses/'


def _cc_badge(low):
    """Return (label, url) for a Creative Commons licence string, or None."""
    if not (('creative commons' in low) or re.search(r'\bcc[\s_-]*by', low)):
        return None
    parts = ['BY']
    if re.search(r'non[\s_-]?commercial|[\s_-]nc\b', low):
        parts.append('NC')
    if re.search(r'no[\s_-]?deriv|[\s_-]nd\b', low):
        parts.append('ND')
    if re.search(r'share[\s_-]?alike|[\s_-]sa\b', low):
        parts.append('SA')
    version = re.search(r'\b([1-4]\.0)\b', low)
    label = 'CC ' + '-'.join(parts)
    url = None
    if version:
        label += ' ' + version.group(1)
        url = '{}{}/{}/'.format(CC_BASE, '-'.join(parts).lower(), version.group(1))
    return label, url


def short_licence(name):
    """Map a DATS licence name to a short badge.

    Returns a dict {"label", "url", "full"} or None when there is no
    licence. Standard licences get their usual short name (the version only
    when the record states one); anything else (a data-use agreement, a
    governance policy, a terms page) is shown as "Data use terms", linked
    when the record gives a URL.
    """
    if name is None:
        return None
    raw = name
    if isinstance(raw, dict):
        raw = raw.get('name') or raw.get('id') or json.dumps(raw)
    s = str(raw).strip()
    if s.startswith('{'):
        try:
            parsed = json.loads(s)
            s = str(parsed.get('name') or parsed.get('id') or s)
        except (ValueError, AttributeError):
            pass
    if not s or s.lower() in ('none', 'null'):
        return None
    low = s.lower()
    full = s

    if re.search(r'\bcc[\s_-]*0\b|cc[\s_-]*zero|creative commons zero', low):
        return {'label': 'CC0 1.0' if '1.0' in low else 'CC0',
                'url': 'https://creativecommons.org/publicdomain/zero/1.0/', 'full': full}
    if low in ('other-pd', 'public domain'):
        return {'label': 'Public domain', 'url': None, 'full': full}
    if 'pddl' in low:
        return {'label': 'PDDL', 'url': 'https://opendatacommons.org/licenses/pddl/', 'full': full}
    if 'odbl' in low or 'open database license' in low:
        return {'label': 'ODbL', 'url': 'https://opendatacommons.org/licenses/odbl/', 'full': full}
    cc = _cc_badge(low)
    if cc:
        return {'label': cc[0], 'url': cc[1], 'full': full}
    if re.fullmatch(r'mit( license)?', low):
        return {'label': 'MIT', 'url': 'https://opensource.org/license/mit', 'full': full}
    if low.startswith('http'):
        return {'label': 'Data use terms', 'url': s, 'full': full}
    return {'label': 'Data use terms', 'url': None, 'full': full}


def licence_badges(licenses):
    """Badges for the DATS licences (a list, a string or None), de-duplicated."""
    if licenses is None:
        return []
    items = licenses if isinstance(licenses, list) else [licenses]
    badges, seen = [], set()
    for item in items:
        badge = short_licence(item)
        if badge and badge['label'] not in seen:
            seen.add(badge['label'])
            badges.append(badge)
    return badges


# --------------------------------------------------------------------------
# README
# --------------------------------------------------------------------------
def _norm(text):
    text = unescape(re.sub(r'<[^>]+>', '', text or ''))
    return re.sub(r'[^a-z0-9]+', ' ', text.lower()).strip()


def strip_title_heading(readme_html, title):
    """Drop the README's first heading when it repeats the dataset title.

    Returns '' when there is no usable README (the route's helper returns a
    ('Readme Not Found', 404) tuple in that case)."""
    if not isinstance(readme_html, str) or not readme_html.strip():
        return ''
    m = re.match(r'\s*(?:<div[^>]*>\s*)?(<h([1-3])[^>]*>(.*?)</h\2>)', readme_html, re.S | re.I)
    if m and title and _norm(m.group(3)) == _norm(title):
        return readme_html[:m.start(1)] + readme_html[m.end(1):]
    return readme_html


# --------------------------------------------------------------------------
# Citation
# --------------------------------------------------------------------------
def clean_version(version):
    """The DATS version, or None when the record has none. The crawlers write
    the string "None" (16 records), which must not show as "version None"."""
    if version is None:
        return None
    version = str(version).strip()
    return None if version.lower() in ('', 'none', 'null', 'n/a') else version


def citation_text(creators, year, title, version, ark_url, doi=None, publisher=None):
    """Plain-text citation built from the record:
    Creators (year). Title, version X. CONP Portal. ARK.
    When the dataset has its own DOI, the DOI and its publisher replace the
    Portal and the ARK: Creators (year). Title [Data set]. Zenodo. DOI URL."""
    names = [c for c in (creators or []) if c]
    if len(names) > 3:
        who = ', '.join(names[:3]) + ', et al.'
    else:
        who = ', '.join(names)
    parts = []
    if who:
        if year:
            parts.append('{} ({}).'.format(who, year))
        else:
            parts.append(who if who.endswith('.') else who + '.')
    head = (title or '').strip()
    if version:
        head += ', version {}'.format(version)
    if doi:
        parts.append(head + ' [Data set].')
        if publisher:
            parts.append(publisher + '.')
        parts.append('https://doi.org/' + doi)
        return ' '.join(parts)
    parts.append(head + '.')
    parts.append('CONP Portal.')
    if ark_url:
        parts.append(ark_url)
    return ' '.join(parts)


# Reference-manager formats (BibTeX, RIS), built from the same fields.
_ORG_WORDS = ('project', 'consortium', 'institute', 'university', 'universit',
              'laboratory', 'lab', 'group', 'initiative', 'network', 'centre',
              'center', 'team', 'foundation', 'core', 'hospital', 'platform')
_BIBTEX_SPECIAL = re.compile(r'([&%$#_])')


def _bibtex_escape(text):
    return _BIBTEX_SPECIAL.sub(r'\\\1', str(text))


def _bibtex_name(name):
    """Organisations go in braces so BibTeX doesn't split them into first and
    last names ("BigBrain project" must not become "project, BigBrain")."""
    name = _bibtex_escape(name.strip())
    words = re.findall(r'[A-Za-z]+', name.lower())
    if any(w.startswith(_ORG_WORDS) for w in words) or len(words) > 4:
        return '{' + name + '}'
    return name


def citation_key(dataset_id, year):
    """conp_<short id>_<year>, e.g. conp_BigBrain_3DClassifiedVolumes_2020."""
    short = re.sub(r'[^A-Za-z0-9]+', '_', str(dataset_id or 'dataset').split('/')[-1]).strip('_')
    return 'conp_' + (short or 'dataset') + ('_' + str(year) if year else '')


def citation_bibtex(creators, year, title, version, ark_url, dataset_id=None, doi=None, publisher=None):
    """BibTeX @misc entry (the type every BibTeX style knows)."""
    names = [c for c in (creators or []) if c]
    fields = []
    if names:
        fields.append(('author', ' and '.join(_bibtex_name(n) for n in names)))
    fields.append(('title', '{' + _bibtex_escape((title or '').strip()) + '}'))
    if year:
        fields.append(('year', str(year)))
    if version:
        fields.append(('version', _bibtex_escape(version)))
    if doi:
        if publisher:
            fields.append(('publisher', publisher))
        fields.append(('doi', doi))
        fields.append(('url', 'https://doi.org/' + doi))
    else:
        fields.append(('publisher', 'CONP Portal'))
        fields.append(('howpublished', 'Dataset, Canadian Open Neuroscience Platform (CONP) Portal'))
        if ark_url:
            fields.append(('url', ark_url))
    body = ',\n'.join('  {} = {{{}}}'.format(k, v) for k, v in fields)
    return '@misc{' + citation_key(dataset_id, year) + ',\n' + body + '\n}'


def citation_ris(creators, year, title, version, ark_url, doi=None, publisher=None):
    """RIS record of type DATA (Zotero, EndNote, Mendeley import it)."""
    lines = ['TY  - DATA']
    for name in (creators or []):
        if name:
            lines.append('AU  - ' + name.strip())
    lines.append('TI  - ' + (title or '').strip())
    if year:
        lines.append('PY  - ' + str(year))
    if version:
        lines.append('ET  - ' + str(version))
    if doi:
        if publisher:
            lines.append('PB  - ' + publisher)
        lines.append('DO  - ' + doi)
        lines.append('UR  - https://doi.org/' + doi)
    else:
        lines.append('PB  - CONP Portal')
        if ark_url:
            lines.append('UR  - ' + ark_url)
    lines.append('ER  - ')
    return '\n'.join(lines)


# --------------------------------------------------------------------------
# Dataset DOI (the depositor's own identifier, e.g. on Zenodo or OSF)
# --------------------------------------------------------------------------
_DOI = re.compile(r'(10\.\d{4,9}/[^\s"<>]+)', re.I)
_DOI_PUBLISHERS = (('10.5281/zenodo', 'Zenodo'), ('10.17605/osf.io', 'OSF'),
                   ('10.5683/sp', 'Borealis'), ('10.20383/', 'FRDR'),
                   ('10.18112/openneuro', 'OpenNeuro'))


def find_doi(value):
    """The bare DOI (10.xxxx/...) in a string, or None."""
    m = _DOI.search(str(value or ''))
    return m.group(1).rstrip('.,;)') if m else None


def dataset_doi(descriptor):
    """(doi, publisher) when the DATS identifier is a DOI, else (None, None)."""
    ident = (descriptor or {}).get('identifier') or {}
    if not isinstance(ident, dict):
        return None, None
    doi = find_doi(ident.get('identifier'))
    if not doi:
        return None, None
    low = doi.lower()
    publisher = next((name for prefix, name in _DOI_PUBLISHERS if low.startswith(prefix)), None)
    return doi, publisher


def created_year(descriptor):
    """Year of the record's "date created" (or first) date, when it has one."""
    dates = (descriptor or {}).get('dates') or []
    if not isinstance(dates, list):
        return None
    chosen = None
    for d in dates:
        if not isinstance(d, dict):
            continue
        kind = str((d.get('type') or {}).get('value', '')).lower()
        if 'creat' in kind or 'publi' in kind or 'release' in kind:
            chosen = d
            break
        chosen = chosen or d
    m = re.match(r'\s*(\d{4})', str((chosen or {}).get('date', '')))
    return m.group(1) if m else None


# --------------------------------------------------------------------------
# Primary publications: one reference each, in Text, BibTeX and RIS
# --------------------------------------------------------------------------
def _pub_authors(pub):
    names = []
    for a in pub.get('authors') or []:
        if not isinstance(a, dict):
            continue
        name = a.get('fullName') or ' '.join(x for x in (a.get('firstName'), a.get('lastName')) if x)
        if name:
            names.append(name.strip())
    if not names and pub.get('authorsList'):
        names = [str(pub['authorsList']).strip()]
    return names


def _pub_year(pub):
    for d in pub.get('dates') or []:
        if isinstance(d, dict):
            m = re.match(r'\s*(\d{4})', str(d.get('date', '')))
            if m:
                return m.group(1)
    return None


def publication_citations(descriptor):
    """The record's primary publications as references in three formats.

    Built from the DATS fields only (authors, title, venue, year, DOI); a
    record that gives little yields a short reference."""
    pubs = (descriptor or {}).get('primaryPublications') or []
    if isinstance(pubs, dict):
        pubs = [pubs]
    out = []
    for i, pub in enumerate(p for p in pubs if isinstance(p, dict)):
        title = str(pub.get('title') or '').strip().rstrip('.')
        if not title:
            continue
        authors = _pub_authors(pub)
        venue = str(pub.get('publicationVenue') or '').strip().rstrip('.')
        year = _pub_year(pub)
        doi = find_doi((pub.get('identifier') or {}).get('identifier') if isinstance(pub.get('identifier'), dict) else pub.get('identifier'))
        url = ('https://doi.org/' + doi) if doi else None
        if not url and isinstance(pub.get('identifier'), dict):
            ident = str(pub['identifier'].get('identifier') or '')
            url = ident if ident.startswith('http') else None

        if len(authors) > 3:
            who = ', '.join(authors[:3]) + ', et al.'
        else:
            who = ', '.join(authors)
        text = []
        if who:
            text.append('{} ({}).'.format(who, year) if year else (who if who.endswith('.') else who + '.'))
        text.append(title + '.')
        if venue:
            text.append(venue + '.')
        if url:
            text.append(url)

        first = re.sub(r'[^a-z]', '', (authors[0].split(',')[0].split()[-1] if authors else 'pub').lower()) or 'pub'
        key = '{}_{}{}'.format(first, year or 'nd', '' if i == 0 else '_' + str(i + 1))
        fields = []
        if authors:
            fields.append(('author', ' and '.join(_bibtex_escape(a) for a in authors)))
        fields.append(('title', '{' + _bibtex_escape(title) + '}'))
        if venue:
            fields.append(('journal', _bibtex_escape(venue)))
        if year:
            fields.append(('year', year))
        if doi:
            fields.append(('doi', doi))
        elif url:
            fields.append(('url', url))
        bibtex = '@article{' + key + ',\n' + ',\n'.join('  {} = {{{}}}'.format(k, v) for k, v in fields) + '\n}'

        ris = ['TY  - JOUR'] + ['AU  - ' + a for a in authors] + ['TI  - ' + title]
        if venue:
            ris.append('JO  - ' + venue)
        if year:
            ris.append('PY  - ' + year)
        if doi:
            ris.append('DO  - ' + doi)
        if url:
            ris.append('UR  - ' + url)
        ris.append('ER  - ')
        out.append({'text': ' '.join(text), 'bibtex': bibtex, 'ris': '\n'.join(ris), 'doi': doi})
    return out


# --------------------------------------------------------------------------
# Direct download from the host (Zenodo, OSF) instead of the Portal archive
# --------------------------------------------------------------------------
CRAWLER_MARKERS = ('.conp-zenodo-crawler.json', '.conp-osf-crawler.json')


def direct_download(descriptor, dataset_dir=None):
    """A browser download link at the dataset's host, when there is one.

    Only for public records on Zenodo or OSF, and only for datasets the
    Zenodo/OSF crawlers imported (their repository carries the crawler's
    marker file), so the files behind the link are the dataset's files. A
    dataset deposited elsewhere whose record still names an older Zenodo/OSF
    project (e.g. Calgary Preschool, now on the CONP community server) gets
    no such link. Uses the record's own access URL; for a Zenodo record
    without one, Zenodo's "download all" archive.
    Returns {"url", "host", "record", "format", "filename"} or None."""
    if dataset_dir is not None:
        import os
        if not any(os.path.exists(os.path.join(dataset_dir, m)) for m in CRAWLER_MARKERS):
            return None
    dists = (descriptor or {}).get('distributions') or []
    dist = dists[0] if isinstance(dists, list) and dists else (dists if isinstance(dists, dict) else {})
    access = dist.get('access') or {}
    auths = access.get('authorizations') or [{}]
    first = auths[0] if isinstance(auths, list) and auths else {}
    if str((first or {}).get('value', '')).lower() != 'public':
        return None
    landing = str(access.get('landingPage') or '')
    url = str(access.get('accessURL') or '')
    host = 'Zenodo' if 'zenodo.org' in (url + landing) else ('OSF' if 'osf.io' in (url + landing) else None)
    if not host:
        return None
    if not url:
        m = re.search(r'zenodo\.org/records?/(\d+)', landing)
        if host == 'Zenodo' and m:
            url = 'https://zenodo.org/api/records/{}/files-archive'.format(m.group(1))
        else:
            return None
    if not url.startswith('https://'):
        return None
    filename = None
    m = re.search(r'/files/([^/?]+)', url)
    if m:
        filename = unescape(m.group(1))
    if '?zip=' in url or 'files-archive' in url or (filename or '').lower().endswith('.zip'):
        fmt = 'ZIP'
    else:
        fmt = None
    return {'url': url, 'host': host, 'record': landing or None, 'format': fmt, 'filename': filename}


# --------------------------------------------------------------------------
# The whole DATS record, formatted for reading
# --------------------------------------------------------------------------
_DATS_LABELS = {
    'title': 'Title', 'description': 'Description', 'identifier': 'Identifier', 'identifierSource': 'Source',
    'alternateIdentifiers': 'Other identifiers', 'licenses': 'Licences', 'creators': 'Creators',
    'types': 'Data types', 'distributions': 'Distributions', 'formats': 'Formats', 'size': 'Size',
    'access': 'Access', 'landingPage': 'Landing page', 'accessURL': 'Access URL',
    'authorizations': 'Authorizations', 'keywords': 'Keywords', 'version': 'Version', 'privacy': 'Privacy',
    'isAbout': 'Is about', 'primaryPublications': 'Primary publications', 'publicationVenue': 'Venue',
    'authorsList': 'Authors', 'authors': 'Authors', 'fullName': 'Name', 'firstName': 'First name',
    'lastName': 'Last name', 'name': 'Name', 'email': 'Email', 'affiliations': 'Affiliations',
    'roles': 'Roles', 'dates': 'Dates', 'date': 'Date', 'type': 'Type', 'storedIn': 'Stored in',
    'spatialCoverage': 'Spatial coverage', 'dimensions': 'Dimensions', 'producedBy': 'Produced by',
    'acknowledges': 'Acknowledges', 'funders': 'Funders', 'abbreviation': 'Abbreviation',
    'extraProperties': 'Additional properties',
}
_DATS_EXTRA = {
    'CONP_status': 'CONP status', 'origin_consortium': 'Origin: consortium', 'origin_institution': 'Origin: institution',
    'origin_city': 'Origin: city', 'origin_province': 'Origin: province', 'origin_country': 'Origin: country',
    'derivedFrom': 'Derived from', 'parent_dataset_id': 'Parent dataset', 'REB_statement': 'Ethics (REB) statement',
    'REB_number': 'Ethics (REB) number', 'registrationPage': 'Registration page', 'downloadOptions': 'Download options',
    'evidence_publication': 'Evidence publication', 'files': 'Files', 'subjects': 'Subjects', 'contact': 'Contact',
    'logo': 'Logo', 'Total number of sessions': 'Sessions',
}


def _dats_flat(v):
    """Collapse DATS wrappers: {"value": x}, {"name": x}, {"information": {...}}."""
    if isinstance(v, dict):
        keys = set(v)
        if 'value' in v and keys <= {'value', 'valueIRI'}:
            return v['value']
        if keys == {'name'}:
            return v['name']
        if keys == {'information'}:
            return _dats_flat(v['information'])
    return v


def _dats_value(v):
    from markupsafe import escape
    s = str(v)
    if s.startswith(('http://', 'https://')):
        return '<a href="{0}" target="_blank" rel="noopener noreferrer">{0}</a>'.format(escape(s))
    return str(escape(s))


def _dats_render(v):
    v = _dats_flat(v)
    if isinstance(v, list):
        items = [_dats_flat(x) for x in v]
        if all(not isinstance(x, (dict, list)) for x in items):
            return ', '.join(_dats_value(x) for x in items)
        return ''.join('<div class="dp-dats-item">{}</div>'.format(_dats_render(x)) for x in items)
    if isinstance(v, dict):
        if 'size' in v and 'unit' in v:
            v = dict(v)
            v['size'] = '{} {}'.format(v['size'], _dats_flat(v.pop('unit')))
        from markupsafe import escape
        rows = ''.join('<dt>{}</dt><dd>{}</dd>'.format(escape(_DATS_LABELS.get(k, k)), _dats_render(x)) for k, x in v.items())
        return '<dl class="dp-dats-sub">{}</dl>'.format(rows)
    return _dats_value(v)


def dats_record_html(descriptor):
    """The DATS record as nested definition lists: readable labels, with the
    raw field name underneath. Values are escaped; URLs become links."""
    from markupsafe import Markup, escape
    rows = []
    for key, value in (descriptor or {}).items():
        if key == 'extraProperties' and isinstance(value, list):
            for prop in value:
                if not isinstance(prop, dict):
                    continue
                cat = str(prop.get('category', ''))
                vals = ', '.join(_dats_value(_dats_flat(x)) for x in prop.get('values') or [])
                rows.append((_DATS_EXTRA.get(cat, cat), 'extraProperties · ' + cat, vals))
            continue
        rows.append((_DATS_LABELS.get(key, key), key, _dats_render(value)))
    body = ''.join('<dt>{}<span class="dp-dats-key">{}</span></dt><dd>{}</dd>'.format(escape(label), escape(raw), val)
                   for label, raw, val in rows)
    return Markup('<dl class="dp-dats">{}</dl>'.format(body))


def title_html(title):
    """The title with every tag escaped except <sub>/<sup> (e.g. "T<sub>1</sub>"),
    which some Zenodo titles carry."""
    from markupsafe import Markup, escape
    s = str(escape(title or ''))
    for tag in ('sub', 'sup'):
        s = s.replace('&lt;{}&gt;'.format(tag), '<{}>'.format(tag)).replace('&lt;/{}&gt;'.format(tag), '</{}>'.format(tag))
    return Markup(s)


# --------------------------------------------------------------------------
# Which ways to get the data apply to this dataset
# --------------------------------------------------------------------------
# Files a dataset repository holds besides its data: the DATS record, the
# README, a logo, crawler bookkeeping, licence files and git/DataLad plumbing.
_METADATA_ONLY = re.compile(
    r'^(DATS\.jsonld?|dats\.json|README(\.md|\.txt)?|readme\.md|logo\.\w+|LICEN[CS]E.*|CHANGES.*|'
    r'temp\.txt|\.gitattributes|\.gitmodules|\.conp-\w+-crawler\.json|[^/]+\.(png|jpe?g|svg|gif))$', re.I)
_PLUMBING_DIRS = ('.git', '.datalad', '.github')


def repository_has_data(dataset_dir):
    """True when the dataset's repository holds data DataLad can fetch
    (annexed files, plain data files or subdatasets), False when it holds
    only metadata (DATS, README, logo). None when the folder can't be read,
    so the page keeps its DataLad instructions rather than hide them."""
    import os
    if not dataset_dir or not os.path.isdir(dataset_dir):
        return None
    try:
        gitmodules = os.path.join(dataset_dir, '.gitmodules')
        if os.path.exists(gitmodules) and '[submodule' in open(gitmodules).read():
            return True
        for root, dirs, files in os.walk(dataset_dir):
            dirs[:] = [d for d in dirs if d not in _PLUMBING_DIRS]
            rel = os.path.relpath(root, dataset_dir)
            if rel != '.':
                return True  # any folder of its own holds data
            if any(not _METADATA_ONLY.match(f) for f in files):
                return True
        return False
    except OSError:
        return None


_HOSTS = (
    ('cbigr', 'C-BIG'), ('cbig.', 'C-BIG'), ('braincode', 'Brain-CODE'), ('eegnet', 'EEGNet'),
    ('preventad', 'PREVENT-AD'), ('centre-stopad', 'PREVENT-AD'), ('zenodo.org', 'Zenodo'),
    ('osf.io', 'OSF'), ('openneuro', 'OpenNeuro'), ('borealisdata', 'Borealis'),
    ('scholarsportal', 'Borealis'), ('frdr', 'FRDR'),
)


def host_name(url):
    """A readable name for the site a URL belongs to: "Brain-CODE" for
    braincode.ca, "C-BIG" for cbigr.loris.ca; otherwise the bare domain."""
    s = str(url or '').lower()
    if not s:
        return None
    for key, name in _HOSTS:
        if key in s:
            return name
    m = re.match(r'(?:mailto:)?(?:https?://)?(?:www\.)?([^/?#@]+@)?([^/?#]+)', s)
    return m.group(2) if m else None


RESTRICTED = ('registered', 'private', 'controlled')


def access_context(authorization, registration_page, landing_page, dataset_dir):
    """What the Get the data tab needs to decide which routes to show.

    restricted: the record's authorization says an account is needed (the
    authorization decides, not the host: LORIS also serves open data).
    has_data: the repository holds something DataLad can fetch.
    host: the name used in "Request access at …" / "Go to …"."""
    restricted = str(authorization or '').strip().lower() in RESTRICTED
    has_data = repository_has_data(dataset_dir)
    return {
        'restricted': restricted,
        'has_data': True if has_data is None else has_data,
        'host': host_name(registration_page) or host_name(landing_page),
        'source_host': host_name(landing_page),
    }
