"""The "Used in research" tab lists papers as references in the Cite tab's
(DataCite) style, with the DOI shown as a full link."""
from app import research_use as ru
from tests.unit_tests.test_research_use_pages import _render

ELIFE = {'title': "Bundle-specific associations between white matter microstructure and Aβ and tau pathology in "
                  "preclinical Alzheimer's disease.", 'year': 2021, 'venue': 'Elife', 'type': 'journal-article',
         'doi': '10.7554/elife.62929', 'authors': ['A. One', 'B. Two', 'C. Three', 'D. Four'],
         'pmid': None, 'pmcid': None, 'openalex': None}


def test_reference_parts():
    r = ru.reference(ELIFE)
    assert r['authors'] == 'A. One; B. Two; C. Three; et al.'
    assert r['venue'] == 'eLife'
    assert r['title'].endswith("disease.") and not r['title'].endswith('..')
    assert r['link'] == r['link_label'] == 'https://doi.org/10.7554/elife.62929'


def test_reference_without_doi_links_pubmed_or_pmc():
    r = ru.reference({**ELIFE, 'doi': None, 'pmid': '31533000', 'authors': ['Lebel C']})
    assert (r['link'], r['link_label']) == ('https://pubmed.ncbi.nlm.nih.gov/31533000/', 'PubMed 31533000')
    assert r['authors'] == 'Lebel C'
    assert ru.reference({'title': 'T', 'authors': []})['link'] is None


def test_tab_shows_the_reference_with_a_visible_doi(app):
    view = {'n': 1, 'n_team': 0, 'cites': [], 'per_year': [(2021, 1)], 'year_max': 1, 'updated': '2026-10-30',
            'curated': 0, 'mentions': [{**ru.reference(ELIFE), 'url': 'https://doi.org/10.7554/elife.62929',
                                        'year': 2021, 'type': 'article', 'how': 'mentions', 'team': False,
                                        'note': None}]}
    html = _render(app, view)
    assert 'A. One; B. Two; C. Three; et al. (2021): <span class="dp-ref-title">Bundle-specific' in html
    assert '<i>eLife</i>.' in html
    assert '>https://doi.org/10.7554/elife.62929</a>' in html
