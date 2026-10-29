"""Research use of CONP datasets: papers that cite a dataset or name it, from
several sources, each paper counted once.

Run by `flask update_research_use` (weekly, from cron). It writes, under
DATA_PATH/research_use/:

  latest.json          what the Portal shows (dataset pages, Data cards, Analytics)
  snapshots/DATE.json  a copy of each run, kept, so any two runs can be compared
  CHANGES.md           one entry per run: papers added and removed for each dataset,
                       totals before and after (also shown at /analytics/research-use/changes)

Sources
  OpenAlex      works that cite the dataset's DOI; works whose full text contains it
                (list queries need OPENALEX_API_KEY; without it only single lookups run)
  Europe PMC    records whose text or references contain the dataset's DOI; records with
                the dataset's exact title that also name the CONP (titles of 5+ words,
                not for external mirrors such as 1000 Genomes)
  DataCite      citation links to the dataset DOI and its versions (Zenodo, OSF)

Counted once: works sharing a DOI, PMID, PMCID, OpenAlex ID or normalised title are
merged and keep the list of sources that found them. Not counted: the dataset's own
records and the publications its DATS record lists (primaryPublications, Evidence),
works whose title is the dataset's own (90% similar), papers about the CONP itself,
and records that are not papers (datasets, software).

Curated corrections live in the repository, in
app/static/datasets/research-use-overrides.json:
  {"add":    [{"dataset": "projects/...", "doi": "10....", "note": "reported by ..."}],
   "remove": [{"dataset": "projects/...", "doi": "10....", "note": "not a use: ..."}]}
They are applied on every run, so a correction is never undone by the next update.

If a source fails on more than a few requests, the run stops without replacing
latest.json, so a network problem never shows up as papers "removed".
"""
import datetime as dt
import difflib
import hashlib
import json
import os
import re
import time
import unicodedata
import urllib.parse
from collections import Counter, defaultdict

import requests

UA = {'User-Agent': 'CONP-Portal-research-use/1.0 (mailto:info@conp.ca)'}
CACHE_DAYS = 6
NOT_PAPERS = {'dataset', 'software', 'paratext', 'other', 'peer-review', 'erratum', 'retraction'}
DATACITE_PREFIXES = ('10.5281/', '10.17605/', '10.18112/', '10.6084/', '10.5061/', '10.48324/', '10.20383/')
CONP_NAME = 'Canadian Open Neuroscience Platform'


# ---------------------------------------------------------------- normalising

def ndoi(d):
    if not d:
        return None
    d = str(d).strip().lower()
    d = re.sub(r'^(https?://(dx\.)?doi\.org/|doi:\s*)', '', d)
    return d if d.startswith('10.') else None


def ntitle(t):
    if not t:
        return None
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'[^a-z0-9]+', ' ', t).strip()
    return t if len(t) >= 25 else None


def name_keys(names):
    """(surname, first initial) for each name, in "First Last", "Last, First" or "Last FM"."""
    out = set()
    for n in names:
        n = unicodedata.normalize('NFKD', n or '').encode('ascii', 'ignore').decode().lower().strip()
        if not n:
            continue
        if ',' in n:
            last, first = [x.strip() for x in n.split(',', 1)]
        else:
            parts = n.replace('.', ' ').split()
            if len(parts) < 2:
                continue
            if len(parts[-1]) <= 2:
                last, first = ' '.join(parts[:-1]), parts[-1]
            else:
                last, first = parts[-1], parts[0]
        if last and first:
            out.add((last.split()[-1], first[0]))
    return out


def is_own_title(t, own_titles):
    n = ntitle(t)
    if not n:
        return False
    return any(n == o or difflib.SequenceMatcher(None, n, o).ratio() >= 0.9 for o in own_titles if o)


def about_conp(t):
    return CONP_NAME.lower() in (ntitle(t) or '')


# ---------------------------------------------------------------- what to look for

