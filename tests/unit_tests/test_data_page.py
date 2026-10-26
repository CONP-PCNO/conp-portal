"""The Data page (/search): cards, filter sidebar, sort, pages (option A)."""
import json

from werkzeug.datastructures import MultiDict

from app.search import dataset_list as dl


def _element(tmp_path, id_, **kw):
    """A dict like routes._dataset_elements gives, with its dataset folder."""
    folder = tmp_path / id_.replace('/', '_')
    folder.mkdir()
    (folder / 'DATS.json').write_text(json.dumps(kw.pop('dats', {'title': id_})))
    for name in kw.pop('files', []):
        (folder / name).write_text('x')
    e = {'id': id_, 'title': id_.split('/')[-1], 'thumbnailURL': '/dataset_logo?id=' + id_, 'logoFilepath': None,
         'authorizations': 'public', 'conpStatus': 'Canadian', 'downloadOptions': None, 'sources': None,
         'registrationPage': None, 'cbrain_id': None, 'showDownloadButton': False, 'creators': ['A. Author'],
         'dateAdded': '2024-01-01', 'dateUpdated': '2024-02-01', 'version': '1.0', 'size': '1.0 GB',
         'subjects': '10', 'modalities': ['mri'], 'formats': ['nifti'], 'licenses': [{'name': 'CC0'}],
         'evidencePublication': None, 'evidencePublicationType': None, 'views': [],
         '_fspath': str(folder), '_description': 'A <b>dataset</b>.', '_keywords': []}
    e.update(kw)
    return e


def test_card_routes_and_labels(tmp_path):
    # Open, data in the repository, Zenodo record: download + DataLad.
    zen = _element(tmp_path, 'projects/zen', files=['sub-01.nii.gz', '.conp-zenodo-crawler.json'],
                   dats={'distributions': [{'access': {'landingPage': 'https://zenodo.org/records/123', 'authorizations': [{'value': 'public'}]}}]},
                   sources=['https://zenodo.org/records/123'], cbrain_id='/cbrain?x=1', subjects='1')
    c = dl.dataset_card(zen)
    assert c['download'] and c['datalad'] and c['cbrain'] and not c['request']
    assert c['routes_facet'] == [dl.ROUTE_DOWNLOAD, dl.ROUTE_DATALAD, dl.ROUTE_CBRAIN]
    assert c['modalities'] == ['MRI'] and c['formats'] == ['NIfTI'] and c['subjects_label'] == '1 subject'
    assert c['description'] == 'A dataset .'
    assert c['origin'] == 'Canadian dataset' and c['access_facet'] == ['Open']

    # Registered, metadata only, Brain-CODE: request access at the source.
    bc = _element(tmp_path, 'projects/braincode_x', authorizations='registered', conpStatus='external',
                  registrationPage='https://www.braincode.ca/content/getting-started', subjects='N/A')
    c = dl.dataset_card(bc)
    assert c['request'] == 'Request access at Brain-CODE' and not c['download'] and not c['datalad']
    assert c['routes_facet'] == [dl.ROUTE_SOURCE] and c['access_facet'] == ['Account needed']
    assert c['origin'] == 'International' and c['subjects_label'] is None

    # downloadOptions offsite wins over files in the repository.
    off = _element(tmp_path, 'projects/eegnet_x', files=['data.edf'], downloadOptions='offsite')
    c = dl.dataset_card(off)
    assert not c['datalad'] and not c['download'] and dl.ROUTE_SOURCE in c['routes_facet']


def test_placeholder_values_are_not_modalities_or_formats(tmp_path):
    c = dl.dataset_card(_element(tmp_path, 'projects/p', modalities=['Unknown', 'Dataset'], formats=['N/A', 'csv']))
    assert c['modalities'] == [] and c['modality_facet'] == [dl.NOT_STATED] and c['formats'] == ['CSV']


def test_filters_counts_and_sort(tmp_path):
    cards = [dl.dataset_card(_element(tmp_path, 'projects/a', modalities=['mri'], dateAdded='2020-01-01', size='5 GB')),
             dl.dataset_card(_element(tmp_path, 'projects/b', modalities=['eeg'], dateAdded='2024-01-01', size='1 TB')),
             dl.dataset_card(_element(tmp_path, 'projects/c', modalities=['mri', 'eeg'], dateAdded='2022-01-01',
                                      authorizations='registered'))]
    shown, facets = dl.filter_cards(cards, {'modality': ['MRI']}, 'added')
    assert [c['id'] for c in shown] == ['projects/c', 'projects/a']
    modality = next(f for f in facets if f['key'] == 'modality')
    # Counts in a facet ignore its own selection: EEG still shows 2.
    assert {i['value']: i['count'] for i in modality['items']} == {'MRI': 2, 'EEG': 2}
    access = next(f for f in facets if f['key'] == 'access')
    assert {i['value']: i['count'] for i in access['items']} == {'Open': 1, 'Account needed': 1}
    shown, _ = dl.filter_cards(cards, {}, 'size')
    assert shown[0]['id'] == 'projects/b'
    shown, _ = dl.filter_cards(cards, {'modality': ['MRI'], 'access': ['Open']}, 'name')
    assert [c['id'] for c in shown] == ['projects/a']


