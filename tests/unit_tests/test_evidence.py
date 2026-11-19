"""Evidence banner (option A): titles and first-page thumbnails of the
NeuroLibre/Evidence publications, and how the dataset page shows them."""
import json

from app.search import evidence
from tests.unit_tests.test_dataset_page import _data, _metadata, _render

LANDING = '''<html><head>
<meta name="citation_title" content="Strong Coupling of Retinal Thickness and Optic Nerve Myelin in Vivo">
<meta name="citation_pdf_url" content="https://neurolibre.org/papers/10.55458/neurolibre.00050.pdf">
<meta property="og:image" content="https://conp-pcno.github.io/images/neurolibre-icon-red.png" />
</head></html>'''


class _Resp:
    def __init__(self, status_code=200, text='', content=b''):
        self.status_code, self.text, self.content = status_code, text, content


def _fake_get(calls):
    def get(url):
        calls.append(url)
        if url.startswith('https://doi.org/'):
            return _Resp(text=LANDING)
        if url.endswith('.pdf'):
            return _Resp(content=b'%PDF-1.5 fake')
        return _Resp(404)
    return get


def _fake_renderer(pdf_bytes, out_png, width=evidence.THUMB_WIDTH):
    with open(out_png, 'wb') as f:
        f.write(b'\x89PNG fake')
    return True


def test_doi_slug_and_landing_page():
    assert evidence.doi_slug('10.55458/NeuroLibre.00050') == '10-55458-neurolibre-00050'
    title, pdf = evidence.parse_landing(LANDING)
    assert title.startswith('Strong Coupling') and pdf.endswith('neurolibre.00050.pdf')
    assert evidence.parse_landing('<html></html>') == (None, None)


def test_update_records_title_and_thumbnail_once(tmp_path):
    calls = []
    index = evidence.update(str(tmp_path), ['10.55458/neurolibre.00050'], get=_fake_get(calls),
                            renderer=_fake_renderer, log=lambda m: None)
    entry = index['10.55458/neurolibre.00050']
    assert entry['thumbnail'] == '10-55458-neurolibre-00050.png' and entry['title'].startswith('Strong Coupling')
    assert (tmp_path / 'evidence-publications' / entry['thumbnail']).exists()
    info = evidence.publication_info(str(tmp_path), '10.55458/NEUROLIBRE.00050')
    assert info == {'title': entry['title'], 'thumbnail': entry['thumbnail']}
    # Done already: nothing is fetched again unless forced.
    calls.clear()
    evidence.update(str(tmp_path), ['10.55458/neurolibre.00050'], get=_fake_get(calls), renderer=_fake_renderer,
                    log=lambda m: None)
    assert calls == []
    evidence.update(str(tmp_path), ['10.55458/neurolibre.00050'], get=_fake_get(calls), renderer=_fake_renderer,
                    force=True, log=lambda m: None)
    assert len(calls) == 2


def test_update_without_a_renderer_keeps_the_title(tmp_path):
    index = evidence.update(str(tmp_path), ['10.55458/neurolibre.00050'], get=_fake_get([]),
                            renderer=lambda *a, **k: False, log=lambda m: None)
    assert index['10.55458/neurolibre.00050']['title'] and 'thumbnail' not in index['10.55458/neurolibre.00050']
    assert evidence.publication_info(str(tmp_path), '10.55458/neurolibre.00050')['thumbnail'] is None


def test_a_missing_thumbnail_file_is_not_offered(tmp_path):
    folder = tmp_path / 'evidence-publications'
    folder.mkdir()
    (folder / 'index.json').write_text(json.dumps({'10.1/x': {'title': 'T', 'thumbnail': '10-1-x.png'}}))
    assert evidence.publication_info(str(tmp_path), '10.1/x') == {'title': 'T', 'thumbnail': None}
    assert evidence.publication_info(str(tmp_path), '10.1/unknown') == {'title': None, 'thumbnail': None}


def test_thumbnail_route(test_client, app, tmp_path, monkeypatch):
    monkeypatch.setitem(app.config, 'DATA_PATH', str(tmp_path))
    folder = tmp_path / 'evidence-publications'
    folder.mkdir()
    (folder / '10-55458-neurolibre-00050.png').write_bytes(b'\x89PNG fake')
    # No .png in the address: nginx would serve it as a static file (404).
    r = test_client.get('/evidence_thumbnail/10-55458-neurolibre-00050')
    assert r.status_code == 200 and r.mimetype == 'image/png' and r.cache_control.max_age == 86400
    assert test_client.get('/evidence_thumbnail/10-55458-neurolibre-00050.png').status_code == 404
    assert test_client.get('/evidence_thumbnail/index').status_code == 404
    assert test_client.get('/evidence_thumbnail/..%2Findex').status_code == 404


def test_banner_with_page_title_and_without(app):
    html = _render(app, _data(evidencePublication='10.55458/neurolibre.00050', evidencePublicationType='Wired',
                              evidenceTitle='Strong Coupling', evidenceThumbnail='/evidence_thumbnail/x.png'),
                   _metadata())
    assert 'class="dp-evidence dp-evidence--page"' in html
    assert '<img class="dp-evidence-page" src="/evidence_thumbnail/x.png" alt="" aria-hidden="true"' in html
    assert ': <cite>Strong Coupling</cite>' in html and '>Wired</span>' in html
    plain = _render(app, _data(evidencePublication='10.55458/neurolibre.00007', evidencePublicationType='Re-executable'),
                    _metadata())
    assert 'class="dp-evidence"' in plain and 'dp-evidence-page' not in plain and '<cite>' not in plain
    assert 'whose analyses you can re-run' in plain


def test_dataset_page_thumbnail_address_has_no_png(app, tmp_path, monkeypatch):
    from app.search import routes
    folder = tmp_path / 'evidence-publications'
    folder.mkdir()
    (folder / '10-55458-neurolibre-00050.png').write_bytes(b'\x89PNG fake')
    (folder / 'index.json').write_text(json.dumps({'10.55458/neurolibre.00050': {
        'title': 'T', 'thumbnail': '10-55458-neurolibre-00050.png'}}))
    ev = evidence.publication_info(str(tmp_path), '10.55458/neurolibre.00050')
    with app.test_request_context('/'):
        url = routes.url_for('search.evidence_thumbnail', slug=ev['thumbnail'][:-4])
    assert url == '/evidence_thumbnail/10-55458-neurolibre-00050' and not url.endswith('.png')


def test_cli_update_evidence_thumbnails(runner, app, tmp_path, monkeypatch):
    import requests

    from app import cli
    monkeypatch.setitem(app.config, 'DATA_PATH', str(tmp_path))
    monkeypatch.setattr(requests, 'get', lambda url, **kw: _fake_get([])(url))
    monkeypatch.setattr(evidence, 'render_first_page', _fake_renderer)
    if 'update_evidence_thumbnails' not in app.cli.commands:
        cli.register(app)
    result = runner.invoke(args=['update_evidence_thumbnails', '--doi', '10.55458/neurolibre.00050'])
    assert 'Done: 1 recorded, 1 with a thumbnail.' in result.output, result.output
