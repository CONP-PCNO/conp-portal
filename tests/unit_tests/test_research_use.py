"""Research use: sources merged, each paper counted once, changes tracked from run to run."""
import json
import os
from collections import Counter

from app import research_use as ru

DESCRIPTOR = {
    'title': 'Calgary Preschool MRI Dataset',
    'creators': [{'firstName': 'Catherine', 'lastName': 'Lebel'}],
    'distributions': [{'access': {'landingPage': 'https://osf.io/axz5r/'}}],
    'primaryPublications': [{'title': 'Calgary Preschool magnetic resonance imaging (MRI) dataset',
                             'identifier': {'identifier': 'https://doi.org/10.1016/j.dib.2020.105224'}}],
    'extraProperties': [{'category': 'CONP_status', 'values': [{'value': 'Canadian'}]}],
}


def oa(wid, doi, title, year=2025, typ='article', authors=()):
    return {'id': 'https://openalex.org/' + wid, 'doi': 'https://doi.org/' + doi, 'title': title,
            'publication_year': year, 'type': typ,
            'authorships': [{'author': {'display_name': a}} for a in authors], 'primary_location': {}}


class FakeFetch:
    def __init__(self):
        self.requests, self.failures = Counter(), Counter()

    def openalex_work(self, doi):
        if doi == '10.17605/osf.io/axz5r':
            return {'id': 'https://openalex.org/W1', 'cited_by_count': 2}
        if doi == '10.1016/j.dib.2020.105224':
            return {'id': 'https://openalex.org/W2'}
        if doi == '10.1/added':
            return oa('W9', '10.1/added', 'A paper someone reported', 2026)
        return {'_not_found': True}

    def openalex_list(self, flt):
        if flt == 'cites:W1':
            return [oa('W10', '10.1/a', 'Growth of the precuneus from birth to early adulthood'),
                    oa('W11', '10.1/b', 'White matter alterations after prenatal alcohol exposure', 2021,
                       authors=['Catherine Lebel']),
                    oa('W12', '10.5281/zenodo.1', 'Another dataset that lists this one as a source', typ='dataset')]
        if flt.startswith('fulltext.search:"Canadian'):
            return [oa('W20', '10.1/c', 'Some study acknowledging the platform')]
        return []

    def europepmc(self, query):
        if query == '"10.17605/osf.io/axz5r"':
            return [{'doi': '10.1/A', 'pmid': '111', 'title': 'Growth of the precuneus from birth to early adulthood.',
                     'pubYear': '2025', 'authorString': 'Smith J, Doe A.'},
                    {'doi': '10.1/d', 'title': 'The Canadian Open Neuroscience Platform: an open science framework',
                     'pubYear': '2023'}]
        if query.startswith('"Canadian'):
            return [{'doi': '10.1/c', 'title': 'Some study acknowledging the platform', 'pubYear': '2024'}]
        return []

    def datacite(self, doi):
        return {'_not_found': True}


def run(overrides=None):
    inp = ru.dataset_inputs('projects/calgary', DESCRIPTOR)
    return inp, ru.build([inp], FakeFetch(), overrides)


def test_inputs_derive_the_osf_doi_and_list_the_publication():
    inp = ru.dataset_inputs('projects/calgary', DESCRIPTOR)
    assert inp['dois'] == ['10.17605/osf.io/axz5r']
    assert inp['publication_dois'] == ['10.1016/j.dib.2020.105224']


def test_each_paper_counted_once_and_exclusions():
    _inp, r = run()
    works = r['datasets']['projects/calgary']['works']
    titles = [w['title'] for w in works]
    # found by OpenAlex and Europe PMC (DOI in different case): one paper, two sources
    precuneus = [w for w in works if w['doi'] == '10.1/a']
    assert len(precuneus) == 1 and precuneus[0]['sources'] == ['europepmc-doi', 'openalex-cites']
    # a dataset record and a paper about the CONP itself are not uses
    assert not any('Another dataset' in t for t in titles)
    assert not any('Canadian Open Neuroscience Platform' in (t or '') for t in titles)
    assert r['totals']['papers'] == 2 and r['totals']['datasets_used'] == 1
    team = [w for w in works if w['doi'] == '10.1/b'][0]
    assert team['by_dataset_team'] is True and team['how'] == 'cites'


def test_outputs_naming_the_conp_counted_once():
    _inp, r = run()
    assert r['conp_mentions']['distinct'] == 1   # same DOI from OpenAlex and Europe PMC


