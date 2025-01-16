import datetime as dt

import pandas as pd
import pytest
from pandas.tseries.offsets import Day, Hour, Minute

from pandas_market_calendars.calendars.cme_globex_crypto import (
    CMEGlobexCryptoExchangeCalendar,
)

TZ = "America/Chicago"


def test_is_different():
    cal = CMEGlobexCryptoExchangeCalendar()
    sched = cal.schedule("2020-01-15", "2020-02-01")

    early = cal.early_closes(sched).index
    assert early.shape == (1,) and early[0] == pd.Timestamp("2020-01-20")

    late = cal.late_opens(sched).index
    assert late.empty

    sched.loc["2020-01-20", "market_open"] += pd.Timedelta("3h")
    late = cal.late_opens(sched).index
    assert late.shape == (1,) and late[0] == pd.Timestamp("2020-01-20")

    cal.change_time(
        "market_open", ((None, dt.time(17), -1), ("2020-01-25", dt.time(9)))
    )

    different = cal.is_different(sched.market_open)
    different = different[different].index
    assert (
        different.shape == (6,)
        and (
            different
            == pd.DatetimeIndex(
                [
                    "2020-01-20",
                    "2020-01-27",
                    "2020-01-28",
                    "2020-01-29",
                    "2020-01-30",
                    "2020-01-31",
                ],
                dtype="datetime64[ns]",
                freq=None,
            )
        ).all()
    )


