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
from itertools import chain
from pytz import timezone
import pickle


import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_index_equal, assert_series_equal
from pandas.tseries.holiday import AbstractHolidayCalendar

from pandas_market_calendars import get_calendar, get_calendar_names
from pandas_market_calendars.holidays_us import (Christmas, HurricaneSandyClosings, MonTuesThursBeforeIndependenceDay,
                                                 USNationalDaysofMourning, USNewYearsDay)
from pandas_market_calendars.market_calendar import MarketCalendar #, clean_dates, days_at_time
from pandas_market_calendars.exchange_calendars_mirror import TradingCalendar
from pandas_market_calendars.exchange_calendar_nyse import NYSEExchangeCalendar

import exchange_calendars as ecal

class FakeCalendar(MarketCalendar):
    regular_market_times = {
        "market_open": ((None, time(11,18)),
                        ("1902-03-04", time(11,13))),
        "market_close": ((None, time(11, 45)),
                         ("1901-02-03", time(11,49)))
    }

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
        return [(time(11, 20), ['2016-12-13', "2016-12-25"])]

    @property
    def special_closes(self):
        return [(time(11, 30), AbstractHolidayCalendar(rules=[MonTuesThursBeforeIndependenceDay]))]

    @property
    def special_closes_adhoc(self):
        return [(time(11, 40), ['2016-12-14'])]


class FakeBreakCalendar(MarketCalendar):

    regular_market_times = {
        "market_open": ((None, time(9, 30)),),
        "market_close": ((None, time(12)),),
        "break_start": ((None, time(10)),),
        "break_end": ((None, time(11)),)
    }

    @property
    def name(self):
        return "BRK"

    @property
    def tz(self):
        return timezone("America/New_York")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[USNewYearsDay, Christmas])

    @property
    def special_opens_adhoc(self):
        return [(time(10, 20), ['2016-12-29'])]

    @property
    def special_closes_adhoc(self):
        return [(time(10, 40), ['2016-12-30'])]

@pytest.fixture
def patch_get_current_time(monkeypatch):
    def get_fake_time():
        return pd.Timestamp('2014-07-02 03:40', tz='UTC')
    monkeypatch.setattr(MarketCalendar, '_get_current_time', get_fake_time)


def test_protected_dictionary(cal= None):
    cal = FakeCalendar() if cal is None else cal
    # shouldn't be able to add
    with pytest.raises(TypeError) as e:
        cal.regular_market_times["market_open"] = time(12)

    # nor delete
    with pytest.raises(TypeError) as e:
        del cal.regular_market_times["market_open"]

def test_pickling():

    for Cal in [FakeCalendar, FakeBreakCalendar, NYSEExchangeCalendar]:
        # instance
        cal = Cal()
        pickled = pickle.dumps(cal)
        unpickled = pickle.loads(pickled)

        assert cal.regular_market_times == unpickled.regular_market_times
        assert cal.market_times == unpickled.market_times
        assert cal.discontinued_market_times == unpickled.discontinued_market_times
        assert cal._regular_market_timedeltas == unpickled._regular_market_timedeltas

        test_protected_dictionary(cal)
        test_protected_dictionary(unpickled)

        # class
        pickled = pickle.dumps(Cal)
        unpickled = pickle.loads(pickled)
        assert Cal.regular_market_times == unpickled.regular_market_times

        test_protected_dictionary(Cal)
        test_protected_dictionary(unpickled)





def test_get_time():
    cal = FakeCalendar()

    assert cal.get_time("market_open") == time(11, 13)
    assert cal.get_time("break_start") is None
    assert cal.get_time("break_end") is None

    assert cal.get_time_on("market_close", "1900-01-01") == time(11, 45)
    assert cal.get_time_on("break_start", "1900-01-01") is None

    cal.remove_time("market_open")
    with pytest.raises(NotImplementedError):
        t = cal.open_time

    with pytest.raises(KeyError):
        t = cal.get_time_on("pre", "1900-01-01")

