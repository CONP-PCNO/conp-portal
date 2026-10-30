"""Research use on the dataset page ("Used in research" tab, chip) and on the
Data page (card chip, filter, sort), read from DATA_PATH/research_use/latest.json."""
import json
import os

from flask import render_template

from app import research_use
from app.search import dataset_list as dl
from tests.unit_tests.test_data_page import _element
from tests.unit_tests.test_dataset_page import _data, _metadata

LATEST = {
    'generated': '2026-10-30T00:30:00Z',
    'datasets': {
        'projects/calgary': {'title': 'Calgary Preschool MRI Dataset', 'n_works': 3, 'n_by_team': 1, 'works': [
            {'title': 'Growth and development of the precuneus', 'year': 2025, 'venue': 'Cerebral Cortex',
             'type': 'article', 'doi': '10.1093/cercor/bhaf305', 'pmid': None, 'pmcid': None, 'openalex': None,
             'sources': ['openalex-cites'], 'how': 'cites', 'by_dataset_team': False},
            {'title': 'AI segmentation requires accounting for brain size', 'year': 2026, 'venue': 'bioRxiv',
             'type': 'posted-content', 'doi': None, 'pmid': None, 'pmcid': 'PMC123', 'openalex': None,
             'sources': ['europepmc-doi'], 'how': 'mentions', 'by_dataset_team': False},
            {'title': 'Cerebral blood flow increases across early childhood', 'year': 2019, 'venue': 'NeuroImage',
             'type': 'article', 'doi': None, 'pmid': '31533000', 'pmcid': None, 'openalex': None,
             'sources': ['europepmc-title', 'openalex-text'], 'how': 'mentions', 'by_dataset_team': True}]},
        'projects/unused': {'title': 'Nobody yet', 'n_works': 0, 'n_by_team': 0, 'works': []},
    },
    'totals': {'datasets_used': 1, 'papers': 3, 'per_source': {}, 'per_year': {}},
    'conp_mentions': {'distinct': 0},
}


def _write(path, data=LATEST):
    os.makedirs(os.path.join(path, 'research_use'), exist_ok=True)
    with open(os.path.join(path, 'research_use', 'latest.json'), 'w') as f:
        json.dump(data, f)


def test_dataset_view_groups_links_and_years(tmp_path):
    _write(str(tmp_path))
    v = research_use.dataset_view(str(tmp_path), 'projects/calgary')
    assert v['n'] == 3 and v['n_team'] == 1
    assert [w['title'] for w in v['cites']] == ['Growth and development of the precuneus']
    assert [w['url'] for w in v['mentions']] == ['https://europepmc.org/article/PMC/123',
                                                 'https://pubmed.ncbi.nlm.nih.gov/31533000/']
    assert v['mentions'][0]['type'] == 'preprint' and v['mentions'][1]['team']
    years = dict(v['per_year'])
    assert years[2019] == 1 and years[2025] == 1 and years[2026] == 1 and years.get(2020) == 0
    assert v['updated'] == '2026-10-30'
    # no paper, unknown dataset, no file: no tab
    assert research_use.dataset_view(str(tmp_path), 'projects/unused') is None
    assert research_use.dataset_view(str(tmp_path), 'projects/nope') is None
    assert research_use.dataset_view(str(tmp_path / 'empty'), 'projects/calgary') is None


def test_paper_count_rereads_when_the_file_changes(tmp_path):
    _write(str(tmp_path))
    assert research_use.paper_count(str(tmp_path), 'projects/calgary') == 3
    assert research_use.paper_count(str(tmp_path), 'projects/unused') == 0
    changed = json.loads(json.dumps(LATEST))
    changed['datasets']['projects/calgary']['n_works'] = 4
    _write(str(tmp_path), changed)
    p = os.path.join(str(tmp_path), 'research_use', 'latest.json')
    os.utime(p, (os.path.getmtime(p) + 5, os.path.getmtime(p) + 5))
    assert research_use.paper_count(str(tmp_path), 'projects/calgary') == 4


def test_data_cards_chip_filter_and_sort(app, tmp_path):
    data = tmp_path / 'data'
    _write(str(data))
    old = app.config['DATA_PATH']
    app.config['DATA_PATH'] = str(data)
    try:
        cards = [dl.dataset_card(_element(tmp_path, 'projects/calgary', title='Calgary')),
                 dl.dataset_card(_element(tmp_path, 'projects/unused', title='Unused'))]
    finally:
        app.config['DATA_PATH'] = old
    assert cards[0]['papers'] == 3 and cards[0]['used_facet'] == [dl.USED]
    assert cards[1]['papers'] == 0 and cards[1]['used_facet'] == []
    shown, facets = dl.filter_cards(cards, {'used': [dl.USED]}, 'added')
    assert [c['id'] for c in shown] == ['projects/calgary']
    used = [f for f in facets if f['key'] == 'used'][0]
    assert used['label'] == 'Used in research' and used['items'][0]['count'] == 1
    shown, _ = dl.filter_cards(list(reversed(cards)), {}, 'used')
    assert shown[0]['id'] == 'projects/calgary'


def test_card_template_shows_the_chip(app, tmp_path):
    data = tmp_path / 'data'
    _write(str(data))
    old = app.config['DATA_PATH']
    app.config['DATA_PATH'] = str(data)
    try:
        card = dl.dataset_card(_element(tmp_path, 'projects/calgary', title='Calgary'))
        with app.test_request_context('/search'):
            tpl = app.jinja_env.from_string("{% from 'macros/cards.html' import dataset_card %}{{ dataset_card(c) }}")
            html = tpl.render(c=card)
    finally:
        app.config['DATA_PATH'] = old
    assert 'href="/dataset?id=projects/calgary#research"' in html and 'Used in 3 papers' in html


def _render(app, research, **over):
    page = {'licences': [], 'citation': 'C.', 'cbrainPipelinesUrl': '/pipeline-search', 'views': 1,
            'research': research, 'doi': '10.17605/osf.io/axz5r', 'publications': [{'text': 'P.', 'doi': None}]}
    page.update(over)
    data = _data(id='projects/calgary', title='Calgary Preschool MRI Dataset')
    with app.test_request_context('/dataset?id=projects/calgary'):
        return render_template('dataset.html', title='t', data=data, metadata=_metadata(),
                               readme='<p>Readme</p>', page=page, ciBadgeUrl='', user=None)


def test_dataset_page_tab_and_chip(app, tmp_path):
    _write(str(tmp_path))
    html = _render(app, research_use.dataset_view(str(tmp_path), 'projects/calgary'))
    assert 'id="tab-research"' in html and 'Used in research <span class="dp-tab-count">(3)</span>' in html
    assert 'href="#research"' in html and 'Used in 3 papers' in html
    assert '3 papers and preprints cite this dataset or mention it in their text. One is from the team' in html
    assert html.index('Cite the dataset') < html.index('Mention it in the text')
    assert '· 2 more' in html and "by the dataset's team" in html
    assert 'https://doi.org/10.1093/cercor/bhaf305' in html
    assert '(10.17605/osf.io/axz5r)' in html and 'Updated 2026-10-30' in html
    assert 'contact_us?topic=other' in html and 'Tell us about a paper we missed' in html
    assert 'Paper describing the dataset' in html
    # the tab is last, after Cite
    assert html.index('aria-controls="cite"') < html.index('aria-controls="research"')


def test_dataset_page_without_research_use(app):
    html = _render(app, None)
    assert 'tab-research' not in html and 'Used in research' not in html and '#research' not in html
