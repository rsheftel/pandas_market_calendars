#
# Copyright 2016 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import time
import pandas as pd
from pytz import timezone
from toolz import concat
from pandas.util.testing import assert_series_equal, assert_frame_equal, assert_index_equal
from itertools import chain
import pytest

from pandas_market_calendars import get_calendar
from pandas_market_calendars.calendar_utils import _calendars, _aliases
from pandas_market_calendars.market_calendar import days_at_time, MarketCalendar, clean_dates

from pandas.tseries.holiday import AbstractHolidayCalendar
from pandas_market_calendars.us_holidays import (
    USNewYearsDay,
    Christmas,
    HurricaneSandyClosings,
    USNationalDaysofMourning,
    MonTuesThursBeforeIndependenceDay
)


class FakeCalendar(MarketCalendar):
    open_time_default = time(11, 13)
    close_time_default = time(11, 49)

    @property
    def name(self):
        return "DMY"

    @property
    def tz(self):
        return timezone("Asia/Ulaanbaatar")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[USNewYearsDay, Christmas])

    @property
    def adhoc_holidays(self):
        return list(chain(HurricaneSandyClosings, USNationalDaysofMourning))

    @property
    def special_opens(self):
        return [(time(11, 15), AbstractHolidayCalendar(rules=[MonTuesThursBeforeIndependenceDay]))]

    @property
    def special_opens_adhoc(self):
        return [(time(11, 20), ['2016-12-13'])]

    @property
    def special_closes(self):
        return [(time(11, 30), AbstractHolidayCalendar(rules=[MonTuesThursBeforeIndependenceDay]))]

    @property
    def special_closes_adhoc(self):
        return [(time(11, 40), ['2016-12-14'])]


def test_default_calendars():
    for name in concat([_calendars, _aliases]):
        assert get_calendar(name) is not None


def test_days_at_time():
    def dat(day, day_offset, time_offset, tz, expected):
        days = pd.DatetimeIndex([pd.Timestamp(day, tz=tz)])
        result = days_at_time(days, time_offset, tz, day_offset)[0]
        expected = pd.Timestamp(expected, tz=tz).tz_convert('UTC')
        assert result == expected

    args_list = [
        # NYSE standard day
        (
            '2016-07-19', 0, time(9, 31), timezone('America/New_York'),
            '2016-07-19 9:31',
        ),
        # CME standard day
        (
            '2016-07-19', -1, time(17, 1), timezone('America/Chicago'),
            '2016-07-18 17:01',
        ),
        # CME day after DST start
        (
            '2004-04-05', -1, time(17, 1), timezone('America/Chicago'),
            '2004-04-04 17:01'
        ),
        # ICE day after DST start
        (
            '1990-04-02', -1, time(19, 1), timezone('America/Chicago'),
            '1990-04-01 19:01',
        ),
    ]

    for args in args_list:
        dat(args[0], args[1], args[2], args[3], args[4])


def test_clean_dates():
    start, end = clean_dates('2016-12-01', '2016-12-31')
    assert start == pd.Timestamp('2016-12-01')
    assert end == pd.Timestamp('2016-12-31')

    start, end = clean_dates('2016-12-01 12:00', '2016-12-31 12:00')
    assert start == pd.Timestamp('2016-12-01')
    assert end == pd.Timestamp('2016-12-31')

    start, end = clean_dates(pd.Timestamp('2016-12-01', tz='America/Chicago'),
                             pd.Timestamp('2016-12-31', tz='America/New_York'))
    assert start == pd.Timestamp('2016-12-01')
    assert end == pd.Timestamp('2016-12-31')

    start, end = clean_dates(pd.Timestamp('2016-12-01 09:31', tz='America/Chicago'),
                             pd.Timestamp('2016-12-31 16:00', tz='America/New_York'))
    assert start == pd.Timestamp('2016-12-01')
    assert end == pd.Timestamp('2016-12-31')


def test_properties():
    cal = FakeCalendar()
    assert cal.name == 'DMY'
    assert cal.tz == timezone('Asia/Ulaanbaatar')


def test_holidays():
    cal = FakeCalendar()

    actual = cal.holidays().holidays
    assert pd.Timestamp('2016-12-26') in actual
    assert pd.Timestamp('2012-01-02') in actual
    assert pd.Timestamp('2012-12-25') in actual
    assert pd.Timestamp('2012-10-29') in actual
    assert pd.Timestamp('2012-10-30') in actual


