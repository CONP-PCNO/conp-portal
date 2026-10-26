"""Experiment pages and the Experiments list (2026 redesign), built like the
dataset page: everything comes from the experiment's DATS.json, its README
and the Experiment row. No conp-react bundle is used."""
import os
import re

from flask import url_for

from app.dats import DEFAULT_LOGO
from app.experiments.dats import DATSExperiment, _flat
from app.search.dataset_page import (
    citation_bibtex,
    citation_key,
    citation_ris,
    citation_text,
    clean_version,
    created_year,
    dataset_doi,
    host_name,
    licence_badges,
    osf_zip_url,
    publication_citations,
)

# DataCite resourceTypeGeneral used in the plain-text citation of a task
# package (stimuli + scripts); the RIS type to match.
RESOURCE_TYPE = 'software'
RIS_TYPE = 'COMP'


def experiment_slug(exp):
    """Folder name in conp-experiments ("projects/BADE-evidence-integration"
    -> "BADE-evidence-integration")."""
    return (exp.experiment_id or str(exp.id)).split('/', 1)[-1]


def software_name(value):
    """'NBS Presentation version 17' -> 'NBS Presentation' (for filters)."""
    return re.split(r'\s+(?:version|v)\s*[\d.]', str(value or ''), maxsplit=1, flags=re.I)[0].strip()


def software_short(value):
    """'NBS Presentation version 17' -> 'NBS Presentation 17' (for chips)."""
    return re.sub(r'\s+version\s+', ' ', str(value or ''), flags=re.I).strip()


def _join(values, sep=', '):
    return sep.join(v for v in values if v)


def _date(value):
    return value.strftime('%Y-%m-%d') if hasattr(value, 'strftime') else (str(value)[:10] if value else None)


def _size(dats):
    try:
        return dats.size
    except Exception:  # an odd size field must not break the page
        return None


def logo_url(exp, dats):
    path = dats.LogoFilepath
    if path and path != DEFAULT_LOGO and not str(path).startswith('http') and os.path.isfile(path):
        return url_for('experiments.get_experiment_logo', experiment_id=exp.id)
    return url_for('static', filename='img/experiments/default.svg')


def experiment_download(exp, dats):
    """The browser download for an experiment: the Portal's own .zip when the
    server has one, else OSF's zip of the authors' record for an open
    experiment on OSF (the address OSF agreed the CONP may link to).
    Returns {"url", "host"} or None."""
    if os.path.isfile((exp.fspath or '') + '.zip'):
        return {'url': url_for('experiments.download', experiment_id=exp.id), 'host': None}
    if str(dats.privacy or '').strip().lower() not in ('open', 'public', ''):
        return None
    osf = osf_zip_url(dats.sources)
    return {'url': osf, 'host': 'OSF'} if osf else None


def experiment_card(exp):
    """What the Experiments list shows for one experiment (and filters on)."""
    dats = DATSExperiment(exp.fspath)
    software = [s for s in (dats.software_requirements or []) if s]
    return {
        'id': exp.id,
        'slug': experiment_slug(exp),
        'url': url_for('experiments.view', key=experiment_slug(exp)),
        'title': exp.name or dats.name,
        'description': dats.description or '',
        'creators': dats.creators or [],
        'added': _date(exp.date_added_to_portal),
        'version': clean_version(dats.version),
        'views': exp.views or 0,
        'logo': logo_url(exp, dats),
        'canadian': str(dats.conpStatus or '').lower() not in ('', 'external'),
        'functions': [str(f).capitalize() for f in _flat([dats.function_assessed]) if f],
        'modalities': _flat(dats.experiment_modalities),
        'software': [software_name(s) for s in software],
        'software_label': _join(software_short(s) for s in software),
        'languages': _flat(dats.languages),
        'size': _size(dats),
        'keywords': [str(k) for k in (dats.keywords or [])],
        # The list's "Get the task" row: the ways the experiment page offers.
        'zip': bool(experiment_download(exp, dats)),
        'open': str(dats.privacy or '').strip().lower() == 'open',
        'source_label': _join([
            (host_name(dats.sources) or 'source record') if str(dats.sources or '').startswith('http') else None,
            'GitHub' if str(exp.remoteUrl or '').startswith('http') else None], ' and '),
    }


FACETS = (('function', 'Function assessed', 'functions'), ('modality', 'Modality', 'modalities'),
          ('software', 'Software', 'software'), ('language', 'Language', 'languages'))
