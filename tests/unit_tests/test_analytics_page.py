"""The Analytics page: server-rendered, no Matomo widgets, every section degrades
quietly when its data is missing, and its numbers are downloadable as CSV."""
import json

from app.analytics import page


def test_page_renders_without_matomo_widgets(test_client):
    page.clear_cache()
    r = test_client.get('/analytics')
    html = r.get_data(as_text=True)
    assert r.status_code == 200
    assert 'moduleToWidgetize' not in html          # no Matomo iframes (Transitions, maps)
    assert 'CONPReact.ChartContainer' not in html   # no React bundle
    assert 'id="catalogue"' in html and 'id="searches"' in html


def test_research_and_visitors_sections_from_data_files(test_client, tmp_path):
    app = test_client.application
    old = app.config['DATA_PATH']
    app.config['DATA_PATH'] = str(tmp_path)
    try:
        (tmp_path / 'research_use').mkdir()
        (tmp_path / 'research_use' / 'latest.json').write_text(json.dumps({
            'generated': '2026-10-29T00:00:00Z',
            'datasets': {'projects/calgary': {'title': 'Calgary Preschool MRI Dataset', 'n_works': 14, 'works': []}},
            'totals': {'datasets_used': 1, 'papers': 14, 'per_source': {'openalex': 9, 'europepmc': 6},
                       'per_year': {'2025': 3, '2026': 6}},
            'conp_mentions': {'distinct': 253}}))
        (tmp_path / 'analytics').mkdir()
        (tmp_path / 'analytics' / 'countries.json').write_text(json.dumps({
            'period': '2025-10-01 – 2026-09-30',
            'rows': [{'label': 'United States', 'code': 'us', 'nb_visits': 2067},
                     {'label': 'Canada', 'code': 'ca', 'nb_visits': 1527}]}))
        page.clear_cache()
        html = test_client.get('/analytics').get_data(as_text=True)
        assert 'Calgary Preschool MRI Dataset' in html and '253' in html
        assert 'United States: 2,067 visits (58%)' in html          # map tooltip
        assert 'contact_us?topic=other' in html
        csv = test_client.get('/analytics/data/countries.csv')
        assert csv.status_code == 200 and 'United States,2067' in csv.get_data(as_text=True)
        assert test_client.get('/analytics/data/nonsense.csv').status_code == 404
    finally:
        app.config['DATA_PATH'] = old
        page.clear_cache()


def test_modality_labels_and_junk_searches():
    assert page.modality_group('electroencephalography') == 'EEG'
    assert page.modality_group('gVCF/VCF files') is None
    assert page.modality_group('Diffusion tensor imaging') == 'Diffusion MRI'
    assert page.JUNK_SEARCH.search('fsssiedxa$sssiedx') and not page.JUNK_SEARCH.search('prevent-ad')


def test_short_titles():
    assert page.short_title('MICA-PNI: Precision NeuroImaging and Connectomics') == 'MICA-PNI'
    assert page.short_title('Synthetic Animated Mouse (SAM), University of British Columbia, Datasets and 3D-models') \
        == 'Synthetic Animated Mouse (SAM)'


class _FakeIndex:
    """Just enough of a Whoosh index for the search-count helper."""
    def __init__(self, docs):
        self.docs = docs
        fields = ['title', 'description', 'keywords']
        self.schema = type('S', (), {'scorable_names': lambda s: fields, 'names': lambda s: fields})()

    def searcher(self):
        docs = self.docs

        class _S:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def documents(self):
                return iter(docs)
        return _S()


def test_search_counts_do_not_rebuild_the_dataset_list(session, monkeypatch):
    """The page went past the server's 30-second limit because it built the whole
    Data list (views, downloads, ARKs, per-dataset queries) for each top search.
    The counts now come from the search index and the Data page's matcher alone."""
    from app.models import MatomoDailyGetSiteSearchKeywords as K
    from app.search import routes as search_routes
    docs = [{'id': 'projects/a', 'title': 'Alzheimer MRI cohort', 'description': 'structural MRI', 'keywords': 'mri'},
            {'id': 'projects/a2', 'title': 'Alzheimer MRI cohort', 'description': 'same title, listed once', 'keywords': 'mri'},
            {'id': 'projects/b', 'title': 'Resting EEG', 'description': 'eeg in adults', 'keywords': 'eeg'}]
    monkeypatch.setattr(search_routes, '_ensure_search_index', lambda: _FakeIndex(docs))

    def boom(*args, **kwargs):
        raise AssertionError('the Analytics page must not build the dataset list per search')
    monkeypatch.setattr(search_routes, '_dataset_elements', boom)

    assert page.dataset_match_counts(['mri', 'eeg', 'alzheimers', 'qwxzy']) == \
        {'mri': 1, 'eeg': 1, 'alzheimers': 1, 'qwxzy': 0}

    import datetime as dt
    day = dt.date.today() - dt.timedelta(days=3)
    for label, n in [('mri', 9), ('<script>', 50), ('eeg', 4)]:
        session.add(K(date=day, label=label, nb_visits=n, segment=label))
    session.commit()
    rows = page.searches([], n=5)
    assert [(r['term'], r['visits'], r['datasets']) for r in rows] == [('mri', 9, 1), ('eeg', 4, 1)]