def test_valid_dates():
    cal = FakeCalendar()

    expected = pd.DatetimeIndex([pd.Timestamp(x, tz='UTC') for x in ['2016-12-23', '2016-12-27', '2016-12-28',
                                                                     '2016-12-29', '2016-12-30', '2017-01-03']])
    actual = cal.valid_days('2016-12-23', '2017-01-03')
    assert_index_equal(actual, expected)


def test_schedule():
    cal = FakeCalendar()
    assert cal.open_time == time(11, 13)
    assert cal.close_time == time(11, 49)

    expected = pd.DataFrame({'market_open': [pd.Timestamp('2016-12-01 03:13:00', tz='UTC'),
                                             pd.Timestamp('2016-12-02 03:13:00', tz='UTC')],
                             'market_close': [pd.Timestamp('2016-12-01 03:49:00', tz='UTC'),
                                              pd.Timestamp('2016-12-02 03:49:00', tz='UTC')]},
                            columns=['market_open', 'market_close'],
                            index=[pd.Timestamp('2016-12-01'), pd.Timestamp('2016-12-02')])
    actual = cal.schedule('2016-12-01', '2016-12-02')
    assert_frame_equal(actual, expected)

    results = cal.schedule('2016-12-01', '2016-12-31')
    assert len(results) == 21

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-01 03:13:00+0000', tz='UTC', freq='B'),
                          'market_close': pd.Timestamp('2016-12-01 03:49:00+0000', tz='UTC', freq='B')},
                         name=pd.Timestamp('2016-12-01'), index=['market_open', 'market_close'], dtype=object)
    assert_series_equal(results.iloc[0], expected)

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-30 03:13:00+0000', tz='UTC', freq='B'),
                          'market_close': pd.Timestamp('2016-12-30 03:49:00+0000', tz='UTC', freq='B')},
                         name=pd.Timestamp('2016-12-30'), index=['market_open', 'market_close'], dtype=object)
    assert_series_equal(results.iloc[-1], expected)

    with pytest.raises(ValueError):
        cal.schedule('2016-02-02', '2016-01-01')


def test_schedule_w_times():
    cal = FakeCalendar(time(12, 12), time(13, 13))

    assert cal.open_time == time(12, 12)
    assert cal.close_time == time(13, 13)

    results = cal.schedule('2016-12-01', '2016-12-31')
    assert len(results) == 21

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-01 04:12:00+0000', tz='UTC', freq='B'),
                          'market_close': pd.Timestamp('2016-12-01 05:13:00+0000', tz='UTC', freq='B')},
                         name=pd.Timestamp('2016-12-01'), index=['market_open', 'market_close'], dtype=object)
    assert_series_equal(results.iloc[0], expected)

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-30 04:12:00+0000', tz='UTC', freq='B'),
                          'market_close': pd.Timestamp('2016-12-30 05:13:00+0000', tz='UTC', freq='B')},
                         name=pd.Timestamp('2016-12-30'), index=['market_open', 'market_close'], dtype=object)
    assert_series_equal(results.iloc[-1], expected)


def test_regular_holidays():
    cal = FakeCalendar()

    results = cal.schedule('2016-12-01', '2017-01-05')
    days = results.index

    # check regular holidays
    # Christmas
    assert pd.Timestamp('2016-12-23') in days
    assert pd.Timestamp('2016-12-26') not in days
    # New Years
    assert pd.Timestamp('2017-01-02') not in days
    assert pd.Timestamp('2017-01-03') in days


def test_adhoc_holidays():
    cal = FakeCalendar()

    results = cal.schedule('2012-10-15', '2012-11-15')
    days = results.index

    # check adhoc holidays
    # Hurricane Sandy
    assert pd.Timestamp('2012-10-26') in days
    assert pd.Timestamp('2012-10-29') not in days
    assert pd.Timestamp('2012-10-30') not in days
    assert pd.Timestamp('2012-10-31') in days


