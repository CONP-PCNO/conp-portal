"""update_analytics runs every step even when one fails (1 Nov 2026: a site
search containing "→" stopped the run before downloads, GitHub traffic,
countries and the page rebuild), and exits with status 1 when any failed."""
import pytest

from app import cli


def test_a_failing_step_does_not_stop_the_others(app, monkeypatch, capsys):
    ran = []
    names = ['_update_analytics_matomo_visits_summary', '_update_analytics_matomo_get_page_urls_summary',
             '_update_analytics_matomo_get_daily_dataset_views_summary', '_backfill_dataset_views',
             '_update_analytics_matomo_get_daily_portal_download_summary', '_update_analytics_matomo_countries']
    for name in names:
        monkeypatch.setattr(cli, name, lambda *a, _n=name, **k: ran.append(_n))
    monkeypatch.setattr(cli, '_update_github_traffic_counts', lambda *a, **k: ran.append('github'))

    def refuses(*a, **k):
        raise ValueError("(1366, \"Incorrect string value: '\\\\xE2\\\\x86\\\\x92 Re...'\")")
    monkeypatch.setattr(cli, '_update_analytics_matomo_get_daily_keyword_searches_summary', refuses)
    import app.analytics.page as page
    monkeypatch.setattr(page, 'rebuild', lambda period: ran.append('rebuild ' + period))
    app.config.update(MATOMO_SERVER_URL='m', MATOMO_SITE_ID='1', MATOMO_TOKEN_AUTH='t')

    with pytest.raises(SystemExit) as stop:
        cli._update_analytics(app)
    assert stop.value.code == 1
    assert set(names) <= set(ran) and 'github' in ran
    assert 'rebuild all' in ran and 'rebuild 12m' in ran
    out = capsys.readouterr().out
    assert 'Analytics step "site searches" failed' in out and '1 step(s) failed: site searches' in out


def test_no_error_exit_when_every_step_works(app, monkeypatch):
    for name in dir(cli):
        if name.startswith('_update_analytics_matomo_') or name in ('_backfill_dataset_views', '_update_github_traffic_counts'):
            monkeypatch.setattr(cli, name, lambda *a, **k: None)
    import app.analytics.page as page
    monkeypatch.setattr(page, 'rebuild', lambda period: None)
    app.config.update(MATOMO_SERVER_URL='m', MATOMO_SITE_ID='1', MATOMO_TOKEN_AUTH='t')
    cli._update_analytics(app)        # no SystemExit
