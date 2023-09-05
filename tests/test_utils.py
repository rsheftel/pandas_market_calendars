import datetime

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_index_equal

import pandas_market_calendars as mcal
from pandas_market_calendars.calendars.nyse import NYSEExchangeCalendar
from tests.test_market_calendar import FakeCalendar, FakeBreakCalendar


def test_get_calendar():
    assert isinstance(mcal.get_calendar('NYSE'), NYSEExchangeCalendar)
    cal = mcal.get_calendar('NYSE', datetime.time(10, 0), datetime.time(14, 30))
    assert isinstance(cal, NYSEExchangeCalendar)
    assert cal.open_time == datetime.time(10, 0)
    assert cal.close_time == datetime.time(14, 30)

    # confirm that import works properly
    _ = mcal.get_calendar('CME_Equity')


def test_get_calendar_names():
    assert 'ASX' in mcal.get_calendar_names()


def test_date_range_exceptions():
    cal = FakeCalendar(open_time= datetime.time(9), close_time= datetime.time(11, 30))
    schedule = cal.schedule("2021-01-05", "2021-01-05")

    # invalid closed argument
    with pytest.raises(ValueError) as e:
        mcal.date_range(schedule, "15min", closed="righ")
    assert e.exconly() == "ValueError: closed must be 'left', 'right', 'both' or None."

    # invalid force_close argument
    with pytest.raises(ValueError) as e:
        mcal.date_range(schedule, "15min", force_close="True")
    assert e.exconly() == "ValueError: force_close must be True, False or None."

    # close_time is before open_time
    schedule = pd.DataFrame([["2020-01-01 12:00:00+00:00", "2020-01-01 11:00:00+00:00"]],
                            index= ["2020-01-01"], columns= ["market_open", "market_close"])
    with pytest.raises(ValueError) as e:
        mcal.date_range(schedule, "15min", closed="right", force_close= True)
    assert e.exconly() == "ValueError: Schedule contains rows where market_close < market_open,"\
                                     " please correct the schedule"

    # Overlap -
    # the end of the last bar goes over the next start time
    bcal = FakeBreakCalendar()
    bschedule = bcal.schedule("2021-01-05", "2021-01-05")
    with pytest.raises(ValueError) as e1:
        # this frequency overlaps
        mcal.date_range(bschedule, "2H", closed= "right", force_close= None)
    # this doesn't
    mcal.date_range(bschedule, "1H", closed="right", force_close=None)

    with pytest.raises(ValueError) as e2:
        mcal.date_range(bschedule, "2H", closed= "both", force_close= None)
    mcal.date_range(bschedule, "1H", closed="right", force_close=None)

    with pytest.raises(ValueError) as e3:
        mcal.date_range(bschedule, "2H", closed= None, force_close= None)
    mcal.date_range(bschedule, "1H", closed="right", force_close=None)

    for e in (e1, e2, e3):
        assert e.exconly() == "ValueError: The chosen frequency will lead to overlaps in the calculated index. "\
                                          "Either choose a higher frequency or avoid setting force_close to None "\
                                          "when setting closed to 'right', 'both' or None."

    try:
        # should all be fine, since force_close cuts the overlapping interval
        mcal.date_range(bschedule, "2H", closed="right", force_close=True)

        with pytest.warns(UserWarning): # should also warn about lost sessions
            mcal.date_range(bschedule, "2H", closed="right", force_close=False)

        mcal.date_range(bschedule, "2H", closed="both", force_close=True)
        mcal.date_range(bschedule, "2H", closed="both", force_close=False)
        # closed = "left" should never be a problem since it won't go outside market hours anyway
        mcal.date_range(bschedule, "2H", closed="left", force_close=True)
        mcal.date_range(bschedule, "2H", closed="left", force_close=False)
        mcal.date_range(bschedule, "2H", closed="left", force_close=None)
    except ValueError as e:
        pytest.fail(f"Unexpected Error: \n{e}")


