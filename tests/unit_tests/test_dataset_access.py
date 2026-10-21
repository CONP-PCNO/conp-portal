"""Tests for the access-by-status rule on the dataset page's Get the data tab."""
from flask import render_template

from app.search.dataset_page import access_context, host_name, repository_has_data
from tests.unit_tests.test_dataset_page import _data, _metadata


def _repo(tmp_path, files=(), dirs=(), gitmodules=False):
    d = tmp_path / 'repo'
    d.mkdir(parents=True)
    for f in ('DATS.json', 'README.md', 'logo.png', '.gitattributes') + tuple(files):
        (d / f).write_text('x')
    (d / '.datalad').mkdir()
    for sub in dirs:
        (d / sub).mkdir(parents=True)
        (d / sub / 'f.nii.gz').write_text('x')
    if gitmodules:
        (d / '.gitmodules').write_text('[submodule "images"]\n\tpath = images\n')
    return str(d)


def test_repository_has_data(tmp_path):
    assert repository_has_data(_repo(tmp_path / 'a')) is False                       # metadata only
    assert repository_has_data(_repo(tmp_path / 'b', files=('data.csv',))) is True
    assert repository_has_data(_repo(tmp_path / 'c', dirs=('sub-01/anat',))) is True
    assert repository_has_data(_repo(tmp_path / 'd', gitmodules=True)) is True     # subdatasets
    assert repository_has_data(str(tmp_path / 'missing')) is None


def test_host_name():
    assert host_name('https://www.braincode.ca/user/register') == 'Brain-CODE'
    assert host_name('https://cbigr-open.loris.ca/login/request-account/') == 'C-BIG'
    assert host_name('https://eegnet.loris.ca/') == 'EEGNet'
    assert host_name('https://openpreventad.loris.ca/login/request-account/') == 'PREVENT-AD'
    assert host_name('https://phantom.loris.ca') == 'phantom.loris.ca'
    assert host_name(None) is None


def _get_tab(app, authorization, has_data, registration=None, landing='https://www.braincode.ca/', offsite=False):
    page = {"licences": [], "citation": "C.", "cbrainPipelinesUrl": "/p", "views": 0,
            "access": {'restricted': authorization in ('registered', 'private', 'controlled'), 'has_data': has_data,
                       'host': host_name(registration) or host_name(landing), 'source_host': host_name(landing)}}
    data = _data(authorizations=authorization, showDownloadButton=(authorization == 'public'))
    meta = _metadata(registrationPage=registration, sources=landing, downloadOptions='offsite' if offsite else None)
    with app.test_request_context('/dataset?id=projects/demo'):
        html = render_template('dataset.html', title='t', data=data, metadata=meta, readme='',
                               page=page, ciBadgeUrl='', user=None)
    return html[html.index('id="get"'):html.index('id="about"')]


def test_get_tab_metadata_only_restricted(app):
    # Brain-CODE fBIRN: private, registration page, repository holds only metadata
    get = _get_tab(app, 'private', False, registration='https://www.braincode.ca/user/register')
    assert '1. Request access at Brain-CODE' in get
    assert '2. Download at the source' in get and 'Go to Brain-CODE' in get
    assert 'datalad install' not in get


def test_get_tab_restricted_with_data(app):
    # PREVENT-AD: private, registration page, files in the repository
    get = _get_tab(app, 'private', True, registration='https://openpreventad.loris.ca/login/request-account/',
                   landing='https://www.centre-stopad.com/en/')
    assert '1. Request access at PREVENT-AD' in get
    assert '2. With DataLad' in get and 'Use your PREVENT-AD account' in get
    assert 'tar.gz' not in get and 'Download at the source' not in get


def test_get_tab_restricted_no_registration_page(app):
    # TLE DR011: registered, no registration page, metadata only
    get = _get_tab(app, 'registered', False)
    assert 'Request access' not in get and 'datalad install' not in get
    assert 'An account is needed' in get and 'Go to Brain-CODE' in get


def test_get_tab_public_with_data_unchanged(app):
    get = _get_tab(app, 'public', True, landing='https://example.org')
    assert 'in a single tar.gz file' in get and 'datalad install demo' in get
    assert 'Request access' not in get


def test_get_tab_public_metadata_only(app):
    get = _get_tab(app, 'public', False, landing='https://dataverse.example.org/x')
    assert 'datalad install' not in get and 'Download at the source' in get and 'Request access' not in get


def test_access_context(tmp_path):
    ctx = access_context('private', 'https://www.braincode.ca/user/register', 'https://www.braincode.ca/', _repo(tmp_path))
    assert ctx == {'restricted': True, 'has_data': False, 'host': 'Brain-CODE', 'source_host': 'Brain-CODE'}
    # the record decides, not the host: open LORIS data needs no account
    assert access_context('public', None, 'https://phantom.loris.ca', None)['restricted'] is False
    assert access_context('public', None, None, None)['has_data'] is True   # unreadable folder: keep DataLad


def test_get_tab_restricted_with_data_no_registration_page(app):
    # PERFORM (Zenodo, restricted): private, files in the repository, no registration page
    get = _get_tab(app, 'private', True, landing='https://zenodo.org/record/3518486')
    assert '1. Request access at Zenodo' in get
    assert "Request it on the dataset page: zenodo.org/record/3518486" in get
    assert '2. With DataLad' in get and 'Use your Zenodo account' in get
    assert 'tar.gz' not in get
