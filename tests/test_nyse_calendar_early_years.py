import os

import pandas as pd
import pytz
from pandas.testing import assert_index_equal

from pandas_market_calendars.exchange_calendar_nyse import NYSEExchangeCalendar

all_holidays = pd.DatetimeIndex(NYSEExchangeCalendar().holidays().holidays)
print(all_holidays[0:10])


def test_time_zone():
    assert NYSEExchangeCalendar().tz == pytz.timezone('America/New_York')
    assert NYSEExchangeCalendar().name == 'NYSE'


def test_open_time_tz():
    nyse = NYSEExchangeCalendar()
    assert nyse.open_time.tzinfo == nyse.tz


def test_close_time_tz():
    nyse = NYSEExchangeCalendar()
    assert nyse.close_time.tzinfo == nyse.tz


def test_1885():
    nyse = NYSEExchangeCalendar()
    holidays_1885 = [
       pd.Timestamp('1885-01-01' , tz='UTC'),
       pd.Timestamp('1885-02-23' , tz='UTC'),
       pd.Timestamp('1885-04-03' , tz='UTC'),
       pd.Timestamp('1885-05-30' , tz='UTC'),
       pd.Timestamp('1885-07-04' , tz='UTC'),
       pd.Timestamp('1885-08-08' , tz='UTC'),
       pd.Timestamp('1885-11-03' , tz='UTC'),
       pd.Timestamp('1885-11-26' , tz='UTC'),
       pd.Timestamp('1885-12-25' , tz='UTC')
    ]
    valid_days = nyse.valid_days('1885-01-01', '1885-12-31')
    for h in holidays_1885:
        assert h not in valid_days
        assert h in all_holidays    
        
    #ensure labor day is a valid trading day
    assert pd.Timestamp('1885-09-07' , tz='UTC') in valid_days

def test_1886():
    nyse = NYSEExchangeCalendar()
    holidays_1886 = [
        pd.Timestamp('1886-01-01' , tz='UTC'),
        pd.Timestamp('1886-02-22' , tz='UTC'),
        pd.Timestamp('1886-04-23' , tz='UTC'),
        pd.Timestamp('1886-05-31' , tz='UTC'),
        pd.Timestamp('1886-07-05' , tz='UTC'),
        pd.Timestamp('1886-11-02' , tz='UTC'),
        pd.Timestamp('1886-11-25' , tz='UTC'),
        pd.Timestamp('1886-12-25' , tz='UTC')
    ]
    valid_days = nyse.valid_days('1886-01-01', '1886-12-31')
    for h in holidays_1886:
        assert h not in valid_days
        assert h in all_holidays


