import pandas as pd
from zoneinfo import ZoneInfo
from pandas.testing import assert_index_equal
from pandas.tseries.offsets import CustomBusinessDay

from pandas_market_calendars.calendars.nyse import NYSEExchangeCalendar

nyse = NYSEExchangeCalendar()


def test_time_zone():
    assert nyse.tz == ZoneInfo("America/New_York")
    assert nyse.name == "NYSE"


def test_open_time_tz():
    assert nyse.open_time.tzinfo == nyse.tz


def test_close_time_tz():
    assert nyse.close_time.tzinfo == nyse.tz


def test_weekmask():
    assert nyse.holidays_pre_1952().weekmask == "Mon Tue Wed Thu Fri Sat"


def _test_holidays(holidays, start, end):
    df = pd.DataFrame(nyse.holidays().holidays, columns=["holidays"])
    mask = (df["holidays"] >= start) & (df["holidays"] <= end)
    df = df[mask]
    assert len(holidays) == len(df)
    df = df.set_index(["holidays"])
    df.index = df.index.tz_localize("UTC")
    assert_index_equal(pd.DatetimeIndex(holidays), df.index, check_names=False)
    valid_days = nyse.valid_days(start, end)
    for h in holidays:
        assert h not in valid_days


def _test_no_special_opens(start, end):
    assert len(nyse.late_opens(nyse.schedule(start, end))) == 0


def _test_no_special_closes(start, end):
    assert len(nyse.early_closes(nyse.schedule(start, end))) == 0


def _test_no_special_opens_closes(start, end):
    _test_no_special_opens(start, end)
    _test_no_special_closes(start, end)


def _test_verify_late_open_time(schedule, timestamp):
    date = pd.Timestamp(pd.Timestamp(timestamp).tz_convert("UTC").date())
    if date in schedule.index:
        return schedule.at[date, "market_open"] == timestamp
    else:
        return False


def _test_has_late_opens(late_opens, start, end):
    schedule = nyse.schedule(start, end)
    expected = nyse.late_opens(schedule)
    assert len(expected) == len(late_opens)
    for ts in late_opens:
        assert _test_verify_late_open_time(schedule, ts) is True


def _test_verify_early_close_time(schedule, timestamp):
    date = pd.Timestamp(pd.Timestamp(timestamp).tz_convert("UTC").date())
    if date in schedule.index:
        return schedule.at[date, "market_close"] == timestamp
    else:
        return False


def _test_has_early_closes(early_closes, start, end):
    schedule = nyse.schedule(start, end)
    expected = nyse.early_closes(schedule)
    assert len(expected) == len(early_closes)
    for ts in early_closes:
        assert _test_verify_early_close_time(schedule, ts) is True


