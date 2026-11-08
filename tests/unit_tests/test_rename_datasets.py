"""Datasets whose submodule path changed (conp-dataset clean-up, 5-6 Nov 2026)
were retired under the old id and listed again under a new one with a new ARK.
`flask rename_datasets` carries them over: original ARK, view history, old
address."""
from datetime import datetime

import pytest

from app import cli
from app.models import ArkId, Dataset, RetiredDataset
from app.models import MatomoDailyGetDatasetPageViewsSummary as Views

OLD, NEW = 'projects/Quantitative_T1_MRI', 'projects/Quantitative-T1-MRI'


@pytest.fixture
def clean(session):
    """These commands commit, so rows outlive a test: start and end empty."""
    def wipe():
        for model in (Views, ArkId, RetiredDataset, Dataset):
            session.query(model).delete()
        session.commit()
    wipe()
    yield session
    wipe()


def _naan(app):
    return app.config['ARK_CONP_NAAN']


def _renamed(app, session):
    """The state the clean-up left: old id retired with its ARK, new id listed
    with a newer ARK, views under both."""
    session.add(ArkId(ark_id=f'ark:/{_naan(app)}/d7originalark01', dataset_id=OLD))
    session.add(RetiredDataset(dataset_id=OLD, name='Quantitative T1 MRI', retired_on=datetime(2026, 11, 6),
                               reason='Normalization: Git Remote Changes, Project Folder Renaming'))
    session.add(Dataset(dataset_id=NEW, name='Quantitative T1 MRI', fspath='/nowhere/qt1'))
    session.commit()
    session.add(ArkId(ark_id=f'ark:/{_naan(app)}/d7newark0000002', dataset_id=NEW))
    for date, hits, ds in (('2026-10-01', 40, OLD), ('2026-11-05', 3, OLD), ('2026-11-06', 2, OLD),
                           ('2026-11-06', 1, NEW), ('2026-11-07', 5, NEW)):
        session.add(Views(date=date, dataset_id=ds, nb_hits=hits, nb_visits=hits))
    session.commit()


def test_dry_run_changes_nothing(app, clean, capsys):
    _renamed(app, clean)
    done = cli._rename_datasets(app, {OLD: NEW})
    assert done[OLD] == '1 ARK(s), 3 day(s) of views'
    assert ArkId.query.filter_by(dataset_id=OLD).count() == 1
    assert 'Dry run' in capsys.readouterr().out


def test_apply_carries_ark_views_and_address_over(app, clean, test_client):
    _renamed(app, clean)
    cli._rename_datasets(app, {OLD: NEW}, apply_changes=True)

    # Both ARKs resolve to the new page; the page shows the original one.
    for tail in ('d7originalark01', 'd7newark0000002'):
        r = test_client.get(f'/ark:/{_naan(app)}/{tail}')
        assert r.status_code == 302 and r.headers['Location'].endswith(f'/dataset?id={NEW}')
    first = ArkId.query.filter_by(dataset_id=NEW).order_by(ArkId.id).first()
    assert first.ark_id.endswith('d7originalark01')

    # View history moved; a day seen under both addresses is added up.
    views = {v.date: v.nb_hits for v in Views.query.filter_by(dataset_id=NEW)}
    assert views == {'2026-10-01': 40, '2026-11-05': 3, '2026-11-06': 3, '2026-11-07': 5}
    assert Views.query.filter_by(dataset_id=OLD).count() == 0

    # The old address redirects permanently to the new page.
    r = test_client.get(f'/dataset?id={OLD}')
    assert r.status_code == 301 and r.headers['Location'].endswith(f'/dataset?id={NEW}')
    retired = RetiredDataset.query.filter_by(dataset_id=OLD).first()
    assert retired.replaced_by == NEW and retired.reason.startswith('Renamed')

    # Running it again changes nothing more.
    assert cli._rename_datasets(app, {OLD: NEW}, apply_changes=True)[OLD] == '0 ARK(s), 0 day(s) of views'