def test_1887():
    nyse = NYSEExchangeCalendar()
    holidays_1887 = [
        pd.Timestamp("1887-01-01", tz='UTC'),
        pd.Timestamp("1887-02-22", tz='UTC'),
        pd.Timestamp("1887-04-08", tz='UTC'),
        pd.Timestamp("1887-05-30", tz='UTC'),
        pd.Timestamp("1887-07-02", tz='UTC'),
        pd.Timestamp("1887-07-04", tz='UTC'),
        pd.Timestamp("1887-09-05", tz='UTC'),
        pd.Timestamp("1887-11-08", tz='UTC'),
        pd.Timestamp("1887-11-24", tz='UTC'),
        pd.Timestamp("1887-12-24", tz='UTC'),
        pd.Timestamp("1887-12-26", tz='UTC')
    ]
    valid_days = nyse.valid_days('1887-01-01', '1887-12-31')
    for h in holidays_1887:
        assert h not in valid_days
        assert h in all_holidays

    # early closes we expect:
    early_closes_1887 = [
        pd.Timestamp(' 1887-01-08 ' , tz='UTC'),
        pd.Timestamp(' 1887-01-15 ' , tz='UTC'),
        pd.Timestamp(' 1887-01-22 ' , tz='UTC'),
        pd.Timestamp(' 1887-01-29 ' , tz='UTC'),
        pd.Timestamp(' 1887-02-05 ' , tz='UTC'),
        pd.Timestamp(' 1887-02-12 ' , tz='UTC'),
        pd.Timestamp(' 1887-02-19 ' , tz='UTC'),
        pd.Timestamp(' 1887-02-26 ' , tz='UTC'),
        pd.Timestamp(' 1887-03-05 ' , tz='UTC'),
        pd.Timestamp(' 1887-03-12 ' , tz='UTC'),
        pd.Timestamp(' 1887-03-19 ' , tz='UTC'),
        pd.Timestamp(' 1887-03-26 ' , tz='UTC'),
        pd.Timestamp(' 1887-04-02 ' , tz='UTC'),
        pd.Timestamp(' 1887-04-09 ' , tz='UTC'),
        pd.Timestamp(' 1887-04-16 ' , tz='UTC'),
        pd.Timestamp(' 1887-04-23 ' , tz='UTC'),
        pd.Timestamp(' 1887-04-30 ' , tz='UTC'),
        pd.Timestamp(' 1887-05-07 ' , tz='UTC'),
        pd.Timestamp(' 1887-05-14 ' , tz='UTC'),
        pd.Timestamp(' 1887-05-21 ' , tz='UTC'),
        pd.Timestamp(' 1887-05-28 ' , tz='UTC'),
        pd.Timestamp(' 1887-06-04 ' , tz='UTC'),
        pd.Timestamp(' 1887-06-11 ' , tz='UTC'),
        pd.Timestamp(' 1887-06-18 ' , tz='UTC'),
        pd.Timestamp(' 1887-06-25 ' , tz='UTC'),
        pd.Timestamp(' 1887-07-09 ' , tz='UTC'),
        pd.Timestamp(' 1887-07-16 ' , tz='UTC'),
        pd.Timestamp(' 1887-07-23 ' , tz='UTC'),
        pd.Timestamp(' 1887-07-30 ' , tz='UTC'),
        pd.Timestamp(' 1887-08-06 ' , tz='UTC'),
        pd.Timestamp(' 1887-08-13 ' , tz='UTC'),
        pd.Timestamp(' 1887-08-20 ' , tz='UTC'),
        pd.Timestamp(' 1887-08-27 ' , tz='UTC'),
        pd.Timestamp(' 1887-09-03 ' , tz='UTC'),
        pd.Timestamp(' 1887-09-10 ' , tz='UTC'),
        pd.Timestamp(' 1887-09-17 ' , tz='UTC'),
        pd.Timestamp(' 1887-09-24 ' , tz='UTC'),
        pd.Timestamp(' 1887-10-01 ' , tz='UTC'),
        pd.Timestamp(' 1887-10-08 ' , tz='UTC'),
        pd.Timestamp(' 1887-10-15 ' , tz='UTC'),
        pd.Timestamp(' 1887-10-22 ' , tz='UTC'),
        pd.Timestamp(' 1887-10-29 ' , tz='UTC'),
        pd.Timestamp(' 1887-11-05 ' , tz='UTC'),
        pd.Timestamp(' 1887-11-12 ' , tz='UTC'),
        pd.Timestamp(' 1887-11-19 ' , tz='UTC'),
        pd.Timestamp(' 1887-11-26 ' , tz='UTC'),
        pd.Timestamp(' 1887-12-03 ' , tz='UTC'),
        pd.Timestamp(' 1887-12-10 ' , tz='UTC'),
        pd.Timestamp(' 1887-12-17 ' , tz='UTC'),
        pd.Timestamp(' 1887-12-31 ' , tz='UTC')
    ]

    expected = nyse.early_closes(nyse.schedule('1887-01-01', '1887-12-31'))
    assert len(expected) == 50
    for early_close_h in early_closes_1887:
        assert early_close_h in expected.index