def test_get_offset():
    cal = FakeBreakCalendar()

    assert cal.open_offset == 0
    assert cal.close_offset == 0

    cal.change_time("market_open", (time(10), -1))
    cal.change_time("market_close", (time(10), 5))

    assert cal.get_offset("market_open") == -1
    assert cal.get_offset("market_close") == 5

def test_special_dates():
    cal = FakeCalendar()

    special = cal.special_dates("market_open", "2016-12-10", "2016-12-31")
    assert special.astype(str).tolist() == ["2016-12-13 03:20:00+00:00"]

    special = cal.special_dates("market_open", "2016-12-10", "2016-12-31", filter_holidays= False)
    assert special.astype(str).tolist() == ["2016-12-13 03:20:00+00:00", "2016-12-25 03:20:00+00:00"]


def test_change_add_remove_time():
    cal = FakeCalendar()

    assert not cal.has_discontinued
    assert not cal.has_custom

    # change/add using the different formats that are supported
    cal.change_time("market_open", time(12))
    cal.add_time("test_time", (None, time(12)))
    cal.add_time("other_test", ((None, time(12)),))
    assert cal.open_time == cal.get_time("test_time") == cal.get_time("other_test")

    assert ("test_time" in cal.regular_market_times and
            "test_time" in cal._regular_market_timedeltas and
            "test_time" in cal._market_times)

    assert cal.has_custom
    assert cal.is_custom("market_open")
    assert cal.is_custom("test_time")
    assert cal.is_custom("other_test")

    # with offset, which will not be returned by get_time
    cal.change_time("market_open", (time(12), -1))
    cal.change_time("test_time", (None, time(12), -1))
    assert cal.open_time == cal.get_time("test_time") == cal.get_time("other_test")

    assert cal.open_offset == -1
    assert cal.get_offset("test_time") == -1
    assert cal.get_offset("other_test") == 0

    cal.change_time("other_test", ((None, time(12), -1),))
    assert cal.open_time == cal.get_time("test_time") == cal.get_time("other_test")

    with pytest.raises(AssertionError):
        cal.add_time("test_time", time(12))   # can't add what is already there

    with pytest.raises(AssertionError):
        cal.change_time("nope", time(12))  # can't change what is not there

    cal.remove_time("test_time")
    assert ("test_time" not in cal.regular_market_times and
            "test_time" not in cal._regular_market_timedeltas and
            "test_time" not in cal._market_times)

    # will be removed completely and therefore not found.
    assert not cal.is_custom("test_time")
    # The others should be untouched
    assert cal.has_custom
    assert cal.is_custom("market_open")
    assert cal.is_custom("other_test")


    # wrong formats
    with pytest.raises(AssertionError):
        cal.add_time("wrong_format", (-1, time(10)))

    with pytest.raises(AssertionError):
        cal.add_time("wrong_format", pd.Timedelta("5H"))


def test_dunder_methods():
    cal = FakeCalendar()

    assert cal["market_open"] == time(11,13)
    assert cal["market_open", "1900-01-01"] == time(11,18)
    assert cal["market_open", "all"] == cal.regular_market_times["market_open"]


    # __setitem__ is adding a time, which refuses to replace
    with pytest.raises(AssertionError):
        cal["market_open"] = time(10)

    # but excplicitly deleting, makes it work
    del cal["market_open"]
    cal["market_open"] = time(9)
    assert cal["market_open"] == time(9)



def test_default_calendars():
    for name in get_calendar_names():
        if name == "XKRX":
            with pytest.warns(UserWarning):
                assert get_calendar(name) is not None
        else:
            assert get_calendar(name) is not None