@pytest.mark.parametrize("tz", ["America/New_York", "Asia/Ulaanbaatar", "UTC"])
def test_date_range_permutations(tz):
    # open_time = 9, close_time = 11.30, freq = "1H"
    cal = FakeCalendar(open_time= datetime.time(9), close_time= datetime.time(11, 30))
    schedule = cal.schedule("2021-01-05", "2021-01-05", tz= tz)

    # result         matching values for:   closed force_close
    # 9 10 11        left False/ left None/ both False/ None False
    expected = pd.DatetimeIndex(
        ["2021-01-05 01:00:00+00:00", "2021-01-05 02:00:00+00:00",
         "2021-01-05 03:00:00+00:00"], tz= tz)
    actual = mcal.date_range(schedule, "1H", closed= "left", force_close= False)
    assert_index_equal(actual, expected)
    actual = mcal.date_range(schedule, "1H", closed= "left", force_close= None)
    assert_index_equal(actual, expected)
    actual = mcal.date_range(schedule, "1H", closed= "both", force_close= False)
    assert_index_equal(actual, expected)
    actual = mcal.date_range(schedule, "1H", closed= None, force_close= False)
    assert_index_equal(actual, expected)

    # 9 10 11 11.30  left True/ both True/ None True
    expected = pd.DatetimeIndex(
        ["2021-01-05 01:00:00+00:00", "2021-01-05 02:00:00+00:00",
         "2021-01-05 03:00:00+00:00", "2021-01-05 03:30:00+00:00"], tz= tz)
    actual = mcal.date_range(schedule, "1H", closed= "left", force_close= True)
    assert_index_equal(actual, expected)
    actual = mcal.date_range(schedule, "1H", closed= "both", force_close= True)
    assert_index_equal(actual, expected)
    actual = mcal.date_range(schedule, "1H", closed= None, force_close= True)
    assert_index_equal(actual, expected)

    # 10 11          right False
    expected = pd.DatetimeIndex(
        ["2021-01-05 02:00:00+00:00", "2021-01-05 03:00:00+00:00"], tz=tz)
    actual = mcal.date_range(schedule, "1H", closed="right", force_close=False)
    assert_index_equal(actual, expected)

    # 10 11 11.30    right True
    expected = pd.DatetimeIndex(
        ["2021-01-05 02:00:00+00:00", "2021-01-05 03:00:00+00:00",
         "2021-01-05 03:30:00+00:00"], tz=tz)
    actual = mcal.date_range(schedule, "1H", closed="right", force_close=True)
    assert_index_equal(actual, expected)

    # 10 11 12       right None
    expected = pd.DatetimeIndex(
        ["2021-01-05 02:00:00+00:00", "2021-01-05 03:00:00+00:00",
         "2021-01-05 04:00:00+00:00"], tz=tz)
    actual = mcal.date_range(schedule, "1H", closed="right", force_close=None)
    assert_index_equal(actual, expected)

    # 9 10 11 12     both None/ None None
    expected = pd.DatetimeIndex(
        ["2021-01-05 01:00:00+00:00", "2021-01-05 02:00:00+00:00",
         "2021-01-05 03:00:00+00:00", "2021-01-05 04:00:00+00:00"], tz=tz)
    actual = mcal.date_range(schedule, "1H", closed="both", force_close=None)
    assert_index_equal(actual, expected)
    actual = mcal.date_range(schedule, "1H", closed=None, force_close=None)
    assert_index_equal(actual, expected)


def test_date_range_daily():
    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(12, 0))

    # If closed='right' and force_close False for daily then the result is empty
    expected = pd.DatetimeIndex([], tz='UTC')
    schedule = cal.schedule('2015-12-31', '2016-01-06')
    with pytest.warns(UserWarning):
        actual = mcal.date_range(schedule, '1D', force_close=False, closed='right')

    assert_index_equal(actual, expected)

    # New years is holiday
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2015-12-31 12:00', '2016-01-04 12:00', '2016-01-05 12:00', '2016-01-06 12:00']])
    schedule = cal.schedule('2015-12-31', '2016-01-06')
    actual = mcal.date_range(schedule, '1D')

    assert_index_equal(actual, expected)

    # July 3 is early close
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2012-07-02 12:00', '2012-07-03 11:30', '2012-07-04 12:00']])
    schedule = cal.schedule('2012-07-02', '2012-07-04')
    actual = mcal.date_range(schedule, '1D')

    assert_index_equal(actual, expected)

    # Dec 14, 2016 is adhoc early close
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2016-12-13 12:00', '2016-12-14 11:40', '2016-12-15 12:00']])
    schedule = cal.schedule('2016-12-13', '2016-12-15')
    actual = mcal.date_range(schedule, '1D')

    assert_index_equal(actual, expected)

    # July 3 is late open
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2012-07-02 09:00', '2012-07-03 11:15', '2012-07-04 09:00']])
    schedule = cal.schedule('2012-07-02', '2012-07-04')
    actual = mcal.date_range(schedule, '1D', force_close=False, closed=None)

    assert_index_equal(actual, expected)

    # Dec 13, 2016 is adhoc late open
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2016-12-13 11:20', '2016-12-13 12:00', '2016-12-14 09:00', '2016-12-14 11:40',
                                  '2016-12-15 09:00', '2016-12-15 12:00']])
    schedule = cal.schedule('2016-12-13', '2016-12-15')
    actual = mcal.date_range(schedule, '1D', force_close=True, closed=None)

    assert_index_equal(actual, expected)

    # closed == "left" and force_close= True, should return the same thing
    actual = mcal.date_range(schedule, '1D', force_close=True, closed="left")
    assert_index_equal(actual, expected)




