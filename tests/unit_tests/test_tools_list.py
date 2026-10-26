"""Tools & Pipelines list (/pipelines): cards, filters, related descriptors."""
from werkzeug.datastructures import MultiDict

from app.pipelines import tool_list as tl

FS = {'label': 'FreeSurfer', 'src': '/static/img/tools/freesurfer.png'}
GENERIC = {'label': 'Tool', 'src': '/static/img/tools/default.svg', 'generic': True}


def _el(id_, title, downloads=1, tags=None, container='singularity', **kw):
    e = {'id': id_, 'title': title, 'downloads': downloads, 'author': 'Lab', 'publicationdate': '2023-01-01',
         'toolversion': '1.0', 'description': 'A tool.', 'tags': tags or {}, 'inputs': [{}, {}],
         'containerimage': {'type': container} if container else {}}
    e.update(kw)
    return e


def test_domain_tags_in_every_shape():
    assert tl.domain_tags({'domain': ['MRI', 'neuroinformatics']}) == ['mri', 'neuroinformatics']
    assert tl.domain_tags({'domain': 'eeg'}) == ['eeg']
    assert tl.domain_tags('Boutiques,domain:neuroinformatics,domain:mri') == ['neuroinformatics', 'mri']
    assert tl.domain_labels({'domain': ['dmri', 'dwi', 'neuroinformatics']}) == ['Diffusion MRI']


def test_card_runs_on_and_facts():
    c = tl.tool_card(_el('z.1', 'FreeSurfer-Recon-all', tags={'domain': ['mri']}),
                     {'software': 'FreeSurfer', 'versions': ['7.1.1', '8.1.0']}, {'z.1'}, {'z.1'}, FS)
    assert c['runs_facet'] == [tl.RUN_CBRAIN, tl.RUN_COMPUTER, tl.RUN_CLUSTER]
    assert c['cbrain_label'] == 'FreeSurfer 7.1.1 to 8.1.0' and c['family'] == 'FreeSurfer'
    assert c['container'] == 'Apptainer / Singularity' and c['inputs'] == 2 and c['domains'] == ['MRI']
    g = tl.tool_card(_el('z.2', 'thing', container=None), None, set(), set(), GENERIC)
    assert g['family'] is None and g['software_facet'] == [tl.OTHER_SOFTWARE]
    assert g['runs_facet'] == [tl.RUN_COMPUTER] and g['domain_facet'] == [tl.NOT_STATED]


def test_related_descriptors_group_under_the_most_downloaded():
    cards = [tl.tool_card(_el('a', 'FreeSurfer-Recon-all', 100), None, set(), set(), FS),
             tl.tool_card(_el('b', 'FreeSurfer7-Recon-all-qcache', 5), None, set(), set(), FS),
             tl.tool_card(_el('c', 'FreeSurfer-Recon-all_v5', 9), None, set(), set(), FS),
             tl.tool_card(_el('d', 'mri_convert', 50), None, set(), set(), FS),
             tl.tool_card(_el('e', 'thing', 1), None, set(), set(), GENERIC),
             tl.tool_card(_el('f', 'thing-test', 1), None, set(), set(), GENERIC)]
    groups = tl.group_related(cards)
    lead = next(g for g in groups if g['id'] == 'a')
    assert [r['title'] for r in lead['related']] == ['FreeSurfer-Recon-all_v5', 'FreeSurfer7-Recon-all-qcache']
    # Different stems, or no software family: never grouped.
    assert {g['id'] for g in groups} == {'a', 'd', 'e', 'f'}


def test_filters_counts_and_old_parameters():
    cards = [tl.tool_card(_el('a', 'A', 10, tags={'domain': ['mri']}), None, {'a'}, set(), FS),
             tl.tool_card(_el('b', 'B', 20, tags={'domain': ['eeg']}, container='docker'), None, set(), set(), GENERIC)]
    shown, facets = tl.filter_cards(cards, '', {'runs': [tl.RUN_CBRAIN]}, 'downloads')
    assert [c['id'] for c in shown] == ['a']
    runs = next(f for f in facets if f['key'] == 'runs')
    assert [i['value'] for i in runs['items']] == [tl.RUN_CBRAIN, tl.RUN_COMPUTER, tl.RUN_CLUSTER]
    shown, _ = tl.filter_cards(cards, 'eeg', {}, 'downloads')
    assert [c['id'] for c in shown] == ['b']
    sel = tl.selected_filters(MultiDict({'tags': 'mri,eeg', 'cbrain': 'true'}))
    assert sel['domain'] == ['MRI', 'EEG'] and sel['runs'] == [tl.RUN_CBRAIN]
    assert tl.chosen_sort(MultiDict({'sortKey': 'title-asc'})) == 'name'
    assert tl.chosen_sort(MultiDict()) == 'downloads'


def test_tools_page_renders(test_client, monkeypatch):
    from app.pipelines import routes
    els = [_el('zenodo.1', 'FreeSurfer-Recon-all', 1000, tags={'domain': ['mri']}),
           _el('zenodo.2', 'FreeSurfer7-Recon-all-qcache', 3),
           _el('zenodo.3', 'thing', 5, container=None)]
    monkeypatch.setattr(routes, '_tool_elements', lambda: els)
    monkeypatch.setattr(routes, 'get_tool_icons', lambda: ({'zenodo.1': FS, 'zenodo.2': FS}, GENERIC))
    html = test_client.get('/pipelines').get_data(as_text=True)
    assert '3 tools' in html and '+ 1 related descriptor' in html and 'FreeSurfer7-Recon-all-qcache' in html
    assert 'href="/pipeline?id=zenodo.1#boutiques"' in html and 'href="/pipeline?id=zenodo.1#hpc"' in html
    assert 'CONPReact.DataTableContainer' not in html
    html = test_client.get('/pipelines?separate=1').get_data(as_text=True)
    assert '+ 1 related descriptor' not in html
    html = test_client.get('/pipelines?container=Docker').get_data(as_text=True)
    assert 'No tool matches' in html


def test_tools_search_box_suggests(test_client, monkeypatch):
    from app.pipelines import routes
    monkeypatch.setattr(routes, '_tool_elements', lambda: [_el('zenodo.1', 'FreeSurfer-Recon-all', tags={'domain': ['mri']})])
    monkeypatch.setattr(routes, 'get_tool_icons', lambda: ({'zenodo.1': FS}, GENERIC))
    html = test_client.get('/pipelines').get_data(as_text=True)
    assert 'data-suggest-terms="lp-terms"' in html and 'js/list-suggest.js' in html
    assert '"FreeSurfer-Recon-all"' in html and '"FreeSurfer"' in html and '"MRI"' in html