@pytest.mark.parametrize(
    "day_status",
    [
        # 2017
        # 2017 Christmas (25th = Monday)
        ("2017-12-22", "open"),
        ("2017-12-25", "closed"),
        ("2017-12-26", "open"),
        # 2017/18 New Year's (Dec 31 = Sunday)
        ("2017-12-29", "open"),
        ("2018-01-01", "closed"),
        ("2018-01-02", "open"),
        # 2018
        # 2018 Martin Luther King Day (15th = Monday)
        ("2018-01-12", "open"),
        ("2018-01-15", "1200"),
        ("2018-01-16", "open"),
        # 2018 Presidents Day (19th = Monday)
        ("2018-02-16", "open"),
        ("2018-02-19", "1200"),
        ("2018-02-20", "open"),
        # 2018 Good Friday (3/30th = Friday)
        ("2018-03-29", "open"),
        ("2018-03-30", "closed"),
        ("2018-04-02", "open"),
        # 2018 Memorial Day (May 28 = Monday)
        ("2018-05-25", "open"),
        ("2018-05-28", "1200"),
        ("2018-05-29", "open"),
        # 2018 Independence Day (4th = Wednesday)
        ("2018-07-02", "open"),
        ("2018-07-03", "1215"),
        ("2018-07-04", "1200"),
        ("2018-07-05", "open"),
        # 2018 Labor Day (3rd = Monday)
        ("2018-08-31", "open"),
        ("2018-09-03", "1200"),
        ("2018-09-04", "open"),
        # 2018 Thanksgiving (22nd = Thursday)
        ("2018-11-21", "open"),
        ("2018-11-22", "1200"),
        ("2018-11-23", "1215"),
        ("2018-11-26", "open"),
        # 2018 Christmas (25th = Friday)
        ("2018-12-21", "open"),
        ("2018-12-24", "1215"),
        ("2018-12-25", "closed"),
        ("2018-12-26", "open"),
        # 2018/19 New Year's (Dec 31 = Thur)
        ("2018-12-31", "open"),
        ("2019-01-01", "closed"),
        ("2019-01-02", "open"),
        # 2019
        # 2019 Martin Luther King Day (21st = Monday)
        ("2019-01-18", "open"),
        ("2019-01-21", "1200"),
        ("2019-01-22", "open"),
        # 2019 Presidents Day (18th = Monday)
        ("2019-02-15", "open"),
        ("2019-02-18", "1200"),
        ("2019-02-19", "open"),
        # 2019 Good Friday (19th = Friday)
        ("2019-04-18", "open"),
        ("2019-04-19", "closed"),
        ("2019-04-22", "open"),
        # 2019 Memorial Day (May 27 = Monday)
        ("2019-05-24", "open"),
        ("2019-05-27", "1200"),
        ("2019-05-28", "open"),
        # 2019 Independence Day (4th = Thursday)
        ("2019-07-02", "open"),
        ("2019-07-03", "1215"),
        ("2019-07-04", "1200"),
        ("2019-07-05", "open"),
        # 2019 Labor Day (2nd = Monday)
        ("2019-08-30", "open"),
        ("2019-09-02", "1200"),
        ("2019-09-03", "open"),
        # 2019 Thanksgiving (28 = Thursday)
        ("2019-11-27", "open"),
        ("2019-11-28", "1200"),
        ("2019-11-29", "1215"),
        ("2019-12-02", "open"),
        # 2019 Christmas (25th = Wednesday)
        ("2019-12-23", "open"),
        ("2019-12-24", "1215"),
        ("2019-12-25", "closed"),
        ("2019-12-26", "open"),
        # 2019/20 New Year's (Dec 31 = Thur)
        ("2019-12-31", "open"),
        ("2020-01-01", "closed"),
        ("2020-01-02", "open"),
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
        ("2020-12-23", "open"),
        ("2020-12-24", "1215"),
        ("2020-12-25", "closed"),
        ("2020-12-28", "open"),
        # 2020/21 New Year's (Dec 31 = Thur)
        ("2020-12-31", "open"),
        ("2021-01-01", "closed"),
        ("2021-01-04", "open"),
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
        ("2021-04-02", "0815"),
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
        ("2021-11-26", "1245"),
        # 2021 Christmas (25th = Saturday)
        ("2021-12-23", "open"),
        ("2021-12-24", "closed"),
        ("2021-12-27", "open"),
        # 2021/22 New Year's (Dec 31 = Friday)
        ("2021-12-31", "open"),
        ("2022-01-03", "open"),
        ("2022-01-03", "open"),
        # 2022
        # 2022 Martin Luther King Day (17th = Monday)
        ("2022-01-14", "open"),
        ("2022-01-17", "1600"),
        ("2022-01-18", "open"),
        # 2022 President's Day (21st = Monday)
        ("2022-02-18", "open"),
        ("2022-02-21", "1600"),
        ("2022-02-22", "open"),
        # 2022 Good Friday (15 = Friday)
        ("2022-04-14", "open"),
        ("2022-04-15", "closed"),
        ("2022-04-18", "open"),
        # 2022 Memorial Day	 (30th = Monday)
        ("2022-05-27", "open"),
        ("2022-05-30", "1600"),
        ("2022-05-31", "open"),
        # 2022 Juneteenth (20th = Monday)
        ("2022-06-17", "open"),
        ("2022-06-20", "1600"),
        ("2022-06-21", "open"),
        # 2022 Independence Day (4th = Monday)
        ("2022-07-01", "open"),
        ("2022-07-04", "1600"),
        ("2022-07-05", "open"),
        # 2022 Labor Day (5th = Monday)
        ("2022-09-02", "open"),
        ("2022-09-05", "1600"),
        ("2022-09-06", "open"),
        # 2022 Thanksgiving (24th = Thursday)
        ("2022-11-23", "open"),
        ("2022-11-24", "1600"),
        ("2022-11-25", "1245"),
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

    year = int(day_str.split("-")[0])
    under_test = CMEGlobexCryptoExchangeCalendar()
    schedule = under_test.schedule(f"{year}-01-01", f"{year + 1}-01-01", tz=TZ)

    if expected_status == "open":
        s = schedule.loc[day_str]
        assert s["market_open"] == day_ts + Day(-1) + Hour(17) + Minute(0)
        assert s["market_close"] == day_ts + Day(0) + Hour(16) + Minute(0)
    elif expected_status == "closed":
        assert day_ts.tz_localize(None) not in schedule.index
    else:  # expected_status contains a special close time like 1215
        s = schedule.loc[day_str]
        hour = int(expected_status[0:2])
        minute = int(expected_status[2:4])
        assert s["market_open"] == day_ts + Day(-1) + Hour(17)
        assert s["market_close"] == day_ts + Day(0) + Hour(hour) + Minute(minute)
