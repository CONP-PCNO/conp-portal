from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.models import eastern


def test_eastern_timezone_uses_zoneinfo_and_daylight_saving():
    assert isinstance(eastern, ZoneInfo)
    assert datetime(2026, 1, 1, tzinfo=eastern).utcoffset() == timedelta(hours=-5)
    assert datetime(2026, 7, 1, tzinfo=eastern).utcoffset() == timedelta(hours=-4)