SORTS = (('added', 'Recently added'), ('name', 'Name A–Z'), ('views', 'Most viewed'))


def filter_cards(cards, query, selected, sort):
    """The list page: text search, facet filters (any value within a facet,
    all facets together), sort, and facet counts over the matching set."""
    words = [w for w in re.split(r'\W+', (query or '').lower()) if w]

    def text(card):
        return ' '.join([card['title'], card['description'], ' '.join(card['creators']),
                         ' '.join(card['keywords']), ' '.join(card['functions']), ' '.join(card['modalities']),
                         card['software_label'], ' '.join(card['languages'])]).lower()

    def keep(card):
        if any(w not in text(card) for w in words):
            return False
        for key, _label, field in FACETS:
            want = selected.get(key) or []
            if want and not set(want) & set(card[field]):
                return False
        return True

    shown = [c for c in cards if keep(c)]
    if sort == 'name':
        shown.sort(key=lambda c: c['title'].lower())
    elif sort == 'views':
        shown.sort(key=lambda c: -c['views'])
    else:
        shown.sort(key=lambda c: c['added'] or '', reverse=True)

    facets = []
    for key, label, field in FACETS:
        counts = {}
        for c in shown:
            for v in set(c[field]):
                counts[v] = counts.get(v, 0) + 1
        for v in selected.get(key) or []:
            counts.setdefault(v, 0)
        items = [{'value': v, 'count': n, 'checked': v in (selected.get(key) or [])}
                 for v, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0].lower()))]
        if items:
            facets.append({'key': key, 'label': label, 'items': items})
    return shown, facets


def experiment_page(exp, readme_html=''):
    """Everything the experiment page template needs."""
    dats = DATSExperiment(exp.fspath)
    descriptor = dats.descriptor
    card = experiment_card(exp)
    doi, publisher = dataset_doi(descriptor)
    year = created_year(descriptor) or (card['added'] or '')[:4] or None
    creators = card['creators']
    version = card['version']
    software = [software_short(s) for s in (dats.software_requirements or []) if s]
    devices = _flat(dats.device_requirements)
    other = dats.additional_requirements
    origin_text = _join(_flat(dats.find_extra_property('origin_' + part))[:1][0]
                        for part in ('institution', 'city', 'province', 'country')
                        if _flat(dats.find_extra_property('origin_' + part)))
    remote = (exp.remoteUrl or '').strip()
    if remote.endswith('.git'):
        remote = remote[:-4]
    return {
        'card': card,
        'doi': doi,
        'doi_publisher': publisher,
        'description': dats.description or '',
        'licences': licence_badges(dats.licenses),
        'licence_names': [str(lic) for lic in (dats.licenses or [])] if isinstance(dats.licenses, list)
        else ([str(dats.licenses)] if dats.licenses else []),
        'stimuli': dats.stimuli,
        'needs': [row for row in (
            ('Software', _join(software)),
            ('Devices', _join(devices + other, '; ')),
            ('Set-ups', _join(card['modalities'])),
            ('Accessibility', _join(_flat(dats.accessibility))),
        ) if row[1]],
        'download': (experiment_download(exp, dats) or {}).get('url'),
        'download_host': (experiment_download(exp, dats) or {}).get('host'),
        'source_url': ('https://doi.org/' + doi) if doi else (dats.sources if str(dats.sources or '').startswith('http') else None),
        'source_name': publisher or host_name(dats.sources),
        'remote_url': remote if remote.startswith('http') else None,
        'readme': readme_html,
        'validation_measures': dats.validation_measures,
        'validation_populations': dats.validation_populations,
        'publications': publication_citations(descriptor),
        'funding': [str(a) for a in (dats.acknowledges or [])],
        'contact': dats.contacts,
        'origin': origin_text,
        'devices': devices,
        'other_requirements': other,
        'is_about': [str(a) for a in (dats.isAbout or [])],
        'citation': citation_text(creators, year, card['title'], version, None, doi=doi, publisher=publisher,
                                  resource_type=RESOURCE_TYPE),
        'citation_bibtex': citation_bibtex(creators, year, card['title'], version, None, card['slug'], doi=doi,
                                           publisher=publisher, kind='Experiment'),
        'citation_ris': citation_ris(creators, year, card['title'], version, None, doi=doi, publisher=publisher,
                                     ris_type=RIS_TYPE),
        'citation_key': citation_key(card['slug'], year),
    }
