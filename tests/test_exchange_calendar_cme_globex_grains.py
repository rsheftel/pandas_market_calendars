import pandas as pd
from zoneinfo import ZoneInfo
from pandas.testing import assert_index_equal

from pandas_market_calendars.calendars.cme_globex_agriculture import (
    CMEGlobexGrainsAndOilseedsExchangeCalendar,
)

cal = CMEGlobexGrainsAndOilseedsExchangeCalendar()


def test_time_zone():
    assert cal.tz == ZoneInfo("America/Chicago")
    assert cal.name == "CMEGlobex_GrainsAndOilseeds"


def test_x():
    schedule = cal.schedule("2023-01-01", "2023-01-10", tz="America/New_York")

    good_dates = cal.valid_days("2023-01-01", "2023-12-31")

    assert all(
        d not in good_dates
        for d in {"2023-01-01", "2023-12-24", "2023-12-25", "2023-12-30", "2023-12-31"}
    )

    assert all(d in good_dates for d in {"2023-01-03", "2023-01-05", "2023-12-26", "2023-12-27", "2023-12-28"})
