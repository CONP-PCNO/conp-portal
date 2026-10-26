"""The Tools & Pipelines list (/pipelines): one card per tool, a filter
sidebar and sort, server-rendered in the Data page pattern (option A of the
Portal page mockups, approved 25 Oct 2026).

Related descriptors (FreeSurfer-Recon-all and its 19 variants, fsl_bet and
FslBet601…) are shown as one card with "+ n related descriptors" unless the
visitor asks to see every descriptor separately.
"""
import re

FACETS = (
    ('runs', 'Runs on', 'runs_facet'),
    ('software', 'Software', 'software_facet'),
    ('domain', 'Domain', 'domain_facet'),
    ('container', 'Container', 'container_facet'),
)
SORTS = (
    ('downloads', 'Most downloaded'),
    ('published', 'Recently published'),
    ('name', 'Name A–Z'),
    ('cbrain', 'Runs on CBRAIN first'),
)
PER_PAGE = (30, 50, 100)
FACET_SHOWN = 8
NOT_STATED = 'Not stated'
OTHER_SOFTWARE = 'Other tools'

RUN_CBRAIN = 'CBRAIN'
RUN_COMPUTER = 'Your computer (Boutiques)'
RUN_CLUSTER = 'Alliance cluster (container)'

# Descriptor domain tags -> filter labels; tags that say nothing about the
# kind of data (neuroinformatics, boutiques, typos) are left out.
_DOMAINS = {
    'mri': 'MRI', 'qsm': 'MRI', 'fmri': 'fMRI', 'dmri': 'Diffusion MRI', 'diffusion mri': 'Diffusion MRI',
    'diffusion': 'Diffusion MRI', 'dwi': 'Diffusion MRI', 'eeg': 'EEG', 'eegnet': 'EEG', 'meg': 'MEG',
    'fnirs': 'fNIRS', 'pet': 'PET', 'nuclear medicine': 'PET', 'bioinformatics': 'Genomics', 'genetic': 'Genomics',
    'blast': 'Genomics', 'connectome': 'Connectomics', 'segmentation': 'Segmentation',
    'image processing': 'Image processing', 'multiple-sclerosis': 'Multiple sclerosis', 'bigbrain': 'BigBrain',
    'quality': 'Quality control', 'testing': None, 'neuroinformatics': None, 'neuroimaging': None,
    'neuroimaing': None, 'boutiques': None, 'bids': None, 'nifti': None, 'norms': None, 'noise': None,
    'glm': None, 'fuzzy': None, 'brainstorm': None, 'aqua': None,
}
_CONTAINERS = {'singularity': 'Apptainer / Singularity', 'apptainer': 'Apptainer / Singularity', 'docker': 'Docker'}


def _int(v):
    try:
        return int(str(v).replace(',', '').strip())
    except (TypeError, ValueError):
        return None


def domain_tags(tags):
    """The descriptor's domain tags as a list, whatever shape they come in
    (a list, one string, or a comma string such as "domain:mri")."""
    if isinstance(tags, dict):
        tags = tags.get('domain') or []
    if isinstance(tags, str):
        parts = [p.strip() for p in tags.split(',')]
        tags = [p.split(':', 1)[1] if p.lower().startswith('domain:') else p for p in parts]
        tags = [t for t in tags if t and t.lower() != 'boutiques']
    return [str(t).strip().lower() for t in (tags or []) if str(t).strip()]


def domain_labels(tags):
    out = set()
    for t in domain_tags(tags):
        label = _DOMAINS.get(t, t[:1].upper() + t[1:])
        if label:
            out.add(label)
    return sorted(out, key=str.lower)


def _stem(title):
    """"FreeSurfer7-Recon-all-qcache" -> "freesurferreconallqcache"."""
    return re.sub(r'[^a-z]', '', str(title or '').lower())


def tool_card(e, cbrain_info, on_cbrain, launch_ids, icon):
    """What the list shows (and filters on) for one tool, from a
    pipeline_search-style element (keys lower-cased, no hyphens)."""
    image = e.get('containerimage') or {}
    ctype = str((image.get('type') if isinstance(image, dict) else '') or e.get('container') or '').lower()
    container = _CONTAINERS.get(ctype)
    domains = domain_labels(e.get('tags'))
    family = (icon or {}).get('label') if icon and not icon.get('generic') else None
    tid = e.get('id')
    runs = []
    if tid in on_cbrain:
        runs.append(RUN_CBRAIN)
    runs.append(RUN_COMPUTER)
    if container:
        runs.append(RUN_CLUSTER)
    versions = (cbrain_info or {}).get('versions') or []
    if versions:
        span = versions[0] if len(versions) == 1 else '{} to {}'.format(versions[0], versions[-1])
        cbrain_label = '{} {}'.format((cbrain_info or {}).get('software', ''), span).strip()
    else:
        cbrain_label = None
    inputs = e.get('inputs') or []
    description = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', str(e.get('description') or ''))).strip()
    return {
        'id': tid,
        'url': '/pipeline?id={}'.format(tid),
        'title': e.get('title') or e.get('name') or tid,
        'author': str(e.get('author') or '').strip(),
        'published': e.get('publicationdate') or None,
        'version': str(e.get('toolversion') or e.get('version') or '').strip() or None,
        'description': description,
        'icon': (icon or {}).get('src'),
        'family': family,
        'domains': domains,
        'container': container,
        'inputs': len(inputs) if isinstance(inputs, list) else None,
        'downloads': _int(e.get('downloads')) or 0,
        'cbrain': tid in on_cbrain,
        'cbrain_label': cbrain_label,
        'cbrain_launch': tid in launch_ids,
        'cluster': bool(container),
        'stem': _stem(e.get('title') or e.get('name')),
        'related': [],
        # facet values
        'runs_facet': runs,
        'software_facet': [family or OTHER_SOFTWARE],
        'domain_facet': domains or [NOT_STATED],
        'container_facet': [container or 'None'],
    }