def test_days_at_time():
    class New_York(FakeCalendar):
        @property
        def tz(self): return timezone('America/New_York')
    new_york = New_York()
    new_york.change_time("market_open", time(12))
    new_york.change_time("market_close", time(13))

    class Chicago(FakeCalendar):
        @property
        def tz(self): return timezone('America/Chicago')
    chicago = Chicago()
    chicago.change_time("market_open", time(10))
    chicago.change_time("market_close", time(11))
    chicago.add_time("with_offset", (time(10, 30), -1))

    def dat(day, day_offset, time_offset, cal, expected):
        days = pd.DatetimeIndex([pd.Timestamp(day, tz=cal.tz)])
        result = cal.days_at_time(days, time_offset, day_offset)[0]
        expected = pd.Timestamp(expected, tz=cal.tz).tz_convert('UTC')
        assert result == expected

    args_list = [
        # NYSE standard day
        (
            '2016-07-19', 0, time(9, 31), new_york, '2016-07-19 9:31',
        ),
        # CME standard day
        (
            '2016-07-19', -1, time(17, 1), chicago, '2016-07-18 17:01',
        ),
        # CME day after DST start
        (
            '2004-04-05', -1, time(17, 1), chicago, '2004-04-04 17:01'
        ),
        # ICE day after DST start
        (
            '1990-04-02', -1, time(19, 1), chicago, '1990-04-01 19:01',
        ),


        ## Built-in times  # day_offset kwarg should automatically be ignored
        (
            '2016-07-19', None, "market_open", new_york, '2016-07-19 12:00',
        ),
        # CME standard day
        (
            '2016-07-19', None, "market_open", chicago, '2016-07-19 10:00',
        ),
        # CME day after DST start
        (
            '2004-04-05', None, "with_offset", chicago, '2004-04-04 10:30'
        ),
        # ICE day after DST start
        (
            '1990-04-02', None, "market_open", chicago, '1990-04-02 10:00',
        ),

        (
            '2016-07-19', None, "market_close", new_york, '2016-07-19 13:00',
        ),
        # CME standard day
        (
            '2016-07-19', None, "market_close", chicago, '2016-07-19 11:00',
        ),
        # CME day after DST start
        (
            '2004-04-05', None, "market_close", chicago, '2004-04-05 11:00'
        ),
        # ICE day after DST start
        (
            '1990-04-02', None, "with_offset", chicago, '1990-04-01 10:30',
        ),
    ]

    for args in args_list:
        dat(args[0], args[1], args[2], args[3], args[4])


def test_clean_dates():
    cal = FakeCalendar()

    start, end = cal.clean_dates('2016-12-01', '2016-12-31')
    assert start == pd.Timestamp('2016-12-01')
    assert end == pd.Timestamp('2016-12-31')

    start, end = cal.clean_dates('2016-12-01 12:00', '2016-12-31 12:00')
    assert start == pd.Timestamp('2016-12-01')
    assert end == pd.Timestamp('2016-12-31')

    start, end = cal.clean_dates(pd.Timestamp('2016-12-01', tz='America/Chicago'),
                             pd.Timestamp('2016-12-31', tz='America/New_York'))
    assert start == pd.Timestamp('2016-12-01')
    assert end == pd.Timestamp('2016-12-31')

    start, end = cal.clean_dates(pd.Timestamp('2016-12-01 09:31', tz='America/Chicago'),
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

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-01 03:13:00+0000', tz='UTC'),
                          'market_close': pd.Timestamp('2016-12-01 03:49:00+0000', tz='UTC')},
                         name=pd.Timestamp('2016-12-01'), index=['market_open', 'market_close'])
    # because of change in pandas in v0.24, pre-0.24 versions need object dtype
    if pd.__version__ < '0.24':
        expected = expected.astype(object)

    assert_series_equal(results.iloc[0], expected)

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-30 03:13:00+0000', tz='UTC'),
                          'market_close': pd.Timestamp('2016-12-30 03:49:00+0000', tz='UTC')},
                         name=pd.Timestamp('2016-12-30'), index=['market_open', 'market_close'])
    # because of change in pandas in v0.24, pre-0.24 versions need object dtype
    if pd.__version__ < '0.24':
        expected = expected.astype(object)

    assert_series_equal(results.iloc[-1], expected)

    # one day schedule
    expected = pd.DataFrame({'market_open': pd.Timestamp('2016-12-01 03:13:00+0000', tz='UTC'),
                             'market_close': pd.Timestamp('2016-12-01 03:49:00+0000', tz='UTC')},
                            index=pd.DatetimeIndex([pd.Timestamp('2016-12-01')], freq='C'),
                            columns=['market_open', 'market_close'])
    actual = cal.schedule('2016-12-01', '2016-12-01')
    if pd.__version__ < '1.1.0':
        assert_frame_equal(actual, expected)
    else:
        assert_frame_equal(actual, expected, check_freq=False)

    # start date after end date
    with pytest.raises(ValueError):
        cal.schedule('2016-02-02', '2016-01-01')
    
    # using a different time zone
    expected = pd.DataFrame({'market_open': pd.Timestamp('2016-11-30 22:13:00-05:00', tz='US/Eastern'),
                             'market_close': pd.Timestamp('2016-11-30 22:49:00-05:00', tz='US/Eastern')},
                            index=pd.DatetimeIndex([pd.Timestamp('2016-12-01')]),
                            columns=['market_open', 'market_close'])

    actual = cal.schedule('2016-12-01', '2016-12-01', tz='US/Eastern')
    if pd.__version__ < '1.1.0':
        assert_frame_equal(actual, expected)
    else:
        assert_frame_equal(actual, expected, check_freq=False)