def test_1888():
    nyse = NYSEExchangeCalendar()
    holidays_1888 = [
        pd.Timestamp('1888-01-02' , tz='UTC'),
        pd.Timestamp('1888-02-22' , tz='UTC'),
        pd.Timestamp('1888-03-12' , tz='UTC'),
        pd.Timestamp('1888-03-13' , tz='UTC'),
        pd.Timestamp('1888-03-30' , tz='UTC'),
        pd.Timestamp('1888-05-30' , tz='UTC'),
        pd.Timestamp('1888-07-04' , tz='UTC'),
        pd.Timestamp('1888-09-01' , tz='UTC'),
        pd.Timestamp('1888-09-03' , tz='UTC'),
        pd.Timestamp('1888-11-06' , tz='UTC'),
        pd.Timestamp('1888-11-29' , tz='UTC'),
        pd.Timestamp('1888-11-30' , tz='UTC'),
        pd.Timestamp('1888-12-25' , tz='UTC')
    ]
    valid_days = nyse.valid_days('1888-01-01', '1888-12-31')
    for h in holidays_1888:
        assert h not in valid_days
        assert h in all_holidays
        
def test_1889():
    nyse = NYSEExchangeCalendar()
    holidays_1889 = [
        pd.Timestamp('1889-01-01' , tz='UTC'),
        pd.Timestamp('1889-02-22' , tz='UTC'),
        pd.Timestamp('1889-04-19' , tz='UTC'),
        pd.Timestamp('1889-04-29' , tz='UTC'),
        pd.Timestamp('1889-04-30' , tz='UTC'),
        pd.Timestamp('1889-05-01' , tz='UTC'),
        pd.Timestamp('1889-05-30' , tz='UTC'),
        pd.Timestamp('1889-07-04' , tz='UTC'),
        pd.Timestamp('1889-09-02' , tz='UTC'),
        pd.Timestamp('1889-11-05' , tz='UTC'),
        pd.Timestamp('1889-11-28' , tz='UTC'),
        pd.Timestamp('1889-12-25' , tz='UTC')
    ]
    valid_days = nyse.valid_days('1889-01-01', '1889-12-31')
    for h in holidays_1889:
        assert h not in valid_days
        assert h in all_holidays        

def test_1890():
    nyse = NYSEExchangeCalendar()
    holidays_1890 = [
        pd.Timestamp('1890-01-01' , tz='UTC'),
        pd.Timestamp('1890-02-22' , tz='UTC'),
        pd.Timestamp('1890-04-04' , tz='UTC'),
        pd.Timestamp('1890-05-30' , tz='UTC'),
        pd.Timestamp('1890-07-04' , tz='UTC'),
        pd.Timestamp('1890-07-05' , tz='UTC'),
        pd.Timestamp('1890-09-01' , tz='UTC'),
        pd.Timestamp('1890-11-04' , tz='UTC'),
        pd.Timestamp('1890-11-27' , tz='UTC'),
        pd.Timestamp('1890-12-25' , tz='UTC')
    ]
    valid_days = nyse.valid_days('1890-01-01', '1890-12-31')  
    for h in holidays_1890:
        assert h not in valid_days
        assert h in all_holidays

def test_1891():
    nyse = NYSEExchangeCalendar()
    holidays_1891 = [
        pd.Timestamp('1891-01-01' , tz='UTC'),
        pd.Timestamp('1891-02-23' , tz='UTC'),
        pd.Timestamp('1891-03-27' , tz='UTC'),
        pd.Timestamp('1891-05-30' , tz='UTC'),
        pd.Timestamp('1891-07-04' , tz='UTC'),
        pd.Timestamp('1891-09-07' , tz='UTC'),
        pd.Timestamp('1891-11-03' , tz='UTC'),
        pd.Timestamp('1891-11-26' , tz='UTC'),
        pd.Timestamp('1891-12-25' , tz='UTC'),
        pd.Timestamp('1891-12-26' , tz='UTC')
    ]
    valid_days = nyse.valid_days('1891-01-01', '1891-12-31') 
    for h in holidays_1891:
        assert h not in valid_days
        assert h in all_holidays
        

