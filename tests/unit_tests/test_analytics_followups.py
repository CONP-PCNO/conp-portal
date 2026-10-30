"""29 Oct follow-ups: placeholder values in DATS records, the Analytics page
kept between requests, every month labelled, quick tooltips, the section
links that no longer shift the page, and "All" on the Data page."""
import json
import os
import time

from werkzeug.datastructures import MultiDict

from app.analytics import page
from app.search import dataset_list as dl
from app.search.models import DATSDataset, real_values


def _dats(tmp_path, record, name='ds'):
    folder = tmp_path / name
    folder.mkdir()
    (folder / 'DATS.json').write_text(json.dumps(record))
    return DATSDataset(str(folder))


def test_placeholders_are_dropped_from_the_record(tmp_path):
    """MICA-PNI, as on 29 Oct: 16 download parts each listing "N/A" as format,
    "dataset" as type, "N/A" as keyword; an empty creator (tau dataset)."""
    d = _dats(tmp_path, {
        'title': 'MICA-PNI', 'creators': [{'name': 'Donna Gift Cabalo'}, {'name': ''}, {'name': 'N/A'}],
        'types': [{'information': {'value': 'dataset'}}],
        'keywords': [{'value': 'N/A'}, {'value': '7T'}, {'value': '7t'}],
        'distributions': [{'formats': ['N/A'], 'size': 3.2, 'unit': {'value': 'GB'}} for _ in range(16)],
    })
    assert d.formats == [] and d.modalities is None and d.keywords == ['7T']
    assert d.creators == ['Donna Gift Cabalo']
    d2 = _dats(tmp_path, {
        'title': 'Zenodo', 'types': [{'information': {'value': 'unknown'}}, {'information': {'value': 'MRI'}}],
        'distributions': [{'formats': ['NIfTI', 'nifti', 'JSON', None, 'unknown']}]}, name='zen')
    assert d2.modalities == ['MRI'] and d2.formats == ['NIfTI', 'JSON']
    assert real_values(['Other', 'n.a.', ' NA ']) == ['Other']


def test_every_month_is_labelled_with_the_year_under_january():
    keys = ['2025-11', '2025-12', '2026-01', '2026-02']
    labels = [(f"{['Nov', 'Dec', 'Jan', 'Feb'][i]}", '2025' if i == 0 else ('2026' if k.endswith('-01') else ''))
              for i, k in enumerate(keys)]
    svg = str(page.line_chart([{'name': 'Visits', 'values': [5, 6, 7, 8], 'color': page.GREEN}], labels, 'Visits',
                              tips=['November 2025: 5 visits', 'December 2025: 6 visits', 'January 2026: 7 visits',
                                    'February 2026: 8 visits']))
    for m in ('>Nov<', '>Dec<', '>Jan<', '>Feb<', '>2025<', '>2026<'):
        assert m in svg
    assert svg.count('class="an-hover"') == 4 and 'data-tip="January 2026: 7 visits"' in svg


def test_visits_chart_labels_all_36_months(session):
    import datetime as dt
    from app.models import MatomoDailyVisitsSummary as V
    day = dt.date(2023, 11, 1)
    while day <= dt.date(2026, 10, 28):
        session.merge(V(date=day, nb_visits=20))
        day += dt.timedelta(days=9)
    session.commit()
    v = page.visits()
    svg = str(v['svg'])
    assert v['months'][0] == '2023-11' and len(v['months']) == 36
    assert svg.count('font-size="11"') == 36                    # one label per month
    assert '>2024<' in svg and '>2025<' in svg and '>2023<' in svg
    assert 'data-tip="October 2026: ' in svg


def test_world_map_tips_need_no_title_delay(app):
    with app.app_context():
        svg = str(page.world_map({'us': 2067, 'ca': 1527}, 3594, {'us': 'United States', 'ca': 'Canada'}))
    assert '<title>' not in svg and 'data-tip="United States: 2,067 visits (58%)"' in svg


def test_page_is_kept_and_renewed_in_the_background(app, tmp_path, monkeypatch):
    old = app.config['DATA_PATH']
    app.config['DATA_PATH'] = str(tmp_path)
    builds, refreshes = [], []
    monkeypatch.setattr(page, 'build_context', lambda period='all': builds.append(period) or {'period': period})
    monkeypatch.setattr(page, '_refresh_in_background', lambda period: refreshes.append(period))
    try:
        with app.test_request_context('/analytics'):
            page.clear_cache()
            assert page.page_context('all') == {'period': 'all'} and builds == ['all']
            assert os.path.exists(tmp_path / 'analytics' / 'page-cache-all.pickle')   # shared with other workers
            page.page_context('12m')
            page.page_context('all')
            assert builds == ['all', '12m']          # the two periods no longer evict each other
            page._CACHE.clear()                       # another worker, or after a restart
            assert page.page_context('all') == {'period': 'all'} and builds == ['all', '12m']
            built, ctx = page._CACHE['all']
            page._CACHE['all'] = (built - page.MAX_AGE - 1, ctx)      # an hour old
            os.utime(tmp_path / 'analytics' / 'page-cache-all.pickle', (time.time() - 7200, time.time() - 7200))
            assert page.page_context('all') == {'period': 'all'}      # still served at once
            assert refreshes == ['all'] and builds == ['all', '12m']   # renewed in the background
    finally:
        page.clear_cache()
        app.config['DATA_PATH'] = old


def test_section_links_do_not_move_the_page():
    css = open(os.path.join('app', 'static', 'css', 'analytics.css')).read()
    assert 'border-bottom: 3px solid transparent' in css
    assert '.an-nav a:hover { color: #1d2129; border-bottom: 3px solid' not in css


def test_quick_tips_on_every_page(test_client):
    html = test_client.get('/analytics').get_data(as_text=True)
    assert 'js/quick-tips.js' in html and 'data-quick-tips' in html
    assert test_client.get('/static/js/quick-tips.js').status_code == 200


def test_show_all_datasets():
    assert dl.chosen_per_page(MultiDict({'show': 'all'})) == dl.ALL
    assert dl.chosen_per_page(MultiDict({'max_per_page': 'All'})) == dl.ALL     # the old list's link
    assert dl.chosen_per_page(MultiDict({'show': '7'})) == 30
    items = list(range(184))
    assert dl.page_of(items, '3', dl.ALL) == (items, 1, 1)


def test_show_menu_offers_all(test_client):
    html = test_client.get('/search?show=all').get_data(as_text=True)
    assert '<option value="all" selected>All</option>' in html