def dataset_inputs(dataset_id, descriptor, evidence_doi=None):
    """DOIs and names for one dataset, from its DATS descriptor."""
    ids = set()
    ident = (descriptor.get('identifier') or {}).get('identifier')
    if ndoi(ident):
        ids.add(ndoi(ident))
    text = json.dumps(descriptor.get('distributions', []))
    for rec in re.findall(r'zenodo\.org/records?/(\d+)', text):
        ids.add(f'10.5281/zenodo.{rec}')
    for osf in re.findall(r'osf\.io/([a-z0-9]{5})(?![a-z0-9])', text.lower()):
        ids.add(f'10.17605/osf.io/{osf}')
    for ds in re.findall(r'openneuro\.org/datasets/(ds\d{6})', text.lower()):
        ids.add(f'10.18112/openneuro.{ds}')
    pubs = descriptor.get('primaryPublications') or []
    if isinstance(pubs, dict):
        pubs = [pubs]
    pub_dois = {ndoi((p.get('identifier') or {}).get('identifier')) for p in pubs if isinstance(p, dict)}
    pub_titles = {ntitle(p.get('title')) for p in pubs if isinstance(p, dict)}
    if ndoi(evidence_doi):
        pub_dois.add(ndoi(evidence_doi))
    names = []
    for c in descriptor.get('creators', []) or []:
        if c.get('lastName') or c.get('firstName'):
            names.append(f"{c.get('firstName', '')} {c.get('lastName', '')}".strip())
        elif c.get('name') and not c.get('abbreviation'):
            names.append(c['name'])
    status = ''
    for p in descriptor.get('extraProperties', []) or []:
        if p.get('category') == 'CONP_status':
            status = str(((p.get('values') or [{}])[0]).get('value', '')).lower()
    return {'id': dataset_id, 'title': re.sub(r'\s+', ' ', descriptor.get('title', '')).strip(),
            'dois': sorted(ids), 'publication_dois': sorted(filter(None, pub_dois)),
            'publication_titles': sorted(filter(None, pub_titles)), 'creators': names, 'external': status == 'external'}


# ---------------------------------------------------------------- fetching

class Fetcher:
    """Cached GETs: a response younger than CACHE_DAYS is reused, so a run that
    stops half-way picks up where it left off. Counts failures per source."""

    def __init__(self, cache_dir, openalex_key=None, session=None):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.key = openalex_key
        self.session = session or requests.Session()
        self.failures = Counter()
        self.requests = Counter()

    def get(self, source, url):
        path = os.path.join(self.cache_dir, hashlib.sha1(url.encode()).hexdigest() + '.json')
        if os.path.exists(path) and time.time() - os.path.getmtime(path) < CACHE_DAYS * 86400:
            with open(path) as f:
                return json.load(f)
        self.requests[source] += 1
        for attempt in range(3):
            try:
                r = self.session.get(url, headers=UA, timeout=40)
                if r.status_code == 404:
                    data = {'_not_found': True}
                elif r.status_code == 200:
                    data = r.json()
                else:
                    time.sleep(2 * (attempt + 1))
                    continue
                with open(path, 'w') as f:
                    json.dump(data, f)
                time.sleep(0.12)
                return data
            except (requests.RequestException, ValueError):
                time.sleep(2 * (attempt + 1))
        self.failures[source] += 1
        return None

    # OpenAlex
    def openalex_work(self, doi):
        return self.get('openalex', 'https://api.openalex.org/works/doi:' + urllib.parse.quote(doi, safe='/:'))

    def openalex_list(self, flt):
        if not self.key:
            return []
        out, cursor = [], '*'
        while cursor and len(out) < 1000:
            q = urllib.parse.urlencode({'filter': flt, 'per-page': 200, 'cursor': cursor, 'api_key': self.key,
                                        'select': 'id,doi,title,publication_year,type,ids,authorships,primary_location'})
            d = self.get('openalex', 'https://api.openalex.org/works?' + q)
            if not d or d.get('_not_found'):
                break
            out += d.get('results', [])
            cursor = (d.get('meta') or {}).get('next_cursor')
            if not d.get('results'):
                break
        return out

    # Europe PMC
    def europepmc(self, query):
        out, cursor = [], '*'
        for _ in range(10):
            u = ('https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resultType=lite&pageSize=100'
                 '&query=' + urllib.parse.quote(query) + '&cursorMark=' + urllib.parse.quote(cursor))
            d = self.get('europepmc', u)
            if not d or d.get('_not_found'):
                break
            res = (d.get('resultList') or {}).get('result', [])
            out += res
            nxt = d.get('nextCursorMark')
            if not res or not nxt or nxt == cursor or len(res) < 100:
                break
            cursor = nxt
        return out

    # DataCite
    def datacite(self, doi):
        return self.get('datacite', 'https://api.datacite.org/dois/' + urllib.parse.quote(doi, safe='/'))


# ---------------------------------------------------------------- one record per find