def test_date_range_lower_freq():
    cal = mcal.get_calendar("NYSE")
    schedule = cal.schedule(pd.Timestamp('2017-09-05 20:00', tz='UTC'), pd.Timestamp('2017-10-23 20:00', tz='UTC'))

    # cannot get date range of frequency lower than 1D
    with pytest.raises(ValueError) as e:
        mcal.date_range(schedule, frequency='3D')
    assert e.exconly() == "ValueError: Frequency must be 1D or higher frequency."

    # instead get for 1D and convert to lower frequency
    short = mcal.date_range(schedule, frequency='1D')
    actual = mcal.convert_freq(short, '3D')
    expected = pd.date_range('2017-09-05 20:00', '2017-10-23 20:00', freq='3D', tz='UTC')
    assert_index_equal(actual, expected)

    actual = mcal.convert_freq(short, '1W')
    expected = pd.date_range('2017-09-05 20:00', '2017-10-23 20:00', freq='1W', tz='UTC')
    assert_index_equal(actual, expected)


def test_date_range_hour():
    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(10, 30))

    # New Years Eve and weekend skipped
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2015-12-31 10:00', '2015-12-31 10:30',
                                  '2016-01-04 10:00', '2016-01-04 10:30',
                                  '2016-01-05 10:00', '2016-01-05 10:30',
                                  '2016-01-06 10:00', '2016-01-06 10:30']])
    schedule = cal.schedule('2015-12-31', '2016-01-06')
    actual = mcal.date_range(schedule, '1H', force_close=True)

    assert_index_equal(actual, expected)

    # If force_close False for then result is missing close if not on even increment
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2015-12-31 10:00', '2016-01-04 10:00', '2016-01-05 10:00', '2016-01-06 10:00']])
    schedule = cal.schedule('2015-12-31', '2016-01-06')
    actual = mcal.date_range(schedule, '1H', force_close=False)

    assert_index_equal(actual, expected)

    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(12, 0))
    # July 3 is late open and early close
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2012-07-02 10:00', '2012-07-02 11:00', '2012-07-02 12:00',
                                  '2012-07-03 11:30',
                                  '2012-07-04 10:00', '2012-07-04 11:00', '2012-07-04 12:00']])
    schedule = cal.schedule('2012-07-02', '2012-07-04')
    actual = mcal.date_range(schedule, '1H')

    assert_index_equal(actual, expected)

    # Dec 14, 2016 is adhoc early close
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2016-12-14 10:00', '2016-12-14 11:00', '2016-12-14 11:40',
                                  '2016-12-15 10:00', '2016-12-15 11:00', '2016-12-15 12:00']])
    schedule = cal.schedule('2016-12-14', '2016-12-15')
    actual = mcal.date_range(schedule, '1H')

    assert_index_equal(actual, expected)

    # Dec 13, 2016 is adhoc late open, include the open with closed=True
    expected = pd.DatetimeIndex([pd.Timestamp(x, tz=cal.tz).tz_convert('UTC') for x in
                                 ['2016-12-13 11:20', '2016-12-13 12:00',
                                  '2016-12-14 09:00', '2016-12-14 10:00', '2016-12-14 11:00', '2016-12-14 11:40']])
    schedule = cal.schedule('2016-12-13', '2016-12-14')
    actual = mcal.date_range(schedule, '1H', closed=None)

    assert_index_equal(actual, expected)