#########################################################################
# YEARLY TESTS BEGIN
#########################################################################
def test_1885():
    start = "1885-01-01"
    end = "1885-12-31"
    holidays = [
        pd.Timestamp("1885-01-01", tz="UTC"),
        pd.Timestamp("1885-02-23", tz="UTC"),
        pd.Timestamp("1885-04-03", tz="UTC"),
        pd.Timestamp("1885-05-30", tz="UTC"),
        pd.Timestamp("1885-07-04", tz="UTC"),
        pd.Timestamp("1885-08-08", tz="UTC"),
        pd.Timestamp("1885-11-03", tz="UTC"),
        pd.Timestamp("1885-11-26", tz="UTC"),
        pd.Timestamp("1885-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

    # ensure labor day is a valid trading day
    assert pd.Timestamp("1885-09-07", tz="UTC") in nyse.valid_days(start, end)


def test_1886():
    start = "1886-01-01"
    end = "1886-12-31"
    holidays = [
        pd.Timestamp("1886-01-01", tz="UTC"),
        pd.Timestamp("1886-02-22", tz="UTC"),
        pd.Timestamp("1886-04-23", tz="UTC"),
        pd.Timestamp("1886-05-31", tz="UTC"),
        pd.Timestamp("1886-07-05", tz="UTC"),
        pd.Timestamp("1886-11-02", tz="UTC"),
        pd.Timestamp("1886-11-25", tz="UTC"),
        pd.Timestamp("1886-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1887():
    start = "1887-01-01"
    end = "1887-12-31"
    holidays = [
        pd.Timestamp("1887-01-01", tz="UTC"),
        pd.Timestamp("1887-02-22", tz="UTC"),
        pd.Timestamp("1887-04-08", tz="UTC"),
        pd.Timestamp("1887-05-30", tz="UTC"),
        pd.Timestamp("1887-07-02", tz="UTC"),
        pd.Timestamp("1887-07-04", tz="UTC"),
        pd.Timestamp("1887-09-05", tz="UTC"),
        pd.Timestamp("1887-11-08", tz="UTC"),
        pd.Timestamp("1887-11-24", tz="UTC"),
        pd.Timestamp("1887-12-24", tz="UTC"),
        pd.Timestamp("1887-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1888():
    start = "1888-01-01"
    end = "1888-12-31"
    holidays = [
        pd.Timestamp("1888-01-02", tz="UTC"),
        pd.Timestamp("1888-02-22", tz="UTC"),
        pd.Timestamp("1888-03-12", tz="UTC"),
        pd.Timestamp("1888-03-13", tz="UTC"),
        pd.Timestamp("1888-03-30", tz="UTC"),
        pd.Timestamp("1888-05-30", tz="UTC"),
        pd.Timestamp("1888-07-04", tz="UTC"),
        pd.Timestamp("1888-09-01", tz="UTC"),
        pd.Timestamp("1888-09-03", tz="UTC"),
        pd.Timestamp("1888-11-06", tz="UTC"),
        pd.Timestamp("1888-11-29", tz="UTC"),
        pd.Timestamp("1888-11-30", tz="UTC"),
        pd.Timestamp("1888-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1889():
    start = "1889-01-01"
    end = "1889-12-31"
    holidays = [
        pd.Timestamp("1889-01-01", tz="UTC"),
        pd.Timestamp("1889-02-22", tz="UTC"),
        pd.Timestamp("1889-04-19", tz="UTC"),
        pd.Timestamp("1889-04-29", tz="UTC"),
        pd.Timestamp("1889-04-30", tz="UTC"),
        pd.Timestamp("1889-05-01", tz="UTC"),
        pd.Timestamp("1889-05-30", tz="UTC"),
        pd.Timestamp("1889-07-04", tz="UTC"),
        pd.Timestamp("1889-09-02", tz="UTC"),
        pd.Timestamp("1889-11-05", tz="UTC"),
        pd.Timestamp("1889-11-28", tz="UTC"),
        pd.Timestamp("1889-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1890():
    start = "1890-01-01"
    end = "1890-12-31"
    holidays = [
        pd.Timestamp("1890-01-01", tz="UTC"),
        pd.Timestamp("1890-02-22", tz="UTC"),
        pd.Timestamp("1890-04-04", tz="UTC"),
        pd.Timestamp("1890-05-30", tz="UTC"),
        pd.Timestamp("1890-07-04", tz="UTC"),
        pd.Timestamp("1890-07-05", tz="UTC"),
        pd.Timestamp("1890-09-01", tz="UTC"),
        pd.Timestamp("1890-11-04", tz="UTC"),
        pd.Timestamp("1890-11-27", tz="UTC"),
        pd.Timestamp("1890-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1891():
    start = "1891-01-01"
    end = "1891-12-31"
    holidays = [
        pd.Timestamp("1891-01-01", tz="UTC"),
        pd.Timestamp("1891-02-23", tz="UTC"),
        pd.Timestamp("1891-03-27", tz="UTC"),
        pd.Timestamp("1891-05-30", tz="UTC"),
        pd.Timestamp("1891-07-04", tz="UTC"),
        pd.Timestamp("1891-09-07", tz="UTC"),
        pd.Timestamp("1891-11-03", tz="UTC"),
        pd.Timestamp("1891-11-26", tz="UTC"),
        pd.Timestamp("1891-12-25", tz="UTC"),
        pd.Timestamp("1891-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1892():
    start = "1892-01-01"
    end = "1892-12-31"
    holidays = [
        pd.Timestamp("1892-01-01", tz="UTC"),
        pd.Timestamp("1892-02-22", tz="UTC"),
        pd.Timestamp("1892-04-15", tz="UTC"),
        pd.Timestamp("1892-05-30", tz="UTC"),
        pd.Timestamp("1892-07-02", tz="UTC"),
        pd.Timestamp("1892-07-04", tz="UTC"),
        pd.Timestamp("1892-09-05", tz="UTC"),
        pd.Timestamp("1892-10-12", tz="UTC"),
        pd.Timestamp("1892-10-21", tz="UTC"),
        pd.Timestamp("1892-10-22", tz="UTC"),
        pd.Timestamp("1892-11-08", tz="UTC"),
        pd.Timestamp("1892-11-24", tz="UTC"),
        pd.Timestamp("1892-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1893():
    start = "1893-01-01"
    end = "1893-12-31"
    holidays = [
        pd.Timestamp("1893-01-02", tz="UTC"),
        pd.Timestamp("1893-02-22", tz="UTC"),
        pd.Timestamp("1893-03-31", tz="UTC"),
        pd.Timestamp("1893-04-27", tz="UTC"),
        pd.Timestamp("1893-05-30", tz="UTC"),
        pd.Timestamp("1893-07-04", tz="UTC"),
        pd.Timestamp("1893-09-04", tz="UTC"),
        pd.Timestamp("1893-11-07", tz="UTC"),
        pd.Timestamp("1893-11-30", tz="UTC"),
        pd.Timestamp("1893-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1894():
    start = "1894-01-01"
    end = "1894-12-31"
    holidays = [
        pd.Timestamp("1894-01-01", tz="UTC"),
        pd.Timestamp("1894-02-22", tz="UTC"),
        pd.Timestamp("1894-03-23", tz="UTC"),
        pd.Timestamp("1894-05-30", tz="UTC"),
        pd.Timestamp("1894-07-04", tz="UTC"),
        pd.Timestamp("1894-09-03", tz="UTC"),
        pd.Timestamp("1894-11-06", tz="UTC"),
        pd.Timestamp("1894-11-29", tz="UTC"),
        pd.Timestamp("1894-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1895():
    start = "1895-01-01"
    end = "1895-12-31"
    holidays = [
        pd.Timestamp("1895-01-01", tz="UTC"),
        pd.Timestamp("1895-02-22", tz="UTC"),
        pd.Timestamp("1895-04-12", tz="UTC"),
        pd.Timestamp("1895-05-30", tz="UTC"),
        pd.Timestamp("1895-07-04", tz="UTC"),
        pd.Timestamp("1895-09-02", tz="UTC"),
        pd.Timestamp("1895-11-05", tz="UTC"),
        pd.Timestamp("1895-11-28", tz="UTC"),
        pd.Timestamp("1895-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1896():
    start = "1896-01-01"
    end = "1896-12-31"
    holidays = [
        pd.Timestamp("1896-01-01", tz="UTC"),
        pd.Timestamp("1896-02-12", tz="UTC"),
        pd.Timestamp("1896-02-22", tz="UTC"),
        pd.Timestamp("1896-04-03", tz="UTC"),
        pd.Timestamp("1896-05-30", tz="UTC"),
        pd.Timestamp("1896-07-04", tz="UTC"),
        pd.Timestamp("1896-09-07", tz="UTC"),
        pd.Timestamp("1896-11-03", tz="UTC"),
        pd.Timestamp("1896-11-26", tz="UTC"),
        pd.Timestamp("1896-12-25", tz="UTC"),
        pd.Timestamp("1896-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1897():
    start = "1897-01-01"
    end = "1897-12-31"
    holidays = [
        pd.Timestamp("1897-01-01", tz="UTC"),
        pd.Timestamp("1897-02-12", tz="UTC"),
        pd.Timestamp("1897-02-22", tz="UTC"),
        pd.Timestamp("1897-04-16", tz="UTC"),
        pd.Timestamp("1897-04-27", tz="UTC"),
        pd.Timestamp("1897-05-31", tz="UTC"),
        pd.Timestamp("1897-07-05", tz="UTC"),
        pd.Timestamp("1897-09-06", tz="UTC"),
        pd.Timestamp("1897-11-02", tz="UTC"),
        pd.Timestamp("1897-11-25", tz="UTC"),
        pd.Timestamp("1897-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1898():
    start = "1898-01-01"
    end = "1898-12-31"
    holidays = [
        pd.Timestamp("1898-01-01", tz="UTC"),
        pd.Timestamp("1898-02-12", tz="UTC"),
        pd.Timestamp("1898-02-22", tz="UTC"),
        pd.Timestamp("1898-05-04", tz="UTC"),
        pd.Timestamp("1898-05-30", tz="UTC"),
        pd.Timestamp("1898-07-02", tz="UTC"),
        pd.Timestamp("1898-07-04", tz="UTC"),
        pd.Timestamp("1898-08-20", tz="UTC"),
        pd.Timestamp("1898-09-03", tz="UTC"),
        pd.Timestamp("1898-09-05", tz="UTC"),
        pd.Timestamp("1898-11-08", tz="UTC"),
        pd.Timestamp("1898-11-24", tz="UTC"),
        pd.Timestamp("1898-12-24", tz="UTC"),
        pd.Timestamp("1898-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1899():
    start = "1899-01-01"
    end = "1899-12-31"
    holidays = [
        pd.Timestamp("1899-01-02", tz="UTC"),
        pd.Timestamp("1899-02-11", tz="UTC"),
        pd.Timestamp("1899-02-13", tz="UTC"),
        pd.Timestamp("1899-02-22", tz="UTC"),
        pd.Timestamp("1899-03-31", tz="UTC"),
        pd.Timestamp("1899-05-29", tz="UTC"),
        pd.Timestamp("1899-05-30", tz="UTC"),
        pd.Timestamp("1899-07-03", tz="UTC"),
        pd.Timestamp("1899-07-04", tz="UTC"),
        pd.Timestamp("1899-09-04", tz="UTC"),
        pd.Timestamp("1899-09-29", tz="UTC"),
        pd.Timestamp("1899-09-30", tz="UTC"),
        pd.Timestamp("1899-11-07", tz="UTC"),
        pd.Timestamp("1899-11-25", tz="UTC"),
        pd.Timestamp("1899-11-30", tz="UTC"),
        pd.Timestamp("1899-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1900():
    start = "1900-01-01"
    end = "1900-12-31"
    holidays = [
        pd.Timestamp("1900-01-01", tz="UTC"),
        pd.Timestamp("1900-02-12", tz="UTC"),
        pd.Timestamp("1900-02-22", tz="UTC"),
        pd.Timestamp("1900-04-13", tz="UTC"),
        pd.Timestamp("1900-04-14", tz="UTC"),
        pd.Timestamp("1900-05-30", tz="UTC"),
        pd.Timestamp("1900-07-04", tz="UTC"),
        pd.Timestamp("1900-09-01", tz="UTC"),
        pd.Timestamp("1900-09-03", tz="UTC"),
        pd.Timestamp("1900-11-06", tz="UTC"),
        pd.Timestamp("1900-11-29", tz="UTC"),
        pd.Timestamp("1900-12-24", tz="UTC"),
        pd.Timestamp("1900-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1901():
    start = "1901-01-01"
    end = "1901-12-31"
    holidays = [
        pd.Timestamp("1901-01-01", tz="UTC"),
        pd.Timestamp("1901-02-02", tz="UTC"),
        pd.Timestamp("1901-02-12", tz="UTC"),
        pd.Timestamp("1901-02-22", tz="UTC"),
        pd.Timestamp("1901-02-23", tz="UTC"),
        pd.Timestamp("1901-04-05", tz="UTC"),
        pd.Timestamp("1901-04-06", tz="UTC"),
        pd.Timestamp("1901-04-27", tz="UTC"),
        pd.Timestamp("1901-05-11", tz="UTC"),
        pd.Timestamp("1901-05-30", tz="UTC"),
        pd.Timestamp("1901-07-04", tz="UTC"),
        pd.Timestamp("1901-07-05", tz="UTC"),
        pd.Timestamp("1901-07-06", tz="UTC"),
        pd.Timestamp("1901-08-31", tz="UTC"),
        pd.Timestamp("1901-09-02", tz="UTC"),
        pd.Timestamp("1901-09-14", tz="UTC"),
        pd.Timestamp("1901-09-19", tz="UTC"),
        pd.Timestamp("1901-11-05", tz="UTC"),
        pd.Timestamp("1901-11-28", tz="UTC"),
        pd.Timestamp("1901-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1902():
    start = "1902-01-01"
    end = "1902-12-31"
    holidays = [
        pd.Timestamp("1902-01-01", tz="UTC"),
        pd.Timestamp("1902-02-12", tz="UTC"),
        pd.Timestamp("1902-02-22", tz="UTC"),
        pd.Timestamp("1902-03-28", tz="UTC"),
        pd.Timestamp("1902-03-29", tz="UTC"),
        pd.Timestamp("1902-05-30", tz="UTC"),
        pd.Timestamp("1902-05-31", tz="UTC"),
        pd.Timestamp("1902-07-04", tz="UTC"),
        pd.Timestamp("1902-07-05", tz="UTC"),
        pd.Timestamp("1902-08-09", tz="UTC"),
        pd.Timestamp("1902-08-30", tz="UTC"),
        pd.Timestamp("1902-09-01", tz="UTC"),
        pd.Timestamp("1902-11-04", tz="UTC"),
        pd.Timestamp("1902-11-27", tz="UTC"),
        pd.Timestamp("1902-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1903():
    start = "1903-01-01"
    end = "1903-12-31"
    holidays = [
        pd.Timestamp("1903-01-01", tz="UTC"),
        pd.Timestamp("1903-02-12", tz="UTC"),
        pd.Timestamp("1903-02-21", tz="UTC"),
        pd.Timestamp("1903-02-23", tz="UTC"),
        pd.Timestamp("1903-04-10", tz="UTC"),
        pd.Timestamp("1903-04-11", tz="UTC"),
        pd.Timestamp("1903-04-22", tz="UTC"),
        pd.Timestamp("1903-05-30", tz="UTC"),
        pd.Timestamp("1903-07-04", tz="UTC"),
        pd.Timestamp("1903-09-05", tz="UTC"),
        pd.Timestamp("1903-09-07", tz="UTC"),
        pd.Timestamp("1903-11-03", tz="UTC"),
        pd.Timestamp("1903-11-26", tz="UTC"),
        pd.Timestamp("1903-12-25", tz="UTC"),
        pd.Timestamp("1903-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1904():
    start = "1904-01-01"
    end = "1904-12-31"
    holidays = [
        pd.Timestamp("1904-01-01", tz="UTC"),
        pd.Timestamp("1904-02-12", tz="UTC"),
        pd.Timestamp("1904-02-22", tz="UTC"),
        pd.Timestamp("1904-04-01", tz="UTC"),
        pd.Timestamp("1904-05-28", tz="UTC"),
        pd.Timestamp("1904-05-30", tz="UTC"),
        pd.Timestamp("1904-07-02", tz="UTC"),
        pd.Timestamp("1904-07-04", tz="UTC"),
        pd.Timestamp("1904-09-03", tz="UTC"),
        pd.Timestamp("1904-09-05", tz="UTC"),
        pd.Timestamp("1904-11-08", tz="UTC"),
        pd.Timestamp("1904-11-24", tz="UTC"),
        pd.Timestamp("1904-12-24", tz="UTC"),
        pd.Timestamp("1904-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1905():
    start = "1905-01-01"
    end = "1905-12-31"
    holidays = [
        pd.Timestamp("1905-01-02", tz="UTC"),
        pd.Timestamp("1905-02-13", tz="UTC"),
        pd.Timestamp("1905-02-22", tz="UTC"),
        pd.Timestamp("1905-04-21", tz="UTC"),
        pd.Timestamp("1905-04-22", tz="UTC"),
        pd.Timestamp("1905-05-30", tz="UTC"),
        pd.Timestamp("1905-07-04", tz="UTC"),
        pd.Timestamp("1905-09-04", tz="UTC"),
        pd.Timestamp("1905-11-07", tz="UTC"),
        pd.Timestamp("1905-11-30", tz="UTC"),
        pd.Timestamp("1905-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1906():
    start = "1906-01-01"
    end = "1906-12-31"
    holidays = [
        pd.Timestamp("1906-01-01", tz="UTC"),
        pd.Timestamp("1906-02-12", tz="UTC"),
        pd.Timestamp("1906-02-22", tz="UTC"),
        pd.Timestamp("1906-05-30", tz="UTC"),
        pd.Timestamp("1906-07-04", tz="UTC"),
        pd.Timestamp("1906-09-03", tz="UTC"),
        pd.Timestamp("1906-11-06", tz="UTC"),
        pd.Timestamp("1906-11-29", tz="UTC"),
        pd.Timestamp("1906-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1907():
    start = "1907-01-01"
    end = "1907-12-31"
    holidays = [
        pd.Timestamp("1907-01-01", tz="UTC"),
        pd.Timestamp("1907-02-12", tz="UTC"),
        pd.Timestamp("1907-02-22", tz="UTC"),
        pd.Timestamp("1907-02-23", tz="UTC"),
        pd.Timestamp("1907-03-30", tz="UTC"),
        pd.Timestamp("1907-05-30", tz="UTC"),
        pd.Timestamp("1907-07-04", tz="UTC"),
        pd.Timestamp("1907-08-31", tz="UTC"),
        pd.Timestamp("1907-09-02", tz="UTC"),
        pd.Timestamp("1907-11-05", tz="UTC"),
        pd.Timestamp("1907-11-28", tz="UTC"),
        pd.Timestamp("1907-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1908():
    start = "1908-01-01"
    end = "1908-12-31"
    holidays = [
        pd.Timestamp("1908-01-01", tz="UTC"),
        pd.Timestamp("1908-02-12", tz="UTC"),
        pd.Timestamp("1908-02-22", tz="UTC"),
        pd.Timestamp("1908-04-17", tz="UTC"),
        pd.Timestamp("1908-04-18", tz="UTC"),
        pd.Timestamp("1908-05-30", tz="UTC"),
        pd.Timestamp("1908-07-04", tz="UTC"),
        pd.Timestamp("1908-09-05", tz="UTC"),
        pd.Timestamp("1908-09-07", tz="UTC"),
        pd.Timestamp("1908-11-03", tz="UTC"),
        pd.Timestamp("1908-11-26", tz="UTC"),
        pd.Timestamp("1908-12-25", tz="UTC"),
        pd.Timestamp("1908-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1908-06-26 1:00PM", tz="America/New_York")
    ]  # Grover Cleveland funeral
    _test_has_early_closes(early_closes, start, end)


def test_1909():
    start = "1909-01-01"
    end = "1909-12-31"
    holidays = [
        pd.Timestamp("1909-01-01", tz="UTC"),
        pd.Timestamp("1909-02-12", tz="UTC"),
        pd.Timestamp("1909-02-13", tz="UTC"),
        pd.Timestamp("1909-02-22", tz="UTC"),
        pd.Timestamp("1909-04-09", tz="UTC"),
        pd.Timestamp("1909-04-10", tz="UTC"),
        pd.Timestamp("1909-05-29", tz="UTC"),
        pd.Timestamp("1909-05-31", tz="UTC"),
        pd.Timestamp("1909-07-03", tz="UTC"),
        pd.Timestamp("1909-07-05", tz="UTC"),
        pd.Timestamp("1909-09-04", tz="UTC"),
        pd.Timestamp("1909-09-06", tz="UTC"),
        pd.Timestamp("1909-09-25", tz="UTC"),
        pd.Timestamp("1909-10-12", tz="UTC"),
        pd.Timestamp("1909-11-02", tz="UTC"),
        pd.Timestamp("1909-11-25", tz="UTC"),
        pd.Timestamp("1909-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1910():
    start = "1910-01-01"
    end = "1910-12-31"
    holidays = [
        pd.Timestamp("1910-01-01", tz="UTC"),
        pd.Timestamp("1910-02-12", tz="UTC"),
        pd.Timestamp("1910-02-22", tz="UTC"),
        pd.Timestamp("1910-03-25", tz="UTC"),
        pd.Timestamp("1910-03-26", tz="UTC"),
        pd.Timestamp("1910-05-28", tz="UTC"),
        pd.Timestamp("1910-05-30", tz="UTC"),
        pd.Timestamp("1910-07-02", tz="UTC"),
        pd.Timestamp("1910-07-04", tz="UTC"),
        pd.Timestamp("1910-09-03", tz="UTC"),
        pd.Timestamp("1910-09-05", tz="UTC"),
        pd.Timestamp("1910-10-12", tz="UTC"),
        pd.Timestamp("1910-11-08", tz="UTC"),
        pd.Timestamp("1910-11-24", tz="UTC"),
        pd.Timestamp("1910-12-24", tz="UTC"),
        pd.Timestamp("1910-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes:
    early_closes = [pd.Timestamp("1910-05-07 11:00AM", tz="America/New_York")]  # King Edward VII death
    _test_has_early_closes(early_closes, start, end)

    # late opens:
    late_opens = [pd.Timestamp("1910-05-20 12:00PM", tz="America/New_York")]  # King Edward VII funderal
    _test_has_late_opens(late_opens, start, end)


def test_1911():
    start = "1911-01-01"
    end = "1911-12-31"
    holidays = [
        pd.Timestamp("1911-01-02", tz="UTC"),
        pd.Timestamp("1911-02-13", tz="UTC"),
        pd.Timestamp("1911-02-22", tz="UTC"),
        pd.Timestamp("1911-04-14", tz="UTC"),
        pd.Timestamp("1911-04-15", tz="UTC"),
        pd.Timestamp("1911-05-30", tz="UTC"),
        pd.Timestamp("1911-07-04", tz="UTC"),
        pd.Timestamp("1911-09-02", tz="UTC"),
        pd.Timestamp("1911-09-04", tz="UTC"),
        pd.Timestamp("1911-10-12", tz="UTC"),
        pd.Timestamp("1911-11-07", tz="UTC"),
        pd.Timestamp("1911-11-30", tz="UTC"),
        pd.Timestamp("1911-12-23", tz="UTC"),
        pd.Timestamp("1911-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1912():
    start = "1912-01-01"
    end = "1912-12-31"
    holidays = [
        pd.Timestamp("1912-01-01", tz="UTC"),
        pd.Timestamp("1912-02-12", tz="UTC"),
        pd.Timestamp("1912-02-22", tz="UTC"),
        pd.Timestamp("1912-04-05", tz="UTC"),
        pd.Timestamp("1912-05-30", tz="UTC"),
        pd.Timestamp("1912-07-04", tz="UTC"),
        pd.Timestamp("1912-08-31", tz="UTC"),
        pd.Timestamp("1912-09-02", tz="UTC"),
        pd.Timestamp("1912-10-12", tz="UTC"),
        pd.Timestamp("1912-11-02", tz="UTC"),
        pd.Timestamp("1912-11-05", tz="UTC"),
        pd.Timestamp("1912-11-28", tz="UTC"),
        pd.Timestamp("1912-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1913():
    start = "1913-01-01"
    end = "1913-12-31"
    holidays = [
        pd.Timestamp("1913-01-01", tz="UTC"),
        pd.Timestamp("1913-02-12", tz="UTC"),
        pd.Timestamp("1913-02-22", tz="UTC"),
        pd.Timestamp("1913-03-21", tz="UTC"),
        pd.Timestamp("1913-03-22", tz="UTC"),
        pd.Timestamp("1913-05-30", tz="UTC"),
        pd.Timestamp("1913-05-31", tz="UTC"),
        pd.Timestamp("1913-07-04", tz="UTC"),
        pd.Timestamp("1913-07-05", tz="UTC"),
        pd.Timestamp("1913-08-30", tz="UTC"),
        pd.Timestamp("1913-09-01", tz="UTC"),
        pd.Timestamp("1913-10-13", tz="UTC"),
        pd.Timestamp("1913-11-04", tz="UTC"),
        pd.Timestamp("1913-11-27", tz="UTC"),
        pd.Timestamp("1913-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_closes(start, end)

    # late opens:
    late_opens = [
        pd.Timestamp("1913-04-14 12:00PM", tz="America/New_York"),  # JP Morgan Funeral
        pd.Timestamp("1913-09-22 12:00PM", tz="America/New_York"),  # Mayor William J. Gaynor Funeral
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1914():
    start = "1914-01-01"
    end = "1914-12-31"
    holidays = [
        pd.Timestamp("1914-01-01", tz="UTC"),
        pd.Timestamp("1914-02-12", tz="UTC"),
        pd.Timestamp("1914-02-23", tz="UTC"),
        pd.Timestamp("1914-04-10", tz="UTC"),
        pd.Timestamp("1914-05-30", tz="UTC"),
        pd.Timestamp("1914-07-04", tz="UTC"),
        pd.Timestamp("1914-07-31", tz="UTC"),
        pd.Timestamp("1914-08-01", tz="UTC"),
        pd.Timestamp("1914-08-03", tz="UTC"),
        pd.Timestamp("1914-08-04", tz="UTC"),
        pd.Timestamp("1914-08-05", tz="UTC"),
        pd.Timestamp("1914-08-06", tz="UTC"),
        pd.Timestamp("1914-08-07", tz="UTC"),
        pd.Timestamp("1914-08-08", tz="UTC"),
        pd.Timestamp("1914-08-10", tz="UTC"),
        pd.Timestamp("1914-08-11", tz="UTC"),
        pd.Timestamp("1914-08-12", tz="UTC"),
        pd.Timestamp("1914-08-13", tz="UTC"),
        pd.Timestamp("1914-08-14", tz="UTC"),
        pd.Timestamp("1914-08-15", tz="UTC"),
        pd.Timestamp("1914-08-17", tz="UTC"),
        pd.Timestamp("1914-08-18", tz="UTC"),
        pd.Timestamp("1914-08-19", tz="UTC"),
        pd.Timestamp("1914-08-20", tz="UTC"),
        pd.Timestamp("1914-08-21", tz="UTC"),
        pd.Timestamp("1914-08-22", tz="UTC"),
        pd.Timestamp("1914-08-24", tz="UTC"),
        pd.Timestamp("1914-08-25", tz="UTC"),
        pd.Timestamp("1914-08-26", tz="UTC"),
        pd.Timestamp("1914-08-27", tz="UTC"),
        pd.Timestamp("1914-08-28", tz="UTC"),
        pd.Timestamp("1914-08-29", tz="UTC"),
        pd.Timestamp("1914-08-31", tz="UTC"),
        pd.Timestamp("1914-09-01", tz="UTC"),
        pd.Timestamp("1914-09-02", tz="UTC"),
        pd.Timestamp("1914-09-03", tz="UTC"),
        pd.Timestamp("1914-09-04", tz="UTC"),
        pd.Timestamp("1914-09-05", tz="UTC"),
        pd.Timestamp("1914-09-07", tz="UTC"),
        pd.Timestamp("1914-09-07", tz="UTC"),
        pd.Timestamp("1914-09-08", tz="UTC"),
        pd.Timestamp("1914-09-09", tz="UTC"),
        pd.Timestamp("1914-09-10", tz="UTC"),
        pd.Timestamp("1914-09-11", tz="UTC"),
        pd.Timestamp("1914-09-12", tz="UTC"),
        pd.Timestamp("1914-09-14", tz="UTC"),
        pd.Timestamp("1914-09-15", tz="UTC"),
        pd.Timestamp("1914-09-16", tz="UTC"),
        pd.Timestamp("1914-09-17", tz="UTC"),
        pd.Timestamp("1914-09-18", tz="UTC"),
        pd.Timestamp("1914-09-19", tz="UTC"),
        pd.Timestamp("1914-09-21", tz="UTC"),
        pd.Timestamp("1914-09-22", tz="UTC"),
        pd.Timestamp("1914-09-23", tz="UTC"),
        pd.Timestamp("1914-09-24", tz="UTC"),
        pd.Timestamp("1914-09-25", tz="UTC"),
        pd.Timestamp("1914-09-26", tz="UTC"),
        pd.Timestamp("1914-09-28", tz="UTC"),
        pd.Timestamp("1914-09-29", tz="UTC"),
        pd.Timestamp("1914-09-30", tz="UTC"),
        pd.Timestamp("1914-10-01", tz="UTC"),
        pd.Timestamp("1914-10-02", tz="UTC"),
        pd.Timestamp("1914-10-03", tz="UTC"),
        pd.Timestamp("1914-10-05", tz="UTC"),
        pd.Timestamp("1914-10-06", tz="UTC"),
        pd.Timestamp("1914-10-07", tz="UTC"),
        pd.Timestamp("1914-10-08", tz="UTC"),
        pd.Timestamp("1914-10-09", tz="UTC"),
        pd.Timestamp("1914-10-10", tz="UTC"),
        pd.Timestamp("1914-10-12", tz="UTC"),
        pd.Timestamp("1914-10-12", tz="UTC"),
        pd.Timestamp("1914-10-13", tz="UTC"),
        pd.Timestamp("1914-10-14", tz="UTC"),
        pd.Timestamp("1914-10-15", tz="UTC"),
        pd.Timestamp("1914-10-16", tz="UTC"),
        pd.Timestamp("1914-10-17", tz="UTC"),
        pd.Timestamp("1914-10-19", tz="UTC"),
        pd.Timestamp("1914-10-20", tz="UTC"),
        pd.Timestamp("1914-10-21", tz="UTC"),
        pd.Timestamp("1914-10-22", tz="UTC"),
        pd.Timestamp("1914-10-23", tz="UTC"),
        pd.Timestamp("1914-10-24", tz="UTC"),
        pd.Timestamp("1914-10-26", tz="UTC"),
        pd.Timestamp("1914-10-27", tz="UTC"),
        pd.Timestamp("1914-10-28", tz="UTC"),
        pd.Timestamp("1914-10-29", tz="UTC"),
        pd.Timestamp("1914-10-30", tz="UTC"),
        pd.Timestamp("1914-10-31", tz="UTC"),
        pd.Timestamp("1914-11-02", tz="UTC"),
        pd.Timestamp("1914-11-03", tz="UTC"),
        pd.Timestamp("1914-11-03", tz="UTC"),
        pd.Timestamp("1914-11-04", tz="UTC"),
        pd.Timestamp("1914-11-05", tz="UTC"),
        pd.Timestamp("1914-11-06", tz="UTC"),
        pd.Timestamp("1914-11-07", tz="UTC"),
        pd.Timestamp("1914-11-09", tz="UTC"),
        pd.Timestamp("1914-11-10", tz="UTC"),
        pd.Timestamp("1914-11-11", tz="UTC"),
        pd.Timestamp("1914-11-12", tz="UTC"),
        pd.Timestamp("1914-11-13", tz="UTC"),
        pd.Timestamp("1914-11-14", tz="UTC"),
        pd.Timestamp("1914-11-16", tz="UTC"),
        pd.Timestamp("1914-11-17", tz="UTC"),
        pd.Timestamp("1914-11-18", tz="UTC"),
        pd.Timestamp("1914-11-19", tz="UTC"),
        pd.Timestamp("1914-11-20", tz="UTC"),
        pd.Timestamp("1914-11-21", tz="UTC"),
        pd.Timestamp("1914-11-23", tz="UTC"),
        pd.Timestamp("1914-11-24", tz="UTC"),
        pd.Timestamp("1914-11-25", tz="UTC"),
        pd.Timestamp("1914-11-26", tz="UTC"),
        pd.Timestamp("1914-11-26", tz="UTC"),
        pd.Timestamp("1914-11-27", tz="UTC"),
        pd.Timestamp("1914-11-28", tz="UTC"),
        pd.Timestamp("1914-11-30", tz="UTC"),
        pd.Timestamp("1914-12-01", tz="UTC"),
        pd.Timestamp("1914-12-02", tz="UTC"),
        pd.Timestamp("1914-12-03", tz="UTC"),
        pd.Timestamp("1914-12-04", tz="UTC"),
        pd.Timestamp("1914-12-05", tz="UTC"),
        pd.Timestamp("1914-12-07", tz="UTC"),
        pd.Timestamp("1914-12-08", tz="UTC"),
        pd.Timestamp("1914-12-09", tz="UTC"),
        pd.Timestamp("1914-12-10", tz="UTC"),
        pd.Timestamp("1914-12-11", tz="UTC"),
        pd.Timestamp("1914-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1915():
    start = "1915-01-01"
    end = "1915-12-31"
    holidays = [
        pd.Timestamp("1915-01-01", tz="UTC"),
        pd.Timestamp("1915-02-12", tz="UTC"),
        pd.Timestamp("1915-02-22", tz="UTC"),
        pd.Timestamp("1915-04-02", tz="UTC"),
        pd.Timestamp("1915-05-31", tz="UTC"),
        pd.Timestamp("1915-07-05", tz="UTC"),
        pd.Timestamp("1915-09-06", tz="UTC"),
        pd.Timestamp("1915-10-12", tz="UTC"),
        pd.Timestamp("1915-11-02", tz="UTC"),
        pd.Timestamp("1915-11-25", tz="UTC"),
        pd.Timestamp("1915-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1916():
    start = "1916-01-01"
    end = "1916-12-31"
    holidays = [
        pd.Timestamp("1916-01-01", tz="UTC"),
        pd.Timestamp("1916-02-12", tz="UTC"),
        pd.Timestamp("1916-02-22", tz="UTC"),
        pd.Timestamp("1916-04-21", tz="UTC"),
        pd.Timestamp("1916-05-30", tz="UTC"),
        pd.Timestamp("1916-07-04", tz="UTC"),
        pd.Timestamp("1916-09-04", tz="UTC"),
        pd.Timestamp("1916-10-12", tz="UTC"),
        pd.Timestamp("1916-11-07", tz="UTC"),
        pd.Timestamp("1916-11-30", tz="UTC"),
        pd.Timestamp("1916-12-25", tz="UTC"),
        pd.Timestamp("1916-12-30", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1917():
    start = "1917-01-01"
    end = "1917-12-31"
    holidays = [
        pd.Timestamp("1917-01-01", tz="UTC"),
        pd.Timestamp("1917-02-12", tz="UTC"),
        pd.Timestamp("1917-02-22", tz="UTC"),
        pd.Timestamp("1917-04-06", tz="UTC"),
        pd.Timestamp("1917-05-30", tz="UTC"),
        pd.Timestamp("1917-06-05", tz="UTC"),
        pd.Timestamp("1917-07-04", tz="UTC"),
        pd.Timestamp("1917-08-04", tz="UTC"),
        pd.Timestamp("1917-09-01", tz="UTC"),
        pd.Timestamp("1917-09-03", tz="UTC"),
        pd.Timestamp("1917-10-12", tz="UTC"),
        pd.Timestamp("1917-10-13", tz="UTC"),
        pd.Timestamp("1917-11-06", tz="UTC"),
        pd.Timestamp("1917-11-29", tz="UTC"),
        pd.Timestamp("1917-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp(" 1917-08-29 12:00PM", tz="America/New_York"),  # Parade of National Guard
        pd.Timestamp(" 1917-10-24 12:00PM", tz="America/New_York"),  # Liberty Day
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1918():
    start = "1918-01-01"
    end = "1918-12-31"
    holidays = [
        pd.Timestamp("1918-01-01", tz="UTC"),
        pd.Timestamp("1918-01-28", tz="UTC"),
        pd.Timestamp("1918-02-04", tz="UTC"),
        pd.Timestamp("1918-02-11", tz="UTC"),
        pd.Timestamp("1918-02-12", tz="UTC"),
        pd.Timestamp("1918-02-22", tz="UTC"),
        pd.Timestamp("1918-03-29", tz="UTC"),
        pd.Timestamp("1918-05-30", tz="UTC"),
        pd.Timestamp("1918-07-04", tz="UTC"),
        pd.Timestamp("1918-09-02", tz="UTC"),
        pd.Timestamp("1918-09-12", tz="UTC"),
        pd.Timestamp("1918-10-12", tz="UTC"),
        pd.Timestamp("1918-11-05", tz="UTC"),
        pd.Timestamp("1918-11-11", tz="UTC"),
        pd.Timestamp("1918-11-28", tz="UTC"),
        pd.Timestamp("1918-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1918-04-26 12:00PM", tz="America/New_York"),  # Liberty Day
        pd.Timestamp("1918-11-07 2:30PM", tz="America/New_York"),  # False armistice report
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1919():
    start = "1919-01-01"
    end = "1919-12-31"
    holidays = [
        pd.Timestamp("1919-01-01", tz="UTC"),
        pd.Timestamp("1919-02-12", tz="UTC"),
        pd.Timestamp("1919-02-22", tz="UTC"),
        pd.Timestamp("1919-03-25", tz="UTC"),
        pd.Timestamp("1919-04-18", tz="UTC"),
        pd.Timestamp("1919-05-06", tz="UTC"),
        pd.Timestamp("1919-05-30", tz="UTC"),
        pd.Timestamp("1919-05-31", tz="UTC"),
        pd.Timestamp("1919-07-04", tz="UTC"),
        pd.Timestamp("1919-07-05", tz="UTC"),
        pd.Timestamp("1919-07-19", tz="UTC"),
        pd.Timestamp("1919-08-02", tz="UTC"),
        pd.Timestamp("1919-08-16", tz="UTC"),
        pd.Timestamp("1919-08-30", tz="UTC"),
        pd.Timestamp("1919-09-01", tz="UTC"),
        pd.Timestamp("1919-09-10", tz="UTC"),
        pd.Timestamp("1919-10-13", tz="UTC"),
        pd.Timestamp("1919-11-04", tz="UTC"),
        pd.Timestamp("1919-11-27", tz="UTC"),
        pd.Timestamp("1919-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [pd.Timestamp("1919-01-07 12:30PM", tz="America/New_York")]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1919-12-30 10:30AM", tz="America/New_York"),  # Traffic block
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1920():
    start = "1920-01-01"
    end = "1920-12-31"
    holidays = [
        pd.Timestamp("1920-01-01", tz="UTC"),
        pd.Timestamp("1920-02-12", tz="UTC"),
        pd.Timestamp("1920-02-23", tz="UTC"),
        pd.Timestamp("1920-04-02", tz="UTC"),
        pd.Timestamp("1920-04-03", tz="UTC"),
        pd.Timestamp("1920-05-01", tz="UTC"),
        pd.Timestamp("1920-05-31", tz="UTC"),
        pd.Timestamp("1920-07-03", tz="UTC"),
        pd.Timestamp("1920-07-05", tz="UTC"),
        pd.Timestamp("1920-09-04", tz="UTC"),
        pd.Timestamp("1920-09-06", tz="UTC"),
        pd.Timestamp("1920-10-12", tz="UTC"),
        pd.Timestamp("1920-11-02", tz="UTC"),
        pd.Timestamp("1920-11-25", tz="UTC"),
        pd.Timestamp("1920-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [pd.Timestamp("1920-09-16 12:00PM", tz="America/New_York")]  # Wall Street explosion
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1920-02-06 10:30AM", tz="America/New_York"),  # traffic block
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1921():
    start = "1921-01-01"
    end = "1921-12-31"
    holidays = [
        pd.Timestamp("1921-01-01", tz="UTC"),
        pd.Timestamp("1921-02-12", tz="UTC"),
        pd.Timestamp("1921-02-22", tz="UTC"),
        pd.Timestamp("1921-03-25", tz="UTC"),
        pd.Timestamp("1921-05-28", tz="UTC"),
        pd.Timestamp("1921-05-30", tz="UTC"),
        pd.Timestamp("1921-07-02", tz="UTC"),
        pd.Timestamp("1921-07-04", tz="UTC"),
        pd.Timestamp("1921-09-03", tz="UTC"),
        pd.Timestamp("1921-09-05", tz="UTC"),
        pd.Timestamp("1921-10-12", tz="UTC"),
        pd.Timestamp("1921-11-08", tz="UTC"),
        pd.Timestamp("1921-11-11", tz="UTC"),
        pd.Timestamp("1921-11-24", tz="UTC"),
        pd.Timestamp("1921-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_closes(start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1921-08-02 1:00PM", tz="America/New_York"),  # fire in annunciator board
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1922():
    start = "1922-01-01"
    end = "1922-12-31"
    holidays = [
        pd.Timestamp("1922-01-02", tz="UTC"),
        pd.Timestamp("1922-02-13", tz="UTC"),
        pd.Timestamp("1922-02-22", tz="UTC"),
        pd.Timestamp("1922-04-14", tz="UTC"),
        pd.Timestamp("1922-05-30", tz="UTC"),
        pd.Timestamp("1922-07-04", tz="UTC"),
        pd.Timestamp("1922-09-04", tz="UTC"),
        pd.Timestamp("1922-10-12", tz="UTC"),
        pd.Timestamp("1922-11-07", tz="UTC"),
        pd.Timestamp("1922-11-30", tz="UTC"),
        pd.Timestamp("1922-12-23", tz="UTC"),
        pd.Timestamp("1922-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1923():
    start = "1923-01-01"
    end = "1923-12-31"
    holidays = [
        pd.Timestamp("1923-01-01", tz="UTC"),
        pd.Timestamp("1923-02-12", tz="UTC"),
        pd.Timestamp("1923-02-22", tz="UTC"),
        pd.Timestamp("1923-03-30", tz="UTC"),
        pd.Timestamp("1923-05-30", tz="UTC"),
        pd.Timestamp("1923-07-04", tz="UTC"),
        pd.Timestamp("1923-08-03", tz="UTC"),
        pd.Timestamp("1923-08-10", tz="UTC"),
        pd.Timestamp("1923-09-03", tz="UTC"),
        pd.Timestamp("1923-10-12", tz="UTC"),
        pd.Timestamp("1923-11-06", tz="UTC"),
        pd.Timestamp("1923-11-29", tz="UTC"),
        pd.Timestamp("1923-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1924():
    start = "1924-01-01"
    end = "1924-12-31"
    holidays = [
        pd.Timestamp("1924-01-01", tz="UTC"),
        pd.Timestamp("1924-02-12", tz="UTC"),
        pd.Timestamp("1924-02-22", tz="UTC"),
        pd.Timestamp("1924-04-18", tz="UTC"),
        pd.Timestamp("1924-05-30", tz="UTC"),
        pd.Timestamp("1924-05-31", tz="UTC"),
        pd.Timestamp("1924-07-04", tz="UTC"),
        pd.Timestamp("1924-09-01", tz="UTC"),
        pd.Timestamp("1924-10-13", tz="UTC"),
        pd.Timestamp("1924-11-04", tz="UTC"),
        pd.Timestamp("1924-11-27", tz="UTC"),
        pd.Timestamp("1924-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1924-02-06 12:30PM", tz="America/New_York")  # Former President Woodrow Wilson funeral
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1925():
    start = "1925-01-01"
    end = "1925-12-31"
    holidays = [
        pd.Timestamp("1925-01-01", tz="UTC"),
        pd.Timestamp("1925-02-12", tz="UTC"),
        pd.Timestamp("1925-02-23", tz="UTC"),
        pd.Timestamp("1925-04-10", tz="UTC"),
        pd.Timestamp("1925-05-30", tz="UTC"),
        pd.Timestamp("1925-07-04", tz="UTC"),
        pd.Timestamp("1925-09-07", tz="UTC"),
        pd.Timestamp("1925-10-12", tz="UTC"),
        pd.Timestamp("1925-11-03", tz="UTC"),
        pd.Timestamp("1925-11-26", tz="UTC"),
        pd.Timestamp("1925-12-25", tz="UTC"),
        pd.Timestamp("1925-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [pd.Timestamp("1925-09-18 2:30PM", tz="America/New_York")]  # Seymour L. Cromwell funeral
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1925-01-24 10:45AM", tz="America/New_York"),  # Eclipse of sun
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1926():
    start = "1926-01-01"
    end = "1926-12-31"
    holidays = [
        pd.Timestamp("1926-01-01", tz="UTC"),
        pd.Timestamp("1926-02-12", tz="UTC"),
        pd.Timestamp("1926-02-22", tz="UTC"),
        pd.Timestamp("1926-04-02", tz="UTC"),
        pd.Timestamp("1926-05-29", tz="UTC"),
        pd.Timestamp("1926-05-31", tz="UTC"),
        pd.Timestamp("1926-07-03", tz="UTC"),
        pd.Timestamp("1926-07-05", tz="UTC"),
        pd.Timestamp("1926-09-04", tz="UTC"),
        pd.Timestamp("1926-09-06", tz="UTC"),
        pd.Timestamp("1926-10-12", tz="UTC"),
        pd.Timestamp("1926-11-02", tz="UTC"),
        pd.Timestamp("1926-11-25", tz="UTC"),
        pd.Timestamp("1926-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1927():
    start = "1927-01-01"
    end = "1927-12-31"
    holidays = [
        pd.Timestamp("1927-01-01", tz="UTC"),
        pd.Timestamp("1927-02-12", tz="UTC"),
        pd.Timestamp("1927-02-22", tz="UTC"),
        pd.Timestamp("1927-04-15", tz="UTC"),
        pd.Timestamp("1927-05-30", tz="UTC"),
        pd.Timestamp("1927-06-13", tz="UTC"),
        pd.Timestamp("1927-07-04", tz="UTC"),
        pd.Timestamp("1927-09-05", tz="UTC"),
        pd.Timestamp("1927-10-12", tz="UTC"),
        pd.Timestamp("1927-11-08", tz="UTC"),
        pd.Timestamp("1927-11-24", tz="UTC"),
        pd.Timestamp("1927-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1928():
    start = "1928-01-01"
    end = "1928-12-31"
    holidays = [
        pd.Timestamp("1928-01-02", tz="UTC"),
        pd.Timestamp("1928-02-13", tz="UTC"),
        pd.Timestamp("1928-02-22", tz="UTC"),
        pd.Timestamp("1928-04-06", tz="UTC"),
        pd.Timestamp("1928-04-07", tz="UTC"),
        pd.Timestamp("1928-04-21", tz="UTC"),
        pd.Timestamp("1928-05-05", tz="UTC"),
        pd.Timestamp("1928-05-12", tz="UTC"),
        pd.Timestamp("1928-05-19", tz="UTC"),
        pd.Timestamp("1928-05-26", tz="UTC"),
        pd.Timestamp("1928-05-30", tz="UTC"),
        pd.Timestamp("1928-07-04", tz="UTC"),
        pd.Timestamp("1928-09-03", tz="UTC"),
        pd.Timestamp("1928-10-12", tz="UTC"),
        pd.Timestamp("1928-11-06", tz="UTC"),
        pd.Timestamp("1928-11-24", tz="UTC"),
        pd.Timestamp("1928-11-29", tz="UTC"),
        pd.Timestamp("1928-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = pd.date_range(
        "1928-05-21 2:00PM",  # Backlog catch up
        "1928-05-25 2:00PM",
        freq=CustomBusinessDay(weekmask="Mon Tue Wed Thu Fri Sat"),
        tz="America/New_York",
    ).to_list()
    _test_has_early_closes(early_closes, start, end)


def test_1929():
    start = "1929-01-01"
    end = "1929-12-31"
    holidays = [
        pd.Timestamp("1929-01-01", tz="UTC"),
        pd.Timestamp("1929-02-09", tz="UTC"),
        pd.Timestamp("1929-02-12", tz="UTC"),
        pd.Timestamp("1929-02-22", tz="UTC"),
        pd.Timestamp("1929-02-23", tz="UTC"),
        pd.Timestamp("1929-03-29", tz="UTC"),
        pd.Timestamp("1929-03-30", tz="UTC"),
        pd.Timestamp("1929-05-30", tz="UTC"),
        pd.Timestamp("1929-07-04", tz="UTC"),
        pd.Timestamp("1929-08-31", tz="UTC"),
        pd.Timestamp("1929-09-02", tz="UTC"),
        pd.Timestamp("1929-10-12", tz="UTC"),
        pd.Timestamp("1929-11-01", tz="UTC"),
        pd.Timestamp("1929-11-02", tz="UTC"),
        pd.Timestamp("1929-11-05", tz="UTC"),
        pd.Timestamp("1929-11-09", tz="UTC"),
        pd.Timestamp("1929-11-16", tz="UTC"),
        pd.Timestamp("1929-11-23", tz="UTC"),
        pd.Timestamp("1929-11-28", tz="UTC"),
        pd.Timestamp("1929-11-29", tz="UTC"),
        pd.Timestamp("1929-11-30", tz="UTC"),
        pd.Timestamp("1929-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [  # All backlog relief
        pd.Timestamp("1929-11-06 1:00PM", tz="America/New_York"),
        pd.Timestamp("1929-11-07 1:00PM", tz="America/New_York"),
        pd.Timestamp("1929-11-08 1:00PM", tz="America/New_York"),
        pd.Timestamp("1929-11-11 1:00PM", tz="America/New_York"),
        pd.Timestamp("1929-11-12 1:00PM", tz="America/New_York"),
        pd.Timestamp("1929-11-13 1:00PM", tz="America/New_York"),
        pd.Timestamp("1929-11-14 1:00PM", tz="America/New_York"),
        pd.Timestamp("1929-11-15 1:00PM", tz="America/New_York"),
        pd.Timestamp("1929-11-18 1:00PM", tz="America/New_York"),
        pd.Timestamp("1929-11-19 1:00PM", tz="America/New_York"),
        pd.Timestamp("1929-11-20 1:00PM", tz="America/New_York"),
        pd.Timestamp("1929-11-21 1:00PM", tz="America/New_York"),
        pd.Timestamp("1929-11-22 1:00PM", tz="America/New_York"),
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1929-10-31 12:00PM", tz="America/New_York"),  # Backlog relief
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1930():
    start = "1930-01-01"
    end = "1930-12-31"
    holidays = [
        pd.Timestamp("1930-01-01", tz="UTC"),
        pd.Timestamp("1930-02-12", tz="UTC"),
        pd.Timestamp("1930-02-22", tz="UTC"),
        pd.Timestamp("1930-04-18", tz="UTC"),
        pd.Timestamp("1930-04-19", tz="UTC"),
        pd.Timestamp("1930-05-30", tz="UTC"),
        pd.Timestamp("1930-05-31", tz="UTC"),
        pd.Timestamp("1930-07-04", tz="UTC"),
        pd.Timestamp("1930-07-05", tz="UTC"),
        pd.Timestamp("1930-08-30", tz="UTC"),
        pd.Timestamp("1930-09-01", tz="UTC"),
        pd.Timestamp("1930-10-13", tz="UTC"),
        pd.Timestamp("1930-11-04", tz="UTC"),
        pd.Timestamp("1930-11-27", tz="UTC"),
        pd.Timestamp("1930-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1930-03-11 12:30PM", tz="America/New_York"),  # Taft funeral
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1931():
    start = "1931-01-01"
    end = "1931-12-31"
    holidays = [
        pd.Timestamp("1931-01-01", tz="UTC"),
        pd.Timestamp("1931-02-12", tz="UTC"),
        pd.Timestamp("1931-02-23", tz="UTC"),
        pd.Timestamp("1931-04-03", tz="UTC"),
        pd.Timestamp("1931-05-30", tz="UTC"),
        pd.Timestamp("1931-07-04", tz="UTC"),
        pd.Timestamp("1931-09-05", tz="UTC"),
        pd.Timestamp("1931-09-07", tz="UTC"),
        pd.Timestamp("1931-10-12", tz="UTC"),
        pd.Timestamp("1931-11-03", tz="UTC"),
        pd.Timestamp("1931-11-26", tz="UTC"),
        pd.Timestamp("1931-12-25", tz="UTC"),
        pd.Timestamp("1931-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1932():
    start = "1932-01-01"
    end = "1932-12-31"
    holidays = [
        pd.Timestamp("1932-01-01", tz="UTC"),
        pd.Timestamp("1932-02-12", tz="UTC"),
        pd.Timestamp("1932-02-22", tz="UTC"),
        pd.Timestamp("1932-03-25", tz="UTC"),
        pd.Timestamp("1932-05-30", tz="UTC"),
        pd.Timestamp("1932-07-02", tz="UTC"),
        pd.Timestamp("1932-07-04", tz="UTC"),
        pd.Timestamp("1932-09-05", tz="UTC"),
        pd.Timestamp("1932-10-12", tz="UTC"),
        pd.Timestamp("1932-11-08", tz="UTC"),
        pd.Timestamp("1932-11-24", tz="UTC"),
        pd.Timestamp("1932-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1933():
    start = "1933-01-01"
    end = "1933-12-31"
    holidays = [
        pd.Timestamp("1933-01-02", tz="UTC"),
        pd.Timestamp("1933-01-07", tz="UTC"),
        pd.Timestamp("1933-02-13", tz="UTC"),
        pd.Timestamp("1933-02-22", tz="UTC"),
        pd.Timestamp("1933-03-04", tz="UTC"),
        pd.Timestamp("1933-03-06", tz="UTC"),
        pd.Timestamp("1933-03-07", tz="UTC"),
        pd.Timestamp("1933-03-08", tz="UTC"),
        pd.Timestamp("1933-03-09", tz="UTC"),
        pd.Timestamp("1933-03-10", tz="UTC"),
        pd.Timestamp("1933-03-11", tz="UTC"),
        pd.Timestamp("1933-03-12", tz="UTC"),
        pd.Timestamp("1933-03-13", tz="UTC"),
        pd.Timestamp("1933-03-14", tz="UTC"),
        pd.Timestamp("1933-04-14", tz="UTC"),
        pd.Timestamp("1933-05-30", tz="UTC"),
        pd.Timestamp("1933-07-04", tz="UTC"),
        pd.Timestamp("1933-07-29", tz="UTC"),
        pd.Timestamp("1933-08-05", tz="UTC"),
        pd.Timestamp("1933-08-12", tz="UTC"),
        pd.Timestamp("1933-08-19", tz="UTC"),
        pd.Timestamp("1933-08-26", tz="UTC"),
        pd.Timestamp("1933-09-02", tz="UTC"),
        pd.Timestamp("1933-09-04", tz="UTC"),
        pd.Timestamp("1933-10-12", tz="UTC"),
        pd.Timestamp("1933-11-07", tz="UTC"),
        pd.Timestamp("1933-11-30", tz="UTC"),
        pd.Timestamp("1933-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1933-07-26 2:00PM", tz="America/New_York"),  # Volume
        pd.Timestamp("1933-07-27 2:00PM", tz="America/New_York"),  # Volume
        pd.Timestamp("1933-07-28 2:00PM", tz="America/New_York"),  # Volume
        pd.Timestamp("1933-08-04 12:30PM", tz="America/New_York"),  # Volume
        pd.Timestamp("1933-09-13 12:00PM", tz="America/New_York"),  # NRA demonstration
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1933-07-24 12:00PM", tz="America/New_York"),  # Volume
        pd.Timestamp("1933-07-25 12:00PM", tz="America/New_York"),  # Volume
        pd.Timestamp("1933-07-26 11:00AM", tz="America/New_York"),  # Volume
        pd.Timestamp("1933-07-27 11:00AM", tz="America/New_York"),  # Volume
        pd.Timestamp("1933-07-28 11:00AM", tz="America/New_York"),  # Volume
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1934():
    start = "1934-01-01"
    end = "1934-12-31"
    holidays = [
        pd.Timestamp("1934-01-01", tz="UTC"),
        pd.Timestamp("1934-02-12", tz="UTC"),
        pd.Timestamp("1934-02-22", tz="UTC"),
        pd.Timestamp("1934-03-30", tz="UTC"),
        pd.Timestamp("1934-05-30", tz="UTC"),
        pd.Timestamp("1934-07-04", tz="UTC"),
        pd.Timestamp("1934-09-03", tz="UTC"),
        pd.Timestamp("1934-10-12", tz="UTC"),
        pd.Timestamp("1934-11-06", tz="UTC"),
        pd.Timestamp("1934-11-12", tz="UTC"),
        pd.Timestamp("1934-11-29", tz="UTC"),
        pd.Timestamp("1934-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # late opens we expect:
    late_opens = [pd.Timestamp("1934-02-20 11:00AM", tz="America/New_York")]  # snow
    _test_has_late_opens(late_opens, start, end)


def test_1935():
    start = "1935-01-01"
    end = "1935-12-31"
    holidays = [
        pd.Timestamp("1935-01-01", tz="UTC"),
        pd.Timestamp("1935-02-12", tz="UTC"),
        pd.Timestamp("1935-02-22", tz="UTC"),
        pd.Timestamp("1935-04-19", tz="UTC"),
        pd.Timestamp("1935-05-30", tz="UTC"),
        pd.Timestamp("1935-07-04", tz="UTC"),
        pd.Timestamp("1935-09-02", tz="UTC"),
        pd.Timestamp("1935-10-12", tz="UTC"),
        pd.Timestamp("1935-11-05", tz="UTC"),
        pd.Timestamp("1935-11-11", tz="UTC"),
        pd.Timestamp("1935-11-28", tz="UTC"),
        pd.Timestamp("1935-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1936():
    start = "1936-01-01"
    end = "1936-12-31"
    holidays = [
        pd.Timestamp("1936-01-01", tz="UTC"),
        pd.Timestamp("1936-02-12", tz="UTC"),
        pd.Timestamp("1936-02-22", tz="UTC"),
        pd.Timestamp("1936-04-10", tz="UTC"),
        pd.Timestamp("1936-05-30", tz="UTC"),
        pd.Timestamp("1936-07-04", tz="UTC"),
        pd.Timestamp("1936-09-07", tz="UTC"),
        pd.Timestamp("1936-10-12", tz="UTC"),
        pd.Timestamp("1936-11-03", tz="UTC"),
        pd.Timestamp("1936-11-11", tz="UTC"),
        pd.Timestamp("1936-11-26", tz="UTC"),
        pd.Timestamp("1936-12-25", tz="UTC"),
        pd.Timestamp("1936-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_closes(start, end)

    # late opens we expect:
    late_opens = [pd.Timestamp("1936-01-28 11:00AM", tz="America/New_York")]  # King George V funeral
    _test_has_late_opens(late_opens, start, end)


def test_1937():
    start = "1937-01-01"
    end = "1937-12-31"
    holidays = [
        pd.Timestamp("1937-01-01", tz="UTC"),
        pd.Timestamp("1937-02-12", tz="UTC"),
        pd.Timestamp("1937-02-22", tz="UTC"),
        pd.Timestamp("1937-03-26", tz="UTC"),
        pd.Timestamp("1937-05-29", tz="UTC"),
        pd.Timestamp("1937-05-31", tz="UTC"),
        pd.Timestamp("1937-07-03", tz="UTC"),
        pd.Timestamp("1937-07-05", tz="UTC"),
        pd.Timestamp("1937-09-06", tz="UTC"),
        pd.Timestamp("1937-10-12", tz="UTC"),
        pd.Timestamp("1937-11-02", tz="UTC"),
        pd.Timestamp("1937-11-11", tz="UTC"),
        pd.Timestamp("1937-11-25", tz="UTC"),
        pd.Timestamp("1937-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1938():
    start = "1938-01-01"
    end = "1938-12-31"
    holidays = [
        pd.Timestamp("1938-01-01", tz="UTC"),
        pd.Timestamp("1938-02-12", tz="UTC"),
        pd.Timestamp("1938-02-22", tz="UTC"),
        pd.Timestamp("1938-04-15", tz="UTC"),
        pd.Timestamp("1938-05-30", tz="UTC"),
        pd.Timestamp("1938-07-04", tz="UTC"),
        pd.Timestamp("1938-09-05", tz="UTC"),
        pd.Timestamp("1938-10-12", tz="UTC"),
        pd.Timestamp("1938-11-08", tz="UTC"),
        pd.Timestamp("1938-11-11", tz="UTC"),
        pd.Timestamp("1938-11-24", tz="UTC"),
        pd.Timestamp("1938-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1939():
    start = "1939-01-01"
    end = "1939-12-31"
    holidays = [
        pd.Timestamp("1939-01-02", tz="UTC"),
        pd.Timestamp("1939-02-13", tz="UTC"),
        pd.Timestamp("1939-02-22", tz="UTC"),
        pd.Timestamp("1939-04-07", tz="UTC"),
        pd.Timestamp("1939-05-30", tz="UTC"),
        pd.Timestamp("1939-07-04", tz="UTC"),
        pd.Timestamp("1939-09-04", tz="UTC"),
        pd.Timestamp("1939-10-12", tz="UTC"),
        pd.Timestamp("1939-11-07", tz="UTC"),
        pd.Timestamp("1939-11-11", tz="UTC"),
        pd.Timestamp("1939-11-23", tz="UTC"),
        pd.Timestamp("1939-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1940():
    start = "1940-01-01"
    end = "1940-12-31"
    holidays = [
        pd.Timestamp("1940-01-01", tz="UTC"),
        pd.Timestamp("1940-02-12", tz="UTC"),
        pd.Timestamp("1940-02-22", tz="UTC"),
        pd.Timestamp("1940-03-22", tz="UTC"),
        pd.Timestamp("1940-05-30", tz="UTC"),
        pd.Timestamp("1940-07-04", tz="UTC"),
        pd.Timestamp("1940-09-02", tz="UTC"),
        pd.Timestamp("1940-10-12", tz="UTC"),
        pd.Timestamp("1940-11-05", tz="UTC"),
        pd.Timestamp("1940-11-11", tz="UTC"),
        pd.Timestamp("1940-11-21", tz="UTC"),
        pd.Timestamp("1940-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1941():
    start = "1941-01-01"
    end = "1941-12-31"
    holidays = [
        pd.Timestamp("1941-01-01", tz="UTC"),
        pd.Timestamp("1941-02-12", tz="UTC"),
        pd.Timestamp("1941-02-22", tz="UTC"),
        pd.Timestamp("1941-04-11", tz="UTC"),
        pd.Timestamp("1941-05-30", tz="UTC"),
        pd.Timestamp("1941-07-04", tz="UTC"),
        pd.Timestamp("1941-09-01", tz="UTC"),
        pd.Timestamp("1941-10-13", tz="UTC"),
        pd.Timestamp("1941-11-04", tz="UTC"),
        pd.Timestamp("1941-11-11", tz="UTC"),
        pd.Timestamp("1941-11-20", tz="UTC"),
        pd.Timestamp("1941-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1942():
    start = "1942-01-01"
    end = "1942-12-31"
    holidays = [
        pd.Timestamp("1942-01-01", tz="UTC"),
        pd.Timestamp("1942-02-12", tz="UTC"),
        pd.Timestamp("1942-02-23", tz="UTC"),
        pd.Timestamp("1942-04-03", tz="UTC"),
        pd.Timestamp("1942-05-30", tz="UTC"),
        pd.Timestamp("1942-07-04", tz="UTC"),
        pd.Timestamp("1942-09-07", tz="UTC"),
        pd.Timestamp("1942-10-12", tz="UTC"),
        pd.Timestamp("1942-11-03", tz="UTC"),
        pd.Timestamp("1942-11-11", tz="UTC"),
        pd.Timestamp("1942-11-26", tz="UTC"),
        pd.Timestamp("1942-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1943():
    start = "1943-01-01"
    end = "1943-12-31"
    holidays = [
        pd.Timestamp("1943-01-01", tz="UTC"),
        pd.Timestamp("1943-02-12", tz="UTC"),
        pd.Timestamp("1943-02-22", tz="UTC"),
        pd.Timestamp("1943-04-23", tz="UTC"),
        pd.Timestamp("1943-05-31", tz="UTC"),
        pd.Timestamp("1943-07-05", tz="UTC"),
        pd.Timestamp("1943-09-06", tz="UTC"),
        pd.Timestamp("1943-10-12", tz="UTC"),
        pd.Timestamp("1943-11-02", tz="UTC"),
        pd.Timestamp("1943-11-11", tz="UTC"),
        pd.Timestamp("1943-11-25", tz="UTC"),
        pd.Timestamp("1943-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1944():
    start = "1944-01-01"
    end = "1944-12-31"
    holidays = [
        pd.Timestamp("1944-01-01", tz="UTC"),
        pd.Timestamp("1944-02-12", tz="UTC"),
        pd.Timestamp("1944-02-22", tz="UTC"),
        pd.Timestamp("1944-04-07", tz="UTC"),
        pd.Timestamp("1944-05-30", tz="UTC"),
        pd.Timestamp("1944-07-04", tz="UTC"),
        pd.Timestamp("1944-08-19", tz="UTC"),
        pd.Timestamp("1944-08-26", tz="UTC"),
        pd.Timestamp("1944-09-02", tz="UTC"),
        pd.Timestamp("1944-09-04", tz="UTC"),
        pd.Timestamp("1944-10-12", tz="UTC"),
        pd.Timestamp("1944-11-07", tz="UTC"),
        pd.Timestamp("1944-11-11", tz="UTC"),
        pd.Timestamp("1944-11-23", tz="UTC"),
        pd.Timestamp("1944-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1945():
    start = "1945-01-01"
    end = "1945-12-31"
    holidays = [
        pd.Timestamp("1945-01-01", tz="UTC"),
        pd.Timestamp("1945-02-12", tz="UTC"),
        pd.Timestamp("1945-02-22", tz="UTC"),
        pd.Timestamp("1945-03-30", tz="UTC"),
        pd.Timestamp("1945-04-14", tz="UTC"),
        pd.Timestamp("1945-05-30", tz="UTC"),
        pd.Timestamp("1945-07-04", tz="UTC"),
        pd.Timestamp("1945-07-07", tz="UTC"),
        pd.Timestamp("1945-07-14", tz="UTC"),
        pd.Timestamp("1945-07-21", tz="UTC"),
        pd.Timestamp("1945-07-28", tz="UTC"),
        pd.Timestamp("1945-08-04", tz="UTC"),
        pd.Timestamp("1945-08-11", tz="UTC"),
        pd.Timestamp("1945-08-15", tz="UTC"),
        pd.Timestamp("1945-08-16", tz="UTC"),
        pd.Timestamp("1945-08-18", tz="UTC"),
        pd.Timestamp("1945-08-25", tz="UTC"),
        pd.Timestamp("1945-09-01", tz="UTC"),
        pd.Timestamp("1945-09-03", tz="UTC"),
        pd.Timestamp("1945-10-12", tz="UTC"),
        pd.Timestamp("1945-10-13", tz="UTC"),
        pd.Timestamp("1945-10-27", tz="UTC"),
        pd.Timestamp("1945-11-06", tz="UTC"),
        pd.Timestamp("1945-11-12", tz="UTC"),
        pd.Timestamp("1945-11-22", tz="UTC"),
        pd.Timestamp("1945-12-24", tz="UTC"),
        pd.Timestamp("1945-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1946():
    start = "1946-01-01"
    end = "1946-12-31"
    holidays = [
        pd.Timestamp("1946-01-01", tz="UTC"),
        pd.Timestamp("1946-02-12", tz="UTC"),
        pd.Timestamp("1946-02-22", tz="UTC"),
        pd.Timestamp("1946-02-23", tz="UTC"),
        pd.Timestamp("1946-04-19", tz="UTC"),
        pd.Timestamp("1946-05-25", tz="UTC"),
        pd.Timestamp("1946-05-30", tz="UTC"),
        pd.Timestamp("1946-06-01", tz="UTC"),
        pd.Timestamp("1946-06-08", tz="UTC"),
        pd.Timestamp("1946-06-15", tz="UTC"),
        pd.Timestamp("1946-06-22", tz="UTC"),
        pd.Timestamp("1946-06-29", tz="UTC"),
        pd.Timestamp("1946-07-04", tz="UTC"),
        pd.Timestamp("1946-07-06", tz="UTC"),
        pd.Timestamp("1946-07-13", tz="UTC"),
        pd.Timestamp("1946-07-20", tz="UTC"),
        pd.Timestamp("1946-07-27", tz="UTC"),
        pd.Timestamp("1946-08-03", tz="UTC"),
        pd.Timestamp("1946-08-10", tz="UTC"),
        pd.Timestamp("1946-08-17", tz="UTC"),
        pd.Timestamp("1946-08-24", tz="UTC"),
        pd.Timestamp("1946-08-31", tz="UTC"),
        pd.Timestamp("1946-09-02", tz="UTC"),
        pd.Timestamp("1946-09-07", tz="UTC"),
        pd.Timestamp("1946-09-14", tz="UTC"),
        pd.Timestamp("1946-09-21", tz="UTC"),
        pd.Timestamp("1946-09-28", tz="UTC"),
        pd.Timestamp("1946-10-12", tz="UTC"),
        pd.Timestamp("1946-11-05", tz="UTC"),
        pd.Timestamp("1946-11-11", tz="UTC"),
        pd.Timestamp("1946-11-28", tz="UTC"),
        pd.Timestamp("1946-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1947():
    start = "1947-01-01"
    end = "1947-12-31"
    holidays = [
        pd.Timestamp("1947-01-01", tz="UTC"),
        pd.Timestamp("1947-02-12", tz="UTC"),
        pd.Timestamp("1947-02-22", tz="UTC"),
        pd.Timestamp("1947-04-04", tz="UTC"),
        pd.Timestamp("1947-05-30", tz="UTC"),
        pd.Timestamp("1947-05-31", tz="UTC"),
        pd.Timestamp("1947-06-07", tz="UTC"),
        pd.Timestamp("1947-06-14", tz="UTC"),
        pd.Timestamp("1947-06-21", tz="UTC"),
        pd.Timestamp("1947-06-28", tz="UTC"),
        pd.Timestamp("1947-07-04", tz="UTC"),
        pd.Timestamp("1947-07-05", tz="UTC"),
        pd.Timestamp("1947-07-12", tz="UTC"),
        pd.Timestamp("1947-07-19", tz="UTC"),
        pd.Timestamp("1947-07-26", tz="UTC"),
        pd.Timestamp("1947-08-02", tz="UTC"),
        pd.Timestamp("1947-08-09", tz="UTC"),
        pd.Timestamp("1947-08-16", tz="UTC"),
        pd.Timestamp("1947-08-23", tz="UTC"),
        pd.Timestamp("1947-08-30", tz="UTC"),
        pd.Timestamp("1947-09-01", tz="UTC"),
        pd.Timestamp("1947-09-06", tz="UTC"),
        pd.Timestamp("1947-09-13", tz="UTC"),
        pd.Timestamp("1947-09-20", tz="UTC"),
        pd.Timestamp("1947-09-27", tz="UTC"),
        pd.Timestamp("1947-10-13", tz="UTC"),
        pd.Timestamp("1947-11-04", tz="UTC"),
        pd.Timestamp("1947-11-11", tz="UTC"),
        pd.Timestamp("1947-11-27", tz="UTC"),
        pd.Timestamp("1947-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1948():
    start = "1948-01-01"
    end = "1948-12-31"
    holidays = [
        pd.Timestamp("1948-01-01", tz="UTC"),
        pd.Timestamp("1948-01-03", tz="UTC"),
        pd.Timestamp("1948-02-12", tz="UTC"),
        pd.Timestamp("1948-02-23", tz="UTC"),
        pd.Timestamp("1948-03-26", tz="UTC"),
        pd.Timestamp("1948-05-29", tz="UTC"),
        pd.Timestamp("1948-05-31", tz="UTC"),
        pd.Timestamp("1948-06-05", tz="UTC"),
        pd.Timestamp("1948-06-12", tz="UTC"),
        pd.Timestamp("1948-06-19", tz="UTC"),
        pd.Timestamp("1948-06-26", tz="UTC"),
        pd.Timestamp("1948-07-03", tz="UTC"),
        pd.Timestamp("1948-07-05", tz="UTC"),
        pd.Timestamp("1948-07-10", tz="UTC"),
        pd.Timestamp("1948-07-17", tz="UTC"),
        pd.Timestamp("1948-07-24", tz="UTC"),
        pd.Timestamp("1948-07-31", tz="UTC"),
        pd.Timestamp("1948-08-07", tz="UTC"),
        pd.Timestamp("1948-08-14", tz="UTC"),
        pd.Timestamp("1948-08-21", tz="UTC"),
        pd.Timestamp("1948-08-28", tz="UTC"),
        pd.Timestamp("1948-09-04", tz="UTC"),
        pd.Timestamp("1948-09-06", tz="UTC"),
        pd.Timestamp("1948-09-11", tz="UTC"),
        pd.Timestamp("1948-09-18", tz="UTC"),
        pd.Timestamp("1948-09-25", tz="UTC"),
        pd.Timestamp("1948-10-12", tz="UTC"),
        pd.Timestamp("1948-11-02", tz="UTC"),
        pd.Timestamp("1948-11-11", tz="UTC"),
        pd.Timestamp("1948-11-25", tz="UTC"),
        pd.Timestamp("1948-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1949():
    start = "1949-01-01"
    end = "1949-12-31"
    holidays = [
        pd.Timestamp("1949-01-01", tz="UTC"),
        pd.Timestamp("1949-02-12", tz="UTC"),
        pd.Timestamp("1949-02-22", tz="UTC"),
        pd.Timestamp("1949-04-15", tz="UTC"),
        pd.Timestamp("1949-05-28", tz="UTC"),
        pd.Timestamp("1949-05-30", tz="UTC"),
        pd.Timestamp("1949-06-04", tz="UTC"),
        pd.Timestamp("1949-06-11", tz="UTC"),
        pd.Timestamp("1949-06-18", tz="UTC"),
        pd.Timestamp("1949-06-25", tz="UTC"),
        pd.Timestamp("1949-07-02", tz="UTC"),
        pd.Timestamp("1949-07-04", tz="UTC"),
        pd.Timestamp("1949-07-09", tz="UTC"),
        pd.Timestamp("1949-07-16", tz="UTC"),
        pd.Timestamp("1949-07-23", tz="UTC"),
        pd.Timestamp("1949-07-30", tz="UTC"),
        pd.Timestamp("1949-08-06", tz="UTC"),
        pd.Timestamp("1949-08-13", tz="UTC"),
        pd.Timestamp("1949-08-20", tz="UTC"),
        pd.Timestamp("1949-08-27", tz="UTC"),
        pd.Timestamp("1949-09-03", tz="UTC"),
        pd.Timestamp("1949-09-05", tz="UTC"),
        pd.Timestamp("1949-09-10", tz="UTC"),
        pd.Timestamp("1949-09-17", tz="UTC"),
        pd.Timestamp("1949-09-24", tz="UTC"),
        pd.Timestamp("1949-10-12", tz="UTC"),
        pd.Timestamp("1949-11-08", tz="UTC"),
        pd.Timestamp("1949-11-11", tz="UTC"),
        pd.Timestamp("1949-11-24", tz="UTC"),
        pd.Timestamp("1949-12-24", tz="UTC"),
        pd.Timestamp("1949-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1950():
    start = "1950-01-01"
    end = "1950-12-31"
    holidays = [
        pd.Timestamp("1950-01-02", tz="UTC"),
        pd.Timestamp("1950-02-13", tz="UTC"),
        pd.Timestamp("1950-02-22", tz="UTC"),
        pd.Timestamp("1950-04-07", tz="UTC"),
        pd.Timestamp("1950-05-30", tz="UTC"),
        pd.Timestamp("1950-06-03", tz="UTC"),
        pd.Timestamp("1950-06-10", tz="UTC"),
        pd.Timestamp("1950-06-17", tz="UTC"),
        pd.Timestamp("1950-06-24", tz="UTC"),
        pd.Timestamp("1950-07-01", tz="UTC"),
        pd.Timestamp("1950-07-04", tz="UTC"),
        pd.Timestamp("1950-07-08", tz="UTC"),
        pd.Timestamp("1950-07-15", tz="UTC"),
        pd.Timestamp("1950-07-22", tz="UTC"),
        pd.Timestamp("1950-07-29", tz="UTC"),
        pd.Timestamp("1950-08-05", tz="UTC"),
        pd.Timestamp("1950-08-12", tz="UTC"),
        pd.Timestamp("1950-08-19", tz="UTC"),
        pd.Timestamp("1950-08-26", tz="UTC"),
        pd.Timestamp("1950-09-02", tz="UTC"),
        pd.Timestamp("1950-09-04", tz="UTC"),
        pd.Timestamp("1950-09-09", tz="UTC"),
        pd.Timestamp("1950-09-16", tz="UTC"),
        pd.Timestamp("1950-09-23", tz="UTC"),
        pd.Timestamp("1950-09-30", tz="UTC"),
        pd.Timestamp("1950-10-12", tz="UTC"),
        pd.Timestamp("1950-11-07", tz="UTC"),
        pd.Timestamp("1950-11-11", tz="UTC"),
        pd.Timestamp("1950-11-23", tz="UTC"),
        pd.Timestamp("1950-12-23", tz="UTC"),
        pd.Timestamp("1950-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1951():
    start = "1951-01-01"
    end = "1951-12-31"
    holidays = [
        pd.Timestamp("1951-01-01", tz="UTC"),
        pd.Timestamp("1951-02-12", tz="UTC"),
        pd.Timestamp("1951-02-22", tz="UTC"),
        pd.Timestamp("1951-03-23", tz="UTC"),
        pd.Timestamp("1951-05-30", tz="UTC"),
        pd.Timestamp("1951-06-02", tz="UTC"),
        pd.Timestamp("1951-06-09", tz="UTC"),
        pd.Timestamp("1951-06-16", tz="UTC"),
        pd.Timestamp("1951-06-23", tz="UTC"),
        pd.Timestamp("1951-06-30", tz="UTC"),
        pd.Timestamp("1951-07-04", tz="UTC"),
        pd.Timestamp("1951-07-07", tz="UTC"),
        pd.Timestamp("1951-07-14", tz="UTC"),
        pd.Timestamp("1951-07-21", tz="UTC"),
        pd.Timestamp("1951-07-28", tz="UTC"),
        pd.Timestamp("1951-08-04", tz="UTC"),
        pd.Timestamp("1951-08-11", tz="UTC"),
        pd.Timestamp("1951-08-18", tz="UTC"),
        pd.Timestamp("1951-08-25", tz="UTC"),
        pd.Timestamp("1951-09-01", tz="UTC"),
        pd.Timestamp("1951-09-03", tz="UTC"),
        pd.Timestamp("1951-09-08", tz="UTC"),
        pd.Timestamp("1951-09-15", tz="UTC"),
        pd.Timestamp("1951-09-22", tz="UTC"),
        pd.Timestamp("1951-09-29", tz="UTC"),
        pd.Timestamp("1951-10-12", tz="UTC"),
        pd.Timestamp("1951-11-06", tz="UTC"),
        pd.Timestamp("1951-11-12", tz="UTC"),
        pd.Timestamp("1951-11-22", tz="UTC"),
        pd.Timestamp("1951-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1951-12-24 1:00PM", tz="America/New_York"),  # Christmas Eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1952():
    start = "1952-01-01"
    end = "1952-12-31"
    holidays = [
        pd.Timestamp("1952-01-01", tz="UTC"),
        pd.Timestamp("1952-02-12", tz="UTC"),
        pd.Timestamp("1952-02-22", tz="UTC"),
        pd.Timestamp("1952-04-11", tz="UTC"),
        pd.Timestamp("1952-05-30", tz="UTC"),
        pd.Timestamp("1952-05-31", tz="UTC"),
        pd.Timestamp("1952-06-07", tz="UTC"),
        pd.Timestamp("1952-06-14", tz="UTC"),
        pd.Timestamp("1952-06-21", tz="UTC"),
        pd.Timestamp("1952-06-28", tz="UTC"),
        pd.Timestamp("1952-07-04", tz="UTC"),
        pd.Timestamp("1952-07-05", tz="UTC"),
        pd.Timestamp("1952-07-12", tz="UTC"),
        pd.Timestamp("1952-07-19", tz="UTC"),
        pd.Timestamp("1952-07-26", tz="UTC"),
        pd.Timestamp("1952-08-02", tz="UTC"),
        pd.Timestamp("1952-08-09", tz="UTC"),
        pd.Timestamp("1952-08-16", tz="UTC"),
        pd.Timestamp("1952-08-23", tz="UTC"),
        pd.Timestamp("1952-08-30", tz="UTC"),
        pd.Timestamp("1952-09-01", tz="UTC"),
        pd.Timestamp("1952-09-06", tz="UTC"),
        pd.Timestamp("1952-09-13", tz="UTC"),
        pd.Timestamp("1952-09-20", tz="UTC"),
        pd.Timestamp("1952-09-27", tz="UTC"),
        pd.Timestamp("1952-10-13", tz="UTC"),
        pd.Timestamp("1952-11-04", tz="UTC"),
        pd.Timestamp("1952-11-11", tz="UTC"),
        pd.Timestamp("1952-11-27", tz="UTC"),
        pd.Timestamp("1952-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1952_no_saturdays():
    start = "1952-09-29"
    end = "2025-12-31"

    # Check no saturdays in valid trading days post 1952-09-29
    valid_days = nyse.valid_days(start, end)
    for d in valid_days:
        assert d.dayofweek != 5

    # Check no Saturdays in Holiday post 1952-09-29
    df = pd.DataFrame(nyse.holidays().holidays, columns=["holidays"])
    mask = df["holidays"].isin(pd.date_range(start, end, freq="W-SAT"))
    df = df[mask]
    assert len(df) == 0


def test_1952_date_range_htf_crossover():
    # Test that Date_Range_HTF can produce the correct range when having
    # to merge ranges from two different holiday objects. This is only
    # A massive pain in the ass when closed='right'
    nyse = NYSEExchangeCalendar()

    actual_week_ends = pd.DatetimeIndex(
        [
            "1952-01-05",  # Saturday
            "1952-01-12",  # Saturday
            "1952-01-19",  # Saturday
            "1952-01-26",  # Saturday
            "1952-02-02",  # Saturday
            "1952-02-09",  # Saturday
            "1952-02-16",  # Saturday
            "1952-02-23",  # Saturday
            "1952-03-01",  # Saturday
            "1952-03-08",  # Saturday
            "1952-03-15",  # Saturday
            "1952-03-22",  # Saturday
            "1952-03-29",  # Saturday
            "1952-04-05",  # Saturday
            "1952-04-12",  # Saturday
            "1952-04-19",  # Saturday
            "1952-04-26",  # Saturday
            "1952-05-03",  # Saturday
            "1952-05-10",  # Saturday
            "1952-05-17",  # Saturday
            "1952-05-24",  # Saturday ## Last Trading Saturday. ##
            "1952-05-29",  # Thursday
            "1952-06-06",  # Friday
            "1952-06-13",  # Friday
            "1952-06-20",  # Friday
            "1952-06-27",  # Friday       All Saturdays, and the
            "1952-07-03",  # Thursday     two fridays, in this
            "1952-07-11",  # Friday       range are omitted since
            "1952-07-18",  # Friday       they are labeled as holidays.
            "1952-07-25",  # Friday
            "1952-08-01",  # Friday
            "1952-08-08",  # Friday
            "1952-08-15",  # Friday
            "1952-08-22",  # Friday
            "1952-08-29",  # Friday
            "1952-09-05",  # Friday
            "1952-09-12",  # Friday
            "1952-09-19",  # Friday
            "1952-09-26",  # Friday ## 1952-09-29 is Crossover ##
            "1952-10-03",  # Friday
            "1952-10-10",  # Friday
            "1952-10-17",  # Friday
            "1952-10-24",  # Friday
            "1952-10-31",  # Friday
            "1952-11-07",  # Friday
            "1952-11-14",  # Friday
            "1952-11-21",  # Friday
            "1952-11-28",  # Friday
            "1952-12-05",  # Friday
            "1952-12-12",  # Friday
            "1952-12-19",  # Friday
            "1952-12-26",  # Friday
        ],
        dtype="datetime64[ns]",
        freq=None,
    )

    # Ensure all three different ways produce the same range.
    assert_index_equal(
        actual_week_ends,
        nyse.date_range_htf("1W", "1952-01-01", "1953-01-01", closed="right"),
    )
    assert_index_equal(
        actual_week_ends,
        nyse.date_range_htf("1W", "1952-01-01", periods=52, closed="right"),
    )
    assert_index_equal(
        actual_week_ends,
        nyse.date_range_htf("1W", end="1953-01-01", periods=52, closed="right"),
    )

    # Ensure all three different ways produce the same range.
    assert_index_equal(
        actual_week_ends[::3],
        nyse.date_range_htf("3W", "1952-01-01", "1953-01-01", closed="right"),
    )
    assert_index_equal(
        actual_week_ends[::3],
        nyse.date_range_htf("3W", "1952-01-01", periods=18, closed="right"),
    )
    assert_index_equal(
        actual_week_ends[::-1][::3][::-1],
        nyse.date_range_htf("3W", end="1953-01-01", periods=18, closed="right"),
    )
    assert_index_equal(
        actual_week_ends[::-1][::7][::-1],
        nyse.date_range_htf("7W", end="1953-01-01", periods=8, closed="right"),
    )

    # Results Should Agree between the two methods in this critical range
    actual_days = nyse.valid_days("1952-05-01", "1952-11-01").tz_localize(None)

    assert_index_equal(
        actual_days,
        nyse.date_range_htf("D", "1952-05-01", "1952-11-01"),
    )
    assert_index_equal(
        actual_days,
        nyse.date_range_htf("D", "1952-05-01", periods=132),
    )
    assert_index_equal(
        actual_days,
        nyse.date_range_htf("D", end="1952-11-01", periods=132),
    )

    assert_index_equal(
        actual_days[::3],
        nyse.date_range_htf("3D", "1952-05-01", "1952-11-01"),
    )
    assert_index_equal(
        actual_days[::3],
        nyse.date_range_htf("3D", "1952-05-01", periods=44),
    )
    assert_index_equal(
        actual_days[::-1][::3][::-1],
        nyse.date_range_htf("3D", end="1952-11-01", periods=44),
    )
    assert_index_equal(
        actual_days[::-1][::7][::-1],
        nyse.date_range_htf("7D", end="1952-11-01", periods=19),
    )


def test_1953():
    start = "1953-01-01"
    end = "1953-12-31"
    holidays = [
        pd.Timestamp("1953-01-01", tz="UTC"),
        pd.Timestamp("1953-02-12", tz="UTC"),
        pd.Timestamp("1953-02-23", tz="UTC"),
        pd.Timestamp("1953-04-03", tz="UTC"),
        pd.Timestamp("1953-09-07", tz="UTC"),
        pd.Timestamp("1953-10-12", tz="UTC"),
        pd.Timestamp("1953-11-03", tz="UTC"),
        pd.Timestamp("1953-11-11", tz="UTC"),
        pd.Timestamp("1953-11-26", tz="UTC"),
        pd.Timestamp("1953-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1954():
    start = "1954-01-01"
    end = "1954-12-31"
    holidays = [
        pd.Timestamp("1954-01-01", tz="UTC"),
        pd.Timestamp("1954-02-22", tz="UTC"),
        pd.Timestamp("1954-04-16", tz="UTC"),
        pd.Timestamp("1954-05-31", tz="UTC"),
        pd.Timestamp("1954-07-05", tz="UTC"),
        pd.Timestamp("1954-09-06", tz="UTC"),
        pd.Timestamp("1954-11-02", tz="UTC"),
        pd.Timestamp("1954-11-25", tz="UTC"),
        pd.Timestamp("1954-12-24", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1955():
    start = "1955-01-01"
    end = "1955-12-31"
    holidays = [
        pd.Timestamp("1955-02-22", tz="UTC"),
        pd.Timestamp("1955-04-08", tz="UTC"),
        pd.Timestamp("1955-05-30", tz="UTC"),
        pd.Timestamp("1955-07-04", tz="UTC"),
        pd.Timestamp("1955-09-05", tz="UTC"),
        pd.Timestamp("1955-11-08", tz="UTC"),
        pd.Timestamp("1955-11-24", tz="UTC"),
        pd.Timestamp("1955-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1956():
    start = "1956-01-01"
    end = "1956-12-31"
    holidays = [
        pd.Timestamp("1956-01-02", tz="UTC"),
        pd.Timestamp("1956-02-22", tz="UTC"),
        pd.Timestamp("1956-03-30", tz="UTC"),
        pd.Timestamp("1956-05-30", tz="UTC"),
        pd.Timestamp("1956-07-04", tz="UTC"),
        pd.Timestamp("1956-09-03", tz="UTC"),
        pd.Timestamp("1956-11-06", tz="UTC"),
        pd.Timestamp("1956-11-22", tz="UTC"),
        pd.Timestamp("1956-12-24", tz="UTC"),
        pd.Timestamp("1956-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1957():
    start = "1957-01-01"
    end = "1957-12-31"
    holidays = [
        pd.Timestamp("1957-01-01", tz="UTC"),
        pd.Timestamp("1957-02-22", tz="UTC"),
        pd.Timestamp("1957-04-19", tz="UTC"),
        pd.Timestamp("1957-05-30", tz="UTC"),
        pd.Timestamp("1957-07-04", tz="UTC"),
        pd.Timestamp("1957-09-02", tz="UTC"),
        pd.Timestamp("1957-11-05", tz="UTC"),
        pd.Timestamp("1957-11-28", tz="UTC"),
        pd.Timestamp("1957-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1958():
    start = "1958-01-01"
    end = "1958-12-31"
    holidays = [
        pd.Timestamp("1958-01-01", tz="UTC"),
        pd.Timestamp("1958-04-04", tz="UTC"),
        pd.Timestamp("1958-05-30", tz="UTC"),
        pd.Timestamp("1958-07-04", tz="UTC"),
        pd.Timestamp("1958-09-01", tz="UTC"),
        pd.Timestamp("1958-11-04", tz="UTC"),
        pd.Timestamp("1958-11-27", tz="UTC"),
        pd.Timestamp("1958-12-25", tz="UTC"),
        pd.Timestamp("1958-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1959():
    start = "1959-01-01"
    end = "1959-12-31"
    holidays = [
        pd.Timestamp("1959-01-01", tz="UTC"),
        pd.Timestamp("1959-02-23", tz="UTC"),
        pd.Timestamp("1959-03-27", tz="UTC"),
        pd.Timestamp("1959-07-03", tz="UTC"),
        pd.Timestamp("1959-09-07", tz="UTC"),
        pd.Timestamp("1959-11-03", tz="UTC"),
        pd.Timestamp("1959-11-26", tz="UTC"),
        pd.Timestamp("1959-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1960():
    start = "1960-01-01"
    end = "1960-12-31"
    holidays = [
        pd.Timestamp("1960-01-01", tz="UTC"),
        pd.Timestamp("1960-02-22", tz="UTC"),
        pd.Timestamp("1960-04-15", tz="UTC"),
        pd.Timestamp("1960-05-30", tz="UTC"),
        pd.Timestamp("1960-07-04", tz="UTC"),
        pd.Timestamp("1960-09-05", tz="UTC"),
        pd.Timestamp("1960-11-08", tz="UTC"),
        pd.Timestamp("1960-11-24", tz="UTC"),
        pd.Timestamp("1960-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_closes(start, end)

    # late opens we expect:
    late_opens = [pd.Timestamp("1960-12-12 11:00AM", tz="America/New_York")]  # snow
    _test_has_late_opens(late_opens, start, end)


def test_1961():
    start = "1961-01-01"
    end = "1961-12-31"
    holidays = [
        pd.Timestamp("1961-01-02", tz="UTC"),
        pd.Timestamp("1961-02-22", tz="UTC"),
        pd.Timestamp("1961-03-31", tz="UTC"),
        pd.Timestamp("1961-05-29", tz="UTC"),
        pd.Timestamp("1961-05-30", tz="UTC"),
        pd.Timestamp("1961-07-04", tz="UTC"),
        pd.Timestamp("1961-09-04", tz="UTC"),
        pd.Timestamp("1961-11-07", tz="UTC"),
        pd.Timestamp("1961-11-23", tz="UTC"),
        pd.Timestamp("1961-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1962():
    start = "1962-01-01"
    end = "1962-12-31"
    holidays = [
        pd.Timestamp("1962-01-01", tz="UTC"),
        pd.Timestamp("1962-02-22", tz="UTC"),
        pd.Timestamp("1962-04-20", tz="UTC"),
        pd.Timestamp("1962-05-30", tz="UTC"),
        pd.Timestamp("1962-07-04", tz="UTC"),
        pd.Timestamp("1962-09-03", tz="UTC"),
        pd.Timestamp("1962-11-06", tz="UTC"),
        pd.Timestamp("1962-11-22", tz="UTC"),
        pd.Timestamp("1962-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1963():
    start = "1963-01-01"
    end = "1963-12-31"
    holidays = [
        pd.Timestamp("1963-01-01", tz="UTC"),
        pd.Timestamp("1963-02-22", tz="UTC"),
        pd.Timestamp("1963-04-12", tz="UTC"),
        pd.Timestamp("1963-05-30", tz="UTC"),
        pd.Timestamp("1963-07-04", tz="UTC"),
        pd.Timestamp("1963-09-02", tz="UTC"),
        pd.Timestamp("1963-11-05", tz="UTC"),
        pd.Timestamp("1963-11-25", tz="UTC"),
        pd.Timestamp("1963-11-28", tz="UTC"),
        pd.Timestamp("1963-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1963-11-22 2:07PM", tz="America/New_York"),  # JFK Assassination
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1964():
    start = "1964-01-01"
    end = "1964-12-31"
    holidays = [
        pd.Timestamp("1964-01-01", tz="UTC"),
        pd.Timestamp("1964-02-21", tz="UTC"),
        pd.Timestamp("1964-03-27", tz="UTC"),
        pd.Timestamp("1964-05-29", tz="UTC"),
        pd.Timestamp("1964-07-03", tz="UTC"),
        pd.Timestamp("1964-09-07", tz="UTC"),
        pd.Timestamp("1964-11-03", tz="UTC"),
        pd.Timestamp("1964-11-26", tz="UTC"),
        pd.Timestamp("1964-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1964-10-23 2:00PM", tz="America/New_York"),  # Hoover funeral
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1965():
    start = "1965-01-01"
    end = "1965-12-31"
    holidays = [
        pd.Timestamp("1965-01-01", tz="UTC"),
        pd.Timestamp("1965-02-22", tz="UTC"),
        pd.Timestamp("1965-04-16", tz="UTC"),
        pd.Timestamp("1965-05-31", tz="UTC"),
        pd.Timestamp("1965-07-05", tz="UTC"),
        pd.Timestamp("1965-09-06", tz="UTC"),
        pd.Timestamp("1965-11-02", tz="UTC"),
        pd.Timestamp("1965-11-25", tz="UTC"),
        pd.Timestamp("1965-12-24", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_closes(start, end)

    # late opens we expect:
    late_opens = [pd.Timestamp("1965-11-10 11:05AM", tz="America/New_York")]  # NY power grid failure
    _test_has_late_opens(late_opens, start, end)


def test_1966():
    start = "1966-01-01"
    end = "1966-12-31"
    holidays = [
        pd.Timestamp("1966-02-22", tz="UTC"),
        pd.Timestamp("1966-04-08", tz="UTC"),
        pd.Timestamp("1966-05-30", tz="UTC"),
        pd.Timestamp("1966-07-04", tz="UTC"),
        pd.Timestamp("1966-09-05", tz="UTC"),
        pd.Timestamp("1966-11-08", tz="UTC"),
        pd.Timestamp("1966-11-24", tz="UTC"),
        pd.Timestamp("1966-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = pd.date_range(
        "1966-01-06 2:00PM",
        "1966-01-14 2:00PM",
        freq=CustomBusinessDay(weekmask="Mon Tue Wed Thu Fri"),
        tz="America/New_York",
    )  # Transit strike
    _test_has_early_closes(early_closes, start, end)


def test_1967():
    start = "1967-01-01"
    end = "1967-12-31"
    holidays = [
        pd.Timestamp("1967-01-02", tz="UTC"),
        pd.Timestamp("1967-02-22", tz="UTC"),
        pd.Timestamp("1967-03-24", tz="UTC"),
        pd.Timestamp("1967-05-30", tz="UTC"),
        pd.Timestamp("1967-07-04", tz="UTC"),
        pd.Timestamp("1967-09-04", tz="UTC"),
        pd.Timestamp("1967-11-07", tz="UTC"),
        pd.Timestamp("1967-11-23", tz="UTC"),
        pd.Timestamp("1967-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1967-02-07 2:00PM", tz="America/New_York"),  # snow
        pd.Timestamp("1967-08-09 2:00PM", tz="America/New_York"),  # Backlog relief
        pd.Timestamp("1967-08-10 2:00PM", tz="America/New_York"),  # Backlog relief
        pd.Timestamp("1967-08-11 2:00PM", tz="America/New_York"),  # Backlog relief
        pd.Timestamp("1967-08-14 2:00PM", tz="America/New_York"),  # Backlog relief
        pd.Timestamp("1967-08-15 2:00PM", tz="America/New_York"),  # Backlog relief
        pd.Timestamp("1967-08-16 2:00PM", tz="America/New_York"),  # Backlog relief
        pd.Timestamp("1967-08-17 2:00PM", tz="America/New_York"),  # Backlog relief
        pd.Timestamp("1967-08-18 2:00PM", tz="America/New_York"),  # Backlog relief
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1967-02-07 10:15AM", tz="America/New_York"),  # snow
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1968():
    start = "1968-01-01"
    end = "1968-12-31"
    holidays = [
        pd.Timestamp("1968-01-01", tz="UTC"),
        pd.Timestamp("1968-02-12", tz="UTC"),
        pd.Timestamp("1968-02-22", tz="UTC"),
        pd.Timestamp("1968-04-09", tz="UTC"),
        pd.Timestamp("1968-04-12", tz="UTC"),
        pd.Timestamp("1968-05-30", tz="UTC"),
        pd.Timestamp("1968-06-12", tz="UTC"),
        pd.Timestamp("1968-06-19", tz="UTC"),
        pd.Timestamp("1968-06-26", tz="UTC"),
        pd.Timestamp("1968-07-04", tz="UTC"),
        pd.Timestamp("1968-07-05", tz="UTC"),
        pd.Timestamp("1968-07-10", tz="UTC"),
        pd.Timestamp("1968-07-17", tz="UTC"),
        pd.Timestamp("1968-07-24", tz="UTC"),
        pd.Timestamp("1968-07-31", tz="UTC"),
        pd.Timestamp("1968-08-07", tz="UTC"),
        pd.Timestamp("1968-08-14", tz="UTC"),
        pd.Timestamp("1968-08-21", tz="UTC"),
        pd.Timestamp("1968-08-28", tz="UTC"),
        pd.Timestamp("1968-09-02", tz="UTC"),
        pd.Timestamp("1968-09-11", tz="UTC"),
        pd.Timestamp("1968-09-18", tz="UTC"),
        pd.Timestamp("1968-09-25", tz="UTC"),
        pd.Timestamp("1968-10-02", tz="UTC"),
        pd.Timestamp("1968-10-09", tz="UTC"),
        pd.Timestamp("1968-10-16", tz="UTC"),
        pd.Timestamp("1968-10-23", tz="UTC"),
        pd.Timestamp("1968-10-30", tz="UTC"),
        pd.Timestamp("1968-11-05", tz="UTC"),
        pd.Timestamp("1968-11-11", tz="UTC"),
        pd.Timestamp("1968-11-20", tz="UTC"),
        pd.Timestamp("1968-11-28", tz="UTC"),
        pd.Timestamp("1968-12-04", tz="UTC"),
        pd.Timestamp("1968-12-11", tz="UTC"),
        pd.Timestamp("1968-12-18", tz="UTC"),
        pd.Timestamp("1968-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect
    early_closes = pd.date_range(
        "1968-01-22 2:00PM",
        "1968-03-01 2:00PM",
        freq=CustomBusinessDay(holidays=nyse.holidays().holidays, weekmask="Mon Tue Wed Thu Fri"),
        tz="America/New_York",
    )  # Backlog relief
    _test_has_early_closes(early_closes, start, end)


def test_1969():
    start = "1969-01-01"
    end = "1969-12-31"
    holidays = [
        pd.Timestamp("1969-01-01", tz="UTC"),
        pd.Timestamp("1969-02-10", tz="UTC"),
        pd.Timestamp("1969-02-21", tz="UTC"),
        pd.Timestamp("1969-03-31", tz="UTC"),
        pd.Timestamp("1969-04-04", tz="UTC"),
        pd.Timestamp("1969-05-30", tz="UTC"),
        pd.Timestamp("1969-07-04", tz="UTC"),
        pd.Timestamp("1969-07-21", tz="UTC"),
        pd.Timestamp("1969-09-01", tz="UTC"),
        pd.Timestamp("1969-11-27", tz="UTC"),
        pd.Timestamp("1969-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    # Every trading day was an early close in 1969 for Paperwork Crisis
    ec1 = pd.date_range(
        "1969-01-01 2:00PM",
        "1969-07-03 2:00PM",
        freq=CustomBusinessDay(holidays=nyse.holidays().holidays, weekmask="Mon Tue Wed Thu Fri"),
        tz="America/New_York",
    )  # Backlog relief

    ec2 = pd.date_range(
        "1969-07-07 2:30PM",
        "1969-09-26 2:30PM",
        freq=CustomBusinessDay(holidays=nyse.holidays().holidays, weekmask="Mon Tue Wed Thu Fri"),
        tz="America/New_York",
    )  # Backlog relief

    ec3 = pd.date_range(
        "1969-09-29 3:00PM",
        "1969-12-31 3:00PM",
        freq=CustomBusinessDay(holidays=nyse.holidays().holidays, weekmask="Mon Tue Wed Thu Fri"),
        tz="America/New_York",
    )  # Backlog relief
    early_closes = ec1.append(ec2).append(ec3)
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1969-02-11 11:00AM", tz="America/New_York"),  # snow
        pd.Timestamp("1969-06-02 10:45AM", tz="America/New_York"),  # storm
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1970():
    start = "1970-01-01"
    end = "1970-12-31"
    holidays = [
        pd.Timestamp("1970-01-01", tz="UTC"),
        pd.Timestamp("1970-02-23", tz="UTC"),
        pd.Timestamp("1970-03-27", tz="UTC"),
        pd.Timestamp("1970-07-03", tz="UTC"),
        pd.Timestamp("1970-09-07", tz="UTC"),
        pd.Timestamp("1970-11-26", tz="UTC"),
        pd.Timestamp("1970-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    early_closes = pd.date_range(
        "1970-01-01 3:00PM",
        "1970-05-01 3:00PM",
        freq=CustomBusinessDay(holidays=nyse.holidays().holidays, weekmask="Mon Tue Wed Thu Fri"),
        tz="America/New_York",
    )  # Backlog relief
    _test_has_early_closes(early_closes, start, end)


def test_1971():
    start = "1971-01-01"
    end = "1971-12-31"
    holidays = [
        pd.Timestamp("1971-01-01", tz="UTC"),
        pd.Timestamp("1971-02-15", tz="UTC"),
        pd.Timestamp("1971-04-09", tz="UTC"),
        pd.Timestamp("1971-05-31", tz="UTC"),
        pd.Timestamp("1971-07-05", tz="UTC"),
        pd.Timestamp("1971-09-06", tz="UTC"),
        pd.Timestamp("1971-11-25", tz="UTC"),
        pd.Timestamp("1971-12-24", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1972():
    start = "1972-01-01"
    end = "1972-12-31"
    holidays = [
        pd.Timestamp("1972-02-21", tz="UTC"),
        pd.Timestamp("1972-03-31", tz="UTC"),
        pd.Timestamp("1972-05-29", tz="UTC"),
        pd.Timestamp("1972-07-04", tz="UTC"),
        pd.Timestamp("1972-09-04", tz="UTC"),
        pd.Timestamp("1972-11-07", tz="UTC"),
        pd.Timestamp("1972-11-23", tz="UTC"),
        pd.Timestamp("1972-12-25", tz="UTC"),
        pd.Timestamp("1972-12-28", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1973():
    start = "1973-01-01"
    end = "1973-12-31"
    holidays = [
        pd.Timestamp("1973-01-01", tz="UTC"),
        pd.Timestamp("1973-01-25", tz="UTC"),
        pd.Timestamp("1973-02-19", tz="UTC"),
        pd.Timestamp("1973-04-20", tz="UTC"),
        pd.Timestamp("1973-05-28", tz="UTC"),
        pd.Timestamp("1973-07-04", tz="UTC"),
        pd.Timestamp("1973-09-03", tz="UTC"),
        pd.Timestamp("1973-11-22", tz="UTC"),
        pd.Timestamp("1973-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_closes(start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1973-12-17 11:00AM", tz="America/New_York"),  # ice storm
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1974():
    start = "1974-01-01"
    end = "1974-12-31"
    holidays = [
        pd.Timestamp("1974-01-01", tz="UTC"),
        pd.Timestamp("1974-02-18", tz="UTC"),
        pd.Timestamp("1974-04-12", tz="UTC"),
        pd.Timestamp("1974-05-27", tz="UTC"),
        pd.Timestamp("1974-07-04", tz="UTC"),
        pd.Timestamp("1974-09-02", tz="UTC"),
        pd.Timestamp("1974-11-28", tz="UTC"),
        pd.Timestamp("1974-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1974-12-24 2:00PM", tz="America/New_York"),
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1974-01-16 10:15AM", tz="America/New_York"),  # Merrill Lynch computer trouble
        pd.Timestamp("1974-11-22 10:15AM", tz="America/New_York"),  # Fire drill
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1975():
    start = "1975-01-01"
    end = "1975-12-31"
    holidays = [
        pd.Timestamp("1975-01-01", tz="UTC"),
        pd.Timestamp("1975-02-17", tz="UTC"),
        pd.Timestamp("1975-03-28", tz="UTC"),
        pd.Timestamp("1975-05-26", tz="UTC"),
        pd.Timestamp("1975-07-04", tz="UTC"),
        pd.Timestamp("1975-09-01", tz="UTC"),
        pd.Timestamp("1975-11-27", tz="UTC"),
        pd.Timestamp("1975-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1975-02-12 2:30PM", tz="America/New_York"),  # snow
        pd.Timestamp("1975-12-24 2:00PM", tz="America/New_York"),  # Christmas Eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1976():
    start = "1976-01-01"
    end = "1976-12-31"
    holidays = [
        pd.Timestamp("1976-01-01", tz="UTC"),
        pd.Timestamp("1976-02-16", tz="UTC"),
        pd.Timestamp("1976-04-16", tz="UTC"),
        pd.Timestamp("1976-05-31", tz="UTC"),
        pd.Timestamp("1976-07-05", tz="UTC"),
        pd.Timestamp("1976-09-06", tz="UTC"),
        pd.Timestamp("1976-11-02", tz="UTC"),
        pd.Timestamp("1976-11-25", tz="UTC"),
        pd.Timestamp("1976-12-24", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1976-08-09 3:00PM", tz="America/New_York"),  # Hurricane watch
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1976-02-02 11:15AM", tz="America/New_York"),  # storm
        pd.Timestamp("1976-06-08 10:15AM", tz="America/New_York"),  # fire drill
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1977():
    start = "1977-01-01"
    end = "1977-12-31"
    holidays = [
        pd.Timestamp("1977-02-21", tz="UTC"),
        pd.Timestamp("1977-04-08", tz="UTC"),
        pd.Timestamp("1977-05-30", tz="UTC"),
        pd.Timestamp("1977-07-04", tz="UTC"),
        pd.Timestamp("1977-07-14", tz="UTC"),
        pd.Timestamp("1977-09-05", tz="UTC"),
        pd.Timestamp("1977-11-24", tz="UTC"),
        pd.Timestamp("1977-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1978():
    start = "1978-01-01"
    end = "1978-12-31"
    holidays = [
        pd.Timestamp("1978-01-02", tz="UTC"),
        pd.Timestamp("1978-02-20", tz="UTC"),
        pd.Timestamp("1978-03-24", tz="UTC"),
        pd.Timestamp("1978-05-29", tz="UTC"),
        pd.Timestamp("1978-07-04", tz="UTC"),
        pd.Timestamp("1978-09-04", tz="UTC"),
        pd.Timestamp("1978-11-23", tz="UTC"),
        pd.Timestamp("1978-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1978-02-06 2:00PM", tz="America/New_York"),  # snow
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1978-01-20 12:00PM", tz="America/New_York"),  # snow
        pd.Timestamp("1978-02-07 11:00AM", tz="America/New_York"),  # snow
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1979():
    start = "1979-01-01"
    end = "1979-12-31"
    holidays = [
        pd.Timestamp("1979-01-01", tz="UTC"),
        pd.Timestamp("1979-02-19", tz="UTC"),
        pd.Timestamp("1979-04-13", tz="UTC"),
        pd.Timestamp("1979-05-28", tz="UTC"),
        pd.Timestamp("1979-07-04", tz="UTC"),
        pd.Timestamp("1979-09-03", tz="UTC"),
        pd.Timestamp("1979-11-22", tz="UTC"),
        pd.Timestamp("1979-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1980():
    start = "1980-01-01"
    end = "1980-12-31"
    holidays = [
        pd.Timestamp("1980-01-01", tz="UTC"),
        pd.Timestamp("1980-02-18", tz="UTC"),
        pd.Timestamp("1980-04-04", tz="UTC"),
        pd.Timestamp("1980-05-26", tz="UTC"),
        pd.Timestamp("1980-07-04", tz="UTC"),
        pd.Timestamp("1980-09-01", tz="UTC"),
        pd.Timestamp("1980-11-04", tz="UTC"),
        pd.Timestamp("1980-11-27", tz="UTC"),
        pd.Timestamp("1980-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1981():
    start = "1981-01-01"
    end = "1981-12-31"
    holidays = [
        pd.Timestamp("1981-01-01", tz="UTC"),
        pd.Timestamp("1981-02-16", tz="UTC"),
        pd.Timestamp("1981-04-17", tz="UTC"),
        pd.Timestamp("1981-05-25", tz="UTC"),
        pd.Timestamp("1981-07-03", tz="UTC"),
        pd.Timestamp("1981-09-07", tz="UTC"),
        pd.Timestamp("1981-11-26", tz="UTC"),
        pd.Timestamp("1981-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1981-03-30 3:17PM", tz="America/New_York"),  # Reagan Assassination attemp
        pd.Timestamp("1981-09-09 3:28PM", tz="America/New_York"),  # Con Edison power failure
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1982():
    start = "1982-01-01"
    end = "1982-12-31"
    holidays = [
        pd.Timestamp("1982-01-01", tz="UTC"),
        pd.Timestamp("1982-02-15", tz="UTC"),
        pd.Timestamp("1982-04-09", tz="UTC"),
        pd.Timestamp("1982-05-31", tz="UTC"),
        pd.Timestamp("1982-07-05", tz="UTC"),
        pd.Timestamp("1982-09-06", tz="UTC"),
        pd.Timestamp("1982-11-25", tz="UTC"),
        pd.Timestamp("1982-12-24", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1983():
    start = "1983-01-01"
    end = "1983-12-31"
    holidays = [
        pd.Timestamp("1983-02-21", tz="UTC"),
        pd.Timestamp("1983-04-01", tz="UTC"),
        pd.Timestamp("1983-05-30", tz="UTC"),
        pd.Timestamp("1983-07-04", tz="UTC"),
        pd.Timestamp("1983-09-05", tz="UTC"),
        pd.Timestamp("1983-11-24", tz="UTC"),
        pd.Timestamp("1983-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1984():
    start = "1984-01-01"
    end = "1984-12-31"
    holidays = [
        pd.Timestamp("1984-01-02", tz="UTC"),
        pd.Timestamp("1984-02-20", tz="UTC"),
        pd.Timestamp("1984-04-20", tz="UTC"),
        pd.Timestamp("1984-05-28", tz="UTC"),
        pd.Timestamp("1984-07-04", tz="UTC"),
        pd.Timestamp("1984-09-03", tz="UTC"),
        pd.Timestamp("1984-11-22", tz="UTC"),
        pd.Timestamp("1984-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1985():
    start = "1985-01-01"
    end = "1985-12-31"
    holidays = [
        pd.Timestamp("1985-01-01", tz="UTC"),
        pd.Timestamp("1985-02-18", tz="UTC"),
        pd.Timestamp("1985-04-05", tz="UTC"),
        pd.Timestamp("1985-05-27", tz="UTC"),
        pd.Timestamp("1985-07-04", tz="UTC"),
        pd.Timestamp("1985-09-02", tz="UTC"),
        pd.Timestamp("1985-09-27", tz="UTC"),
        pd.Timestamp("1985-11-28", tz="UTC"),
        pd.Timestamp("1985-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1986():
    start = "1986-01-01"
    end = "1986-12-31"
    holidays = [
        pd.Timestamp("1986-01-01", tz="UTC"),
        pd.Timestamp("1986-02-17", tz="UTC"),
        pd.Timestamp("1986-03-28", tz="UTC"),
        pd.Timestamp("1986-05-26", tz="UTC"),
        pd.Timestamp("1986-07-04", tz="UTC"),
        pd.Timestamp("1986-09-01", tz="UTC"),
        pd.Timestamp("1986-11-27", tz="UTC"),
        pd.Timestamp("1986-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1987():
    start = "1987-01-01"
    end = "1987-12-31"
    holidays = [
        pd.Timestamp("1987-01-01", tz="UTC"),
        pd.Timestamp("1987-02-16", tz="UTC"),
        pd.Timestamp("1987-04-17", tz="UTC"),
        pd.Timestamp("1987-05-25", tz="UTC"),
        pd.Timestamp("1987-07-03", tz="UTC"),
        pd.Timestamp("1987-09-07", tz="UTC"),
        pd.Timestamp("1987-11-26", tz="UTC"),
        pd.Timestamp("1987-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    ec1 = pd.date_range(
        "1987-10-23 2:00PM",
        "1987-10-30 2:00PM",
        freq=CustomBusinessDay(holidays=nyse.holidays().holidays, weekmask="Mon Tue Wed Thu Fri"),
        tz="America/New_York",
    )  # Backlog Relief
    ec2 = pd.date_range(
        "1987-11-02 2:30PM",
        "1987-11-04 2:30PM",
        freq=CustomBusinessDay(holidays=nyse.holidays().holidays, weekmask="Mon Tue Wed Thu Fri"),
        tz="America/New_York",
    )  # Backlog Relief
    ec3 = pd.date_range(
        "1987-11-05 3:00PM",
        "1987-11-06 3:00PM",
        freq=CustomBusinessDay(holidays=nyse.holidays().holidays, weekmask="Mon Tue Wed Thu Fri"),
        tz="America/New_York",
    )  # Backlog Relief
    ec4 = pd.date_range(
        "1987-11-09 3:30PM",
        "1987-11-11 3:30PM",
        freq=CustomBusinessDay(holidays=nyse.holidays().holidays, weekmask="Mon Tue Wed Thu Fri"),
        tz="America/New_York",
    )  # Backlog Relief
    early_closes = ec1.append(ec2).append(ec3).append(ec4)

    _test_has_early_closes(early_closes, start, end)


def test_1988():
    start = "1988-01-01"
    end = "1988-12-31"
    holidays = [
        pd.Timestamp("1988-01-01", tz="UTC"),
        pd.Timestamp("1988-02-15", tz="UTC"),
        pd.Timestamp("1988-04-01", tz="UTC"),
        pd.Timestamp("1988-05-30", tz="UTC"),
        pd.Timestamp("1988-07-04", tz="UTC"),
        pd.Timestamp("1988-09-05", tz="UTC"),
        pd.Timestamp("1988-11-24", tz="UTC"),
        pd.Timestamp("1988-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1989():
    start = "1989-01-01"
    end = "1989-12-31"
    holidays = [
        pd.Timestamp("1989-01-02", tz="UTC"),
        pd.Timestamp("1989-02-20", tz="UTC"),
        pd.Timestamp("1989-03-24", tz="UTC"),
        pd.Timestamp("1989-05-29", tz="UTC"),
        pd.Timestamp("1989-07-04", tz="UTC"),
        pd.Timestamp("1989-09-04", tz="UTC"),
        pd.Timestamp("1989-11-23", tz="UTC"),
        pd.Timestamp("1989-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_closes(start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1989-11-10 11:00AM", tz="America/New_York"),  # electrical fire
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1990():
    start = "1990-01-01"
    end = "1990-12-31"
    holidays = [
        pd.Timestamp("1990-01-01", tz="UTC"),
        pd.Timestamp("1990-02-19", tz="UTC"),
        pd.Timestamp("1990-04-13", tz="UTC"),
        pd.Timestamp("1990-05-28", tz="UTC"),
        pd.Timestamp("1990-07-04", tz="UTC"),
        pd.Timestamp("1990-09-03", tz="UTC"),
        pd.Timestamp("1990-11-22", tz="UTC"),
        pd.Timestamp("1990-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1990-12-24 2:00PM", tz="America/New_York"),  # Christmas Eve
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1990-12-27 9:31AM", tz="America/New_York"),  # Con Edison transformer explosioin
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1991():
    start = "1991-01-01"
    end = "1991-12-31"
    holidays = [
        pd.Timestamp("1991-01-01", tz="UTC"),
        pd.Timestamp("1991-02-18", tz="UTC"),
        pd.Timestamp("1991-03-29", tz="UTC"),
        pd.Timestamp("1991-05-27", tz="UTC"),
        pd.Timestamp("1991-07-04", tz="UTC"),
        pd.Timestamp("1991-09-02", tz="UTC"),
        pd.Timestamp("1991-11-28", tz="UTC"),
        pd.Timestamp("1991-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1991-12-24 2:00PM", tz="America/New_York"),  # Christmas Eve
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1991-01-17 9:31AM", tz="America/New_York"),  # Troops in Gulf moment of silence
        pd.Timestamp("1991-02-25 9:31AM", tz="America/New_York"),  # Troops in Gulf moment of silence
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1992():
    start = "1992-01-01"
    end = "1992-12-31"
    holidays = [
        pd.Timestamp("1992-01-01", tz="UTC"),
        pd.Timestamp("1992-02-17", tz="UTC"),
        pd.Timestamp("1992-04-17", tz="UTC"),
        pd.Timestamp("1992-05-25", tz="UTC"),
        pd.Timestamp("1992-07-03", tz="UTC"),
        pd.Timestamp("1992-09-07", tz="UTC"),
        pd.Timestamp("1992-11-26", tz="UTC"),
        pd.Timestamp("1992-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1992-11-27 2:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("1992-12-24 2:00PM", tz="America/New_York"),  # Christmas Eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1993():
    start = "1993-01-01"
    end = "1993-12-31"
    holidays = [
        pd.Timestamp("1993-01-01", tz="UTC"),
        pd.Timestamp("1993-02-15", tz="UTC"),
        pd.Timestamp("1993-04-09", tz="UTC"),
        pd.Timestamp("1993-05-31", tz="UTC"),
        pd.Timestamp("1993-07-05", tz="UTC"),
        pd.Timestamp("1993-09-06", tz="UTC"),
        pd.Timestamp("1993-11-25", tz="UTC"),
        pd.Timestamp("1993-12-24", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1993-11-26 1:00PM", tz="America/New_York"),  # Christmas Eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1994():
    start = "1994-01-01"
    end = "1994-12-31"
    holidays = [
        pd.Timestamp("1994-02-21", tz="UTC"),
        pd.Timestamp("1994-04-01", tz="UTC"),
        pd.Timestamp("1994-04-27", tz="UTC"),
        pd.Timestamp("1994-05-30", tz="UTC"),
        pd.Timestamp("1994-07-04", tz="UTC"),
        pd.Timestamp("1994-09-05", tz="UTC"),
        pd.Timestamp("1994-11-24", tz="UTC"),
        pd.Timestamp("1994-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1994-02-11 2:30PM", tz="America/New_York"),  # snowstorm
        pd.Timestamp("1994-11-25 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1995():
    start = "1995-01-01"
    end = "1995-12-31"
    holidays = [
        pd.Timestamp("1995-01-02", tz="UTC"),
        pd.Timestamp("1995-02-20", tz="UTC"),
        pd.Timestamp("1995-04-14", tz="UTC"),
        pd.Timestamp("1995-05-29", tz="UTC"),
        pd.Timestamp("1995-07-04", tz="UTC"),
        pd.Timestamp("1995-09-04", tz="UTC"),
        pd.Timestamp("1995-11-23", tz="UTC"),
        pd.Timestamp("1995-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1995-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("1995-11-24 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1995-12-18 10:30AM", tz="America/New_York"),  # Computer system troubles
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1996():
    start = "1996-01-01"
    end = "1996-12-31"
    holidays = [
        pd.Timestamp("1996-01-01", tz="UTC"),
        pd.Timestamp("1996-02-19", tz="UTC"),
        pd.Timestamp("1996-04-05", tz="UTC"),
        pd.Timestamp("1996-05-27", tz="UTC"),
        pd.Timestamp("1996-07-04", tz="UTC"),
        pd.Timestamp("1996-09-02", tz="UTC"),
        pd.Timestamp("1996-11-28", tz="UTC"),
        pd.Timestamp("1996-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1996-01-08 2:00PM", tz="America/New_York"),  # snow
        pd.Timestamp("1996-07-05 1:00PM", tz="America/New_York"),  # Day after Independence Day
        pd.Timestamp("1996-11-29 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("1996-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("1996-01-08 11:00AM", tz="America/New_York"),  # snow
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1997():
    start = "1997-01-01"
    end = "1997-12-31"
    holidays = [
        pd.Timestamp("1997-01-01", tz="UTC"),
        pd.Timestamp("1997-02-17", tz="UTC"),
        pd.Timestamp("1997-03-28", tz="UTC"),
        pd.Timestamp("1997-05-26", tz="UTC"),
        pd.Timestamp("1997-07-04", tz="UTC"),
        pd.Timestamp("1997-09-01", tz="UTC"),
        pd.Timestamp("1997-11-27", tz="UTC"),
        pd.Timestamp("1997-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1997-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("1997-10-27 3:30PM", tz="America/New_York"),  # Circuit breaker triggered
        pd.Timestamp("1997-11-28 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("1997-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
        pd.Timestamp("1997-12-26 1:00PM", tz="America/New_York"),  # Day after Christmas
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1998():
    start = "1998-01-01"
    end = "1998-12-31"
    holidays = [
        pd.Timestamp("1998-01-01", tz="UTC"),
        pd.Timestamp("1998-01-19", tz="UTC"),
        pd.Timestamp("1998-02-16", tz="UTC"),
        pd.Timestamp("1998-04-10", tz="UTC"),
        pd.Timestamp("1998-05-25", tz="UTC"),
        pd.Timestamp("1998-07-03", tz="UTC"),
        pd.Timestamp("1998-09-07", tz="UTC"),
        pd.Timestamp("1998-11-26", tz="UTC"),
        pd.Timestamp("1998-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1998-11-27 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("1998-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_1999():
    start = "1999-01-01"
    end = "1999-12-31"
    holidays = [
        pd.Timestamp("1999-01-01", tz="UTC"),
        pd.Timestamp("1999-01-18", tz="UTC"),
        pd.Timestamp("1999-02-15", tz="UTC"),
        pd.Timestamp("1999-04-02", tz="UTC"),
        pd.Timestamp("1999-05-31", tz="UTC"),
        pd.Timestamp("1999-07-05", tz="UTC"),
        pd.Timestamp("1999-09-06", tz="UTC"),
        pd.Timestamp("1999-11-25", tz="UTC"),
        pd.Timestamp("1999-12-24", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("1999-11-26 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2000():
    start = "2000-01-01"
    end = "2000-12-31"
    holidays = [
        pd.Timestamp("2000-01-17", tz="UTC"),
        pd.Timestamp("2000-02-21", tz="UTC"),
        pd.Timestamp("2000-04-21", tz="UTC"),
        pd.Timestamp("2000-05-29", tz="UTC"),
        pd.Timestamp("2000-07-04", tz="UTC"),
        pd.Timestamp("2000-09-04", tz="UTC"),
        pd.Timestamp("2000-11-23", tz="UTC"),
        pd.Timestamp("2000-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2000-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2000-11-24 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2001():
    start = "2001-01-01"
    end = "2001-12-31"
    holidays = [
        pd.Timestamp("2001-01-01", tz="UTC"),
        pd.Timestamp("2001-01-15", tz="UTC"),
        pd.Timestamp("2001-02-19", tz="UTC"),
        pd.Timestamp("2001-04-13", tz="UTC"),
        pd.Timestamp("2001-05-28", tz="UTC"),
        pd.Timestamp("2001-07-04", tz="UTC"),
        pd.Timestamp("2001-09-03", tz="UTC"),
        pd.Timestamp("2001-09-11", tz="UTC"),
        pd.Timestamp("2001-09-12", tz="UTC"),
        pd.Timestamp("2001-09-13", tz="UTC"),
        pd.Timestamp("2001-09-14", tz="UTC"),
        pd.Timestamp("2001-11-22", tz="UTC"),
        pd.Timestamp("2001-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2001-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2001-11-23 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2001-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("2001-09-17 9:33AM", tz="America/New_York"),  # 9/11 victims moment of silence
        pd.Timestamp("2001-10-08 9:31AM", tz="America/New_York"),  # Enduring Freedom troops moment of silence
    ]
    _test_has_late_opens(late_opens, start, end)


def test_2002():
    start = "2002-01-01"
    end = "2002-12-31"
    holidays = [
        pd.Timestamp("2002-01-01", tz="UTC"),
        pd.Timestamp("2002-01-21", tz="UTC"),
        pd.Timestamp("2002-02-18", tz="UTC"),
        pd.Timestamp("2002-03-29", tz="UTC"),
        pd.Timestamp("2002-05-27", tz="UTC"),
        pd.Timestamp("2002-07-04", tz="UTC"),
        pd.Timestamp("2002-09-02", tz="UTC"),
        pd.Timestamp("2002-11-28", tz="UTC"),
        pd.Timestamp("2002-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2002-07-05 1:00PM", tz="America/New_York"),  # Day after Independence Day
        pd.Timestamp("2002-11-29 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2002-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("2002-09-11 12:00PM", tz="America/New_York"),  # 9/11 anniversary
    ]
    _test_has_late_opens(late_opens, start, end)


def test_2003():
    start = "2003-01-01"
    end = "2003-12-31"
    holidays = [
        pd.Timestamp("2003-01-01", tz="UTC"),
        pd.Timestamp("2003-01-20", tz="UTC"),
        pd.Timestamp("2003-02-17", tz="UTC"),
        pd.Timestamp("2003-04-18", tz="UTC"),
        pd.Timestamp("2003-05-26", tz="UTC"),
        pd.Timestamp("2003-07-04", tz="UTC"),
        pd.Timestamp("2003-09-01", tz="UTC"),
        pd.Timestamp("2003-11-27", tz="UTC"),
        pd.Timestamp("2003-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2003-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2003-11-28 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2003-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
        pd.Timestamp("2003-12-26 1:00PM", tz="America/New_York"),  # Friday after Christmas
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("2003-03-20 9:32AM", tz="America/New_York"),  # Iraqi freedom moment of silence
    ]
    _test_has_late_opens(late_opens, start, end)


def test_2004():
    start = "2004-01-01"
    end = "2004-12-31"
    holidays = [
        pd.Timestamp("2004-01-01", tz="UTC"),
        pd.Timestamp("2004-01-19", tz="UTC"),
        pd.Timestamp("2004-02-16", tz="UTC"),
        pd.Timestamp("2004-04-09", tz="UTC"),
        pd.Timestamp("2004-05-31", tz="UTC"),
        pd.Timestamp("2004-06-11", tz="UTC"),
        pd.Timestamp("2004-07-05", tz="UTC"),
        pd.Timestamp("2004-09-06", tz="UTC"),
        pd.Timestamp("2004-11-25", tz="UTC"),
        pd.Timestamp("2004-12-24", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2004-11-26 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("2004-06-07 9:32AM", tz="America/New_York"),  # President Reagan moment of silence
    ]
    _test_has_late_opens(late_opens, start, end)


def test_2005():
    start = "2005-01-01"
    end = "2005-12-31"
    holidays = [
        pd.Timestamp("2005-01-17", tz="UTC"),
        pd.Timestamp("2005-02-21", tz="UTC"),
        pd.Timestamp("2005-03-25", tz="UTC"),
        pd.Timestamp("2005-05-30", tz="UTC"),
        pd.Timestamp("2005-07-04", tz="UTC"),
        pd.Timestamp("2005-09-05", tz="UTC"),
        pd.Timestamp("2005-11-24", tz="UTC"),
        pd.Timestamp("2005-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2005-06-01 3:56PM", tz="America/New_York"),  # Systems communication problem
        pd.Timestamp("2005-11-25 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2006():
    start = "2006-01-01"
    end = "2006-12-31"
    holidays = [
        pd.Timestamp("2006-01-02", tz="UTC"),
        pd.Timestamp("2006-01-16", tz="UTC"),
        pd.Timestamp("2006-02-20", tz="UTC"),
        pd.Timestamp("2006-04-14", tz="UTC"),
        pd.Timestamp("2006-05-29", tz="UTC"),
        pd.Timestamp("2006-07-04", tz="UTC"),
        pd.Timestamp("2006-09-04", tz="UTC"),
        pd.Timestamp("2006-11-23", tz="UTC"),
        pd.Timestamp("2006-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2006-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2006-11-24 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
        pd.Timestamp("2006-12-27 9:32AM", tz="America/New_York"),  # President Ford moment of silence
    ]
    _test_has_late_opens(late_opens, start, end)


def test_2007():
    start = "2007-01-01"
    end = "2007-12-31"
    holidays = [
        pd.Timestamp("2007-01-01", tz="UTC"),
        pd.Timestamp("2007-01-02", tz="UTC"),
        pd.Timestamp("2007-01-15", tz="UTC"),
        pd.Timestamp("2007-02-19", tz="UTC"),
        pd.Timestamp("2007-04-06", tz="UTC"),
        pd.Timestamp("2007-05-28", tz="UTC"),
        pd.Timestamp("2007-07-04", tz="UTC"),
        pd.Timestamp("2007-09-03", tz="UTC"),
        pd.Timestamp("2007-11-22", tz="UTC"),
        pd.Timestamp("2007-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2007-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2007-11-23 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2007-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2008():
    start = "2008-01-01"
    end = "2008-12-31"
    holidays = [
        pd.Timestamp("2008-01-01", tz="UTC"),
        pd.Timestamp("2008-01-21", tz="UTC"),
        pd.Timestamp("2008-02-18", tz="UTC"),
        pd.Timestamp("2008-03-21", tz="UTC"),
        pd.Timestamp("2008-05-26", tz="UTC"),
        pd.Timestamp("2008-07-04", tz="UTC"),
        pd.Timestamp("2008-09-01", tz="UTC"),
        pd.Timestamp("2008-11-27", tz="UTC"),
        pd.Timestamp("2008-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2008-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2008-11-28 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2008-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2009():
    start = "2009-01-01"
    end = "2009-12-31"
    holidays = [
        pd.Timestamp("2009-01-01", tz="UTC"),
        pd.Timestamp("2009-01-19", tz="UTC"),
        pd.Timestamp("2009-02-16", tz="UTC"),
        pd.Timestamp("2009-04-10", tz="UTC"),
        pd.Timestamp("2009-05-25", tz="UTC"),
        pd.Timestamp("2009-07-03", tz="UTC"),
        pd.Timestamp("2009-09-07", tz="UTC"),
        pd.Timestamp("2009-11-26", tz="UTC"),
        pd.Timestamp("2009-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2009-11-27 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2009-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2010():
    start = "2010-01-01"
    end = "2010-12-31"
    holidays = [
        pd.Timestamp("2010-01-01", tz="UTC"),
        pd.Timestamp("2010-01-18", tz="UTC"),
        pd.Timestamp("2010-02-15", tz="UTC"),
        pd.Timestamp("2010-04-02", tz="UTC"),
        pd.Timestamp("2010-05-31", tz="UTC"),
        pd.Timestamp("2010-07-05", tz="UTC"),
        pd.Timestamp("2010-09-06", tz="UTC"),
        pd.Timestamp("2010-11-25", tz="UTC"),
        pd.Timestamp("2010-12-24", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2010-11-26 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2011():
    start = "2011-01-01"
    end = "2011-12-31"
    holidays = [
        pd.Timestamp("2011-01-17", tz="UTC"),
        pd.Timestamp("2011-02-21", tz="UTC"),
        pd.Timestamp("2011-04-22", tz="UTC"),
        pd.Timestamp("2011-05-30", tz="UTC"),
        pd.Timestamp("2011-07-04", tz="UTC"),
        pd.Timestamp("2011-09-05", tz="UTC"),
        pd.Timestamp("2011-11-24", tz="UTC"),
        pd.Timestamp("2011-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2011-11-25 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2012():
    start = "2012-01-01"
    end = "2012-12-31"
    holidays = [
        pd.Timestamp("2012-01-02", tz="UTC"),
        pd.Timestamp("2012-01-16", tz="UTC"),
        pd.Timestamp("2012-02-20", tz="UTC"),
        pd.Timestamp("2012-04-06", tz="UTC"),
        pd.Timestamp("2012-05-28", tz="UTC"),
        pd.Timestamp("2012-07-04", tz="UTC"),
        pd.Timestamp("2012-09-03", tz="UTC"),
        pd.Timestamp("2012-10-29", tz="UTC"),
        pd.Timestamp("2012-10-30", tz="UTC"),
        pd.Timestamp("2012-11-22", tz="UTC"),
        pd.Timestamp("2012-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2012-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2012-11-23 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2012-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2013():
    start = "2013-01-01"
    end = "2013-12-31"
    holidays = [
        pd.Timestamp("2013-01-01", tz="UTC"),
        pd.Timestamp("2013-01-21", tz="UTC"),
        pd.Timestamp("2013-02-18", tz="UTC"),
        pd.Timestamp("2013-03-29", tz="UTC"),
        pd.Timestamp("2013-05-27", tz="UTC"),
        pd.Timestamp("2013-07-04", tz="UTC"),
        pd.Timestamp("2013-09-02", tz="UTC"),
        pd.Timestamp("2013-11-28", tz="UTC"),
        pd.Timestamp("2013-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2013-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2013-11-29 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2013-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2014():
    start = "2014-01-01"
    end = "2014-12-31"
    holidays = [
        pd.Timestamp("2014-01-01", tz="UTC"),
        pd.Timestamp("2014-01-20", tz="UTC"),
        pd.Timestamp("2014-02-17", tz="UTC"),
        pd.Timestamp("2014-04-18", tz="UTC"),
        pd.Timestamp("2014-05-26", tz="UTC"),
        pd.Timestamp("2014-07-04", tz="UTC"),
        pd.Timestamp("2014-09-01", tz="UTC"),
        pd.Timestamp("2014-11-27", tz="UTC"),
        pd.Timestamp("2014-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2014-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2014-11-28 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2014-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2015():
    start = "2015-01-01"
    end = "2015-12-31"
    holidays = [
        pd.Timestamp("2015-01-01", tz="UTC"),
        pd.Timestamp("2015-01-19", tz="UTC"),
        pd.Timestamp("2015-02-16", tz="UTC"),
        pd.Timestamp("2015-04-03", tz="UTC"),
        pd.Timestamp("2015-05-25", tz="UTC"),
        pd.Timestamp("2015-07-03", tz="UTC"),
        pd.Timestamp("2015-09-07", tz="UTC"),
        pd.Timestamp("2015-11-26", tz="UTC"),
        pd.Timestamp("2015-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2015-11-27 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2015-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2016():
    start = "2016-01-01"
    end = "2016-12-31"
    holidays = [
        pd.Timestamp("2016-01-01", tz="UTC"),
        pd.Timestamp("2016-01-18", tz="UTC"),
        pd.Timestamp("2016-02-15", tz="UTC"),
        pd.Timestamp("2016-03-25", tz="UTC"),
        pd.Timestamp("2016-05-30", tz="UTC"),
        pd.Timestamp("2016-07-04", tz="UTC"),
        pd.Timestamp("2016-09-05", tz="UTC"),
        pd.Timestamp("2016-11-24", tz="UTC"),
        pd.Timestamp("2016-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2016-11-25 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2017():
    start = "2017-01-01"
    end = "2017-12-31"
    holidays = [
        pd.Timestamp("2017-01-02", tz="UTC"),
        pd.Timestamp("2017-01-16", tz="UTC"),
        pd.Timestamp("2017-02-20", tz="UTC"),
        pd.Timestamp("2017-04-14", tz="UTC"),
        pd.Timestamp("2017-05-29", tz="UTC"),
        pd.Timestamp("2017-07-04", tz="UTC"),
        pd.Timestamp("2017-09-04", tz="UTC"),
        pd.Timestamp("2017-11-23", tz="UTC"),
        pd.Timestamp("2017-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2017-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2017-11-24 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2018():
    start = "2018-01-01"
    end = "2018-12-31"
    holidays = [
        pd.Timestamp("2018-01-01", tz="UTC"),
        pd.Timestamp("2018-01-15", tz="UTC"),
        pd.Timestamp("2018-02-19", tz="UTC"),
        pd.Timestamp("2018-03-30", tz="UTC"),
        pd.Timestamp("2018-05-28", tz="UTC"),
        pd.Timestamp("2018-07-04", tz="UTC"),
        pd.Timestamp("2018-09-03", tz="UTC"),
        pd.Timestamp("2018-11-22", tz="UTC"),
        pd.Timestamp("2018-12-05", tz="UTC"),
        pd.Timestamp("2018-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2018-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2018-11-23 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2018-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2019():
    start = "2019-01-01"
    end = "2019-12-31"
    holidays = [
        pd.Timestamp("2019-01-01", tz="UTC"),
        pd.Timestamp("2019-01-21", tz="UTC"),
        pd.Timestamp("2019-02-18", tz="UTC"),
        pd.Timestamp("2019-04-19", tz="UTC"),
        pd.Timestamp("2019-05-27", tz="UTC"),
        pd.Timestamp("2019-07-04", tz="UTC"),
        pd.Timestamp("2019-09-02", tz="UTC"),
        pd.Timestamp("2019-11-28", tz="UTC"),
        pd.Timestamp("2019-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2019-07-03 1:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2019-11-29 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2019-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2020():
    start = "2020-01-01"
    end = "2020-12-31"
    holidays = [
        pd.Timestamp("2020-01-01", tz="UTC"),
        pd.Timestamp("2020-01-20", tz="UTC"),
        pd.Timestamp("2020-02-17", tz="UTC"),
        pd.Timestamp("2020-04-10", tz="UTC"),
        pd.Timestamp("2020-05-25", tz="UTC"),
        pd.Timestamp("2020-07-03", tz="UTC"),
        pd.Timestamp("2020-09-07", tz="UTC"),
        pd.Timestamp("2020-11-26", tz="UTC"),
        pd.Timestamp("2020-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2020-11-27 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2020-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2021():
    start = "2021-01-01"
    end = "2021-12-31"
    holidays = [
        pd.Timestamp("2021-01-01", tz="UTC"),
        pd.Timestamp("2021-01-18", tz="UTC"),
        pd.Timestamp("2021-02-15", tz="UTC"),
        pd.Timestamp("2021-04-02", tz="UTC"),
        pd.Timestamp("2021-05-31", tz="UTC"),
        pd.Timestamp("2021-07-05", tz="UTC"),
        pd.Timestamp("2021-09-06", tz="UTC"),
        pd.Timestamp("2021-11-25", tz="UTC"),
        pd.Timestamp("2021-12-24", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2021-11-26 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2022():
    start = "2022-01-01"
    end = "2022-12-31"
    holidays = [
        pd.Timestamp("2022-01-17", tz="UTC"),
        pd.Timestamp("2022-02-21", tz="UTC"),
        pd.Timestamp("2022-04-15", tz="UTC"),
        pd.Timestamp("2022-05-30", tz="UTC"),
        pd.Timestamp("2022-06-20", tz="UTC"),
        pd.Timestamp("2022-07-04", tz="UTC"),
        pd.Timestamp("2022-09-05", tz="UTC"),
        pd.Timestamp("2022-11-24", tz="UTC"),
        pd.Timestamp("2022-12-26", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2022-11-25 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2023():
    start = "2023-01-01"
    end = "2023-12-31"
    holidays = [
        pd.Timestamp("2023-01-02", tz="UTC"),
        pd.Timestamp("2023-01-16", tz="UTC"),
        pd.Timestamp("2023-02-20", tz="UTC"),
        pd.Timestamp("2023-04-07", tz="UTC"),
        pd.Timestamp("2023-05-29", tz="UTC"),
        pd.Timestamp("2023-06-19", tz="UTC"),
        pd.Timestamp("2023-07-04", tz="UTC"),
        pd.Timestamp("2023-09-04", tz="UTC"),
        pd.Timestamp("2023-11-23", tz="UTC"),
        pd.Timestamp("2023-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2023-07-03 1:00PM", tz="America/New_York"),  # Day before July 4th
        pd.Timestamp("2023-11-24 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2024():
    start = "2024-01-01"
    end = "2024-12-31"
    holidays = [
        pd.Timestamp("2024-01-01", tz="UTC"),
        pd.Timestamp("2024-01-15", tz="UTC"),
        pd.Timestamp("2024-02-19", tz="UTC"),
        pd.Timestamp("2024-03-29", tz="UTC"),
        pd.Timestamp("2024-05-27", tz="UTC"),
        pd.Timestamp("2024-06-19", tz="UTC"),
        pd.Timestamp("2024-07-04", tz="UTC"),
        pd.Timestamp("2024-09-02", tz="UTC"),
        pd.Timestamp("2024-11-28", tz="UTC"),
        pd.Timestamp("2024-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2024-07-03 1:00PM", tz="America/New_York"),  # Day before July 4th
        pd.Timestamp("2024-11-29 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2024-12-24 1:00PM", tz="America/New_York"),  # Christmas eve
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2025():
    start = "2025-01-01"
    end = "2025-12-31"
    holidays = [
        pd.Timestamp("2025-01-01", tz="UTC"),
        pd.Timestamp("2025-01-09", tz="UTC"),
        pd.Timestamp("2025-01-20", tz="UTC"),
        pd.Timestamp("2025-02-17", tz="UTC"),
        pd.Timestamp("2025-04-18", tz="UTC"),
        pd.Timestamp("2025-05-26", tz="UTC"),
        pd.Timestamp("2025-06-19", tz="UTC"),
        pd.Timestamp("2025-07-04", tz="UTC"),
        pd.Timestamp("2025-09-01", tz="UTC"),
        pd.Timestamp("2025-11-27", tz="UTC"),
        pd.Timestamp("2025-12-25", tz="UTC"),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2025-07-03 1:00PM", tz="America/New_York"),  # Day before July 4th
        pd.Timestamp("2025-11-28 1:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2025-12-24 1:00PM", tz="America/New_York"),  # Christmas Eve
    ]
    _test_has_early_closes(early_closes, start, end)
