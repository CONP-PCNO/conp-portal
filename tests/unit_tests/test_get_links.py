"""Data page "Get it" items link to the dataset page's ways to get the data;
no header "?"; no CircleCI badge."""
from flask import render_template


def test_card_ways_link_to_the_dataset_page(session, test_client, tmp_path, monkeypatch):
    from app.search import routes
    from tests.unit_tests.test_data_page import _element
    open_ = _element(tmp_path, 'projects/zen', files=['sub-01.nii.gz', '.conp-zenodo-crawler.json'],
                     dats={'distributions': [{'access': {'landingPage': 'https://zenodo.org/records/1',
                                                         'authorizations': [{'value': 'public'}]}}]},
                     sources=['https://zenodo.org/records/1'], cbrain_id='/cbrain?x=1')
    locked = _element(tmp_path, 'projects/bc', authorizations='registered',
                      registrationPage='https://www.braincode.ca/content/getting-started')
    monkeypatch.setattr(routes, '_dataset_elements', lambda q, authorized: [open_, locked])
    html = test_client.get('/search').get_data(as_text=True)
    assert 'href="/dataset?id=projects/zen#route-browser"' in html
    assert 'href="/dataset?id=projects/zen#dataladInstructions"' in html
    assert 'href="/dataset?id=projects/zen#route-cbrain"' in html
    assert 'href="/dataset?id=projects/bc#route-request"' in html and 'Request access at Brain-CODE' in html


def test_dataset_page_ways_have_ids_and_no_circleci(app):
    from tests.unit_tests.test_dataset_page import ZEN, _data, _metadata
    from app.search.dataset_page import dats_record_html, direct_download, publication_citations
    page = {"licences": [], "citation": "C.", "cbrainPipelinesUrl": "/p", "views": 0,
            "publications": publication_citations({}), "direct_download": direct_download(ZEN),
            "dats_html": dats_record_html(ZEN), "doi": None, "parents": []}
    with app.test_request_context('/dataset?id=projects/demo'):
        html = render_template('dataset.html', title='t', data=_data(), metadata=_metadata(), readme='',
                               page=page, user=None)
    assert 'id="route-browser"' in html and 'id="dataladInstructions"' in html
    assert 'circleci' not in html.lower() and 'Test status' not in html


def test_no_header_question_mark(test_client):
    html = test_client.get('/about').get_data(as_text=True)
    assert 'btnShowTut' not in html and 'Context-aware' not in html


def test_data_search_box_suggests(session, test_client, monkeypatch):
    from app.search import routes
    monkeypatch.setattr(routes, '_dataset_elements', lambda q, authorized: [])
    html = test_client.get('/search').get_data(as_text=True)
    assert 'data-suggest-url="/dataset-search-suggestions"' in html and 'list="lp-suggestions"' in html
    assert 'js/list-suggest.js' in html
