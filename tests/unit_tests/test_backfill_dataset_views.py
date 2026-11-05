"""Dataset page views a dataset missed (it was off the Portal on the days
update_analytics processed) are fetched again from Matomo, once per dataset
for the whole period, and only the missing (dataset, day) rows are added."""
import datetime as dt

import pytest

from app import cli
from app.models import Dataset, MatomoDailyGetDatasetPageViewsSummary as V


def _row(hits):
    return [{'url': 'u', 'label': 'l', 'nb_hits': hits, 'nb_visits': hits, 'nb_uniq_visitors': 1,
             'sum_time_spent': 10, 'avg_time_on_page': 5.0}]


def _views(session, dataset_id):
    return {r.date: r.nb_hits for r in session.query(V).filter(V.dataset_id == dataset_id)}


@pytest.fixture
def clean(session):
    """This suite's rollback does not undo commits: remove what the test added."""
    yield session
    session.query(V).filter(V.dataset_id.like('projects/bf-%')).delete(synchronize_session=False)
    session.query(Dataset).filter(Dataset.dataset_id.like('projects/bf-%')).delete(synchronize_session=False)
    session.commit()


def test_backfill_adds_only_missing_days(clean):
    session = clean
    session.merge(Dataset(dataset_id='projects/bf-htt', name='5HTT', fspath='/x',
                          date_added_to_portal=dt.datetime(2026, 5, 12)))
    session.add(V(date='2026-10-01', dataset_id='projects/bf-htt', url='u', label='l', nb_hits=7, nb_visits=7))
    session.commit()
    asked = []

    def get(url):
        asked.append(url)
        return {'2026-10-01': _row(99),     # already in the table: kept as is
                '2026-10-02': _row(2),      # missed: added
                '2026-10-03': []}           # no views that day: nothing added

    n = cli._backfill_dataset_views(None, 'https://m/?module=API', dataset_ids=['projects/bf-htt'],
                                    since='2026-10-01', get=get)
    assert n == 1
    assert _views(session, 'projects/bf-htt') == {'2026-10-01': 7, '2026-10-02': 2}
    assert len(asked) == 1 and 'period=day&date=2026-10-01,' in asked[0]
    assert 'pageUrl=https://portal.conp.ca/dataset?id=projects/bf-htt' in asked[0]

    # Running it again adds nothing twice.
    assert cli._backfill_dataset_views(None, 'https://m/?module=API', dataset_ids=['projects/bf-htt'],
                                       since='2026-10-01', get=get) == 0


def test_backfill_starts_at_date_added_and_survives_errors(clean):
    session = clean
    session.merge(Dataset(dataset_id='projects/bf-new', name='New', fspath='/x',
                          date_added_to_portal=dt.datetime(2026, 9, 2)))
    session.merge(Dataset(dataset_id='projects/bf-bad', name='Bad', fspath='/x',
                          date_added_to_portal=dt.datetime(2019, 1, 1)))
    session.commit()
    asked = []

    def get(url):
        asked.append(url)
        if 'projects/bf-bad' in url:
            raise ValueError('timeout')
        return {'2026-09-02': _row(1)}

    n = cli._backfill_dataset_views(None, 'https://m/?module=API', dataset_ids=['projects/bf-new', 'projects/bf-bad'], get=get)
    assert n == 1
    assert any('date=2026-09-02,' in u for u in asked)
    assert any('bf-bad' in u and 'date=2020-05-01,' in u for u in asked)   # never before the Portal's start
