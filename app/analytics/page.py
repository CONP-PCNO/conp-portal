"""The Analytics page (/analytics): what the Portal holds, how it is used, and
where its datasets show up in research. Everything is computed here, on the
server, from the Portal's own data:

  the catalogue   the datasets the Data page lists, the tools the Tools page lists
  use             Matomo's daily tables, filled by `flask update_analytics`
  research use    DATA_PATH/research_use/latest.json, written by `flask update_research_use`
  visitors        DATA_PATH/analytics/countries.json, written by `flask update_analytics`

Every chart has its numbers in a table underneath and as CSV (/analytics/data/<name>.csv).
The page is computed at most once an hour.
"""
import datetime as dt
import json
import math
import os
import re
import time
from collections import Counter, defaultdict
from html import escape

from flask import current_app
from markupsafe import Markup
from sqlalchemy import func

GREEN, BLUE, INK, MUTED, GRID = '#177245', '#1a5fb4', '#1d2129', '#5b6270', '#eceef1'

# Search terms that are scanner probes, not people searching.
JUNK_SEARCH = re.compile(r'sssied|knxs|[<>$"\'`;{}]|script|https?:|\.\./|^.{60,}$', re.I)

# Access levels, from each dataset's DATS "privacy" (records without one are open).
ACCESS_LEVELS = [
    ('Open', 'freely available, no account needed'),
    ('Registered', 'for researchers who register with the data provider'),
    ('Controlled', 'after a committee approves a research proposal'),
    ('Private', "only the project's own researchers; listed so the data can be found"),
]


# ------------------------------------------------------------------ modality labels

def modality_group(value):
    """A short display label for a DATS modality value, or None for values that are
    not a modality (file formats, placeholders). Draft grouping (value-labels list)."""
    v = str(value or '').strip().rstrip(',').lower()
    if not v or re.search(r'vcf|bam|fastq|hdf5|nifti|ped file', v) or v in (
            'unknown', 'dataset', 'quality control subject', 'qa summary results'):
        return None
    rules = [
        (r'sequenc|genom|genet|genotype|cytoscan', 'Genomics'),
        (r'transcript|expression', 'Transcriptomics'),
        (r'diffusion|dti', 'Diffusion MRI'),
        (r'fmri|functional|bold|resting state', 'fMRI'),
        (r'mri|t1w|^mr$|structural|angio|asl|susceptib|weighted|neuroimaging|imaging studies|connectome', 'MRI'),
        (r'eeg|electroenceph', 'EEG'),
        (r'^meg$', 'MEG'), (r'^pet$', 'PET'), (r'^ct$', 'CT'), (r'^mrs$', 'MR spectroscopy'),
        (r'histolog|brain bank', 'Histology'),
        (r'demograph|clinic|medic|registry|follow-up|risk|symptom|surgical|treatment|quality of life',
         'Clinical and demographic'),
        (r'cognit|behav|neuropsych|survey|abilit|mood|reaction|memory|neurosensory|saccad|balance|locomotion|sleep|pain',
         'Behavioural and cognitive'),
        (r'protein|metabol|biomarker|cerebrospinal|epigen|sample', 'Other omics, biospecimens'),
    ]
    for pattern, label in rules:
        if re.search(pattern, v):
            return label
    return None


# ------------------------------------------------------------------ small SVG / HTML charts

def _nice_tick(ymax):
    step = 10 ** math.floor(math.log10(max(ymax, 1))) / 10
    for m in (1, 2, 2.5, 5, 10, 20, 25, 50):
        if ymax / (m * step) <= 5:
            return m * step
    return 10 * step


