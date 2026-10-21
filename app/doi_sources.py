"""Where a DOI comes from, so pages can show a small icon of the service
that registered it (Zenodo, OSF, ...) next to the DOI.

Known repository prefixes get the repository's own icon. Repositories that
register their DOIs through DataCite but have no icon here get DataCite's.
Any other DOI (journal articles, most of them registered through Crossref,
which can't be told from the prefix alone) gets the generic DOI icon.
To add a repository: put a 64 px PNG in app/static/img/doi/ and a line in
_SOURCES (longest prefixes first)."""
import re

_DOI = re.compile(r'(10\.\d{4,9}/[^\s"<>]+)', re.I)

# (prefix, name, icon file under static/img/doi/)
_SOURCES = (
    ('10.5281/zenodo', 'Zenodo', 'zenodo.svg'),
    ('10.17605/osf.io', 'OSF', 'osf.png'),
    ('10.20383/', 'FRDR', 'frdr.png'),
    ('10.18112/openneuro', 'OpenNeuro', 'openneuro.png'),
    ('10.55458/neurolibre', 'NeuroLibre/Evidence', None),   # uses img/evidence_logo.svg
    ('10.5683/', 'Borealis (DataCite)', 'datacite.png'),
    ('10.6084/m9.figshare', 'figshare (DataCite)', 'datacite.png'),
    ('10.5061/dryad', 'Dryad (DataCite)', 'datacite.png'),
)


def bare_doi(value):
    """The DOI (10.xxxx/...) in a string or URL, or None."""
    m = _DOI.search(str(value or ''))
    return m.group(1).rstrip('.,;)') if m else None


def doi_source(value):
    """{'doi', 'url', 'name', 'icon'} for a DOI or DOI URL, or None.
    'icon' is a path under static/."""
    doi = bare_doi(value)
    if not doi:
        return None
    low = doi.lower()
    for prefix, name, icon in _SOURCES:
        if low.startswith(prefix):
            return {'doi': doi, 'url': 'https://doi.org/' + doi, 'name': name,
                    'icon': 'img/doi/' + icon if icon else 'img/evidence_logo.svg'}
    return {'doi': doi, 'url': 'https://doi.org/' + doi, 'name': None, 'icon': 'img/doi/doi.png'}