def test_custom_schedule():
    cal = FakeBreakCalendar()
    cal.add_time("pre", time(9))
    cal.add_time("post", time(13))

    # test default
    schedule = cal.schedule("2016-12-23", "2016-12-31")
    assert schedule.columns.tolist() == ["market_open", "break_start", "break_end", "market_close"]

    # special market_open should take effect
    assert schedule.loc["2016-12-29"].astype(str).to_list() == ["2016-12-29 15:20:00+00:00",
                                                                "2016-12-29 15:20:00+00:00",
                                                                "2016-12-29 16:00:00+00:00",
                                                                "2016-12-29 17:00:00+00:00"]
    # special market_close as well
    assert schedule.loc["2016-12-30"].astype(str).to_list() == ["2016-12-30 14:30:00+00:00",
                                                                "2016-12-30 15:00:00+00:00",
                                                                "2016-12-30 15:40:00+00:00",
                                                                "2016-12-30 15:40:00+00:00"]

    # test custom start end
    schedule = cal.schedule("2016-12-23", "2016-12-31", start= "pre", end= "break_end")
    assert schedule.columns.tolist() == ["pre", "market_open", "break_start", "break_end"]

    # market_open is present, so special times should take effect
    assert schedule.loc["2016-12-29"].astype(str).to_list() == ["2016-12-29 15:20:00+00:00",
                                                                "2016-12-29 15:20:00+00:00",
                                                                "2016-12-29 15:20:00+00:00",
                                                                "2016-12-29 16:00:00+00:00"]

    # market_close is not present, so special times should NOT take effect
    assert schedule.loc["2016-12-30"].astype(str).to_list() == ["2016-12-30 14:00:00+00:00",
                                                                "2016-12-30 14:30:00+00:00",
                                                                "2016-12-30 15:00:00+00:00",
                                                                "2016-12-30 16:00:00+00:00"]

    # test custom market times
    schedule = cal.schedule("2016-12-23", "2016-12-31", market_times= ["post", "pre"])
    assert schedule.columns.tolist() == ["post", "pre"]
    # Neither market_open nor market_close are present, so no specials should take effect
    assert schedule.loc["2016-12-29"].astype(str).to_list() == ["2016-12-29 18:00:00+00:00",
                                                                "2016-12-29 14:00:00+00:00"]

    assert schedule.loc["2016-12-30"].astype(str).to_list() == ["2016-12-30 18:00:00+00:00",
                                                                "2016-12-30 14:00:00+00:00"]


    # only adjust column itself
    schedule = cal.schedule("2016-12-23", "2016-12-31", force_special_times= False)
    assert schedule.columns.tolist() == ["market_open", "break_start", "break_end", "market_close"]

    # special market_open should only take effect on itself
    assert schedule.loc["2016-12-29"].astype(str).to_list() == ["2016-12-29 15:20:00+00:00",
                                                                "2016-12-29 15:00:00+00:00",
                                                                "2016-12-29 16:00:00+00:00",
                                                                "2016-12-29 17:00:00+00:00"]
    # special market_close as well
    assert schedule.loc["2016-12-30"].astype(str).to_list() == ["2016-12-30 14:30:00+00:00",
                                                                "2016-12-30 15:00:00+00:00",
                                                                "2016-12-30 16:00:00+00:00",
                                                                "2016-12-30 15:40:00+00:00"]



    # ignore special times completely
    schedule = cal.schedule("2016-12-23", "2016-12-31", force_special_times= None)
    assert schedule.columns.tolist() == ["market_open", "break_start", "break_end", "market_close"]

    # special market_open should NOT take effect anywhere
    assert schedule.loc["2016-12-29"].astype(str).to_list() == ["2016-12-29 14:30:00+00:00",
                                                                "2016-12-29 15:00:00+00:00",
                                                                "2016-12-29 16:00:00+00:00",
                                                                "2016-12-29 17:00:00+00:00"]
    # special market_close neither
    assert schedule.loc["2016-12-30"].astype(str).to_list() == ["2016-12-30 14:30:00+00:00",
                                                                "2016-12-30 15:00:00+00:00",
                                                                "2016-12-30 16:00:00+00:00",
                                                                "2016-12-30 17:00:00+00:00"]