def test_1892():
    nyse = NYSEExchangeCalendar()
    holidays_1892 = [
        pd.Timestamp('1892-01-01' , tz='UTC'),
        pd.Timestamp('1892-02-22' , tz='UTC'),
        pd.Timestamp('1892-04-15' , tz='UTC'),
        pd.Timestamp('1892-05-30' , tz='UTC'),
        pd.Timestamp('1892-07-02' , tz='UTC'),
        pd.Timestamp('1892-07-04' , tz='UTC'),
        pd.Timestamp('1892-09-05' , tz='UTC'),
        pd.Timestamp('1892-10-12' , tz='UTC'),
        pd.Timestamp('1892-10-21' , tz='UTC'),
        pd.Timestamp('1892-10-22' , tz='UTC'),
        pd.Timestamp('1892-11-08' , tz='UTC'),
        pd.Timestamp('1892-11-24' , tz='UTC'),
        pd.Timestamp('1892-12-26' , tz='UTC')
    ]
    valid_days = nyse.valid_days('1892-01-01', '1892-12-31')
    for h in holidays_1892:
        assert h not in valid_days
        assert h in all_holidays
        
def test_1893():
    nyse = NYSEExchangeCalendar()
    holidays_1893 = [
        pd.Timestamp('1893-01-02', tz='UTC'),
        pd.Timestamp('1893-02-22', tz='UTC'),
        pd.Timestamp('1893-03-31', tz='UTC'),
        pd.Timestamp('1893-04-27', tz='UTC'),
        pd.Timestamp('1893-05-30', tz='UTC'),
        pd.Timestamp('1893-07-04', tz='UTC'),
        pd.Timestamp('1893-09-04', tz='UTC'),
        pd.Timestamp('1893-11-07', tz='UTC'),
        pd.Timestamp('1893-11-30', tz='UTC'),
        pd.Timestamp('1893-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1893-01-01', '1893-12-31')
    for h in holidays_1893:
        assert h not in valid_days
        assert h in all_holidays

def test_1894():
    nyse = NYSEExchangeCalendar()
    holidays_1894 = [
        pd.Timestamp('1894-01-01', tz='UTC'),
        pd.Timestamp('1894-02-22', tz='UTC'),
        pd.Timestamp('1894-03-23', tz='UTC'),
        pd.Timestamp('1894-05-30', tz='UTC'),
        pd.Timestamp('1894-07-04', tz='UTC'),
        pd.Timestamp('1894-09-03', tz='UTC'),
        pd.Timestamp('1894-11-06', tz='UTC'),
        pd.Timestamp('1894-11-29', tz='UTC'),
        pd.Timestamp('1894-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1894-01-01', '1894-12-31')
    for h in holidays_1894:
        assert h not in valid_days
        assert h in all_holidays

def test_1895():
    nyse = NYSEExchangeCalendar()
    holidays_1895 = [
        pd.Timestamp('1895-01-01', tz='UTC'),
        pd.Timestamp('1895-02-22', tz='UTC'),
        pd.Timestamp('1895-04-12', tz='UTC'),
        pd.Timestamp('1895-05-30', tz='UTC'),
        pd.Timestamp('1895-07-04', tz='UTC'),
        pd.Timestamp('1895-09-02', tz='UTC'),
        pd.Timestamp('1895-11-05', tz='UTC'),
        pd.Timestamp('1895-11-28', tz='UTC'),
        pd.Timestamp('1895-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1895-01-01', '1895-12-31')
    for h in holidays_1895:
        assert h not in valid_days
        assert h in all_holidays


def test_1896():
    nyse = NYSEExchangeCalendar()
    holidays_1896 = [
        pd.Timestamp('1896-01-01', tz='UTC'),
        pd.Timestamp('1896-02-12', tz='UTC'),
        pd.Timestamp('1896-02-22', tz='UTC'),
        pd.Timestamp('1896-04-03', tz='UTC'),
        pd.Timestamp('1896-05-30', tz='UTC'),
        pd.Timestamp('1896-07-04', tz='UTC'),
        pd.Timestamp('1896-09-07', tz='UTC'),
        pd.Timestamp('1896-11-03', tz='UTC'),
        pd.Timestamp('1896-11-26', tz='UTC'),
        pd.Timestamp('1896-12-25', tz='UTC'),
        pd.Timestamp('1896-12-26', tz='UTC')
    ]
    valid_days = nyse.valid_days('1896-01-01', '1896-12-31')
    for h in holidays_1896:
        assert h not in valid_days
        assert h in all_holidays

def test_1897():
    nyse = NYSEExchangeCalendar()
    holidays_1897 = [
        pd.Timestamp('1897-01-01', tz='UTC'),
        pd.Timestamp('1897-02-12', tz='UTC'),
        pd.Timestamp('1897-02-22', tz='UTC'),
        pd.Timestamp('1897-04-16', tz='UTC'),
        pd.Timestamp('1897-04-27', tz='UTC'),
        pd.Timestamp('1897-05-31', tz='UTC'),
        pd.Timestamp('1897-07-05', tz='UTC'),
        pd.Timestamp('1897-09-06', tz='UTC'),
        pd.Timestamp('1897-11-02', tz='UTC'),
        pd.Timestamp('1897-11-25', tz='UTC'),
        pd.Timestamp('1897-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1897-01-01', '1897-12-31')
    for h in holidays_1897:
        assert h not in valid_days
        assert h in all_holidays

def test_1898():
    nyse = NYSEExchangeCalendar()
    holidays_1898 = [
        pd.Timestamp('1898-01-01', tz='UTC'),
        pd.Timestamp('1898-02-12', tz='UTC'),
        pd.Timestamp('1898-02-22', tz='UTC'),
        pd.Timestamp('1898-05-04', tz='UTC'),
        pd.Timestamp('1898-05-30', tz='UTC'),
        pd.Timestamp('1898-07-02', tz='UTC'),
        pd.Timestamp('1898-07-04', tz='UTC'),
        pd.Timestamp('1898-08-20', tz='UTC'),
        pd.Timestamp('1898-09-03', tz='UTC'),
        pd.Timestamp('1898-09-05', tz='UTC'),
        pd.Timestamp('1898-11-08', tz='UTC'),
        pd.Timestamp('1898-11-24', tz='UTC'),
        pd.Timestamp('1898-12-24', tz='UTC'),
        pd.Timestamp('1898-12-26', tz='UTC')
    ]
    valid_days = nyse.valid_days('1898-01-01', '1898-12-31')
    for h in holidays_1898:
        assert h not in valid_days
        assert h in all_holidays

def test_1899():
    nyse = NYSEExchangeCalendar()
    holidays_1899 = [
        pd.Timestamp('1899-01-02', tz='UTC'),
        pd.Timestamp('1899-02-11', tz='UTC'),
        pd.Timestamp('1899-02-13', tz='UTC'),
        pd.Timestamp('1899-02-22', tz='UTC'),
        pd.Timestamp('1899-03-31', tz='UTC'),
        pd.Timestamp('1899-05-29', tz='UTC'),
        pd.Timestamp('1899-05-30', tz='UTC'),
        pd.Timestamp('1899-07-04', tz='UTC'),
        pd.Timestamp('1899-09-04', tz='UTC'),
        pd.Timestamp('1899-09-29', tz='UTC'),
        pd.Timestamp('1899-09-30', tz='UTC'),
        pd.Timestamp('1899-11-07', tz='UTC'),
        pd.Timestamp('1899-11-25', tz='UTC'),
        pd.Timestamp('1899-11-30', tz='UTC'),
        pd.Timestamp('1899-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1899-01-01', '1899-12-31')
    for h in holidays_1899:
        assert h not in valid_days
        assert h in all_holidays

def test_1900():
    nyse = NYSEExchangeCalendar()
    holidays_1900 = [
        pd.Timestamp('1900-01-01', tz='UTC'),
        pd.Timestamp('1900-02-12', tz='UTC'),
        pd.Timestamp('1900-02-22', tz='UTC'),
        pd.Timestamp('1900-04-13', tz='UTC'),
        pd.Timestamp('1900-04-14', tz='UTC'),
        pd.Timestamp('1900-05-30', tz='UTC'),
        pd.Timestamp('1900-07-04', tz='UTC'),
        pd.Timestamp('1900-09-01', tz='UTC'),
        pd.Timestamp('1900-09-03', tz='UTC'),
        pd.Timestamp('1900-11-06', tz='UTC'),
        pd.Timestamp('1900-11-29', tz='UTC'),
        pd.Timestamp('1900-12-24', tz='UTC'),
        pd.Timestamp('1900-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1900-01-01', '1900-12-31')
    for h in holidays_1900:
        assert h not in valid_days
        assert h in all_holidays

def test_1901():
    nyse = NYSEExchangeCalendar()
    holidays_1901 = [
        pd.Timestamp('1901-01-01', tz='UTC'),
        pd.Timestamp('1901-02-02', tz='UTC'),
        pd.Timestamp('1901-02-12', tz='UTC'),
        pd.Timestamp('1901-02-22', tz='UTC'),
        pd.Timestamp('1901-02-23', tz='UTC'),
        pd.Timestamp('1901-04-05', tz='UTC'),
        pd.Timestamp('1901-04-06', tz='UTC'),
        pd.Timestamp('1901-04-27', tz='UTC'),
        pd.Timestamp('1901-05-11', tz='UTC'),
        pd.Timestamp('1901-05-30', tz='UTC'),
        pd.Timestamp('1901-07-04', tz='UTC'),
        pd.Timestamp('1901-07-05', tz='UTC'),
        pd.Timestamp('1901-07-06', tz='UTC'),
        pd.Timestamp('1901-08-31', tz='UTC'),
        pd.Timestamp('1901-09-02', tz='UTC'),
        pd.Timestamp('1901-09-14', tz='UTC'),
        pd.Timestamp('1901-09-19', tz='UTC'),
        pd.Timestamp('1901-11-05', tz='UTC'),
        pd.Timestamp('1901-11-28', tz='UTC'),
        pd.Timestamp('1901-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1901-01-01', '1901-12-31')
    for h in holidays_1901:
        assert h not in valid_days
        assert h in all_holidays

def test_1902():
    nyse = NYSEExchangeCalendar()
    holidays_1902 = [
        pd.Timestamp('1902-01-01', tz='UTC'),
        pd.Timestamp('1902-02-12', tz='UTC'),
        pd.Timestamp('1902-02-22', tz='UTC'),
        pd.Timestamp('1902-03-28', tz='UTC'),
        pd.Timestamp('1902-03-29', tz='UTC'),
        pd.Timestamp('1902-05-30', tz='UTC'),
        pd.Timestamp('1902-05-31', tz='UTC'),
        pd.Timestamp('1902-07-04', tz='UTC'),
        pd.Timestamp('1902-07-05', tz='UTC'),
        pd.Timestamp('1902-08-09', tz='UTC'),
        pd.Timestamp('1902-08-30', tz='UTC'),
        pd.Timestamp('1902-09-01', tz='UTC'),
        pd.Timestamp('1902-11-04', tz='UTC'),
        pd.Timestamp('1902-11-27', tz='UTC'),
        pd.Timestamp('1902-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1902-01-01', '1902-12-31')
    for h in holidays_1902:
        assert h not in valid_days
        assert h in all_holidays

def test_1903():
    nyse = NYSEExchangeCalendar()
    holidays_1903 = [
        pd.Timestamp('1903-01-01', tz='UTC'),
        pd.Timestamp('1903-02-12', tz='UTC'),
        pd.Timestamp('1903-02-21', tz='UTC'),
        pd.Timestamp('1903-02-23', tz='UTC'),
        pd.Timestamp('1903-04-10', tz='UTC'),
        pd.Timestamp('1903-04-11', tz='UTC'),
        pd.Timestamp('1903-04-22', tz='UTC'),
        pd.Timestamp('1903-05-30', tz='UTC'),
        pd.Timestamp('1903-07-04', tz='UTC'),
        pd.Timestamp('1903-09-05', tz='UTC'),
        pd.Timestamp('1903-09-07', tz='UTC'),
        pd.Timestamp('1903-11-03', tz='UTC'),
        pd.Timestamp('1903-11-26', tz='UTC'),
        pd.Timestamp('1903-12-25', tz='UTC'),
        pd.Timestamp('1903-12-26', tz='UTC')
    ]
    valid_days = nyse.valid_days('1903-01-01', '1903-12-31')
    for h in holidays_1903:
        assert h not in valid_days
        assert h in all_holidays
        
def test_special_holidays():
    nyse = NYSEExchangeCalendar()
    good_dates = nyse.valid_days('1885-01-01', '1952-12-31')
    assert pd.Timestamp("1885-08-08") not in good_dates #Grant's funeral




