import pandas as pd
import pytest
from pandas.tseries.offsets import Day, Hour, Minute

from pandas_market_calendars.calendars.cme_globex_fixed_income import (
    CMEGlobexFixedIncomeCalendar,
)

TZ = "America/Chicago"


@pytest.mark.parametrize(
    "day_status",
    [
        # 2009
        # 2009 Martin Luther King Day (19th = Monday)
        ("2009-01-16", "1515"),
        ("2009-01-19", "1200"),
        ("2009-01-20", "open"),
        # # 2009 Presidents Day (16th = Monday)
        ("2009-02-13", "1515"),
        ("2009-02-16", "1200"),
        ("2009-02-17", "open"),
        # 2009 Good Friday (10th = Friday)
        ("2009-04-09", "1515"),
        ("2009-04-10", "closed"),
        ("2009-04-13", "open"),
        # 2009 Memorial Day (May 25 = Monday)
        ("2009-05-22", "1515"),
        ("2009-05-25", "1200"),
        ("2009-05-26", "open"),
        # 2009 Independence Day (4th = Saturday)
        ("2009-07-02", "open"),
        ("2009-07-03", "1200"),
        ("2009-07-06", "open"),
        # 2009 Labor Day (7th = Monday)
        ("2009-09-04", "1515"),
        ("2009-09-07", "1200"),
        ("2009-09-08", "open"),
        # 2009 Thanksgiving (26th = Thursday)
        ("2009-11-25", "open"),
        ("2009-11-26", "1200"),
        ("2009-11-27", "1215"),
        ("2009-11-30", "open"),
        # 2009 Christmas (25th = Friday)
        ("2009-12-24", "1215"),
        ("2009-12-25", "closed"),
        ("2009-12-28", "open"),
        ("2009-12-29", "open"),
        # 2009/10 New Year's (Dec 31 = Thur)
        ("2009-12-31", "open"),
        ("2010-01-01", "closed"),
        ("2010-01-04", "open"),
        # 2010
        # 2010 Martin Luther King Day (18th = Monday)
        ("2010-01-15", "1515"),
        ("2010-01-18", "1200"),
        ("2010-01-19", "open"),
        # # 2010 Presidents Day (15th = Monday)
        ("2010-02-12", "1515"),
        ("2010-02-15", "1200"),
        ("2010-02-16", "open"),
        # 2010 Good Friday (2nd = Friday)
        ("2010-04-01", "open"),
        ("2010-04-02", "1015"),
        ("2010-04-05", "open"),
        # 2010 Memorial Day (May 31 = Monday)
        ("2010-05-28", "1515"),
        ("2010-05-31", "1200"),
        ("2010-06-01", "open"),
        # 2010 Independence Day (4th = Sunday)
        ("2010-07-02", "1515"),
        ("2010-07-05", "1200"),
        ("2010-07-06", "open"),
        # 2010 Labor Day (6th = Monday)
        ("2010-09-03", "1515"),
        ("2010-09-06", "1200"),
        ("2010-09-07", "open"),
        # 2010 Thanksgiving (25th = Thursday)
        ("2010-11-24", "open"),
        ("2010-11-25", "1200"),
        ("2010-11-26", "1215"),
        ("2010-11-29", "open"),
        # 2010 Christmas (25th = Saturday)
        ("2010-12-23", "open"),
        ("2010-12-24", "closed"),
        ("2010-12-27", "open"),
        # 2010/11 New Year's (Dec 31 = Fri)
        ("2010-12-30", "open"),
        ("2010-12-31", "1215"),
        ("2011-01-03", "open"),
        # 2011
        # 2011 Martin Luther King Day (17th = Monday)
        ("2011-01-14", "1515"),
        ("2011-01-17", "1200"),
        ("2011-01-18", "open"),
        # 2011 Presidents Day (21st = Monday)
        ("2011-02-18", "1515"),
        ("2011-02-21", "1200"),
        ("2011-02-22", "open"),
        # 2011 Good Friday (22th = Friday)
        ("2011-04-21", "open"),
        ("2011-04-22", "closed"),
        ("2011-04-25", "open"),
        # 2011 Memorial Day (May 30 = Monday)
        ("2011-05-27", "1515"),
        ("2011-05-30", "1200"),
        ("2011-05-31", "open"),
        # 2011 Independence Day (4th = Monday)
        ("2011-07-01", "1515"),
        ("2011-07-04", "1200"),
        ("2011-07-05", "open"),
        # 2011 Labor Day (5th = Monday)
        ("2011-09-02", "1515"),
        ("2011-09-05", "1200"),
        ("2011-09-06", "open"),
        # 2011 Thanksgiving (24th = Thursday)
        ("2011-11-23", "open"),
        ("2011-11-24", "1200"),
        ("2011-11-25", "1215"),
        ("2011-11-28", "open"),
        # 2011 Christmas (25th = Sunday)
        ("2011-12-23", "open"),
        ("2011-12-26", "closed"),
        ("2011-12-27", "open"),  ## 5am special open on 27th
        # 2011/12 New Year's (Dec 31 = Saturday)
        ("2011-12-30", "open"),
        ("2012-01-02", "closed"),
        ("2012-01-03", "open"),  ## 5am open on 3rd
        # 2012
        # 2012 Martin Luther King Day (16th = Monday)
        ("2012-01-13", "1515"),
        ("2012-01-16", "1200"),
        ("2012-01-17", "open"),
        # 2012 Presidents Day (20th = Monday)
        ("2012-02-17", "1515"),
        ("2012-02-20", "1200"),
        ("2012-02-21", "open"),
        # 2012 Good Friday (06th = Friday)
        ("2012-04-05", "open"),
        ("2012-04-06", "1015"),
        ("2012-04-09", "open"),
        # 2012 Memorial Day (May 28 = Monday)
        ("2012-05-25", "1515"),
        ("2012-05-28", "1200"),
        ("2012-05-29", "open"),
        # 2012 Independence Day (4th = Wednesday)
        ("2012-07-02", "open"),
        ("2012-07-03", "open"),
        ("2012-07-04", "1200"),
        ("2012-07-05", "open"),
        # 2012 Labor Day (3rd = Monday)
        ("2012-08-31", "1515"),
        ("2012-09-03", "1200"),
        ("2012-09-04", "open"),
        # 2012 Thanksgiving (22 = Thursday)
        ("2012-11-21", "open"),
        ("2012-11-22", "1200"),
        ("2012-11-23", "1215"),
        ("2012-11-26", "open"),
        # 2012 Christmas (25th = Friday)
        ("2012-12-24", "1215"),
        ("2012-12-25", "closed"),
        ("2012-12-26", "open"),  ## 5am on 26th
        # 2012/13 New Year's (Dec 31 = Monday)
        ("2012-12-31", "open"),
        ("2013-01-01", "closed"),
        ("2013-01-02", "open"),  ## 5am on 2nd
        # 2013
        # 2013 Martin Luther King Day (21st = Monday)
        ("2013-01-18", "1515"),
        ("2013-01-21", "1200"),
        ("2013-01-22", "open"),
        # 2013 Presidents Day (18th = Monday)
        ("2013-02-15", "1515"),
        ("2013-02-18", "1200"),
        ("2013-02-19", "open"),
        # 2013 Good Friday (3/29 = Friday)
        ("2013-03-28", "open"),
        ("2013-03-29", "closed"),
        ("2013-04-01", "open"),
        # 2013 Memorial Day (May 27 = Monday)
        ("2013-05-24", "1515"),
        ("2013-05-27", "1200"),
        ("2013-05-28", "open"),
        # 2013 Independence Day (4th = Thursday)
        ("2013-07-03", "open"),
        ("2013-07-04", "1200"),
        ("2013-07-05", "open"),
        # 2013 Labor Day (2nd = Monday)
        ("2013-08-30", "1515"),
        ("2013-09-02", "1200"),
        ("2013-09-03", "open"),
        # 2013 Thanksgiving (28th = Thursday)
        ("2013-11-27", "open"),
        ("2013-11-28", "1200"),
        ("2013-11-29", "1215"),
        ("2013-04-02", "open"),
        # 2013 Christmas (25th = Wednesday)
        ("2013-12-24", "1215"),
        ("2013-12-25", "closed"),
        ("2013-12-26", "open"),  ### 5am 26th
        # 2013/14 New Year's (Dec 31 = Tue)
        ("2013-12-31", "open"),
        ("2014-01-01", "closed"),
        ("2014-01-02", "open"),  ### 5am 2nd
        # 2014
        # 2014 Martin Luther King Day (20th = Monday)
        ("2014-01-17", "1515"),
        ("2014-01-20", "1200"),
        ("2014-01-21", "open"),
        # 2014 Presidents Day (17th = Monday)
        ("2014-02-14", "1515"),
        ("2014-02-17", "1200"),
        ("2014-02-18", "open"),
        # 2014 Good Friday (18th = Friday)
        ("2014-04-17", "open"),
        ("2014-04-18", "closed"),
        ("2014-04-21", "open"),
        # 2014 Memorial Day (May 26 = Monday)
        ("2014-05-23", "1515"),
        ("2014-05-26", "1200"),
        ("2014-05-27", "open"),
        # 2014 Independence Day (4th = Friday)
        ("2014-07-02", "open"),
        ("2014-07-03", "open"),
        ("2014-07-04", "1200"),
        ("2014-07-07", "open"),
        # 2014 Labor Day (1st = Monday)
        ("2014-08-29", "1515"),
        ("2014-09-01", "1200"),
        ("2014-09-02", "open"),
        # 2014 Thanksgiving (27th = Thursday)
        ("2014-11-26", "open"),
        ("2014-11-27", "1200"),
        ("2014-11-28", "1215"),
        ("2014-12-01", "open"),
        # 2014 Christmas (25th = Thursday)
        ("2014-12-24", "1215"),
        ("2014-12-25", "closed"),
        ("2014-12-26", "open"),
        # 2014/15 New Year's (Dec 31 = Wednesday)
        ("2014-12-31", "open"),
        ("2015-01-01", "closed"),
        ("2015-01-02", "open"),
        # 2015
        # 2015 Martin Luther King Day (19th = Monday)
        ("2015-01-16", "1515"),
        ("2015-01-19", "1200"),
        ("2015-01-20", "open"),
        # 2015 Presidents Day (16th = Monday)
        ("2015-02-13", "1515"),
        ("2015-02-16", "1200"),
        ("2015-02-17", "open"),
        # 2015 Good Friday (03th = Friday)
        ("2015-04-02", "open"),
        ("2015-04-03", "1015"),
        ("2015-04-06", "open"),
        # 2015 Memorial Day (May 25 = Monday)
        ("2015-05-22", "1515"),
        ("2015-05-25", "1200"),
        ("2015-05-26", "open"),
        # 2015 Independence Day (4th = Saturday)
        ("2015-07-02", "open"),
        ("2015-07-03", "1200"),
        ("2015-07-06", "open"),
        # 2015 Labor Day (7th = Monday)
        ("2015-09-04", "open"),
        ("2015-09-07", "1200"),
        ("2015-09-08", "open"),
        # 2015 Thanksgiving (26th = Thursday)
        ("2015-11-25", "open"),
        ("2015-11-26", "1200"),
        ("2015-11-27", "1215"),
        ("2015-11-30", "open"),
        # 2015 Christmas (25th = Friday)
        ("2015-12-23", "open"),
        ("2015-12-24", "1215"),
        ("2015-12-25", "closed"),
        ("2015-12-28", "open"),
        # 2015/16 New Year's (Dec 31 = Thur)
        ("2015-12-31", "open"),
        ("2016-01-01", "closed"),
        ("2016-01-04", "open"),
        # 2016
        # 2016 Martin Luther King Day (18th = Monday)
        ("2016-01-15", "open"),
        ("2016-01-18", "1200"),
        ("2016-01-19", "open"),
        # 2016 Presidents Day (15th = Monday)
        ("2016-02-12", "open"),
        ("2016-02-15", "1200"),
        ("2016-02-16", "open"),
        # 2016 Good Friday (3/25th = Friday)
        ("2016-03-24", "open"),
        ("2016-03-25", "closed"),
        ("2016-03-28", "open"),
        # 2016 Memorial Day (May 30 = Monday)
        ("2016-05-27", "open"),
        ("2016-05-30", "1200"),
        ("2016-05-31", "open"),
        # 2016 Independence Day (4th = Monday)
        ("2016-07-01", "open"),
        ("2016-07-04", "1200"),
        ("2016-07-05", "open"),
        # 2016 Labor Day (5th = Monday)
        ("2016-09-02", "open"),
        ("2016-09-05", "1200"),
        ("2016-09-06", "open"),
        # 2016 Thanksgiving (24 = Thursday)
        ("2016-11-23", "open"),
        ("2016-11-24", "1200"),
        ("2016-11-25", "1215"),
        ("2016-11-28", "open"),
        # 2016 Christmas (25th = Sunday)
        ("2016-12-23", "open"),
        ("2016-12-26", "closed"),
        ("2016-12-27", "open"),
        # 2016/17 New Year's (Dec 31 = Saturday)
        ("2016-12-30", "open"),
        ("2017-01-02", "closed"),
        ("2017-01-03", "open"),
        # 2017
        # 2017 Martin Luther King Day (16th = Monday)
        ("2017-01-13", "open"),
        ("2017-01-16", "1200"),
        ("2017-01-17", "open"),
        # 2017 Presidents Day (20th = Monday)
        ("2017-02-17", "open"),
        ("2017-02-20", "1200"),
        ("2017-02-21", "open"),
        # 2017 Good Friday (14th = Friday)
        ("2017-04-13", "open"),
        ("2017-04-14", "closed"),
        ("2017-04-17", "open"),
        # 2017 Memorial Day (May 29 = Monday)
        ("2017-05-26", "open"),
        ("2017-05-29", "1200"),
        ("2017-05-30", "open"),
        # 2017 Independence Day (4th = Tuesday)
        ("2017-06-30", "open"),
        ("2017-07-03", "open"),
        ("2017-07-04", "1200"),
        ("2017-07-05", "open"),
        # 2017 Labor Day (4th = Monday)
        ("2017-09-01", "open"),
        ("2017-09-04", "1200"),
        ("2017-09-05", "open"),
        # 2017 Thanksgiving (23 = Thursday)
        ("2017-11-22", "open"),
        ("2017-11-23", "1200"),
        ("2017-11-24", "1215"),
        ("2017-11-27", "open"),
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
        ("2018-07-03", "open"),
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
        ("2019-07-03", "open"),
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
        # 2021/22 New Year's (Dec 31 = Friday)
        ("2021-12-31", "open"),
        ("2022-01-03", "open"),
        ("2022-01-04", "open"),
        # 2022
        # 2022 Martin Luther King Day (17th = Monday)
        ("2022-01-14", "open"),
        ("2022-01-17", "1200"),
        ("2022-01-18", "open"),
        # 2022 President's Day (21st = Monday)
        ("2022-02-18", "open"),
        ("2022-02-21", "1200"),
        ("2022-02-22", "open"),
        # 2022 Good Friday (15 = Friday)
        ("2022-04-14", "open"),
        ("2022-04-15", "closed"),
        ("2022-04-18", "open"),
        # 2022 Memorial Day	 (30th = Monday)
        ("2022-05-27", "open"),
        ("2022-05-30", "1200"),
        ("2022-05-31", "open"),
        # 2022 Juneteenth (20th = Monday)
        ("2022-06-17", "open"),
        ("2022-06-20", "1200"),
        ("2022-06-21", "open"),
        # 2022 Independence Day (4th = Monday)
        ("2022-07-01", "open"),
        ("2022-07-04", "1200"),
        ("2022-07-05", "open"),
        # 2022 Labor Day (5th = Monday)
        ("2022-09-02", "open"),
        ("2022-09-05", "1200"),
        ("2022-09-06", "open"),
        # 2022 Thanksgiving (24th = Thursday)
        ("2022-11-23", "open"),
        ("2022-11-24", "1200"),
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

    year = int(day_str.split("-")[0])
    under_test = CMEGlobexFixedIncomeCalendar()
    schedule = under_test.schedule(f"{year}-01-01", f"{year + 1}-01-01", tz=TZ)

    if expected_status == "open":
        s = schedule.loc[day_str]
        assert s["market_open"] == day_ts + Day(-1) + Hour(18) + Minute(0)
        assert s["market_close"] == day_ts + Day(0) + Hour(17) + Minute(0)
    elif expected_status == "closed":
        assert day_ts.tz_localize(None) not in schedule.index
    else:
        s = schedule.loc[day_str]
        hour = int(expected_status[0:2])
        minute = int(expected_status[2:4])
        assert s["market_open"] == day_ts + Day(-1) + Hour(18)
        assert s["market_close"] == day_ts + Day(0) + Hour(hour) + Minute(minute)