def test_schedule_w_breaks():
    cal = FakeBreakCalendar()
    assert cal.open_time == time(9, 30)
    assert cal.close_time == time(12, 00)
    assert cal.break_start == time(10, 00)
    assert cal.break_end == time(11, 00)

    expected = pd.DataFrame({'market_open': [pd.Timestamp('2016-12-01 14:30:00', tz='UTC'),
                                             pd.Timestamp('2016-12-02 14:30:00', tz='UTC')],
                             'market_close': [pd.Timestamp('2016-12-01 17:00:00', tz='UTC'),
                                              pd.Timestamp('2016-12-02 17:00:00', tz='UTC')],
                             'break_start': [pd.Timestamp('2016-12-01 15:00:00', tz='UTC'),
                                             pd.Timestamp('2016-12-02 15:00:00', tz='UTC')],
                             'break_end': [pd.Timestamp('2016-12-01 16:00:00', tz='UTC'),
                                           pd.Timestamp('2016-12-02 16:00:00', tz='UTC')]
    },
                            columns=['market_open', 'break_start', 'break_end', 'market_close'],
                            index=[pd.Timestamp('2016-12-01'), pd.Timestamp('2016-12-02')])
    actual = cal.schedule('2016-12-01', '2016-12-02')
    assert_frame_equal(actual, expected)

    results = cal.schedule('2016-12-01', '2016-12-31')
    assert len(results) == 21

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-01 14:30:00+0000', tz='UTC'),
                          'market_close': pd.Timestamp('2016-12-01 17:00:00+0000', tz='UTC'),
                          'break_start': pd.Timestamp('2016-12-01 15:00:00+0000', tz='UTC'),
                          'break_end': pd.Timestamp('2016-12-01 16:00:00+0000', tz='UTC')
    },
                         name=pd.Timestamp('2016-12-01'),
                         index=['market_open', 'break_start', 'break_end', 'market_close'])

    assert_series_equal(results.iloc[0], expected)

    # special open is after break start
    expected = pd.Series({'market_open': pd.Timestamp('2016-12-29 15:20:00+0000', tz='UTC'),
                          'market_close': pd.Timestamp('2016-12-29 17:00:00+0000', tz='UTC'),
                          'break_start': pd.Timestamp('2016-12-29 15:20:00+0000', tz='UTC'),
                          'break_end': pd.Timestamp('2016-12-29 16:00:00+0000', tz='UTC')},
                         name=pd.Timestamp('2016-12-29'),
                         index=['market_open', 'break_start', 'break_end', 'market_close'])

    assert_series_equal(results.iloc[-2], expected)

    # special close is before break end
    expected = pd.Series({'market_open': pd.Timestamp('2016-12-30 14:30:00+0000', tz='UTC'),
                          'market_close': pd.Timestamp('2016-12-30 15:40:00+0000', tz='UTC'),
                          'break_start': pd.Timestamp('2016-12-30 15:00:00+0000', tz='UTC'),
                          'break_end': pd.Timestamp('2016-12-30 15:40:00+0000', tz='UTC')},
                         name=pd.Timestamp('2016-12-30'),
                         index=['market_open', 'break_start', 'break_end', 'market_close'])

    assert_series_equal(results.iloc[-1], expected)

    # using a different time zone
    expected = pd.DataFrame({'market_open': pd.Timestamp('2016-12-28 09:30:00-05:00', tz='America/New_York'),
                             'market_close': pd.Timestamp('2016-12-28 12:00:00-05:00', tz='America/New_York'),
                             'break_start': pd.Timestamp('2016-12-28 10:00:00-05:00', tz='America/New_York'),
                             'break_end': pd.Timestamp('2016-12-28 11:00:00-05:00', tz='America/New_York')},
                            index=pd.DatetimeIndex([pd.Timestamp('2016-12-28')]),
                            columns=['market_open', 'break_start', 'break_end', 'market_close'])

    actual = cal.schedule('2016-12-28', '2016-12-28', tz='America/New_York')
    if pd.__version__ < '1.1.0':
        assert_frame_equal(actual, expected)
    else:
        assert_frame_equal(actual, expected, check_freq=False)


