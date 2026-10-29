"""Removing datasets that conp-dataset no longer lists (flask prune_datasets)
while keeping their ARKs, and the ARK redirect's not-found cases."""
import pytest

import app.cli as cli
from app.models import ArkId, Dataset, DatasetAncestry, RetiredDataset


@pytest.fixture
def clean(session):
    """prune_datasets commits, so rows outlive a test: start from empty tables."""
    for model in (Dataset, DatasetAncestry, RetiredDataset, ArkId):
        session.query(model).delete()
    session.commit()
    return session


def _naan(app):
    return app.config['ARK_CONP_NAAN']


def _gitmodules(tmp_path, names):
    repo = tmp_path / 'conp-dataset'
    repo.mkdir(parents=True, exist_ok=True)
    lines = []
    for name in names:
        lines += ['[submodule "{}"]'.format(name), '\tpath = {}'.format(name.replace('bigbrain-datalad', 'BigBrain')),
                  '\turl = https://github.com/example/x']
    (repo / '.gitmodules').write_text('\n'.join(lines) + '\n')
    return tmp_path


def _add(session, *ids):
    for i in ids:
        session.add(Dataset(dataset_id=i, name=i.split('/')[-1].replace('_', ' '), fspath='/nowhere/' + i))
    session.commit()


def test_submodule_names_are_names_not_paths(tmp_path):
    root = _gitmodules(tmp_path, ['projects/bigbrain-datalad', 'projects/Khanlab/HCPUR100-Template'])
    assert cli._submodule_names(root / 'conp-dataset') == {'projects/bigbrain-datalad', 'projects/Khanlab/HCPUR100-Template'}
    assert cli._submodule_names(tmp_path / 'missing') == set()


def test_dry_run_lists_and_changes_nothing(app, clean, session, tmp_path, monkeypatch, capsys):
    monkeypatch.setitem(app.config, 'DATA_PATH', str(_gitmodules(tmp_path, ['projects/keep_a', 'projects/keep_b',
                                                                             'projects/keep_c', 'projects/keep_d'])))
    _add(session, 'projects/keep_a', 'projects/keep_b', 'projects/keep_c', 'projects/keep_d', 'projects/raw_PNC001_PNC003')
    assert cli._prune_datasets(app) == ['projects/raw_PNC001_PNC003']
    assert Dataset.query.filter_by(dataset_id='projects/raw_PNC001_PNC003').first() is not None
    assert 'Dry run' in capsys.readouterr().out


def test_apply_removes_rows_keeps_the_ark(app, clean, session, tmp_path, monkeypatch):
    monkeypatch.setitem(app.config, 'DATA_PATH', str(_gitmodules(tmp_path, ['projects/keep_a', 'projects/keep_b',
                                                                             'projects/keep_c', 'projects/keep_d'])))
    monkeypatch.setattr(cli, '_update_index', lambda *a, **k: None)
    _add(session, 'projects/keep_a', 'projects/keep_b', 'projects/keep_c', 'projects/keep_d', 'projects/processed_PNC007')
    ark = 'ark:/{}/d7retiredtest01'.format(_naan(app))
    session.add(ArkId(ark_id=ark, dataset_id='projects/processed_PNC007'))
    session.add(DatasetAncestry(id='x1', parent_dataset_id='projects/keep_a', child_dataset_id='projects/processed_PNC007'))
    session.commit()
    assert cli._prune_datasets(app, apply_changes=True, replaced_by='projects/not-a-dataset') == []   # checked first
    assert cli._prune_datasets(app, apply_changes=True, reason='Withdrawn by the provider.',
                               replaced_by='projects/keep_a') == ['projects/processed_PNC007']
    assert Dataset.query.filter_by(dataset_id='projects/processed_PNC007').first() is None
    assert DatasetAncestry.query.filter_by(child_dataset_id='projects/processed_PNC007').count() == 0
    assert ArkId.query.filter_by(ark_id=ark).first().dataset_id == 'projects/processed_PNC007'   # ARK kept
    r = RetiredDataset.query.filter_by(dataset_id='projects/processed_PNC007').first()
    assert r.name == 'processed PNC007' and r.reason == 'Withdrawn by the provider.' and r.replaced_by == 'projects/keep_a'
    assert Dataset.query.filter_by(dataset_id='projects/keep_a').first() is not None


