"""Browser downloads read from DATS (app.downloads): every link is checked
against the record, records split into parts list one link per part, and no
zip address is guessed from an OSF landing page."""
import json

import pytest
from flask import render_template

from app.downloads import check_access_url, download_parts, size_label, total_bytes
from app.search.dataset_page import direct_download, get_routes

ZIP = 'https://files.us.osf.io/v1/resources/{}/providers/{}/?zip='


def _dist(landing, url=None, size=1, unit='MB', title=None, identifier=None, auth='public'):
    access = {'landingPage': landing, 'authorizations': [{'value': auth}]}
    if url:
        access['accessURL'] = url
    d = {'size': size, 'unit': {'value': unit}, 'formats': ['N/A'], 'access': access}
    if title:
        d['title'] = title
    if identifier:
        d['identifier'] = {'identifier': identifier, 'identifierSource': 'OSF'}
    return d


@pytest.mark.parametrize('node', ['q482e', 'vmg62', 'm7nz2', 'k5zb9', 'xhvsk', 'h3ec5'])
def test_the_six_records_that_served_the_tau_dataset(node):
    # live until this fix: OSF ignores the zip= value, so each of these served znt9d (22.6 GB)
    dist = _dist('https://osf.io/{}/'.format(node), 'https://files.us.osf.io/v1/resources/znt9d/providers/osfstorage/?zip=' + node)
    host, fmt, problem = check_access_url(dist)
    assert host == 'OSF' and 'znt9d' in problem
    assert download_parts({'distributions': [dist]}) == []


def test_zip_value_must_be_empty_even_for_the_right_node():
    dist = _dist('https://osf.io/znt9d', 'https://files.us.osf.io/v1/resources/znt9d/providers/osfstorage/?zip=znt9d')
    assert 'empty' in check_access_url(dist)[2]


def test_osf_addon_zip_is_refused():
    # OSF stops add-on zip streams after 64 KiB (GitHub/GitLab-backed experiments)
    dist = _dist('https://doi.org/10.17605/OSF.IO/4DGBY', ZIP.format('4dgby', 'github'))
    assert '64 KiB' in check_access_url(dist)[2]


def test_component_parts_named_by_identifier():
    # Neural capacity limits (osf.io/xwajn): the project's own storage is empty, files in components
    desc = {'distributions': [
        _dist('https://osf.io/xwajn/', ZIP.format('qzucv', 'osfstorage'), 303.6, 'MB',
              'Participant level contrast maps', 'https://osf.io/qzucv/'),
        _dist('https://osf.io/xwajn/', ZIP.format('8bwys', 'osfstorage'), 22.5, 'KB',
              'Behavioral Data', 'https://osf.io/8bwys/'),
    ]}
    parts = download_parts(desc)
    assert [p['title'] for p in parts] == ['Participant level contrast maps', 'Behavioral Data']
    assert parts[0]['size'] == '303.6 MB' and parts[1]['size'] == '22.5 KB'
    assert all(p['host'] == 'OSF' and p['format'] == 'ZIP' and not p['too_large'] for p in parts)
    assert size_label(total_bytes(desc)) == '303.6 MB'
    # a component zip without the component named as the part's identifier is refused
    desc['distributions'][1].pop('identifier')
    assert len(download_parts(desc)) == 1


def test_no_zip_guessed_and_private_records_get_none():
    assert download_parts({'distributions': [_dist('https://osf.io/xwajn/')]}) == []
    assert download_parts({'distributions': [_dist('https://osf.io/q482e', ZIP.format('q482e', 'osfstorage'),
                                                   auth='private')]}) == []


def test_size_limit_lists_the_part_without_a_button(app, tmp_path):
    desc = {'distributions': [_dist('https://osf.io/m7nz2/', ZIP.format('m7nz2', 'osfstorage'), 106.7, 'GB')]}
    parts = download_parts(desc)
    assert parts[0]['too_large'] is True and parts[0]['streamed'] is True
    assert direct_download(desc) is None
    # the page says why, and links the OSF record; the Data page card offers no download
    (tmp_path / '.conp-osf-crawler.json').write_text('{}')
    routes = get_routes('public', None, None, 'https://osf.io/m7nz2/', str(tmp_path), descriptor=desc, has_data=True)
    assert routes['browser'] == 'too_large' and routes['record']['host'] == 'OSF'
    from tests.unit_tests.test_dataset_page import _data, _metadata
    page = {'licences': [], 'citation': 'C.', 'cbrainPipelinesUrl': '/p', 'views': 0, 'publications': [],
            'direct_download': None, 'dats_html': '', 'doi': None, 'parents': [], 'routes': routes}
    with app.test_request_context('/dataset?id=projects/demo'):
        html = render_template('dataset.html', title='t', data=_data(size='106.7 GB'), metadata=_metadata(),
                               readme='', page=page, user=None)
    assert 'At 106.7 GB, the dataset is too large for one browser download' in html
    assert 'data-dp-download' not in html and 'Go to OSF' in html