def test_schedule_w_times():
    cal = FakeCalendar(time(12, 12), time(13, 13))

    assert cal.open_time == time(12, 12)
    assert cal.close_time == time(13, 13)

    results = cal.schedule('2016-12-01', '2016-12-31')
    assert len(results) == 21

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-01 04:12:00+0000', tz='UTC'),
                          'market_close': pd.Timestamp('2016-12-01 05:13:00+0000', tz='UTC')},
                         name=pd.Timestamp('2016-12-01'), index=['market_open', 'market_close'])
    # because of change in pandas in v0.24, pre-0.24 versions need object dtype
    if pd.__version__ < '0.24':
        expected = expected.astype(object)

    assert_series_equal(results.iloc[0], expected)

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-30 04:12:00+0000', tz='UTC'),
                          'market_close': pd.Timestamp('2016-12-30 05:13:00+0000', tz='UTC')},
                         name=pd.Timestamp('2016-12-30'), index=['market_open', 'market_close'])
    # because of change in pandas in v0.24, pre-0.24 versions need object dtype
    if pd.__version__ < '0.24':
        expected = expected.astype(object)

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

    schedule = cal.schedule("1901-02-01", "1901-02-05")
    assert cal.early_closes(schedule).empty

def test_late_opens():
    cal = FakeCalendar()
    schedule = cal.schedule("1902-03-01", "1902-03-06")
    assert cal.late_opens(schedule).empty