def _from_openalex(w, source):
    ids = w.get('ids') or {}
    loc = (w.get('primary_location') or {}).get('source') or {}
    return {'doi': ndoi(w.get('doi')), 'pmid': (ids.get('pmid') or '').rsplit('/', 1)[-1] or None,
            'pmcid': (ids.get('pmcid') or '').rsplit('/', 1)[-1] or None, 'openalex': w.get('id'),
            'title': w.get('title') or w.get('display_name'), 'year': w.get('publication_year'),
            'type': w.get('type'), 'venue': loc.get('display_name'),
            'authors': [a['author']['display_name'] for a in w.get('authorships', []) or [] if a.get('author')],
            'source': source}


def _from_europepmc(h, source):
    return {'doi': ndoi(h.get('doi')), 'pmid': h.get('pmid'), 'pmcid': h.get('pmcid'), 'openalex': None,
            'title': h.get('title'), 'year': int(h['pubYear']) if str(h.get('pubYear', '')).isdigit() else None,
            'type': 'preprint' if h.get('source') == 'PPR' else 'article', 'venue': h.get('journalTitle'),
            'authors': [a.strip() for a in (h.get('authorString') or '').rstrip('.').split(',') if a.strip()],
            'source': source}


def find_works(inp, fetch):
    """Every record any source returns for one dataset (before merging)."""
    finds, own_ids = [], set(inp['dois']) | set(inp['publication_dois'])
    for d in inp['dois']:
        # Full-text and Europe PMC searches run whether or not OpenAlex has a record
        # for the DOI itself; citations need that record.
        w = fetch.openalex_work(d)
        if w and not w.get('_not_found'):
            own_ids.add(w.get('id'))
            if w.get('cited_by_count'):
                wid = w['id'].rsplit('/', 1)[-1]
                finds += [_from_openalex(x, 'openalex-cites') for x in fetch.openalex_list('cites:' + wid)]
        finds += [_from_openalex(x, 'openalex-text') for x in fetch.openalex_list(f'fulltext.search:"{d}"')]
        finds += [_from_europepmc(h, 'europepmc-doi') for h in fetch.europepmc(f'"{d}"')]
    for d in inp['publication_dois']:
        w = fetch.openalex_work(d)
        if w and not w.get('_not_found'):
            own_ids.add(w.get('id'))
    words = re.findall(r'[A-Za-z0-9]+', inp['title'])
    if not inp['external'] and len(words) >= 5:
        q = inp['title'].replace('"', '')
        finds += [_from_europepmc(h, 'europepmc-title') for h in fetch.europepmc(f'"{q}" AND ("{CONP_NAME}" OR "CONP")')]
    seen, queue = set(), [d for d in inp['dois'] if d.startswith(DATACITE_PREFIXES)]
    while queue and len(seen) <= 25:
        d = queue.pop(0)
        if d in seen:
            continue
        seen.add(d)
        own_ids.add(d)
        j = fetch.datacite(d)
        if not j or j.get('_not_found'):
            continue
        data = j.get('data') or {}
        for ri in (data.get('attributes') or {}).get('relatedIdentifiers', []) or []:
            if ri.get('relationType') in ('HasVersion', 'IsVersionOf') and ri.get('relatedIdentifierType') == 'DOI':
                queue.append(ndoi(ri.get('relatedIdentifier')))
        for c in ((data.get('relationships') or {}).get('citations') or {}).get('data', []) or []:
            doi = ndoi(c.get('id'))
            w = fetch.openalex_work(doi) if doi else None
            if w and not w.get('_not_found'):
                f = _from_openalex(w, 'datacite')
            else:
                f = {'doi': doi, 'pmid': None, 'pmcid': None, 'openalex': None, 'title': None, 'year': None,
                     'type': None, 'venue': None, 'authors': [], 'source': 'datacite'}
            finds.append(f)
    return finds, own_ids


