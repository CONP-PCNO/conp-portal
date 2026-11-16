"""`flask backup_analytics`: a dated copy of the use history (tables as CSV,
research use without its request cache, countries), old daily copies pruned
except the first of each month."""
import csv
import datetime as dt
import gzip
import os

from app.cli import _backup_analytics
from app.models import GithubDailyClonesCount


def _data(tmp_path):
    data = tmp_path / 'data'
    (data / 'research_use' / 'cache').mkdir(parents=True)
    (data / 'research_use' / 'cache' / 'x.json').write_text('{}')
    (data / 'research_use' / 'latest.json').write_text('{"totals": {}}')
    (data / 'research_use' / 'CHANGES.md').write_text('# changes\n')
    (data / 'analytics').mkdir()
    (data / 'analytics' / 'countries.json').write_text('{"rows": []}')
    return data


def test_backup_writes_tables_and_files(app, session, tmp_path):
    session.add(GithubDailyClonesCount(repo='conp-bot/x', date='2026-10-29', timestamp='t', count=5, unique_count=2))
    session.commit()
    old = app.config['DATA_PATH']
    app.config['DATA_PATH'] = str(_data(tmp_path))
    try:
        msg = _backup_analytics(app, str(tmp_path / 'bk'), today=dt.date(2026, 10, 30))
    finally:
        app.config['DATA_PATH'] = old
    out = tmp_path / 'bk' / '2026-10-30'
    with gzip.open(out / 'github_daily_clones_count.csv.gz', 'rt') as f:
        rows = list(csv.reader(f))
    assert rows[0][:3] == ['id', 'repo', 'date'] and rows[1][1:3] == ['conp-bot/x', '2026-10-29']
    assert (out / 'research_use' / 'latest.json').exists() and (out / 'research_use' / 'CHANGES.md').exists()
    assert not (out / 'research_use' / 'cache').exists()
    assert (out / 'countries.json').exists()
    assert 'research use, countries' in msg and 'set ANALYTICS_BACKUP_PATH' not in msg


def test_default_location_warns_and_old_copies_are_pruned(app, session, tmp_path):
    old = app.config['DATA_PATH']
    data = _data(tmp_path)
    app.config['DATA_PATH'] = str(data)
    dest = data / 'analytics' / 'backups'
    for d in ('2026-08-01', '2026-08-02', '2026-09-03', '2026-09-04', '2026-10-28', '2026-10-29'):
        (dest / d).mkdir(parents=True)
    try:
        msg = _backup_analytics(app, None, keep=2, today=dt.date(2026, 10, 30))
    finally:
        app.config['DATA_PATH'] = old
    assert 'set ANALYTICS_BACKUP_PATH' in msg
    # newest 2 kept, plus the first copy of each month
    assert sorted(os.listdir(dest)) == ['2026-08-01', '2026-09-03', '2026-10-28', '2026-10-29', '2026-10-30']