def test_size_limit_only_for_streamed_zips():
    # a stored Zenodo file has a known size and can be resumed: no limit
    big = {'distributions': [_dist('https://zenodo.org/records/7', 'https://zenodo.org/records/7/files/a.zip/content',
                                   50, 'GB')]}
    part = download_parts(big)[0]
    assert part['streamed'] is False and part['too_large'] is False


def test_zenodo_record_must_match_and_github_archive_is_accepted():
    zen = _dist('https://zenodo.org/records/3518486', 'https://zenodo.org/records/999/files/x.zip/content')
    assert 'Zenodo record 999' in check_access_url(zen)[2]
    gh = _dist('https://doi.org/10.17605/OSF.IO/6CTSJ',
               'https://github.com/katielavigne/sternberg-working-memory-task/archive/refs/heads/main.zip')
    assert check_access_url(gh) == ('GitHub', 'ZIP', None)


def test_dataset_page_lists_each_part(app, tmp_path):
    from tests.unit_tests.test_dataset_page import _data, _metadata
    (tmp_path / '.conp-osf-crawler.json').write_text('{}')
    desc = {'distributions': [
        _dist('https://osf.io/xhvsk/', ZIP.format('pny28', 'osfstorage'), 220.6, 'MB', 'Participant level contrast maps',
              'https://osf.io/pny28/'),
        _dist('https://osf.io/xhvsk/', ZIP.format('px49j', 'osfstorage'), 12, 'KB', 'Behavioral data',
              'https://osf.io/px49j/'),
        _dist('https://osf.io/xhvsk/', None, 60, 'GB', 'Raw images', 'https://osf.io/abcde/'),
    ]}
    desc['distributions'][2]['access']['accessURL'] = ZIP.format('abcde', 'osfstorage')
    routes = get_routes('public', None, None, 'https://osf.io/xhvsk/', str(tmp_path), descriptor=desc,
                        has_data=True)
    assert routes['browser'] == 'direct' and len(routes['parts']) == 3
    page = {'licences': [], 'citation': 'C.', 'cbrainPipelinesUrl': '/p', 'views': 0, 'publications': [],
            'direct_download': routes['direct'], 'dats_html': '', 'doi': None, 'parents': [], 'routes': routes}
    with app.test_request_context('/dataset?id=projects/demo'):
        html = render_template('dataset.html', title='t', data=_data(size='60.2 GB'), metadata=_metadata(),
                               readme='', page=page, user=None)
    assert 'come in 3 parts' in html
    assert html.count('data-dp-download') == 2   # the 60 GB part has no button
    assert 'Too large for a browser: use DataLad' in html
    assert ZIP.format('pny28', 'osfstorage') in html and ZIP.format('px49j', 'osfstorage') in html


def test_experiment_download_reads_the_access_url(session, test_client, tmp_path, monkeypatch):
    from app.models import Experiment
    from app.services import github
    monkeypatch.setattr(github, 'render_content', lambda raw: '<p>Sternberg.</p>')
    folder = tmp_path / 'sternberg'
    folder.mkdir()
    (folder / 'README.md').write_text('Sternberg.')
    url = 'https://github.com/katielavigne/sternberg-working-memory-task/archive/refs/heads/main.zip'
    (folder / 'DATS.json').write_text(json.dumps({
        'title': 'Sternberg Working Memory Task', 'version': '1.0', 'privacy': 'open',
        'creators': [{'name': 'Katie M. Lavigne'}], 'description': 'A working memory task.',
        'types': [{'information': {'value': 'experiment'}}], 'licenses': [{'name': 'CC BY'}],
        'keywords': [{'value': 'memory'}],
        'distributions': [_dist('https://doi.org/10.17605/OSF.IO/6CTSJ', url, 31.6, 'KB')],
        'extraProperties': [{'category': 'CONP_status', 'values': [{'value': 'Canadian'}]}]}))
    session.add(Experiment(experiment_id='projects/sternberg', name='Sternberg Working Memory Task',
                           fspath=str(folder), version='1', is_private=False))
    session.flush()
    html = test_client.get('/experiments/view/sternberg').get_data(as_text=True)
    assert 'href="{}"'.format(url) in html
    assert "downloaded directly from the authors' GitHub repository" in html


def test_default_limit_is_50_gb():
    # chosen 26 Oct 2026: tau (45.2 GB) and the MICA-PNI subject parts (up to 38.6 GB) keep their button
    under = {'distributions': [_dist('https://osf.io/znt9d', ZIP.format('znt9d', 'osfstorage'), 45.2, 'GB')]}
    over = {'distributions': [_dist('https://osf.io/m7nz2/', ZIP.format('m7nz2', 'osfstorage'), 50.1, 'GB')]}
    assert download_parts(under)[0]['too_large'] is False
    assert download_parts(over)[0]['too_large'] is True
