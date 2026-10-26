"""One access decision for the dataset page and its Data page card; README
links that work on the Portal; card titles and descriptions as written."""
import json

from app.search import dataset_list as dl
from app.search.dataset_page import as_url, fix_readme_links, get_routes


def _element(tmp_path, id_, **kw):
    folder = tmp_path / id_.replace('/', '_')
    folder.mkdir()
    (folder / 'DATS.json').write_text(json.dumps(kw.pop('dats', {'title': id_})))
    for name in kw.pop('files', []):
        (folder / name).write_text('x')
    e = {'id': id_, 'title': id_.split('/')[-1], 'thumbnailURL': '/x', 'logoFilepath': None,
         'authorizations': 'public', 'conpStatus': 'Canadian', 'downloadOptions': None, 'sources': None,
         'registrationPage': None, 'cbrain_id': None, 'showDownloadButton': False, 'creators': [],
         'dateAdded': '2024-01-01', 'dateUpdated': '2024-02-01', 'version': '1.0', 'size': '1 GB',
         'subjects': None, 'modalities': [], 'formats': [], 'licenses': [], 'evidencePublication': None,
         'evidencePublicationType': None, 'views': [], '_fspath': str(folder), '_description': '', '_keywords': []}
    e.update(kw)
    return e


def test_card_never_offers_a_step_the_page_lacks(tmp_path):
    # C-BIG genomics: registered, offsite, no registration page, a landing page.
    cbig = _element(tmp_path, 'projects/cbig_x_wgs', authorizations='registered', downloadOptions='offsite',
                    sources=['https://cbigr.loris.ca/'])
    c = dl.dataset_card(cbig)
    r = get_routes('registered', 'offsite', None, 'https://cbigr.loris.ca/', cbig['_fspath'])
    assert not r['request'] and r['source']                 # the page: "Download at the source" only
    assert c['request'] is None and c['at_source']          # the card links to #route-source, not #route-request
    assert c['access_facet'] == ['Account needed'] and dl.ROUTE_SOURCE in c['routes_facet']
    # with a registration page both show the request step
    c = dl.dataset_card(_element(tmp_path, 'projects/cbig_y', authorizations='registered', downloadOptions='offsite',
                                 sources=['https://cbigr.loris.ca/'], registrationPage='https://cbigr.loris.ca/register'))
    assert c['request'] == 'Request access at C-BIG'


def test_zenodo_record_without_a_single_file(tmp_path):
    dats = {'distributions': [{'access': {'landingPage': 'https://zenodo.org/records/4041549',
                                          'authorizations': [{'value': 'public'}]}}]}
    e = _element(tmp_path, 'projects/multi', files=['a.h5', '.conp-zenodo-crawler.json'], dats=dats,
                 sources=['https://zenodo.org/records/4041549'])
    r = get_routes('public', None, None, 'https://zenodo.org/records/4041549', e['_fspath'], descriptor=dats)
    assert r['browser'] == 'record' and r['record']['host'] == 'Zenodo' and r['direct'] is None
    r = get_routes('public', None, None, 'https://zenodo.org/records/4041549', e['_fspath'], descriptor=dats, archive=True)
    assert r['browser'] == 'archive'                        # the Portal archive comes before the record
    assert dl.dataset_card(e)['download']


def test_readme_links_and_identifiers():
    html = ('<a href="10.3389/fnagi.2016.00040">a</a><a href="www.cdip-pcid.ca">b</a>'
            '<img src="media/figure_2.png" alt=""><a href="#x">c</a><a href="/search?q=a">d</a>'
            '<a href="mailto:a@b.ca">e</a><a href="https://ok.org">f</a><a href="data.csv">g</a>')
    out = fix_readme_links(html, 'https://github.com/conpdatasets/algonauts_2025_competitors\n')
    assert 'href="https://doi.org/10.3389/fnagi.2016.00040"' in out and 'href="https://www.cdip-pcid.ca"' in out
    assert 'src="https://raw.githubusercontent.com/conpdatasets/algonauts_2025_competitors/HEAD/media/figure_2.png"' in out
    assert 'href="https://github.com/conpdatasets/algonauts_2025_competitors/blob/HEAD/data.csv"' in out
    for kept in ('href="#x"', 'href="/search?q=a"', 'href="mailto:a@b.ca"', 'href="https://ok.org"'):
        assert kept in out
    assert as_url('10.1002/alz.12632') == 'https://doi.org/10.1002/alz.12632'
    assert as_url('https://doi.org:10.1038/s41597-025-04863-7') == 'https://doi.org/10.1038/s41597-025-04863-7'
    assert as_url('https://example.org/a') == 'https://example.org/a'


def test_card_title_and_description_as_written(tmp_path):
    c = dl.dataset_card(_element(tmp_path, 'projects/t', title='Results of the T<sub>1</sub> challenge',
                                 _description='Rock&amp;nbsp;Island &amp;#39;quoted&amp;#39;'))
    assert str(c['title_html']) == 'Results of the T<sub>1</sub> challenge'
    assert c['description'] == "Rock Island 'quoted'"
    cards = [{'title': '(Dataset) Zeta'}, {'title': 'alpha'}, {'title': 'Beta'}]
    assert [x['title'] for x in sorted(cards, key=lambda x: dl.sort_title(x['title']))] == ['alpha', 'Beta', '(Dataset) Zeta']
