"""Browser downloads from a dataset's or experiment's host, read from DATS.

Each DATS distribution with an ``access.accessURL`` is one downloadable part
of the record: the whole record for most, or one OSF component (or the code
repository linked to the OSF project) for records whose files are spread over
several. The Portal only shows a link it can check against the record itself:

- an OSF zip (``files.<region>.osf.io/v1/resources/<node>/providers/osfstorage/?zip=``)
  must name the record's own OSF project (its landing page) or the component
  the distribution names as its ``identifier``, and the ``zip`` parameter must
  be empty: OSF ignores its value, so ``.../resources/znt9d/...?zip=q482e``
  is the znt9d project, whatever follows ``zip=``;
- OSF zips of add-on storage (GitHub, GitLab, ...) are refused: OSF cuts
  those streams off after 64 KiB;
- a Zenodo file must be in the record named by the landing page;
- no zip address is guessed from a landing page any more: an OSF project's
  own storage can be empty (files in components or add-ons), and the guessed
  zip was then an empty 22-byte file.

OSF builds every zip on the fly (no stored copy, no Content-Length, no
resume; GitHub's archives likewise), so such a "streamed" zip larger than
``BROWSER_DOWNLOAD_MAX_GB`` (app config, default 50) is listed without a
download button: DataLad, which fetches file by file and can resume, is the
way to get it. Stored files (a Zenodo file, the Portal's own tar.gz) have a
known size and can be resumed, so the limit does not apply to them.
"""
import re
from html import unescape

DEFAULT_MAX_GB = 50

_UNITS = {'B': 1, 'KB': 1e3, 'MB': 1e6, 'GB': 1e9, 'TB': 1e12, 'PB': 1e15,
          'KIB': 1024, 'MIB': 1024 ** 2, 'GIB': 1024 ** 3, 'TIB': 1024 ** 4}

_OSF_NODE = re.compile(r'osf\.io/([a-z0-9]{5})(?:[/?#]|$)', re.I)
_OSF_WB = re.compile(r'^https://files\.(?:[a-z0-9-]+\.)?osf\.io/v1/resources/([a-z0-9]{5})/providers/([a-z0-9_-]+)(/[^?#]*)?(\?[^#]*)?$', re.I)
_OSF_FILE = re.compile(r'^https://osf\.io/download/[a-z0-9]+/?$', re.I)
_ZENODO_REC = re.compile(r'zenodo\.org/(?:records?|deposit)/(\d+)', re.I)
_ZENODO_DOI = re.compile(r'10\.5281/zenodo\.(\d+)', re.I)
_GITHUB_ARCHIVE = re.compile(r'^https://(?:github\.com/[^/]+/[^/]+/archive/|codeload\.github\.com/)', re.I)


def _as_list(dists):
    if isinstance(dists, list):
        return [d for d in dists if isinstance(d, dict)]
    if isinstance(dists, dict):
        return [dists]
    return []


def distribution_bytes(dist):
    """A distribution's size in bytes, or None when it has none we can read."""
    try:
        size = float((dist or {}).get('size'))
    except (TypeError, ValueError):
        return None
    unit = str(((dist or {}).get('unit') or {}).get('value', 'B')).strip().upper() or 'B'
    return size * _UNITS[unit] if unit in _UNITS else None


def total_bytes(descriptor):
    """Sum of the distributions' sizes (a record split into parts lists one
    size per part), or None when none can be read."""
    sizes = [distribution_bytes(d) for d in _as_list((descriptor or {}).get('distributions'))]
    sizes = [s for s in sizes if s is not None]
    return sum(sizes) if sizes else None


def human_size(n):
    """1234567 -> '1.2 MB' (decimal units, like the rest of the Portal)."""
    if n is None:
        return None
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    n = float(n)
    while n >= 1000 and i < len(units) - 1:
        n /= 1000
        i += 1
    return '{} {}'.format(round(n, 1), units[i]).replace('.0 ', ' ')


def size_label(n):
    """Bytes in the Portal's DATS size style ("303.8 MB", "1.0 GB")."""
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    n = float(n)
    i = 0
    while n > 1000 and i < len(units) - 1:
        n /= 1000
        i += 1
    return '{} {}'.format(round(n, 1), units[i])


def osf_node(url):
    m = _OSF_NODE.search(str(url or ''))
    return m.group(1).lower() if m else None


def zenodo_record(url):
    url = str(url or '')
    m = _ZENODO_REC.search(url) or _ZENODO_DOI.search(url)
    return m.group(1) if m else None


def _identifier_url(dist):
    ident = (dist or {}).get('identifier')
    if isinstance(ident, dict):
        return str(ident.get('identifier') or '')
    return str(ident or '')