def line_chart(series, labels, label, gaps=(), w=1040, h=240, end_labels=True):
    """One or more lines over the same x labels; None values leave a gap; `gaps`
    are (first index, last index) ranges drawn hatched with "not recorded"."""
    pl, pr, pt, pb = 46, 130 if end_labels else 16, 14, 30
    iw, ih = w - pl - pr, h - pt - pb
    n = max(len(labels) - 1, 1)
    ymax = max([v for s in series for v in s['values'] if v is not None] or [1])
    tick = _nice_tick(ymax)
    top = tick * math.ceil(ymax / tick)

    def X(i):
        return pl + iw * i / n

    def Y(v):
        return pt + ih * (1 - v / top)
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{escape(label)}" class="an-svg">',
           '<defs><pattern id="an-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           '<rect width="6" height="6" fill="#f6f7f8"/><line x1="0" y1="0" x2="0" y2="6" stroke="#dfe2e6" stroke-width="2"/></pattern></defs>']
    half = iw / n / 2
    for a, b in gaps:
        x0, x1 = X(a) - half, X(b) + half
        out.append(f'<rect x="{x0:.1f}" y="{pt}" width="{x1 - x0:.1f}" height="{ih}" fill="url(#an-hatch)"/>')
        if b - a >= 2:
            out.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{pt + 14}" font-size="11.5" fill="{MUTED}" text-anchor="middle">not recorded</text>')
    t = 0
    while t <= top + 1e-9:
        out.append(f'<line x1="{pl}" x2="{pl + iw}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="{GRID}"/>')
        out.append(f'<text x="{pl - 8}" y="{Y(t) + 4:.1f}" font-size="12" fill="{MUTED}" text-anchor="end">{int(t):,}</text>')
        t += tick
    for i, lab in enumerate(labels):
        if lab:
            out.append(f'<text x="{X(i):.1f}" y="{h - 8}" font-size="12" fill="{MUTED}" text-anchor="middle">{escape(lab)}</text>')
    for s in series:
        segs, cur = [], []
        for i, v in enumerate(s['values']):
            if v is None:
                if cur:
                    segs.append(cur)
                cur = []
            else:
                cur.append((X(i), Y(v)))
        if cur:
            segs.append(cur)
        for seg in segs:
            pts = ' '.join(f'{x:.1f},{y:.1f}' for x, y in seg)
            out.append(f'<polyline fill="none" stroke="{s["color"]}" stroke-width="2" stroke-linejoin="round" '
                       f'stroke-linecap="round" points="{pts}"/>')
            if len(seg) == 1:
                out.append(f'<circle cx="{seg[0][0]:.1f}" cy="{seg[0][1]:.1f}" r="3" fill="{s["color"]}"/>')
        if end_labels:
            idx = [i for i, v in enumerate(s['values']) if v is not None]
            if idx:
                li = idx[-1]
                lv = s['values'][li]
                out.append(f'<circle cx="{X(li):.1f}" cy="{Y(lv):.1f}" r="4" fill="{s["color"]}" stroke="#fff" stroke-width="2"/>')
                out.append(f'<text x="{X(li) + 10:.1f}" y="{Y(lv) + 4 + s.get("dy", 0):.1f}" font-size="13" font-weight="600" '
                           f'fill="{INK}">{escape(s["name"])} {lv:,}</text>')
    out.append('</svg>')
    return Markup(''.join(out))


def world_map(counts, total, labels=None):
    """Countries shaded by visits (four steps); small places as dots; each with a tooltip."""
    path = os.path.join(current_app.root_path, 'static', 'analytics', 'world-110m-paths.json')
    with open(path) as f:
        geo = json.load(f)
    ramp = ['#cfe8d7', '#7cc297', '#2e8b57', '#14532d']

    def fill(v):
        if not v:
            return '#eef0f3'
        return ramp[3 if v >= 1000 else 2 if v >= 200 else 1 if v >= 50 else 0]

    def tip(code, v):
        name = (labels or {}).get(code) or geo['names'].get(code, code.upper())
        if not v:
            return f'{name}: no visits recorded'
        share = 100 * v / total
        return f'{name}: {v:,} visits ({share:.0f}%)' if share >= 1 else f'{name}: {v:,} visits ({share:.1f}%)'
    out = [f'<svg viewBox="{geo["viewBox"]}" width="100%" role="img" class="an-svg" '
           'aria-label="Map of visits by country; the table beside it lists the numbers">']
    for code, d in geo['shapes'].items():
        v = counts.get(code, 0)
        out.append(f'<path d="{d}" fill="{fill(v)}" stroke="#fff" stroke-width="0.6"><title>{escape(tip(code, v))}</title></path>')
    for code, (x, y) in geo['dots'].items():
        v = counts.get(code, 0)
        if v:
            out.append(f'<circle cx="{x}" cy="{y}" r="{5 if v >= 100 else 3.5}" fill="{fill(v)}" stroke="#fff" stroke-width="1.5">'
                       f'<title>{escape(tip(code, v))}</title></circle>')
    out.append('</svg>')
    return Markup(''.join(out))


# ------------------------------------------------------------------ the sections