def test_special_opens():
    cal = FakeCalendar()

    results = cal.schedule('2012-07-01', '2012-07-06')
    opens = results['market_open'].tolist()

    # confirm that the day before July 4th is an 11:15 open not 11:13
    assert pd.Timestamp('2012-07-02 11:13', tz='Asia/Ulaanbaatar').tz_convert('UTC') in opens
    assert pd.Timestamp('2012-07-03 11:15', tz='Asia/Ulaanbaatar').tz_convert('UTC') in opens
    assert pd.Timestamp('2012-07-04 11:13', tz='Asia/Ulaanbaatar').tz_convert('UTC') in opens


def test_special_opens_adhoc():
    cal = FakeCalendar()

    results = cal.schedule('2016-12-10', '2016-12-20')
    opens = results['market_open'].tolist()

    # confirm that 2016-12-13 is an 11:20 open not 11:13
    assert pd.Timestamp('2016-12-12 11:13', tz='Asia/Ulaanbaatar').tz_convert('UTC') in opens
    assert pd.Timestamp('2016-12-13 11:20', tz='Asia/Ulaanbaatar').tz_convert('UTC') in opens
    assert pd.Timestamp('2016-12-14 11:13', tz='Asia/Ulaanbaatar').tz_convert('UTC') in opens


def test_special_closes():
    cal = FakeCalendar()

    results = cal.schedule('2012-07-01', '2012-07-06')
    closes = results['market_close'].tolist()

    # confirm that the day before July 4th is an 11:30 close not 11:49
    assert pd.Timestamp('2012-07-02 11:49', tz='Asia/Ulaanbaatar').tz_convert('UTC') in closes
    assert pd.Timestamp('2012-07-03 11:30', tz='Asia/Ulaanbaatar').tz_convert('UTC') in closes
    assert pd.Timestamp('2012-07-04 11:49', tz='Asia/Ulaanbaatar').tz_convert('UTC') in closes

    # early close first date
    results = cal.schedule('2012-07-03', '2012-07-04')
    actual = results['market_close'].tolist()
    expected = [pd.Timestamp('2012-07-03 11:30', tz='Asia/Ulaanbaatar').tz_convert('UTC'),
                pd.Timestamp('2012-07-04 11:49', tz='Asia/Ulaanbaatar').tz_convert('UTC')]
    assert actual == expected

    # early close last date
    results = cal.schedule('2012-07-02', '2012-07-03')
    actual = results['market_close'].tolist()
    expected = [pd.Timestamp('2012-07-02 11:49', tz='Asia/Ulaanbaatar').tz_convert('UTC'),
                pd.Timestamp('2012-07-03 11:30', tz='Asia/Ulaanbaatar').tz_convert('UTC')]
    assert actual == expected


def test_special_closes_adhoc():
    cal = FakeCalendar()

    results = cal.schedule('2016-12-10', '2016-12-20')
    closes = results['market_close'].tolist()

    # confirm that 2016-12-14 is an 11:40 close not 11:49
    assert pd.Timestamp('2016-12-13 11:49', tz='Asia/Ulaanbaatar').tz_convert('UTC') in closes
    assert pd.Timestamp('2016-12-14 11:40', tz='Asia/Ulaanbaatar').tz_convert('UTC') in closes
    assert pd.Timestamp('2016-12-15 11:49', tz='Asia/Ulaanbaatar').tz_convert('UTC') in closes

    # now with the early close as end date
    results = cal.schedule('2016-12-13', '2016-12-14')
    closes = results['market_close'].tolist()
    assert pd.Timestamp('2016-12-13 11:49', tz='Asia/Ulaanbaatar').tz_convert('UTC') in closes
    assert pd.Timestamp('2016-12-14 11:40', tz='Asia/Ulaanbaatar').tz_convert('UTC') in closes


def test_early_closes():
    cal = FakeCalendar()

    schedule = cal.schedule('2014-01-01', '2016-12-31')
    results = cal.early_closes(schedule)
    assert pd.Timestamp('2014-07-03') in results.index
    assert pd.Timestamp('2016-12-14') in results.index


def test_open_at_time():
    cal = FakeCalendar()

    schedule = cal.schedule('2014-01-01', '2016-12-31')
    # regular trading day
    assert cal.open_at_time(schedule, pd.Timestamp('2014-07-02 03:40', tz='UTC')) is True
    # early close
    assert cal.open_at_time(schedule, pd.Timestamp('2014-07-03 03:40', tz='UTC')) is False
    # holiday
    assert cal.open_at_time(schedule, pd.Timestamp('2014-12-25 03:30', tz='UTC')) is False