def test_open_at_time():
    cal = FakeCalendar()

    schedule = cal.schedule('2014-01-01', '2016-12-31')
    # regular trading day
    assert cal.open_at_time(schedule, pd.Timestamp('2014-07-02 03:40', tz='UTC')) is True
    # early close
    assert cal.open_at_time(schedule, pd.Timestamp('2014-07-03 03:40', tz='UTC')) is False
    # holiday
    assert cal.open_at_time(schedule, pd.Timestamp('2014-12-25 03:30', tz='UTC')) is False

    # last bar of the day defaults to False
    assert cal.open_at_time(schedule, pd.Timestamp('2016-09-07 11:49', tz='Asia/Ulaanbaatar')) is False

    # last bar of the day is True if include_close is True
    assert cal.open_at_time(schedule, pd.Timestamp('2016-09-07 11:49', tz='Asia/Ulaanbaatar'),
                            include_close=True) is True
    # equivalent to 2014-07-02 03:40 UTC
    assert cal.open_at_time(schedule, pd.Timestamp('2014-07-01 23:40:00-0400', tz='America/New_York')) is True

    cal["pre"] = time(11) # which is 3 am in Ulaanbaatar
    schedule = cal.schedule('2014-07-01', '2014-07-10', market_times= "all")
    assert cal.open_at_time(schedule, "2014-07-02 02:55:00+00:00") is False
    # only_rth = True makes it ignore anything before market_open or after market_close
    assert cal.open_at_time(schedule, "2014-07-02 03:05:00+00:00", only_rth= True) is False
    assert cal.open_at_time(schedule, "2014-07-02 03:05:00+00:00") is True

    # handle market times that cross midnight
    cal.change_time("pre", time(7)) # is the day before in UTC
    cal.add_time("post", (time(9), 1))
    schedule = cal.schedule('2014-07-01', '2014-07-10', market_times= "all")
    assert cal.open_at_time(schedule, pd.Timestamp("2014-07-03 23:30:00+00:00")) is True
    assert cal.open_at_time(schedule, pd.Timestamp("2014-07-05 00:30:00+00:00")) is True
    assert cal.open_at_time(schedule, pd.Timestamp("2014-07-05 00:30:00+00:00"), only_rth= True) is False

    cal.change_time("market_open", (cal.open_time, -2))
    cal.change_time("market_close", (cal.close_time, 3))
    schedule = cal.schedule('2014-07-01', '2014-07-10', market_times= "all")
    assert cal.open_at_time(schedule, "2014-06-29 04:00:00+00:00") is True
    assert cal.open_at_time(schedule, "2014-07-13 06:00:00+03:00") is True

    # should raise error if not all columns are in self.market_times
    with pytest.raises(ValueError):
        cal.open_at_time(schedule.rename(columns= {"pre": "other"}), "2014-07-02 02:55:00+00:00")

    # or if the date is before/after the first/last dates covered by the schedule
    with pytest.raises(ValueError):
        cal.open_at_time(schedule, "2014-07-12 23:00:00-05:00")
    with pytest.raises(ValueError):
        cal.open_at_time(schedule, "2014-06-29 03:00:00+00:00")


def test_open_at_time_breaks():
    cal = FakeBreakCalendar()

    schedule = cal.schedule('2016-12-20', '2016-12-30')

    # between open and break
    assert cal.open_at_time(schedule, pd.Timestamp('2016-12-28 09:50', tz='America/New_York')) is True
    # at break start
    assert cal.open_at_time(schedule, pd.Timestamp('2016-12-28 10:00', tz='America/New_York')) is False
    assert cal.open_at_time(schedule, pd.Timestamp('2016-12-28 10:00', tz='America/New_York'), include_close=True) is True
    # during break
    assert cal.open_at_time(schedule, pd.Timestamp('2016-12-28 10:30', tz='America/New_York')) is False
    assert cal.open_at_time(schedule, pd.Timestamp('2016-12-28 10:59', tz='America/New_York')) is False
    # at break end
    assert cal.open_at_time(schedule, pd.Timestamp('2016-12-28 11:00', tz='America/New_York')) is True
    # between break and close
    assert cal.open_at_time(schedule, pd.Timestamp('2016-12-28 11:30', tz='America/New_York')) is True

    # handle market times that cross midnight
    cal.change_time("market_open", time(7)) # is the day before in UTC
    cal.change_time("market_close", (time(9), 1))
    cal.add_time("post", (time(10), 1))
    schedule = cal.schedule('2014-07-01', '2014-07-10', market_times= "all")
    assert cal.open_at_time(schedule, pd.Timestamp("2014-07-03 23:30:00+00:00")) is True
    assert cal.open_at_time(schedule, pd.Timestamp("2014-07-05 00:30:00+00:00")) is True
    assert cal.open_at_time(schedule, pd.Timestamp("2014-07-04 14:30:00+00:00")) is False
    assert cal.open_at_time(schedule, pd.Timestamp("2014-07-11 12:00:00+00:00")) is True

    assert cal.open_at_time(schedule, pd.Timestamp("2014-07-11 14:00:00+00:00"), include_close= True) is True
    assert cal.open_at_time(schedule, pd.Timestamp("2014-07-11 14:00:00+00:00")) is False
    with pytest.raises(ValueError):
        cal.open_at_time(schedule, pd.Timestamp("2014-07-11 14:00:00+00:00"), only_rth= True)


def test_is_open_now(patch_get_current_time):
    cal = FakeCalendar()

    schedule = cal.schedule('2014-01-01', '2016-12-31')

    assert cal.is_open_now(schedule) is True