def test_date_range_minute():
    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(10, 30))

    # New Years Eve and weekend skipped
    schedule = cal.schedule('2015-12-31', '2016-01-06')
    actual = mcal.date_range(schedule, '1min', force_close=True)
    assert len(actual) == 4 * 90
    assert actual[0] == pd.Timestamp('2015-12-31 09:01', tz=cal.tz)
    assert actual[len(actual) - 1] == pd.Timestamp('2016-01-06 10:30', tz=cal.tz)

    for x in ['2015-12-31 09:02', '2015-12-31 10:30', '2016-01-04 09:01', '2016-01-06 09:01']:
        assert pd.Timestamp(x, tz=cal.tz) in actual

    for x in ['2015-12-31 09:00', '2015-12-31 10:31', '2016-01-02 09:01', '2016-01-03 09:01', '2016-01-06 09:00']:
        assert pd.Timestamp(x, tz=cal.tz) not in actual

    # July 3 is late open and early close
    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(12, 0))
    schedule = cal.schedule('2012-07-02', '2012-07-04')
    actual = mcal.date_range(schedule, '1min')
    assert len(actual) == 375  # 2 days of 3 hours, and one day of 15 mins
    assert actual[0] == pd.Timestamp('2012-07-02 09:01', tz=cal.tz)
    assert actual[len(actual) - 1] == pd.Timestamp('2012-07-04 12:00', tz=cal.tz)

    for x in ['2012-07-02 09:02', '2012-07-02 12:00', '2012-07-03 11:16', '2012-07-03 11:30', '2012-07-04 09:01']:
        assert pd.Timestamp(x, tz=cal.tz) in actual

    for x in ['2012-07-02 09:00', '2012-07-02 12:01', '2012-07-03 11:15', '2012-07-03 11:31', '2012-07-04 09:00']:
        assert pd.Timestamp(x, tz=cal.tz) not in actual

    # Dec 13, 2016 is ad-hoc late open, include the open with closed=True, Dec 14 is ad-hoc early close
    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(12, 0))
    schedule = cal.schedule('2016-12-13', '2016-12-14')
    actual = mcal.date_range(schedule, '1min', closed=None)

    assert len(actual) == 41 + (61 + 60 + 40)
    assert actual[0] == pd.Timestamp('2016-12-13 11:20', tz=cal.tz)
    assert actual[len(actual) - 1] == pd.Timestamp('2016-12-14 11:40', tz=cal.tz)

    for x in ['2016-12-13 11:21', '2016-12-13 12:00', '2016-12-14 09:00']:
        assert pd.Timestamp(x, tz=cal.tz) in actual

    for x in ['2016-12-13 11:19', '2016-12-13 12:01', '2016-12-14 08:59', '2016-12-14 11:41']:
        assert pd.Timestamp(x, tz=cal.tz) not in actual


