"""DOI source icons: which service registered a DOI, and the link macro."""
from flask import render_template_string

from app.doi_sources import bare_doi, doi_source
from app.search.dataset_page import licence_badges
from tests.unit_tests.test_dataset_page import _data, _metadata


def test_doi_source_known_repositories():
    assert doi_source('10.5281/zenodo.3518486')['name'] == 'Zenodo'
    assert doi_source('https://doi.org/10.17605/OSF.IO/EKDU5')['icon'] == 'img/doi/osf.png'
    assert doi_source('doi:10.20383/101.0123')['name'] == 'FRDR'
    assert doi_source('10.18112/openneuro.ds000001.v1.0.0')['name'] == 'OpenNeuro'
    assert doi_source('10.55458/neurolibre.00023')['icon'] == 'img/evidence_logo.svg'
    assert doi_source('10.5683/SP2/ABCDEF')['icon'] == 'img/doi/datacite.png'


def test_doi_source_other_and_none():
    src = doi_source('https://doi.org/10.1093/schbul/sbz032')
    assert src['name'] is None and src['icon'] == 'img/doi/doi.png' and src['doi'] == '10.1093/schbul/sbz032'
    assert doi_source(None) is None and doi_source('not a doi') is None
    assert bare_doi('see doi:10.1016/j.cortex.2019.12.014.') == '10.1016/j.cortex.2019.12.014'


def test_doi_link_macro(app):
    with app.test_request_context('/'):
        html = render_template_string(
            "{% from 'macros/doi.html' import doi_link %}{{ doi_link(v) }}|{{ doi_link(v, 'zenodo.1') }}",
            v='10.5281/zenodo.1')
    assert 'href="https://doi.org/10.5281/zenodo.1"' in html
    assert '/static/img/doi/zenodo.svg' in html and 'DOI registered through Zenodo' in html
    assert '>doi:10.5281/zenodo.1</a>' in html and '>zenodo.1</a>' in html


def test_dataset_page_shows_doi_with_icon(app):
    with app.test_request_context('/dataset?id=projects/demo'):
        page = {"licences": licence_badges(["CC0"]), "citation": "C.", "cbrainPipelinesUrl": "/p", "views": 0,
                "doi": "10.5281/zenodo.3518486"}
        html = render_template_string("{% extends 'dataset.html' %}", data=_data(), metadata=_metadata(),
                                      readme='', page=page, ciBadgeUrl='', user=None, title='t')
    # only on the DOI line of All metadata, not in the header next to the ARK
    assert html.count('/static/img/doi/zenodo.svg') == 1
    assert 'class="dp-doi"' not in html