def test_skips_while_old_id_still_listed_or_new_id_missing(app, clean):
    clean.add(Dataset(dataset_id='projects/old_still_here', name='x', fspath='/n'))
    clean.add(Dataset(dataset_id='projects/new_here', name='x', fspath='/n'))
    clean.commit()
    done = cli._rename_datasets(app, {'projects/old_still_here': 'projects/new_here',
                                      'projects/gone_old': 'projects/not_on_portal'}, apply_changes=True)
    assert done['projects/old_still_here'].startswith('skipped: the old id is still listed')
    assert done['projects/gone_old'].startswith('skipped: the new id is not on the Portal')


def test_a_replacement_keeps_its_retired_page(app, clean, test_client):
    # replaced_by alone (a dataset superseded, ARK left on the old id) still
    # shows the 410 "removed, replaced by" page: only a rename redirects.
    clean.add(ArkId(ark_id=f'ark:/{_naan(app)}/d7replacedtest1', dataset_id='projects/v1'))
    clean.add(Dataset(dataset_id='projects/v2', name='Version 2', fspath='/n'))
    clean.add(RetiredDataset(dataset_id='projects/v1', name='Version 1', retired_on=datetime(2026, 11, 1),
                             reason='Superseded.', replaced_by='projects/v2'))
    clean.commit()
    assert test_client.get('/dataset?id=projects/v1').status_code == 410


def test_command_reads_the_map_file_and_the_shipped_map_is_sound(app, clean, tmp_path):
    import json
    import os
    _renamed(app, clean)
    path = tmp_path / 'renames.json'
    path.write_text(json.dumps({OLD: NEW}))
    if 'rename_datasets' not in app.cli.commands:
        cli.register(app)    # done by the app's entry script, not create_app
    result = app.test_cli_runner().invoke(args=['rename_datasets', str(path)])
    assert result.exit_code == 0 and 'Dry run' in result.output
    shipped = os.path.join(os.path.dirname(__file__), '..', '..', 'deploy', 'dataset-renames-2026-11-06.json')
    pairs = json.load(open(shipped))
    assert len(pairs) == 32 and all(k.startswith('projects/') and v.startswith('projects/') for k, v in pairs.items())
    assert len(set(pairs.values())) == len(pairs)          # no two old ids onto one new id


def test_added_date_comes_from_the_old_folder(app, clean, tmp_path, monkeypatch):
    import os
    import subprocess
    repo = tmp_path / 'conp-dataset'
    (repo / 'projects').mkdir(parents=True)

    def commit(path, when):
        (repo / path).write_text(when)
        env = dict(os.environ, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when,
                   GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t')
        subprocess.run(['git', 'add', path], cwd=repo, check=True, env=env)
        subprocess.run(['git', 'commit', '-q', '-m', path], cwd=repo, check=True, env=env)
    subprocess.run(['git', 'init', '-q'], cwd=repo, check=True)
    commit(OLD, '2021-03-04T12:00:00')
    commit(NEW, '2026-11-05T12:00:00')
    monkeypatch.setitem(app.config, 'DATA_PATH', str(tmp_path))
    _renamed(app, clean)
    row = Dataset.query.filter_by(dataset_id=NEW).first()
    row.date_added_to_portal = datetime(2026, 11, 5, 12)
    clean.commit()

    done = cli._rename_datasets(app, {OLD: NEW})                          # dry run reports it
    assert done[OLD].endswith('added 2026-11-05 -> 2021-03-04')
    assert Dataset.query.filter_by(dataset_id=NEW).first().date_added_to_portal.year == 2026
    cli._rename_datasets(app, {OLD: NEW}, apply_changes=True)
    assert Dataset.query.filter_by(dataset_id=NEW).first().date_added_to_portal.date().isoformat() == '2021-03-04'
    # Re-running after the first --apply still fixes the date (and only the date).
    assert cli._rename_datasets(app, {OLD: NEW}, apply_changes=True)[OLD] == '0 ARK(s), 0 day(s) of views'