def merge(finds, inp, own_ids):
    """Works for one dataset, each counted once."""
    own_titles = {ntitle(inp['title'])} | set(inp['publication_titles'])
    keep = [f for f in finds
            if not ({f['doi'], f['openalex']} & own_ids) and not is_own_title(f['title'], own_titles)
            and not about_conp(f['title']) and (f['type'] or 'article') not in NOT_PAPERS
            and (f['doi'] or f['pmid'] or f['title'])]
    parent = list(range(len(keep)))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    index = {}
    for i, f in enumerate(keep):
        for k in (('doi', f['doi']), ('pmid', f['pmid']), ('pmcid', f['pmcid']), ('oa', f['openalex']),
                  ('t', ntitle(f['title']))):
            if k[1]:
                if k in index:
                    parent[root(i)] = root(index[k])
                else:
                    index[k] = i
    groups = defaultdict(list)
    for i in range(len(keep)):
        groups[root(i)].append(keep[i])
    team_keys = name_keys(inp['creators'])
    works = []
    for g in groups.values():
        best = max(g, key=lambda f: (bool(f['title']), bool(f['venue']), len(f['authors'])))
        authors = max((f['authors'] for f in g), key=len)
        sources = sorted({f['source'] for f in g})
        years = [f['year'] for f in g if f['year']]
        works.append({
            'title': best['title'], 'year': min(years) if years else None, 'venue': best['venue'],
            'type': best['type'], 'doi': next((f['doi'] for f in g if f['doi']), None),
            'pmid': next((f['pmid'] for f in g if f['pmid']), None),
            'pmcid': next((f['pmcid'] for f in g if f['pmcid']), None),
            'openalex': next((f['openalex'] for f in g if f['openalex']), None),
            'sources': sources,
            'how': 'cites' if any(s in ('openalex-cites', 'datacite') for s in sources) else 'mentions',
            'by_dataset_team': bool(team_keys & name_keys(authors)),
        })
    works.sort(key=lambda w: (-(w['year'] or 0), w['title'] or ''))
    return works


def work_key(w):
    return w.get('doi') or (('pmid:' + w['pmid']) if w.get('pmid') else None) or w.get('openalex') or ntitle(w.get('title'))


def apply_overrides(datasets, overrides, fetch):
    for r in overrides.get('remove', []):
        d = datasets.get(r.get('dataset'))
        if d:
            gone = ndoi(r.get('doi'))
            d['works'] = [w for w in d['works'] if w.get('doi') != gone]
    for a in overrides.get('add', []):
        d = datasets.get(a.get('dataset'))
        doi = ndoi(a.get('doi'))
        if not d or not doi or any(w.get('doi') == doi for w in d['works']):
            continue
        w = fetch.openalex_work(doi)
        f = _from_openalex(w, 'curated') if w and not w.get('_not_found') else {
            'title': a.get('title') or doi, 'year': a.get('year'), 'venue': None, 'type': 'article', 'pmid': None,
            'pmcid': None, 'openalex': None, 'authors': []}
        d['works'].append({'title': f['title'], 'year': f['year'], 'venue': f['venue'], 'type': f['type'], 'doi': doi,
                           'pmid': f['pmid'], 'pmcid': f['pmcid'], 'openalex': f['openalex'], 'sources': ['curated'],
                           'how': a.get('how', 'cites'), 'by_dataset_team': bool(a.get('by_dataset_team')),
                           'note': a.get('note')})


def conp_mentions(fetch):
    finds = [_from_openalex(w, 'openalex-text') for w in fetch.openalex_list(f'fulltext.search:"{CONP_NAME}"')]
    finds += [_from_europepmc(h, 'europepmc-text') for h in fetch.europepmc(f'"{CONP_NAME}"')]
    finds += [_from_europepmc(h, 'europepmc-funding') for h in
              fetch.europepmc(f'ACK_FUND:"{CONP_NAME}" OR GRANT_AGENCY:"{CONP_NAME}"')]
    # Not merge(): papers about the CONP itself count here.
    works_all = _merge_keep_all(finds)
    fams = Counter(f for w in works_all for f in {s.split('-')[0] for s in w['sources']})
    return {'distinct': len(works_all), 'per_source': dict(fams),
            'per_year': dict(sorted(Counter(w['year'] for w in works_all if w['year']).items()))}


def _merge_keep_all(finds):
    parent = list(range(len(finds)))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    index = {}
    for i, f in enumerate(finds):
        for k in (('doi', f['doi']), ('pmid', f['pmid']), ('pmcid', f['pmcid']), ('oa', f['openalex']),
                  ('t', ntitle(f['title']))):
            if k[1]:
                if k in index:
                    parent[root(i)] = root(index[k])
                else:
                    index[k] = i
    groups = defaultdict(list)
    for i in range(len(finds)):
        groups[root(i)].append(finds[i])
    return [{'sources': sorted({f['source'] for f in g}),
             'year': min([f['year'] for f in g if f['year']] or [0]) or None} for g in groups.values()]


