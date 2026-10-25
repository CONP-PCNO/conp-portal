"""Experiments: stable page addresses, DATS download, logo type, README
escaping and the retired submission form."""
import os
import shutil

from app.models import Experiment

FIXTURE = os.path.join(os.path.dirname(__file__), 'fixtures', 'experiment_BADE')
PNG = b'\x89PNG\r\n\x1a\n' + b'\x00' * 16


def _experiment(session, tmp_path, readme='# BADE\n\nA `code` span and ${not a template}.'):
    folder = tmp_path / 'BADE-evidence-integration'
    shutil.copytree(FIXTURE, folder)
    (folder / 'README.md').write_text(readme)
    (folder / 'logo.png').write_bytes(PNG)
    Experiment.query.filter_by(experiment_id='projects/BADE-evidence-integration').delete()
    exp = Experiment(experiment_id='projects/BADE-evidence-integration', name='BADE Evidence Integration',
                     fspath=str(folder), version='1.0', is_private=False)
    session.add(exp)
    session.flush()
    return exp


def test_numeric_address_moves_to_stable_address(session, test_client, tmp_path):
    exp = _experiment(session, tmp_path)
    res = test_client.get(f'/experiments/view/{exp.id}')
    assert res.status_code == 301
    assert res.headers['Location'].endswith('/experiments/view/BADE-evidence-integration')
    res = test_client.get('/experiments/view/projects/BADE-evidence-integration')
    assert res.status_code == 301


def test_stable_address_renders_and_readme_is_escaped(session, test_client, tmp_path):
    _experiment(session, tmp_path)
    res = test_client.get('/experiments/view/BADE-evidence-integration')
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert 'rel="canonical"' in html and '/experiments/view/BADE-evidence-integration' in html
    # the README is rendered on the server (a backtick or ${ in it can't break the page)
    assert 'readme: `' not in html
    assert test_client.get('/experiments/view/no-such-experiment').status_code == 404


def test_search_skips_an_experiment_with_missing_metadata(session, test_client, tmp_path, caplog):
    good = _experiment(session, tmp_path)
    bad = Experiment(
        experiment_id='projects/missing-metadata',
        name='Missing metadata',
        fspath=str(tmp_path / 'missing-metadata'),
        version='1.0',
        is_private=False,
    )
    session.add(bad)
    session.flush()

    response = test_client.get('/experiments/')

    assert response.status_code == 200
    assert good.name in response.get_data(as_text=True)
    assert 'Skipping experiment projects/missing-metadata' in caplog.text


def test_dats_download(session, test_client, tmp_path):
    exp = _experiment(session, tmp_path)
    for key in (exp.id, 'BADE-evidence-integration'):
        res = test_client.get('/download_metadata_experiment', query_string={'experiment': key})
        assert res.status_code == 200, key
        assert 'BADE_Evidence_Integration.dats.json' in res.headers['Content-Disposition']
        assert res.get_json()['title'] == 'BADE Evidence Integration'


def test_logo_is_an_image(session, test_client, tmp_path):
    exp = _experiment(session, tmp_path)
    res = test_client.get(f'/experiments/experiment_logo/{exp.id}')
    assert res.status_code == 200 and res.mimetype == 'image/png'


def test_submit_goes_to_the_dats_editor(test_client):
    res = test_client.get('/experiments/submit')
    assert res.status_code == 302 and res.headers['Location'].endswith('/dats-editor')


def test_unreadable_experiment_page_is_not_found(session, test_client, tmp_path):
    """
    GIVEN an experiment row whose folder no longer exists (e.g. a submodule
          renamed in conp-experiments, like RISE on 23 Oct 2026)
    THEN its page answers 404, not 500
    """
    gone = Experiment(experiment_id='projects/renamed-away', name='Renamed away',
                      fspath=str(tmp_path / 'renamed-away'), version='1.0', is_private=False)
    session.add(gone)
    session.flush()
    assert test_client.get('/experiments/view/renamed-away').status_code == 404
