"""Breadcrumbs on dataset, tool and experiment pages; header logo spacing."""
import os

from flask import render_template


def test_breadcrumb_links_back_to_the_visitors_search(app):
    from tests.unit_tests.test_dataset_page import ZEN, _data, _metadata
    from app.search.dataset_page import dats_record_html, direct_download, publication_citations
    page = {"licences": [], "citation": "C.", "cbrainPipelinesUrl": "/p", "views": 0,
            "publications": publication_citations({}), "direct_download": direct_download(ZEN),
            "dats_html": dats_record_html(ZEN), "doi": None, "parents": []}

    def render(referrer):
        headers = {'Referer': referrer} if referrer else {}
        with app.test_request_context('/dataset?id=projects/demo', headers=headers):
            return render_template('dataset.html', title='t', data=_data(), metadata=_metadata(), readme='',
                                   page=page, ciBadgeUrl='', user=None)

    html = render(None)
    assert 'aria-label="Breadcrumb"' in html and '<a href="/search">Data</a>' in html
    html = render('http://localhost/search?search=mri&access=Open')
    assert '<a href="http://localhost/search?search=mri&amp;access=Open">Data</a>' in html
    # Another site's address never becomes the link, even if it mentions ours.
    html = render('https://example.org/?u=http://localhost/search')
    assert '<a href="/search">Data</a>' in html


def test_logo_has_room_on_the_left():
    css = open(os.path.join('app', 'static', 'css', 'conp-theme.css')).read()
    assert '.navigation-bar .navbar-brand' in css and 'margin-left: 16px' in css


def test_unknown_dataset_is_not_found(session, test_client):
    assert test_client.get('/dataset?id=projects/no-such-dataset').status_code == 404