def catalogue():
    from app.pipelines.routes import _tool_elements, get_cbrain_availability, get_tool_icons, tool_icon
    from app.pipelines.tool_list import tool_card
    from app.search.routes import _dataset_elements

    elements = _dataset_elements(None, False)
    with open(os.path.join(os.getcwd(), 'app/static/pipelines/cbrain-conp-pipeline.json')) as f:
        launch_ids = set(json.load(f).keys())
    availability = get_cbrain_availability()
    on_cbrain = launch_ids | set(availability.keys())
    icons, default_icon = get_tool_icons()
    tools = [tool_card(e, availability.get(e.get('id')), on_cbrain, launch_ids,
                       tool_icon(e.get('id'), icons, default_icon)) for e in _tool_elements()]

    years = sorted({str(e.get('dateAdded') or '')[:4] for e in elements if e.get('dateAdded')}
                   | {str(t.get('published') or '')[:4] for t in tools if t.get('published')})
    years = [y for y in years if y.isdigit()]
    ds_by_year = Counter(str(e.get('dateAdded') or '')[:4] for e in elements)
    tl_by_year = Counter(str(t.get('published') or '')[:4] for t in tools)
    ds_cum, tl_cum, a, b = [], [], 0, 0
    for y in years:
        a += ds_by_year.get(y, 0)
        b += tl_by_year.get(y, 0)
        ds_cum.append(a if a else None)
        tl_cum.append(b if b else None)

    modalities = Counter()
    for e in elements:
        for g in {modality_group(m) for m in (e.get('modalities') or [])} - {None}:
            modalities[g] += 1

    access = Counter()
    for e in elements:
        p = str(e.get('privacy') or 'open').strip().lower()
        access[{'public': 'Open', 'open': 'Open', 'registered': 'Registered', 'controlled': 'Controlled',
                'private': 'Private'}.get(p, 'Open')] += 1
    origin = Counter('International' if str(e.get('conpStatus') or '').lower() == 'external' else 'Canadian'
                     for e in elements)
    runs = Counter()
    for t in tools:
        runs['On CBRAIN' if t['cbrain'] else 'Computer or HPC only'] += 1

    return {
        'n_datasets': len(elements), 'n_tools': len(tools), 'n_open': access.get('Open', 0),
        'n_canadian': origin.get('Canadian', 0),
        'growth': {'years': years, 'datasets': ds_cum, 'tools': tl_cum, 'rows': list(zip(years, ds_cum, tl_cum)),
                   'svg': line_chart([{'name': 'Datasets', 'values': ds_cum, 'color': GREEN, 'dy': -6},
                                      {'name': 'Tools', 'values': tl_cum, 'color': BLUE, 'dy': 10}], years,
                                     'Datasets and tools on the Portal, running total by year')},
        'modality': modalities.most_common(14),
        'access': [(lvl, access.get(lvl, 0), why) for lvl, why in ACCESS_LEVELS],
        'origin': [('Canadian', origin.get('Canadian', 0)), ('International', origin.get('International', 0))],
        'runs': [('On CBRAIN', runs.get('On CBRAIN', 0)), ('Computer or HPC only', runs.get('Computer or HPC only', 0))],
        'tool_titles': {t['id']: t['title'] for t in tools},
        'tools': tools,
    }


def visits(months=36):
    from app.models import MatomoDailyVisitsSummary as V
    rows = V.query.with_entities(V.date, V.nb_visits).all()
    by_month, zero_days, days = defaultdict(int), Counter(), Counter()
    for date, n in rows:
        m = str(date)[:7]
        by_month[m] += n or 0
        days[m] += 1
        if not n:
            zero_days[m] += 1
    if not by_month:
        return None
    last = max(by_month)
    y, mo = int(last[:4]), int(last[5:7])
    keys = []
    for _ in range(months):
        keys.append(f'{y:04d}-{mo:02d}')
        mo -= 1
        if mo == 0:
            y, mo = y - 1, 12
    keys.reverse()
    gap = [m for m in keys if days[m] and zero_days[m] / days[m] >= 0.4]
    values = [None if m in gap else by_month.get(m) for m in keys]
    gaps, start = [], None
    for i, m in enumerate(keys + ['']):
        if m in gap and start is None:
            start = i
        elif m not in gap and start is not None:
            gaps.append((start, i - 1))
            start = None
    labels = [f'Jan {m[:4]}' if m.endswith('-01') else (f'{dt.date(1, int(m[5:7]), 1):%b} {m[:4]}' if i == 0 else '')
              for i, m in enumerate(keys)]
    return {'months': keys, 'values': [by_month.get(m, 0) for m in keys], 'gap_months': gap,
            'rows': [(m, by_month.get(m, 0), 'no' if m in gap else 'yes') for m in keys],
            'last12': sum(by_month.get(m, 0) for m in keys[-12:]), 'period': f'{keys[-12]} – {keys[-1]}',
            'svg': line_chart([{'name': 'Visits', 'values': values, 'color': GREEN}], labels, 'Visits per month',
                              gaps=gaps)}


