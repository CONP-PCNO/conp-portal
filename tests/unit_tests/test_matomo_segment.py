"""update_analytics sends one Matomo segment with every query (by default it
leaves out headless browsers and the fake-Chrome crawler), and --refetch-since backs up the
tables, then deletes the Matomo rows from a day on so they are fetched again."""
import pytest

from app import cli
from app.models import MatomoDailyVisitsSummary as V
from config import Config


def _base(app, segment):
    app.config.update(MATOMO_SERVER_URL='m.example.org', MATOMO_SITE_ID='2', MATOMO_TOKEN_AUTH='t',
                      MATOMO_SEGMENT=segment)
    return cli._matomo_api_baseurl(app)


def test_default_segment_leaves_out_automated_visits():
    assert Config.MATOMO_SEGMENT == 'browserName!=Headless Chrome;resolution!=1800x1125,operatingSystemCode!=WIN'


def test_segment_is_url_encoded_in_every_query(app):
    url = _base(app, 'browserName!=Headless Chrome;resolution!=1800x1125,operatingSystemCode!=WIN')
    assert url.endswith('&segment=browserName%21%3DHeadless%20Chrome%3Bresolution%21%3D1800x1125%2CoperatingSystemCode%21%3DWIN')


@pytest.mark.parametrize('segment', ['', '  ', None])
def test_empty_segment_counts_every_visit(app, segment):
    assert '&segment=' not in _base(app, segment)


@pytest.fixture
def clean(session):
    yield session
    session.query(V).filter(V.date.like('2099-%')).delete(synchronize_session=False)
    session.commit()


def test_refetch_since_backs_up_then_deletes_only_later_days(app, clean, monkeypatch):
    session = clean
    for day in ('2099-01-31', '2099-02-01', '2099-02-02'):
        session.add(V(date=day, nb_visits=1))
    session.commit()
    order = []
    monkeypatch.setattr(cli, '_backup_analytics', lambda app: order.append('backup') or 'backed up')

    message = cli._refetch_matomo_since(app, '2099-02-01')

    assert order == ['backup']
    assert sorted(r.date for r in session.query(V).filter(V.date.like('2099-%'))) == ['2099-01-31']
    assert 'from 2099-02-01 on deleted' in message


def test_refetch_since_refuses_a_bad_date(app):
    with pytest.raises(ValueError):
        cli._refetch_matomo_since(app, '1 Oct')