def test_refuses_when_gitmodules_unreadable_or_too_many(app, clean, session, tmp_path, monkeypatch):
    monkeypatch.setitem(app.config, 'DATA_PATH', str(tmp_path / 'empty'))
    _add(session, 'projects/one', 'projects/two')
    assert cli._prune_datasets(app, apply_changes=True) == []          # can't read .gitmodules: nothing
    monkeypatch.setitem(app.config, 'DATA_PATH', str(_gitmodules(tmp_path, ['projects/one'])))
    assert cli._prune_datasets(app, apply_changes=True) == []          # 1 of 2 = more than a quarter
    assert Dataset.query.filter_by(dataset_id='projects/two').first() is not None


def test_retired_dataset_and_its_ark(app, clean, session, test_client):
    from datetime import datetime
    ark_tail = 'd7retiredtest02'
    session.add(ArkId(ark_id='ark:/{}/{}'.format(_naan(app), ark_tail), dataset_id='projects/gone'))
    session.add(Dataset(dataset_id='projects/new_one', name='The new one', fspath='/nowhere'))
    session.add(RetiredDataset(dataset_id='projects/gone', name='Gone dataset', retired_on=datetime(2026, 10, 28),
                               reason='Removed from the CONP catalogue.', replaced_by='projects/new_one'))
    session.commit()
    r = test_client.get('/ark:/{}/{}'.format(_naan(app), ark_tail))
    assert r.status_code == 302 and r.headers['Location'].endswith('/dataset?id=projects/gone')
    r = test_client.get('/dataset?id=projects/gone')
    html = r.get_data(as_text=True)
    assert r.status_code == 410 and 'Gone dataset' in html and '2026-10-28' in html and ark_tail in html
    assert 'replaced by <a href="/dataset?id=projects/new_one">The new one</a>' in html
    assert test_client.get('/dataset?id=projects/never-existed').status_code == 404


def test_unknown_ark_is_not_found(app, test_client):
    assert test_client.get('/ark:/{}/d7doesnotexist0000'.format(_naan(app))).status_code == 404   # was 500
    assert test_client.get('/ark:/{}/e7doesnotexist0000'.format(_naan(app))).status_code == 404
    assert test_client.get('/ark:/00000/d7doesnotexist0000').status_code == 404


def test_experiment_ark_redirects(app, clean, session, test_client):
    session.add(ArkId(ark_id='ark:/{}/e7exptest01'.format(_naan(app)), experiment_id='projects/BADE-evidence-integration'))
    session.commit()
    r = test_client.get('/ark:/{}/e7exptest01'.format(_naan(app)))
    assert r.status_code == 302 and r.headers['Location'].endswith('/experiments/view/BADE-evidence-integration')


def test_slash_puts_focus_in_the_search_box(test_client):
    html = test_client.get('/find?q=mri').get_data(as_text=True)
    assert "e.key !== '/'" in html and "aria-keyshortcuts" in html


def test_flask_command_is_a_dry_run_by_default(app, clean, session, tmp_path, monkeypatch):
    monkeypatch.setitem(app.config, 'DATA_PATH', str(_gitmodules(tmp_path, ['projects/keep_a', 'projects/keep_b',
                                                                             'projects/keep_c', 'projects/keep_d'])))
    _add(session, 'projects/keep_a', 'projects/keep_b', 'projects/keep_c', 'projects/keep_d', 'projects/raw_PNC004_PNC006')
    if 'prune_datasets' not in app.cli.commands:
        cli.register(app)    # done by the app's entry script, not create_app
    out = app.test_cli_runner().invoke(args=['prune_datasets']).output
    assert 'projects/raw_PNC004_PNC006' in out and 'Dry run' in out
    assert Dataset.query.filter_by(dataset_id='projects/raw_PNC004_PNC006').first() is not None


def test_unreadable_dataset_is_unavailable_not_a_server_error(app, clean, session, test_client):
    # A row whose folder is gone (failed checkout, or removed from conp-dataset
    # and not yet pruned): 503 with an explanation, not 500.
    session.add(Dataset(dataset_id='projects/folder_gone', name='Folder gone', fspath='/nowhere/folder_gone'))
    session.commit()
    r = test_client.get('/dataset?id=projects/folder_gone')
    assert r.status_code == 503