def most_viewed(period, tool_titles, n=10):
    from app.models import Dataset
    from app.models import MatomoDailyGetDatasetPageViewsSummary as D
    from app.models import MatomoDailyGetPageUrlsSummary as P
    since = (dt.date.today() - dt.timedelta(days=365)).isoformat() if period == '12m' else '0000'
    ds = (D.query.with_entities(D.dataset_id, func.sum(D.nb_visits)).filter(D.date >= since)
          .group_by(D.dataset_id).order_by(func.sum(D.nb_visits).desc()).limit(n * 2).all())
    names = {d.dataset_id: d.name for d in Dataset.query.filter(Dataset.dataset_id.in_([r[0] for r in ds])).all()}
    datasets = [{'id': i, 'title': names[i], 'url': f'/dataset?id={i}', 'visits': int(v or 0)}
                for i, v in ds if i in names][:n]
    tl = (P.query.with_entities(P.label, func.sum(P.nb_visits)).filter(P.date >= since)
          .filter(P.label.like('/pipeline?id=%')).group_by(P.label).order_by(func.sum(P.nb_visits).desc())
          .limit(n * 3).all())
    tools = []
    for label, v in tl:
        tid = label.split('id=', 1)[1]
        if tid in tool_titles:
            tools.append({'id': tid, 'title': tool_titles[tid], 'url': label, 'visits': int(v or 0)})
    return {'datasets': datasets, 'tools': tools[:n]}


def searches(tools, n=15):
    from app.models import MatomoDailyGetSiteSearchKeywords as K
    from app.pipelines.tool_list import filter_cards
    from app.search.routes import _dataset_elements
    since = (dt.date.today() - dt.timedelta(days=365)).isoformat()
    rows = (K.query.with_entities(K.label, func.sum(K.nb_visits)).filter(K.date >= since)
            .group_by(K.label).order_by(func.sum(K.nb_visits).desc()).limit(400).all())
    out = []
    for label, v in rows:
        if not label or JUNK_SEARCH.search(label):
            continue
        n_ds = len(_dataset_elements(label, False))
        shown, _facets = filter_cards([dict(t) for t in tools], label, {}, 'relevance')
        out.append({'term': label, 'visits': int(v or 0), 'datasets': n_ds, 'tools': len(shown)})
        if len(out) >= n:
            break
    return out


def countries():
    path = os.path.join(current_app.config['DATA_PATH'], 'analytics', 'countries.json')
    if not os.path.exists(path):
        return None
    with open(path) as f:
        data = json.load(f)
    rows = [r for r in data.get('rows', []) if r.get('nb_visits')]
    total = sum(r['nb_visits'] for r in rows)
    counts = {str(r.get('code') or '').lower(): r['nb_visits'] for r in rows}
    top = [{'name': r['label'], 'visits': r['nb_visits'], 'share': 100 * r['nb_visits'] / total} for r in rows[:12]]
    rest = total - sum(r['visits'] for r in top)
    return {'total': total, 'n': len([r for r in rows if (r.get('code') or 'xx') != 'xx']), 'top': top,
            'rest': rest, 'rest_n': max(len(rows) - 12, 0), 'period': data.get('period'),
            'map': world_map(counts, total, {str(r.get('code') or '').lower(): r['label'] for r in rows}), 'rows': rows}


def research():
    from app import research_use
    latest = research_use.load_latest(current_app.config['DATA_PATH'])
    if not latest:
        return None
    used = sorted([(i, d) for i, d in latest['datasets'].items() if d['n_works']], key=lambda x: (-x[1]['n_works'], x[1]['title']))
    t = latest['totals']
    yrs = t['per_year']
    first = min([int(y) for y in yrs] or [dt.date.today().year])
    years = [(str(y), yrs.get(str(y), 0)) for y in range(max(first, dt.date.today().year - 7), dt.date.today().year + 1)]
    names = {'openalex': 'OpenAlex', 'europepmc': 'Europe PMC', 'datacite': 'DataCite', 'curated': 'reported to us'}
    found_by = ', '.join(f"{names.get(k, k)} {v}" for k, v in sorted(t['per_source'].items(), key=lambda x: -x[1]) if v)
    return {'updated': latest['generated'][:10], 'datasets_used': t['datasets_used'], 'papers': t['papers'], 'found_by': found_by,
            'per_source': t['per_source'], 'conp_mentions': latest['conp_mentions']['distinct'],
            'rows': [{'id': i, 'title': d['title'], 'short': short_title(d['title']), 'n': d['n_works']} for i, d in used],
            'bar_rows': [(short_title(d['title']), d['n_works'], i, d['title']) for i, d in used],
            'table_rows': [(d['title'], d['n_works']) for i, d in used],
            'years': years, 'year_max': max([v for _y, v in years] or [1]) or 1}


