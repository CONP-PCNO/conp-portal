"""Helpers for the tool page (pipeline.html).

Everything is derived from the tool's Boutiques descriptor (as cached from
Zenodo) and the Portal's own data files; nothing is written per tool.
"""
import re


def _as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def tag_list(tags):
    """Flatten the descriptor's tags ({"domain": [...]} or a string) into a
    list of display tags. The bare "Boutiques" tag the importer adds to every
    tool is dropped, since it says nothing about the tool."""
    out = []
    if isinstance(tags, dict):
        for value in tags.values():
            for v in _as_list(value):
                if isinstance(v, (str, int, float)) and not isinstance(v, bool):
                    out.append(str(v))
    elif isinstance(tags, str):
        out = [t.strip() for t in tags.split(',')]
    seen, result = set(), []
    for t in out:
        if t and t.lower() != 'boutiques' and t.lower() not in seen:
            seen.add(t.lower())
            result.append(t)
    return result


_DOCKER_HUB_HOSTS = ('index.docker.io', 'docker.io', 'hub.docker.com',
                     'registry.hub.docker.com', 'registry-1.docker.io')


def container_info(image):
    """Describe the descriptor's container image.

    Returns None when there is no image, otherwise a dict with the full
    reference (e.g. docker://freesurfer/freesurfer:8.2.0), a Docker Hub link
    when the image lives there, and the Apptainer build source and image file
    name for running it on an HPC cluster."""
    if not isinstance(image, dict) or not image.get('image'):
        return None
    name = str(image['image']).strip()
    index = str(image.get('index') or '').strip()
    ctype = str(image.get('type') or '').strip().lower()
    # Descriptors name Docker images' registry in several ways; Apptainer
    # builds all of them from docker://. Docker Hub given as a host name
    # (index.docker.io, docker.io, hub.docker.com, ...) is docker://; another
    # registry host (ghcr.io, quay.io, ...) goes in front of the image name
    # unless the name already starts with it; "docker:<image>:<tag>" (no //)
    # carries the full image reference itself.
    if index.startswith('docker:') and not index.startswith('docker://'):
        name = index[len('docker:'):].strip() or name
        index = 'docker://'
    elif ctype == 'docker' and index and '://' not in index:
        host = index.strip('/').lower()
        if host not in _DOCKER_HUB_HOSTS and not name.lower().startswith(host + '/'):
            name = host + '/' + name
        index = 'docker://'
    if not index:
        index = 'docker://' if ctype == 'docker' or '/' in name or ':' in name else ''
    if index and not index.endswith('://'):
        index = index.rstrip('/') + '/'
    reference = index + name if index else name

    hub_url = None
    if index in ('docker://', 'index.docker.io/', 'docker.io/'):
        repo = name.split('@')[0].rsplit(':', 1)[0] if ':' in name.split('/')[-1] else name.split('@')[0]
        first = repo.split('/')[0]
        if '.' not in first and ':' not in first:  # not another registry (quay.io, ghcr.io, ...)
            repo = repo.lower()  # Docker Hub names are lower-case; descriptors sometimes aren't
            hub_url = ('https://hub.docker.com/r/' + repo) if '/' in repo else ('https://hub.docker.com/_/' + repo)

    pull = None
    if index == 'docker://':
        pull = reference
    elif index.startswith(('shub://', 'library://', 'oras://')):
        pull = reference
    sif = re.sub(r'[^A-Za-z0-9._-]+', '_', name.split('/')[-1]) + '.sif' if pull else None
    return {'reference': reference, 'hub_url': hub_url, 'pull': pull, 'sif': sif}


def _num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _fmt(n):
    return ('%d' % n) if float(n).is_integer() else ('%.1f' % n)


def resources_text(resources):
    """Suggested resources as one line, in the descriptor's own terms:
    "4 cores, 16 GB memory, walltime estimate about 24 min".

    Boutiques asks for RAM in GB, but many descriptors give it in MB; values of
    256 or more are read as MB. The walltime estimate is in seconds."""
    if not isinstance(resources, dict):
        return None
    parts = []
    cores = _num(resources.get('cpu-cores'))
    if cores:
        parts.append('{} core{}'.format(_fmt(cores), '' if cores == 1 else 's'))
    ram = _num(resources.get('ram'))
    if ram:
        gb = ram / 1024 if ram >= 256 else ram
        parts.append('{} GB memory'.format(_fmt(round(gb, 1))))
    nodes = _num(resources.get('nodes'))
    if nodes and nodes > 1:
        parts.append('{} nodes'.format(_fmt(nodes)))
    wall = _num(resources.get('walltime-estimate'))
    if wall:
        if wall < 90:
            when = '{} s'.format(_fmt(wall))
        elif wall < 3600:
            when = '{} min'.format(_fmt(round(wall / 60)))
        else:
            when = '{} h'.format(_fmt(round(wall / 3600, 1)))
        parts.append('walltime estimate about ' + when)
    return ', '.join(parts) or None