def test_date_range_w_breaks():
    cal = FakeBreakCalendar()
    schedule = cal.schedule('2016-12-28', '2016-12-28')

    with pytest.warns(UserWarning):
        mcal.date_range(schedule, "1H", closed= "right", force_close= False)

    expected = ['2016-12-28 14:30:00+00:00', '2016-12-28 15:00:00+00:00',
                '2016-12-28 16:00:00+00:00', '2016-12-28 16:30:00+00:00', '2016-12-28 17:00:00+00:00']
    actual = mcal.date_range(schedule, '30min', closed=None)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    expected = ['2016-12-28 15:00:00+00:00', '2016-12-28 16:30:00+00:00', '2016-12-28 17:00:00+00:00']
    actual = mcal.date_range(schedule, '30min', closed='right')
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    expected = ['2016-12-28 14:30:00+00:00', '2016-12-28 16:00:00+00:00', '2016-12-28 16:30:00+00:00']
    actual = mcal.date_range(schedule, '30min', closed='left', force_close=False)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    expected = ['2016-12-28 14:30:00+00:00', '2016-12-28 15:00:00+00:00', '2016-12-28 16:00:00+00:00',
                '2016-12-28 16:30:00+00:00', '2016-12-28 17:00:00+00:00']
    actual = mcal.date_range(schedule, '30min', closed='left', force_close=True)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    # when the open is the break start
    schedule = cal.schedule('2016-12-29', '2016-12-29')
    expected = ['2016-12-29 16:00:00+00:00', '2016-12-29 16:15:00+00:00', '2016-12-29 16:30:00+00:00',
                '2016-12-29 16:45:00+00:00', '2016-12-29 17:00:00+00:00']
    actual = mcal.date_range(schedule, '15min', closed=None)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    expected = ['2016-12-29 16:15:00+00:00', '2016-12-29 16:30:00+00:00',
                '2016-12-29 16:45:00+00:00', '2016-12-29 17:00:00+00:00']
    actual = mcal.date_range(schedule, '15min', closed='right')
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    # when the close is the break end
    schedule = cal.schedule('2016-12-30', '2016-12-30')

    # force close True
    expected = ['2016-12-30 14:30:00+00:00', '2016-12-30 14:45:00+00:00', '2016-12-30 15:00:00+00:00']
    actual = mcal.date_range(schedule, '15min', closed=None, force_close=True)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    # force close False
    expected = ['2016-12-30 14:30:00+00:00', '2016-12-30 14:45:00+00:00', '2016-12-30 15:00:00+00:00']
    actual = mcal.date_range(schedule, '15min', closed=None, force_close=False)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    expected = ['2016-12-30 14:45:00+00:00', '2016-12-30 15:00:00+00:00']
    actual = mcal.date_range(schedule, '15min', closed='right', force_close=False)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual


def test_merge_schedules():
    cal1 = FakeCalendar()
    cal2 = NYSEExchangeCalendar()

    # cal1 is open on 2016-07-04 and cal2 is not
    sch1 = cal1.schedule('2016-07-01', '2016-07-06')
    sch2 = cal2.schedule('2016-07-01', '2016-07-06')

    # outer join will include July 4th and have
    expected = pd.DataFrame({'market_open': [pd.Timestamp(x, tz='UTC') for x in
                                             ['2016-07-01 02:13', '2016-07-04 02:13',
                                              '2016-07-05 02:13', '2016-07-06 02:13']],
                             'market_close': [pd.Timestamp(x, tz='UTC') for x in
                                              ['2016-07-01 20:00', '2016-07-04 02:49',
                                               '2016-07-05 20:00', '2016-07-06 20:00']]},
                            columns=['market_open', 'market_close'],
                            index=pd.DatetimeIndex(['2016-07-01', '2016-07-04', '2016-07-05', '2016-07-06']))
    actual = mcal.merge_schedules([sch1, sch2], how='outer')
    assert_frame_equal(actual, expected)

    # inner join will exclude July 4th because not open for both
    expected = pd.DataFrame({'market_open': [pd.Timestamp(x, tz='UTC') for x in
                                             ['2016-07-01 13:30', '2016-07-05 13:30', '2016-07-06 13:30']],
                             'market_close': [pd.Timestamp(x, tz='UTC') for x in
                                              ['2016-07-01 02:49', '2016-07-05 02:49', '2016-07-06 02:49']]},
                            columns=['market_open', 'market_close'],
                            index=pd.DatetimeIndex(['2016-07-01', '2016-07-05', '2016-07-06']))
    actual = mcal.merge_schedules([sch1, sch2], how='inner')
    assert_frame_equal(actual, expected)

    # joining more than two calendars works correctly
    actual = mcal.merge_schedules([sch1, sch1, sch1], how='inner')
    assert_frame_equal(actual, sch1)

    with pytest.raises(ValueError):
        mcal.merge_schedules([sch1, sch2], how='left')


def test_merge_schedules_w_break():
    # this currently does not work as all breaks are lost
    cal = FakeCalendar()
    cal_breaks = FakeBreakCalendar()

    schedule = cal.schedule('2016-12-20', '2016-12-30')
    schedule_breaks = cal_breaks.schedule('2016-12-20', '2016-12-30')

    with pytest.warns(Warning) as w:
        result = mcal.merge_schedules([schedule, schedule_breaks])
    assert w[0].message.args[0] == 'Merge schedules will drop the break_start and break_end from result.'

    assert 'break_start' not in result.columns
    assert 'break_end' not in result.columns