def test_overrides_add_and_remove():
    _inp, r = run({'add': [{'dataset': 'projects/calgary', 'doi': '10.1/added', 'note': 'reported'}],
                   'remove': [{'dataset': 'projects/calgary', 'doi': '10.1/b'}]})
    dois = [w['doi'] for w in r['datasets']['projects/calgary']['works']]
    assert '10.1/added' in dois and '10.1/b' not in dois


def test_changes_are_recorded_run_to_run(tmp_path):
    _inp, first = run()
    ru.save(str(tmp_path), first)
    _inp, second = run({'add': [{'dataset': 'projects/calgary', 'doi': '10.1/added'}],
                        'remove': [{'dataset': 'projects/calgary', 'doi': '10.1/b'}]})
    entry = ru.save(str(tmp_path), second)
    assert 'Papers 2 → 2' in entry
    assert '- added: A paper someone reported' in entry
    assert '- removed: White matter alterations after prenatal alcohol exposure' in entry
    root = tmp_path / 'research_use'
    assert (root / 'latest.json').exists() and len(os.listdir(root / 'snapshots')) == 1   # same day
    log = (root / 'CHANGES.md').read_text()
    assert log.startswith('# Research use') and log.count('## ') == 2
    assert json.loads((root / 'latest.json').read_text())['totals']['papers'] == 2


def test_a_failing_source_stops_the_run():
    f = FakeFetch()
    f.requests['europepmc'], f.failures['europepmc'] = 20, 10
    assert ru.too_many_failures(f) == ['europepmc']
    f.failures['europepmc'] = 1
    assert ru.too_many_failures(f) == []


def test_changes_page(test_client, tmp_path):
    app = test_client.application
    old = app.config['DATA_PATH']
    app.config['DATA_PATH'] = str(tmp_path)
    try:
        assert 'No update has run yet' in test_client.get('/analytics/research-use/changes').get_data(as_text=True)
        _inp, r = run()
        ru.save(str(tmp_path), r)
        html = test_client.get('/analytics/research-use/changes').get_data(as_text=True)
        assert 'First run: 2 papers using 1 datasets' in html
    finally:
        app.config['DATA_PATH'] = old


def test_openneuro_doi_from_landing_page_and_search_without_openalex_record():
    inp = ru.dataset_inputs('projects/vwm', {'title': 'Visual working memory study', 'distributions': [
        {'access': {'landingPage': 'https://openneuro.org/datasets/ds001635/'}}]})
    assert inp['dois'] == ['10.18112/openneuro.ds001635']

    class F(FakeFetch):
        def europepmc(self, query):
            if query == '"10.18112/openneuro.ds001635"':
                return [{'doi': '10.1/x', 'title': 'Dynamic network coding of working-memory domains', 'pubYear': '2019'}]
            return []
    finds, _own = ru.find_works(inp, F())   # OpenAlex has no record for this DOI
    assert [f['doi'] for f in finds] == ['10.1/x']


def test_a_journal_article_doi_given_as_the_dataset_identifier_is_not_the_dataset():
    """MouseBytes records give the paper's DOI (JCI, FASEB J) as identifier: papers
    citing that article were counted as uses of the data (79 of 108 on 29 Oct)."""
    inp = ru.dataset_inputs('projects/mousebytes/MB-Co-transmission', {
        'title': 'Mouse models that differ in neurotransmitter release from striatal cholinergic interneurons',
        'identifier': {'identifier': 'https://doi.org/10.1172/JCI138532'}, 'distributions': []})
    assert inp['dois'] == ['10.1172/jci138532']

    class F(FakeFetch):
        def openalex_work(self, doi):
            if doi == '10.1172/jci138532':
                return {'id': 'https://openalex.org/W77', 'cited_by_count': 3}
            return super().openalex_work(doi)

        def openalex_list(self, flt):
            if flt == 'cites:W77':
                return [oa('W78', '10.1/anorexia', 'Avoidance habit learning in anorexia nervosa')]
            return super().openalex_list(flt)
    result = ru.build([inp], F())
    assert result['datasets'][inp['id']]['n_works'] == 0          # citing the article is not using the data
    assert ru.data_dois(inp, F()) == ([], ['10.1172/jci138532'])

    class Down(F):
        def datacite(self, doi):
            return None                                          # DataCite unreachable: keep the DOI
    assert ru.data_dois(inp, Down()) == (['10.1172/jci138532'], [])
    # repository DOIs (Zenodo, OSF, OpenNeuro, ...) are the dataset's without asking DataCite
    osf = ru.dataset_inputs('projects/calgary', DESCRIPTOR)
    assert ru.data_dois(osf, FakeFetch())[0] == ['10.17605/osf.io/axz5r']