def short_title(t, n=46):
    t = re.sub(r'\s+', ' ', t).strip()
    if ':' in t and 3 <= len(t.split(':')[0]) <= 32:
        return t.split(':')[0]
    m = re.match(r'^(.{3,40}?\([A-Z][A-Za-z0-9-]{1,10}\))', t)
    if m and len(t) > n and len(m.group(1)) <= 34:
        return m.group(1)
    if len(t) <= n:
        return t
    return t[:n - 1].rsplit(' ', 1)[0] + '…'


_CACHE = {}
EMPTY_CATALOGUE = {'n_datasets': 0, 'n_tools': 0, 'n_open': 0, 'n_canadian': 0,
                   'growth': {'years': [], 'datasets': [], 'tools': [], 'rows': [], 'svg': ''},
                   'modality': [], 'access': [], 'origin': [], 'runs': [], 'tool_titles': {}, 'tools': []}


def page_context(period='all'):
    """Everything the page shows, computed at most once an hour per period."""
    key = (period, int(time.time() // 3600))
    if key in _CACHE:
        return _CACHE[key]

    def safe(fn, *args, default=None):
        try:
            return fn(*args)
        except Exception:   # one section's missing data never takes the page down
            current_app.logger.exception('Analytics section %s failed', fn.__name__)
            return default
    cat = safe(catalogue, default=None) or EMPTY_CATALOGUE
    ctx = {'catalogue': cat, 'visits': safe(visits), 'period': period,
           'viewed': safe(most_viewed, period, cat['tool_titles'], default={'datasets': [], 'tools': []}),
           'searches': safe(searches, cat['tools'], default=[]), 'countries': safe(countries),
           'research': safe(research), 'updated': dt.date.today().isoformat()}
    _CACHE.clear()
    _CACHE[key] = ctx
    return ctx


def csv_rows(ctx, name):
    """(header, rows) for /analytics/data/<name>.csv."""
    cat = ctx['catalogue']
    if name == 'catalogue-growth':
        g = cat['growth']
        return ['year', 'datasets (running total)', 'tools (running total)'], list(zip(g['years'], g['datasets'], g['tools']))
    if name == 'modality':
        return ['modality', 'datasets'], cat['modality']
    if name == 'access':
        return ['access level', 'datasets', 'meaning'], cat['access']
    if name == 'origin':
        return ['origin', 'datasets'], cat['origin']
    if name == 'tools-runs':
        return ['runs on', 'tools'], cat['runs']
    if name == 'visits' and ctx['visits']:
        v = ctx['visits']
        return ['month', 'visits', 'recorded'], [(m, n, 'no' if m in v['gap_months'] else 'yes')
                                                 for m, n in zip(v['months'], v['values'])]
    if name == 'most-viewed-datasets':
        return ['dataset', 'id', 'visits'], [(d['title'], d['id'], d['visits']) for d in ctx['viewed']['datasets']]
    if name == 'most-viewed-tools':
        return ['tool', 'id', 'visits'], [(d['title'], d['id'], d['visits']) for d in ctx['viewed']['tools']]
    if name == 'research-use' and ctx['research']:
        return ['dataset', 'id', 'papers'], [(r['title'], r['id'], r['n']) for r in ctx['research']['rows']]
    if name == 'research-use-years' and ctx['research']:
        return ['year', 'papers'], ctx['research']['years']
    if name == 'searches':
        rows = [(s['term'], s['visits'], s['datasets'], s['tools']) for s in ctx['searches']]
        return ['search', 'visits', 'datasets found', 'tools found'], rows
    if name == 'countries' and ctx['countries']:
        return ['country', 'visits'], [(r['label'], r['nb_visits']) for r in ctx['countries']['rows']]
    return None, None