def check_access_url(dist, landing=None):
    """(host, format, problem) for a distribution's accessURL.

    ``landing`` is the record's landing page (the first distribution's) when
    the distribution has none of its own. ``problem`` is None for a link the
    Portal can show, else a short reason (also used by conp-dataset's
    validator wording)."""
    access = (dist or {}).get('access') or {}
    url = str(access.get('accessURL') or '').strip()
    own_landing = str(access.get('landingPage') or landing or '')
    if not url:
        return None, None, 'no accessURL'
    if not url.startswith('https://'):
        return None, None, 'not an https address'
    if 'files-archive' in url:
        return 'Zenodo', None, 'Zenodo does not serve /files-archive'

    m = _OSF_WB.match(url)
    if m:
        node, provider, query = m.group(1).lower(), m.group(2).lower(), m.group(4) or ''
        allowed = {osf_node(own_landing), osf_node(_identifier_url(dist))} - {None}
        if node not in allowed:
            return 'OSF', None, 'names OSF project {} but the record is {}'.format(
                node, ', '.join(sorted(allowed)) or 'not an OSF project')
        params = dict(p.split('=', 1) if '=' in p else (p, '') for p in query.lstrip('?').split('&') if p)
        if 'zip' in params:
            if params['zip']:
                return 'OSF', 'ZIP', 'the zip= parameter must be empty (OSF ignores its value)'
            if provider != 'osfstorage':
                return 'OSF', 'ZIP', 'OSF cannot zip {} add-on storage (the stream stops after 64 KiB)'.format(provider)
            return 'OSF', 'ZIP', None
        return 'OSF', None, None
    if _OSF_FILE.match(url):
        return 'OSF', None, None

    if 'zenodo.org' in url:
        rec, own = zenodo_record(url), zenodo_record(own_landing) or zenodo_record(_identifier_url(dist))
        if rec and own and rec != own:
            return 'Zenodo', None, 'names Zenodo record {} but the record is {}'.format(rec, own)
        fmt = 'ZIP' if re.search(r'\.zip(?:/content)?(?:[?#]|$)', url, re.I) else None
        return 'Zenodo', fmt, None
    if _GITHUB_ARCHIVE.match(url):
        return 'GitHub', 'ZIP', None
    return None, ('ZIP' if re.search(r'\.zip(?:[?#]|$)', url, re.I) else None), None


def _authorized(descriptor):
    dists = _as_list((descriptor or {}).get('distributions'))
    auths = ((dists[0].get('access') or {}).get('authorizations') if dists else None) or [{}]
    first = auths[0] if isinstance(auths, list) and auths else (auths if isinstance(auths, dict) else {})
    return str((first or {}).get('value', '')).strip().lower() in ('public', 'open')


def max_bytes():
    try:
        from flask import current_app
        gb = current_app.config.get('BROWSER_DOWNLOAD_MAX_GB', DEFAULT_MAX_GB)
    except Exception:  # outside an app context (scripts, unit tests)
        gb = DEFAULT_MAX_GB
    try:
        return float(gb) * 1e9 if gb not in (None, '') else None
    except (TypeError, ValueError):
        return DEFAULT_MAX_GB * 1e9


def is_streamed(url):
    """A zip the host builds while it streams it: no size known in advance,
    no resume (OSF ``?zip=``, GitHub archives)."""
    url = str(url or '')
    return bool(_OSF_WB.match(url) and re.search(r'[?&]zip(?:=|&|$)', url)) or bool(_GITHUB_ARCHIVE.match(url))


def download_parts(descriptor, require_public=True):
    """The record's browser-downloadable parts, in DATS order.

    Each: {"url", "host", "format", "filename", "title", "size", "bytes",
    "streamed", "too_large", "record"}; only a streamed zip can be too large. Distributions whose accessURL fails the checks
    are left out. Empty list when the record is not public."""
    if require_public and not _authorized(descriptor):
        return []
    dists = _as_list((descriptor or {}).get('distributions'))
    landing = str(((dists[0].get('access') or {}).get('landingPage') if dists else '') or '')
    limit = max_bytes()
    parts = []
    for dist in dists:
        host, fmt, problem = check_access_url(dist, landing)
        if problem:
            continue
        access = dist.get('access') or {}
        url = str(access['accessURL']).strip()
        filename = None
        m = re.search(r'/files/([^/?]+)', url)
        if m:
            filename = unescape(m.group(1))
            if filename.lower().endswith('.zip'):
                fmt = 'ZIP'
        n = distribution_bytes(dist)
        parts.append({
            'url': url, 'host': host, 'format': fmt, 'filename': filename,
            'title': str(dist.get('title') or '').strip() or None,
            'size': human_size(n), 'bytes': n, 'streamed': is_streamed(url),
            'too_large': bool(is_streamed(url) and limit is not None and n is not None and n > limit),
            'record': str(access.get('landingPage') or landing or '') or None,
        })
    return parts