def group_related(cards):
    """One card per group of related descriptors: same software family and
    one title the start of the other once digits and punctuation are
    dropped ("FreeSurfer-Recon-all", "FreeSurfer7-Recon-all-qcache"). The
    most downloaded leads; the others go in its "related" list."""
    leaders = []
    for c in sorted(cards, key=lambda c: (-c['downloads'], c['title'].lower())):
        lead = None
        if c['family'] and len(c['stem']) >= 5:
            for g in leaders:
                if g['family'] == c['family'] and (c['stem'].startswith(g['stem']) or g['stem'].startswith(c['stem'])):
                    lead = g
                    break
        if lead is None:
            c = dict(c, related=[])
            leaders.append(c)
        else:
            lead['related'].append({'title': c['title'], 'url': c['url']})
    return leaders


def selected_filters(args):
    """Ticked values, plus the old list's parameters: tags= (domain tags,
    comma-separated) and cbrain=."""
    selected = {key: [v for v in args.getlist(key) if v] for key, _label, _field in FACETS}
    for t in (args.get('tags') or '').split(','):
        if t.strip():
            selected['domain'] += domain_labels([t.strip()]) or []
    if (args.get('cbrain') or '').lower() in ('true', '1', 'yes', 'on'):
        selected['runs'].append(RUN_CBRAIN)
    return {k: list(dict.fromkeys(v)) for k, v in selected.items()}


_OLD_SORTS = {'downloads-desc': 'downloads', 'publicationdate-desc': 'published', 'title-asc': 'name',
              'conpStatus': 'published'}


def chosen_sort(args):
    sort = args.get('sort') or _OLD_SORTS.get(args.get('sortKey') or '', 'downloads')
    return sort if sort in dict(SORTS) else 'downloads'


def chosen_per_page(args):
    n = _int(args.get('show') or args.get('max_per_page'))
    return n if n in PER_PAGE else PER_PAGE[0]


def filter_cards(cards, query, selected, sort):
    words = [w for w in re.split(r'\W+', (query or '').lower()) if w]

    def text(c):
        return ' '.join([c['title'], c['description'], c['author'], c['family'] or '', ' '.join(c['domains']),
                         c['id'] or '']).lower()

    def keep(c, skip=None):
        # Every word must start a word somewhere (as on the Data page since #1021).
        if words:
            tokens = re.findall(r'\w+', text(c))
            if not all(any(t.startswith(w) for t in tokens) for w in words):
                return False
        for key, _label, field in FACETS:
            if key == skip:
                continue
            want = selected.get(key) or []
            if want and not set(want) & set(c[field]):
                return False
        return True

    shown = [c for c in cards if keep(c)]
    if sort == 'name':
        shown.sort(key=lambda c: c['title'].lower())
    elif sort == 'published':
        shown.sort(key=lambda c: c['published'] or '', reverse=True)
    elif sort == 'cbrain':
        shown.sort(key=lambda c: (not c['cbrain'], -c['downloads']))
    else:
        shown.sort(key=lambda c: (-c['downloads'], c['title'].lower()))

    facets = []
    for key, label, field in FACETS:
        counts = {}
        for c in cards:
            if keep(c, skip=key):
                for v in set(c[field]):
                    counts[v] = counts.get(v, 0) + 1
        for v in selected.get(key) or []:
            counts.setdefault(v, 0)
        last = (NOT_STATED, OTHER_SOFTWARE, 'None')
        items = [{'value': v, 'count': n, 'checked': v in (selected.get(key) or [])}
                 for v, n in sorted(counts.items(), key=lambda kv: (kv[0] in last, -kv[1], kv[0].lower()))]
        if key == 'runs':  # fixed order: CBRAIN, computer, cluster
            order = [RUN_CBRAIN, RUN_COMPUTER, RUN_CLUSTER]
            items.sort(key=lambda i: order.index(i['value']) if i['value'] in order else 9)
        if items:
            head = items[:FACET_SHOWN] + [i for i in items[FACET_SHOWN:] if i['checked']]
            more = [i for i in items[FACET_SHOWN:] if not i['checked']]
            facets.append({'key': key, 'label': label, 'items': head, 'more': more})
    return shown, facets