# ---------------------------------------------------------------- one run

def build(inputs, fetch, overrides=None):
    datasets = {}
    for inp in inputs:
        finds, own = find_works(inp, fetch)
        datasets[inp['id']] = {'title': inp['title'], 'works': merge(finds, inp, own)}
    apply_overrides(datasets, overrides or {}, fetch)
    for d in datasets.values():
        d['n_works'] = len(d['works'])
        d['n_by_team'] = sum(1 for w in d['works'] if w['by_dataset_team'])
    distinct = {}
    for d in datasets.values():
        for w in d['works']:
            distinct[work_key(w)] = w
    fams = Counter()
    for w in distinct.values():
        for fam in {s.split('-')[0] for s in w['sources']}:
            fams[fam] += 1
    return {
        'generated': dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'datasets': datasets,
        'totals': {'datasets_used': sum(1 for d in datasets.values() if d['n_works']),
                   'papers': len(distinct), 'per_source': dict(fams),
                   'per_year': dict(sorted(Counter(w['year'] for w in distinct.values() if w['year']).items()))},
        'conp_mentions': conp_mentions(fetch),
        'requests': dict(fetch.requests), 'failures': dict(fetch.failures),
    }


def changes(old, new):
    """Markdown for CHANGES.md: what differs between two runs."""
    date = new['generated'][:10]
    lines = [f'## {date}', '']
    if not old:
        t = new['totals']
        lines += [f"First run: {t['papers']} papers using {t['datasets_used']} datasets; "
                  f"{new['conp_mentions']['distinct']} outputs name the CONP.", '']
        return '\n'.join(lines) + '\n'
    ot, nt = old['totals'], new['totals']
    lines.append(f"Papers {ot['papers']} → {nt['papers']} · datasets used {ot['datasets_used']} → {nt['datasets_used']} · "
                 f"outputs naming the CONP {old['conp_mentions']['distinct']} → {new['conp_mentions']['distinct']}")
    lines.append('')
    any_change = False
    for ds in sorted(set(old['datasets']) | set(new['datasets'])):
        ow = {work_key(w): w for w in old['datasets'].get(ds, {}).get('works', [])}
        nw = {work_key(w): w for w in new['datasets'].get(ds, {}).get('works', [])}
        added, removed = [nw[k] for k in nw if k not in ow], [ow[k] for k in ow if k not in nw]
        if not added and not removed:
            continue
        any_change = True
        title = (new['datasets'].get(ds) or old['datasets'].get(ds))['title']
        lines.append(f'**{title}** (`{ds}`)')
        for w in added:
            lines.append(f"- added: {w['title']} ({w['year'] or 'n.d.'}){' · doi:' + w['doi'] if w['doi'] else ''} "
                         f"· found by {', '.join(w['sources'])}")
        for w in removed:
            lines.append(f"- removed: {w['title']} ({w['year'] or 'n.d.'}){' · doi:' + w['doi'] if w['doi'] else ''}")
        lines.append('')
    if not any_change:
        lines += ['No papers added or removed.', '']
    return '\n'.join(lines) + '\n'


def too_many_failures(fetch, limit=0.1):
    return [s for s, n in fetch.failures.items() if n > 3 and n > limit * max(fetch.requests[s], 1)]


def load_latest(data_path):
    p = os.path.join(data_path, 'research_use', 'latest.json')
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return None


def save(data_path, result):
    """Write latest.json and the dated snapshot, append to CHANGES.md; returns the change entry."""
    root = os.path.join(data_path, 'research_use')
    os.makedirs(os.path.join(root, 'snapshots'), exist_ok=True)
    old = load_latest(data_path)
    entry = changes(old, result)
    with open(os.path.join(root, 'snapshots', result['generated'][:10] + '.json'), 'w') as f:
        json.dump(result, f, indent=1)
    tmp = os.path.join(root, 'latest.json.tmp')
    with open(tmp, 'w') as f:
        json.dump(result, f, indent=1)
    os.replace(tmp, os.path.join(root, 'latest.json'))
    log = os.path.join(root, 'CHANGES.md')
    prev = open(log).read() if os.path.exists(log) else '# Research use: changes from one update to the next\n\n'
    head, _, rest = prev.partition('\n\n')
    with open(log, 'w') as f:
        f.write(head + '\n\n' + entry + '\n' + rest)   # newest first
    return entry
