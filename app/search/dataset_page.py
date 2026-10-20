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


def citation_text(creators, year, title, version, ark_url):
    """Plain-text citation built from the record:
    Creators (year). Title, version X. CONP Portal. ARK."""
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


def citation_bibtex(creators, year, title, version, ark_url, dataset_id=None):
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
    fields.append(('publisher', 'CONP Portal'))
    fields.append(('howpublished', 'Dataset, Canadian Open Neuroscience Platform (CONP) Portal'))
    if ark_url:
        fields.append(('url', ark_url))
    body = ',\n'.join('  {} = {{{}}}'.format(k, v) for k, v in fields)
    return '@misc{' + citation_key(dataset_id, year) + ',\n' + body + '\n}'


def citation_ris(creators, year, title, version, ark_url):
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
    lines.append('PB  - CONP Portal')
    if ark_url:
        lines.append('UR  - ' + ark_url)
    lines.append('ER  - ')
    return '\n'.join(lines)