def split_inputs(inputs):
    """Required inputs first (in descriptor order), then the optional ones."""
    items = [i for i in _as_list(inputs) if isinstance(i, dict)]
    required = [i for i in items if not i.get('optional', False)]
    optional = [i for i in items if i.get('optional', False)]
    return required, optional


def licence_input(element):
    """The required input that asks for a software licence file (FreeSurfer's
    license.txt in 41 descriptors), so the page can say where to get one.
    Returns {"id", "name", "freesurfer"} or None."""
    text = ' '.join(str(element.get(k) or '') for k in ('name', 'title', 'description', 'tool-version')).lower()
    image = str((element.get('container-image') or {}).get('image') or '').lower()
    icon = element.get('icon') if isinstance(element.get('icon'), dict) else {}
    for i in _as_list(element.get('inputs')):
        if not isinstance(i, dict) or i.get('optional', False):
            continue
        label = '{} {}'.format(i.get('id') or '', i.get('name') or '').lower()
        if 'licen' in label:
            fs = ('freesurfer' in label or 'freesurfer' in text or 'freesurfer' in image
                  or 'recon-all' in text or str(icon.get('label') or '').lower() == 'freesurfer')
            return {'id': i.get('id'), 'name': i.get('name') or i.get('id'), 'freesurfer': fs}
    return None


def runs_long(element):
    """True for tools whose real runs take hours whatever the descriptor's
    estimate says (FreeSurfer's recon-all family)."""
    text = ' '.join(str(element.get(k) or '') for k in ('name', 'title', 'description')).lower()
    return 'recon-all' in text or 'recon_all' in text or 'reconall' in text


def tool_citation(element):
    """The tool's references in the three formats the dataset pages use. A
    tool on the Portal is its Boutiques descriptor's Zenodo record, so that is
    what is cited (DataCite form, resource type "software"); the page says to
    cite the software itself too. Returns a dict, or None without a DOI."""
    from app.search.dataset_page import citation_bibtex, citation_key, citation_ris, citation_text
    doi = str(element.get('doi') or '').strip()
    if not doi:
        return None
    doi = re.sub(r'^(https?://(dx\.)?doi\.org/|doi:)', '', doi, flags=re.I)
    author = re.sub(r'\s+', ' ', str(element.get('author') or '')).strip()
    creators = [author] if author else []
    year = str(element.get('publicationdate') or '')[:4] or None
    title = element.get('title') or element.get('name') or element.get('id')
    version = str(element.get('tool-version') or element.get('version') or '').strip() or None
    args = (creators, year, title, version, None)
    key_id = str(element.get('id') or 'tool').replace('.', '_')
    return {
        'text': citation_text(*args, doi=doi, publisher='Zenodo', resource_type='software'),
        'bibtex': citation_bibtex(*args, key_id, doi=doi, publisher='Zenodo', kind='Software'),
        'ris': citation_ris(*args, doi=doi, publisher='Zenodo', ris_type='COMP'),
        'key': citation_key(key_id, year),
        'doi': doi,
    }


def job_size(resources):
    """Cores and memory (GB, rounded up) for the example job script, from the
    descriptor's suggested resources (RAM over 256 is read as MB)."""
    import math
    if not isinstance(resources, dict):
        return None, None
    cores = _num(resources.get('cpu-cores'))
    ram = _num(resources.get('ram'))
    if ram and ram >= 256:
        ram = ram / 1024.0
    return (int(cores) if cores and cores >= 1 else None), (int(math.ceil(ram)) if ram and ram > 0 else None)


def tool_page_context(element):
    """Everything the tool page needs beyond the descriptor fields."""
    required, optional = split_inputs(element.get('inputs'))
    platforms = element.get('platforms') or [{}]
    return {
        'tags': tag_list(element.get('tags')),
        'container': container_info(element.get('container-image')),
        'resources': resources_text(element.get('suggested-resources')),
        'runs_long': runs_long(element),
        'cpus': job_size(element.get('suggested-resources'))[0],
        'mem_gb': job_size(element.get('suggested-resources'))[1],
        'licence_input': licence_input(element),
        'cite': tool_citation(element),
        'required_inputs': required,
        'optional_inputs': optional,
        'outputs': [o for o in _as_list(element.get('output-files')) if isinstance(o, dict)],
        'cbrain_launch': (platforms[0] or {}).get('uri') or '',
        'zenodo_record': 'https://zenodo.org/records/' + element['id'].split('.', 1)[1]
        if str(element.get('id', '')).startswith('zenodo.') else None,
    }
