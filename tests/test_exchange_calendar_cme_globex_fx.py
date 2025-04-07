import pandas as pd
import pytest
from zoneinfo import ZoneInfo
from pandas.tseries.offsets import Day, Hour, Minute

from pandas_market_calendars.calendars.cme_globex_fx import CMEGlobexFXExchangeCalendar

TZ = "America/Chicago"


def test_time_zone():
    assert CMEGlobexFXExchangeCalendar().tz == ZoneInfo(TZ)
    assert CMEGlobexFXExchangeCalendar().name == "CMEGlobex_FX"


def test_sunday_opens():
    cme = CMEGlobexFXExchangeCalendar()
    schedule = cme.schedule("2020-01-01", "2020-01-31")
    assert (
        pd.Timestamp("2020-01-12 17:00:00", tz=TZ)
        == schedule.loc["2020-01-13", "market_open"]
    )


@pytest.mark.parametrize(
    "day_status",
    [
        # 2020
        # 2020 Martin Luther King Day (20th = Monday)
        ("2020-01-17", "open"),
        ("2020-01-20", "1200"),
        ("2020-01-21", "open"),
        # 2020 Presidents Day (17th = Monday)
        ("2020-02-14", "open"),
        ("2020-02-17", "1200"),
        ("2020-02-18", "open"),
        # 2020 Good Friday (10th = Friday)
        ("2020-04-09", "open"),
        ("2020-04-10", "closed"),
        ("2020-04-13", "open"),
        # 2020 Memorial Day (May 25 = Monday)
        ("2020-05-22", "open"),
        ("2020-05-25", "1200"),
        ("2020-05-26", "open"),
        # 2020 Independence Day (4th = Saturday)
        ("2020-07-02", "open"),
        ("2020-07-03", "1200"),
        ("2020-07-06", "open"),
        # 2020 Labor Day (4th = Monday)
        ("2020-09-04", "open"),
        ("2020-09-07", "1200"),
        ("2020-09-08", "open"),
        # 2020 Thanksgiving (26th = Thursday)
        ("2020-11-25", "open"),
        ("2020-11-26", "1200"),
        ("2020-11-27", "1215"),
        ("2020-11-30", "open"),
        # 2020 Christmas (25th = Friday)
        ("2020-12-24", "1215"),
        ("2020-12-25", "closed"),
        ("2020-12-28", "open"),
        ("2020-12-29", "open"),
        # 2020/21 New Year's (Dec 31 = Thur)
        ("2020-12-31", "open"),
        ("2021-01-01", "closed"),
        ("2022-01-04", "open"),
        # 2021
        # 2021 Martin Luther King Day (18th = Monday)
        ("2021-01-15", "open"),
        ("2021-01-18", "1200"),
        ("2021-01-19", "open"),
        # 2021 Presidents Day (15th = Monday)
        ("2021-02-12", "open"),
        ("2021-02-15", "1200"),
        ("2021-02-16", "open"),
        # 2021 Good Friday (2nd = Friday)
        ("2021-04-01", "open"),
        ("2021-04-02", "1015"),
        ("2021-04-05", "open"),
        # 2021 Memorial Day (May 31 = Monday)
        ("2021-05-28", "open"),
        ("2021-05-31", "1200"),
        ("2021-06-01", "open"),
        # 2021 Independence Day (4th = Sunday)
        ("2021-07-02", "open"),
        ("2021-07-05", "1200"),
        ("2021-07-06", "open"),
        # 2021 Labor Day (6th = Monday)
        ("2021-09-03", "open"),
        ("2021-09-06", "1200"),
        ("2021-09-07", "open"),
        # 2021 Thanksgiving (25th = Thursday)
        ("2021-11-24", "open"),
        ("2021-11-25", "1200"),
        ("2021-11-26", "1215"),
        # 2021 Christmas (25th = Saturday)
        ("2021-12-23", "open"),
        ("2021-12-24", "closed"),
        ("2021-12-27", "open"),
        # 2021/22 New Year's (Dec 31 = Friday) (unusually this period was fully open)
        ("2021-12-31", "open"),
        ("2022-01-03", "open"),
        ("2022-01-03", "open"),
        # 2022
        # 2022 Martin Luther King Day (17th = Monday)
        ("2022-01-14", "open"),
        ("2022-01-17", "open"),
        ("2022-01-18", "open"),
        # 2022 President's Day (21st = Monday)
        ("2022-02-18", "open"),
        ("2022-02-21", "open"),
        ("2022-02-22", "open"),
        # 2022 Good Friday (15 = Friday)
        ("2022-04-14", "open"),
        ("2022-04-15", "closed"),
        ("2022-04-18", "open"),
        # 2022 Memorial Day	 (30th = Monday)
        ("2022-05-27", "open"),
        ("2022-05-30", "open"),
        ("2022-05-31", "open"),
        # 2022 Juneteenth (20th = Monday)
        ("2022-06-17", "open"),
        ("2022-06-20", "open"),
        ("2022-06-21", "open"),
        # 2022 Independence Day (4th = Monday)
        ("2022-07-01", "open"),
        ("2022-07-04", "open"),
        ("2022-07-05", "open"),
        # 2022 Labor Day (5th = Monday)
        ("2022-09-02", "open"),
        ("2022-09-05", "open"),
        ("2022-09-06", "open"),
        # 2022 Thanksgiving (24th = Thursday)
        ("2022-11-23", "open"),
        ("2022-11-24", "open"),
        ("2022-11-25", "1215"),
        ("2022-11-28", "open"),
        # 2022 Christmas (25 = Sunday)
        ("2022-12-23", "open"),
        ("2022-12-26", "closed"),
        ("2022-12-27", "open"),
        # 2022/23 New Years (Jan 1 = Sunday)
        ("2022-12-30", "open"),
        ("2023-01-02", "closed"),
        ("2023-01-03", "open"),
        ("2023-04-07", "1015"),
    ],
    ids=lambda x: f"{x[0]} {x[1]}",
)
def test_2020_through_2022_and_prior_holidays(day_status):
    day_str = day_status[0]
    day_ts = pd.Timestamp(day_str, tz=TZ)
    expected_status = day_status[1]

    under_test = CMEGlobexFXExchangeCalendar()
    schedule = under_test.schedule("2020-01-01", "2023-04-28", tz=TZ)

    if expected_status == "open":
        s = schedule.loc[day_str]
        assert s["market_open"] == day_ts + Day(-1) + Hour(17) + Minute(0)
        assert s["market_close"] == day_ts + Day(0) + Hour(16) + Minute(0)
    elif expected_status == "closed":
        assert day_ts.tz_localize(None) not in schedule.index
    else:
        s = schedule.loc[day_str]
        hour = int(expected_status[0:2])
        minute = int(expected_status[2:4])
        assert s["market_open"] == day_ts + Day(-1) + Hour(17)
        assert s["market_close"] == day_ts + Day(0) + Hour(hour) + Minute(minute)
