"""The dataset list (Data page, /find, Analytics) is built with one query per
table and kept: same counts as before, the same download-cache lookup, and a
new list as soon as the datasets table changes."""
import datetime as dt
import json
import time

from app.analytics.routes import datasets_downloads, datasets_views
from app.models import Dataset, MatomoDailyGetDatasetPageViewsSummary as V
from app.models import MatomoDailyGetPortalDownloadSummary as D
from app.search import routes


def _seed(session, n_days=40):
    for i in ('projects/a', 'projects/b'):
        session.merge(Dataset(dataset_id=i, name=i[-1].upper(), fspath='/x/conp-dataset/' + i))
    day = dt.date(2026, 1, 1)
    for k in range(n_days):
        d = day + dt.timedelta(days=k)
        session.add(V(date=d, dataset_id='projects/a', url='u', label='l', nb_hits=3, nb_visits=2, nb_uniq_visitors=1))
        if k % 2:
            session.add(V(date=d, dataset_id='projects/b', url='u', label='l', nb_hits=1, nb_visits=1, nb_uniq_visitors=1))
        session.add(V(date=d))                      # "no stats that day" rows
        session.add(D(date=d, url='https://portal.conp.ca/data/a_version-1.0.tar.gz', label='a', nb_hits=2,
                      nb_visits=1, nb_uniq_visitors=1, segment='s'))
        session.add(D(date=d, url='https://elsewhere.org/file.zip', label='x', nb_hits=9, nb_visits=1,
                      nb_uniq_visitors=1, segment='s'))
    session.commit()


def test_counts_match_the_old_endpoints(session, app):
    _seed(session)
    with app.test_request_context('/analytics/datasets/views'):
        old_views = {e['dataset_id']: e['nb_hits'] for e in json.loads(datasets_views())}
        old_downloads = {e['dataset_id']: e['nb_hits'] for e in json.loads(datasets_downloads())}
    views, downloads = routes._view_and_download_counts()
    assert views == old_views == {'projects/a': 120, 'projects/b': 20}
    assert downloads == old_downloads == {'a_version-1.0.tar.gz': 80}


def test_zip_lookup_matches_dataset_cache(tmp_path):
    folder = tmp_path / 'conp-dataset' / 'projects' / 'demo'
    folder.mkdir(parents=True)
    (folder / 'DATS.json').write_text(json.dumps({'title': 'Demo', 'version': '1.0'}))
    names = {'demo_version-1.0.tar.gz', 'other_version-2.tar.gz'}
    assert routes._zip_location(str(folder), '/cache', names) == '/cache/demo_version-1.0.tar.gz'
    assert routes._zip_location(str(folder), '/cache', {'demo_version-0.9.tar.gz'}) is None
    (folder / 'DATS.json').write_text(json.dumps({'title': 'Demo'}))
    assert routes._zip_location(str(folder), '/cache', names) is None      # no version: no zip


def test_list_is_kept_until_the_datasets_change(session, monkeypatch):
    builds = []
    monkeypatch.setattr(routes, '_build_dataset_elements', lambda authorized: builds.append(1) or [{'id': 'x'}])
    routes._elements_cache.clear()
    first = routes._all_dataset_elements(False)
    routes._all_dataset_elements(False)
    assert len(builds) == 1 and first == [{'id': 'x'}]
    session.merge(Dataset(dataset_id='projects/new', name='New', fspath='/x', date_updated=dt.datetime.now()))
    session.commit()
    routes._all_dataset_elements(False)
    assert len(builds) == 2                           # a dataset added: built again
    routes._elements_cache[False] = (routes._elements_cache[False][0],
                                     time.time() - routes.ELEMENTS_MAX_AGE - 1, [{'id': 'x'}])
    routes._all_dataset_elements(False)
    assert len(builds) == 3                           # ten minutes old: built again
    routes._elements_cache.clear()


def test_search_takes_its_datasets_from_the_kept_list(monkeypatch):
    kept = [{'id': 'projects/a', 'title': 'Alzheimer MRI'}, {'id': 'projects/b', 'title': 'EEG'}]
    monkeypatch.setattr(routes, '_all_dataset_elements', lambda authorized: kept)
    from tests.unit_tests.test_analytics_page import _FakeIndex
    docs = [{'id': 'projects/a', 'title': 'Alzheimer MRI', 'description': 'mri', 'keywords': 'mri'},
            {'id': 'projects/b', 'title': 'EEG', 'description': 'eeg', 'keywords': 'eeg'}]
    monkeypatch.setattr(routes, '_ensure_search_index', lambda: _FakeIndex(docs))
    out = routes._dataset_elements('eeg', False)
    assert [e['id'] for e in out] == ['projects/b'] and out[0]['_score'] > 0
    assert '_score' not in kept[1]                    # the kept dicts are not changed
    assert [e['id'] for e in routes._dataset_elements(None, False)] == ['projects/a', 'projects/b']