def test_bad_dates():
    cal = FakeCalendar()

    empty = pd.DataFrame(columns=['market_open', 'market_close'], index=pd.DatetimeIndex([], freq='C'))

    # single weekend date
    schedule = cal.schedule('2018-06-30', '2018-06-30')
    assert_frame_equal(schedule, empty)

    # two weekend dates
    schedule = cal.schedule('2018-06-30', '2018-07-01')
    assert_frame_equal(schedule, empty)

    # single holiday
    schedule = cal.schedule('2018-01-01', '2018-01-01')
    assert_frame_equal(schedule, empty)

    # weekend and holiday
    schedule = cal.schedule('2017-12-30', '2018-01-01')
    assert_frame_equal(schedule, empty)

############################################
# TESTS FOR EXCHANGE_CALENDAR INTEGRATION  #
############################################


mcal_iepa = get_calendar("IEPA")
ecal_iepa = ecal.get_calendar("IEPA")

start, end = ecal_iepa._closes[[0, -1]]

# No exchange_calendar has a close_offset so this class implements it for testing
class _TstExchangeCalendar:
    def __init__(self):
        self.a_test_var = "initialized"
    @property
    def open_offset(self):
        return -2
    @property
    def close_offset(self):
        return 3


TstExchangeCalendar = type("TestExchangeCalendar", (TradingCalendar,), {'_ec_class': _TstExchangeCalendar})

test_cal = TstExchangeCalendar()

def test_mirror():

    assert not hasattr(mcal_iepa, "aliases")

    assert not isinstance(ecal_iepa, mcal_iepa.__class__)

    assert isinstance(ecal_iepa, mcal_iepa._ec.__class__)

def test_basic_information():

    assert mcal_iepa._EC_NOT_INITIALIZED
    assert mcal_iepa.tz == timezone("America/New_York") == ecal_iepa.tz
    assert mcal_iepa.open_offset == -1 == ecal_iepa.open_offset
    assert mcal_iepa.open_time == time(20)
    assert mcal_iepa.close_time == time(18)

    assert test_cal._EC_NOT_INITIALIZED
    assert test_cal.open_offset == -2
    assert test_cal.close_offset == 3
    assert test_cal["market_close", "all"] == ((None, time(23), 3),)
    assert test_cal._EC_NOT_INITIALIZED


def assert_same(one, two):
    assert one.shape[0] == two.shape[0], f"the shape is different {one.shape[0]} != {two.shape[0]}"
    assert (one.values == two.values).all()

def test_closes_opens():
    sched = mcal_iepa.schedule(start, end)

    assert_same(ecal_iepa._closes, sched.market_close)
    assert_same(ecal_iepa._opens, sched.market_open)

def test_ec_property():
    mcaliepa = get_calendar("IEPA")

    assert mcaliepa._EC_NOT_INITIALIZED
    ec = mcaliepa.ec
    assert not mcaliepa._EC_NOT_INITIALIZED

    assert test_cal._EC_NOT_INITIALIZED
    assert not hasattr(test_cal._ec, "a_test_var")
    assert test_cal.ec.a_test_var == "initialized"
    assert not test_cal._EC_NOT_INITIALIZED


def test_ec_schedule():
    mcaliepa = get_calendar("IEPA")

    assert mcaliepa._EC_NOT_INITIALIZED
    ours = mcaliepa.schedule(start, end)
    assert mcaliepa._EC_NOT_INITIALIZED

    theirs = mcaliepa.ec.schedule[["open", "close"]]
    assert not mcaliepa._EC_NOT_INITIALIZED

    theirs.index.freq = None
    theirs = theirs.rename(columns={"open": "market_open", "close": "market_close"})
    assert_frame_equal(ours, theirs)



if __name__ == '__main__':

    test_open_at_time()
    # test_ec_property()
    # test_custom_schedule()
    # test_special_opens()
    #
    # test_open_at_time_breaks()
    exit()
    for ref, obj in locals().copy().items():
        if ref.startswith("test_"):
            print("running: ", ref)
            obj()