def test_long_facets_fold_behind_more(tmp_path):
    cards = [dl.dataset_card(_element(tmp_path, 'projects/f{}'.format(i), formats=['fmt{}'.format(i)]))
             for i in range(12)]
    _, facets = dl.filter_cards(cards, {'format': ['FMT9']}, 'added')
    fmt = next(f for f in facets if f['key'] == 'format')
    assert len(fmt['items']) == dl.FACET_SHOWN + 1  # the checked one stays visible
    assert any(i['value'] == 'FMT9' and i['checked'] for i in fmt['items'])
    assert len(fmt['more']) == 12 - dl.FACET_SHOWN - 1


def test_old_links_keep_their_filters():
    args = MultiDict({'modalities': 'mri,eeg', 'formats': 'nifti', 'authorizations': 'Yes', 'cbrain': 'true',
                      'sortKey': 'title', 'max_per_page': '50'})
    sel = dl.selected_filters(args)
    assert sel['modality'] == ['MRI', 'EEG'] and sel['format'] == ['NIfTI']
    assert sel['access'] == ['Account needed'] and sel['get'] == [dl.ROUTE_CBRAIN]
    assert dl.chosen_sort(args) == 'name' and dl.chosen_per_page(args) == 50
    assert dl.chosen_sort(MultiDict()) == 'added' and dl.chosen_per_page(MultiDict({'show': '7'})) == 30


def test_pages():
    items, page, pages = dl.page_of(list(range(45)), '3', 20)
    assert (items, page, pages) == (list(range(40, 45)), 3, 3)
    assert dl.page_of([], None, 20)[1:] == (1, 1)
    assert dl.page_links(1, 10) == [1, 2, 3, None, 10]
    assert dl.page_links(6, 10) == [1, None, 5, 6, 7, None, 10]
    assert dl.size_bytes('8.4 GB') == 8.4e9 and dl.size_bytes(None) == 0


def test_data_page_renders(session, test_client, tmp_path, monkeypatch):
    from app.search import routes
    elements = [_element(tmp_path, 'projects/d{}'.format(i), title='Dataset {}'.format(i),
                         dateAdded='2024-{:02d}-{:02d}'.format(i // 28 + 1, i % 28 + 1)) for i in range(35)]
    elements.append(_element(tmp_path, 'projects/locked', title='Locked dataset', authorizations='registered',
                             registrationPage='https://cbigr.loris.ca', modalities=['genomics'],
                             evidencePublication='10.55458/neurolibre.00004', evidencePublicationType='Re-executable'))
    monkeypatch.setattr(routes, '_dataset_elements', lambda q, authorized: elements)
    html = test_client.get('/search').get_data(as_text=True)
    assert 'Search by name, keyword, modality, contributor' in html
    assert '36 datasets' in html and 'rel="next"' in html and 'Locked dataset' not in html
    html = test_client.get('/search?sort=evidence').get_data(as_text=True)
    assert 'Locked dataset' in html and 'Request access at C-BIG' in html and 'Account needed' in html and 'Re-executable publication' in html
    assert 'CONPReact.DataTableContainer' not in html
    html = test_client.get('/search?modality=Genomics').get_data(as_text=True)
    assert '1 dataset</strong>' in html and 'Dataset 3' not in html and 'Clear search and filters' in html
    html = test_client.get('/search?page=2').get_data(as_text=True)
    assert 'aria-current="page">2<' in html
    # Old links: ?sortKey=title&max_per_page=50 sorts by name and shows 50.
    html = test_client.get('/search?sortKey=title&max_per_page=50').get_data(as_text=True)
    assert '<option value="name" selected>' in html and 'rel="next"' not in html


def test_dataset_search_json_hides_server_paths(session, test_client, monkeypatch, tmp_path):
    from app.search import routes
    monkeypatch.setattr(routes, '_dataset_elements', lambda q, authorized: [_element(tmp_path, 'projects/x')])
    body = test_client.get('/dataset-search').get_json(force=True)
    assert body['elements'] and not any(k.startswith('_') for k in body['elements'][0])
