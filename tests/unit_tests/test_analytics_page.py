"""The Analytics page: server-rendered, no Matomo widgets, every section degrades
quietly when its data is missing, and its numbers are downloadable as CSV."""
import json

from app.analytics import page


def test_page_renders_without_matomo_widgets(test_client):
    page._CACHE.clear()
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
        page._CACHE.clear()
        html = test_client.get('/analytics').get_data(as_text=True)
        assert 'Calgary Preschool MRI Dataset' in html and '253' in html
        assert 'United States: 2,067 visits (58%)' in html          # map tooltip
        assert 'contact_us?topic=other' in html
        csv = test_client.get('/analytics/data/countries.csv')
        assert csv.status_code == 200 and 'United States,2067' in csv.get_data(as_text=True)
        assert test_client.get('/analytics/data/nonsense.csv').status_code == 404
    finally:
        app.config['DATA_PATH'] = old
        page._CACHE.clear()


def test_modality_labels_and_junk_searches():
    assert page.modality_group('electroencephalography') == 'EEG'
    assert page.modality_group('gVCF/VCF files') is None
    assert page.modality_group('Diffusion tensor imaging') == 'Diffusion MRI'
    assert page.JUNK_SEARCH.search('fsssiedxa$sssiedx') and not page.JUNK_SEARCH.search('prevent-ad')


def test_short_titles():
    assert page.short_title('MICA-PNI: Precision NeuroImaging and Connectomics') == 'MICA-PNI'
    assert page.short_title('Synthetic Animated Mouse (SAM), University of British Columbia, Datasets and 3D-models') \
        == 'Synthetic Animated Mouse (SAM)'
