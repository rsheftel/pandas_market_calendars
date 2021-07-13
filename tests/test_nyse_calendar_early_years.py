import os
import pytz

import pandas as pd
from pandas.testing import assert_index_equal
from pandas.tseries.offsets import CustomBusinessDay

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
        
def test_1904():
    nyse = NYSEExchangeCalendar()
    holidays_1904 = [
        pd.Timestamp('1904-01-01', tz='UTC'),
        pd.Timestamp('1904-02-12', tz='UTC'),
        pd.Timestamp('1904-02-22', tz='UTC'),
        pd.Timestamp('1904-04-01', tz='UTC'),
        pd.Timestamp('1904-05-28', tz='UTC'),
        pd.Timestamp('1904-05-30', tz='UTC'),
        pd.Timestamp('1904-07-02', tz='UTC'),
        pd.Timestamp('1904-07-04', tz='UTC'),
        pd.Timestamp('1904-09-03', tz='UTC'),
        pd.Timestamp('1904-09-05', tz='UTC'),
        pd.Timestamp('1904-11-08', tz='UTC'),
        pd.Timestamp('1904-11-24', tz='UTC'),
        pd.Timestamp('1904-12-24', tz='UTC'),
        pd.Timestamp('1904-12-26', tz='UTC')
    ]
    valid_days = nyse.valid_days('1904-01-01', '1904-12-31')
    for h in holidays_1904:
        assert h not in valid_days
        assert h in all_holidays        

def test_1905():
    nyse = NYSEExchangeCalendar()
    holidays_1905 = [
        pd.Timestamp('1905-01-02', tz='UTC'),
        pd.Timestamp('1905-02-13', tz='UTC'),
        pd.Timestamp('1905-02-22', tz='UTC'),
        pd.Timestamp('1905-04-21', tz='UTC'),
        pd.Timestamp('1905-04-22', tz='UTC'),
        pd.Timestamp('1905-05-30', tz='UTC'),
        pd.Timestamp('1905-07-04', tz='UTC'),
        pd.Timestamp('1905-09-04', tz='UTC'),
        pd.Timestamp('1905-11-07', tz='UTC'),
        pd.Timestamp('1905-11-30', tz='UTC'),
        pd.Timestamp('1905-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1905-01-01', '1905-12-31')
    for h in holidays_1905:
        assert h not in valid_days
        assert h in all_holidays 

def test_1906():
    nyse = NYSEExchangeCalendar()
    holidays_1906 = [
        pd.Timestamp('1906-01-01', tz='UTC'),
        pd.Timestamp('1906-02-12', tz='UTC'),
        pd.Timestamp('1906-02-22', tz='UTC'),
        pd.Timestamp('1906-05-30', tz='UTC'),
        pd.Timestamp('1906-07-04', tz='UTC'),
        pd.Timestamp('1906-09-03', tz='UTC'),
        pd.Timestamp('1906-11-06', tz='UTC'),
        pd.Timestamp('1906-11-29', tz='UTC'),
        pd.Timestamp('1906-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1906-01-01', '1906-12-31')
    for h in holidays_1906:
        assert h not in valid_days
        assert h in all_holidays 

def test_1907():
    nyse = NYSEExchangeCalendar()
    holidays_1907 = [
        pd.Timestamp('1907-01-01', tz='UTC'),
        pd.Timestamp('1907-02-12', tz='UTC'),
        pd.Timestamp('1907-02-22', tz='UTC'),
        pd.Timestamp('1907-02-23', tz='UTC'),
        pd.Timestamp('1907-03-30', tz='UTC'),
        pd.Timestamp('1907-05-30', tz='UTC'),
        pd.Timestamp('1907-07-04', tz='UTC'),
        pd.Timestamp('1907-08-31', tz='UTC'),
        pd.Timestamp('1907-09-02', tz='UTC'),
        pd.Timestamp('1907-11-05', tz='UTC'),
        pd.Timestamp('1907-11-28', tz='UTC'),
        pd.Timestamp('1907-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1907-01-01', '1907-12-31')
    for h in holidays_1907:
        assert h not in valid_days
        assert h in all_holidays 

def test_1908():
    nyse = NYSEExchangeCalendar()
    holidays_1908 = [
        pd.Timestamp('1908-01-01', tz='UTC'),
        pd.Timestamp('1908-02-12', tz='UTC'),
        pd.Timestamp('1908-02-22', tz='UTC'),
        pd.Timestamp('1908-04-17', tz='UTC'),
        pd.Timestamp('1908-04-18', tz='UTC'),
        pd.Timestamp('1908-05-30', tz='UTC'),
        pd.Timestamp('1908-07-04', tz='UTC'),
        pd.Timestamp('1908-09-05', tz='UTC'),
        pd.Timestamp('1908-09-07', tz='UTC'),
        pd.Timestamp('1908-11-03', tz='UTC'),
        pd.Timestamp('1908-11-26', tz='UTC'),
        pd.Timestamp('1908-12-25', tz='UTC'),
        pd.Timestamp('1908-12-26', tz='UTC')
    ]
    valid_days = nyse.valid_days('1908-01-01', '1908-12-31')
    for h in holidays_1908:
        assert h not in valid_days
        assert h in all_holidays 
        
    # early closes we expect:
    early_close_grover_cleveland_funeral = [
        pd.Timestamp(' 1908-06-26' , tz='UTC')
    ]

    expected = nyse.early_closes(nyse.schedule('1908-01-01', '1908-12-31'))
    for ec in early_close_grover_cleveland_funeral:
        assert ec in expected.index

def test_1909():
    nyse = NYSEExchangeCalendar()
    holidays_1909 = [
        pd.Timestamp('1909-01-01', tz='UTC'),
        pd.Timestamp('1909-02-12', tz='UTC'),
        pd.Timestamp('1909-02-13', tz='UTC'),
        pd.Timestamp('1909-02-22', tz='UTC'),
        pd.Timestamp('1909-04-09', tz='UTC'),
        pd.Timestamp('1909-04-10', tz='UTC'),
        pd.Timestamp('1909-05-29', tz='UTC'),
        pd.Timestamp('1909-05-31', tz='UTC'),
        pd.Timestamp('1909-07-03', tz='UTC'),
        pd.Timestamp('1909-07-05', tz='UTC'),
        pd.Timestamp('1909-09-04', tz='UTC'),
        pd.Timestamp('1909-09-06', tz='UTC'),
        pd.Timestamp('1909-09-25', tz='UTC'),
        pd.Timestamp('1909-10-12', tz='UTC'),
        pd.Timestamp('1909-11-02', tz='UTC'),
        pd.Timestamp('1909-11-25', tz='UTC'),
        pd.Timestamp('1909-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1909-01-01', '1909-12-31')
    for h in holidays_1909:
        assert h not in valid_days
        assert h in all_holidays 

def test_1910():
    nyse = NYSEExchangeCalendar()
    holidays_1910 = [
        pd.Timestamp('1910-01-01', tz='UTC'),
        pd.Timestamp('1910-02-12', tz='UTC'),
        pd.Timestamp('1910-02-22', tz='UTC'),
        pd.Timestamp('1910-03-25', tz='UTC'),
        pd.Timestamp('1910-03-26', tz='UTC'),
        pd.Timestamp('1910-05-28', tz='UTC'),
        pd.Timestamp('1910-05-30', tz='UTC'),
        pd.Timestamp('1910-07-02', tz='UTC'),
        pd.Timestamp('1910-07-04', tz='UTC'),
        pd.Timestamp('1910-09-03', tz='UTC'),
        pd.Timestamp('1910-09-05', tz='UTC'),
        pd.Timestamp('1910-10-12', tz='UTC'),
        pd.Timestamp('1910-11-08', tz='UTC'),
        pd.Timestamp('1910-11-24', tz='UTC'),
        pd.Timestamp('1910-12-24', tz='UTC'),
        pd.Timestamp('1910-12-26', tz='UTC')
    ]
    valid_days = nyse.valid_days('1910-01-01', '1910-12-31')
    for h in holidays_1910:
        assert h not in valid_days
        assert h in all_holidays

def test_1911():
    nyse = NYSEExchangeCalendar()
    holidays_1911 = [
        pd.Timestamp('1911-01-02', tz='UTC'),
        pd.Timestamp('1911-02-13', tz='UTC'),
        pd.Timestamp('1911-02-22', tz='UTC'),
        pd.Timestamp('1911-04-14', tz='UTC'),
        pd.Timestamp('1911-04-15', tz='UTC'),
        pd.Timestamp('1911-05-30', tz='UTC'),
        pd.Timestamp('1911-07-04', tz='UTC'),
        pd.Timestamp('1911-09-02', tz='UTC'),
        pd.Timestamp('1911-09-04', tz='UTC'),
        pd.Timestamp('1911-10-12', tz='UTC'),
        pd.Timestamp('1911-11-07', tz='UTC'),
        pd.Timestamp('1911-11-30', tz='UTC'),
        pd.Timestamp('1911-12-23', tz='UTC'),
        pd.Timestamp('1911-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1911-01-01', '1911-12-31')
    for h in holidays_1911:
        assert h not in valid_days
        assert h in all_holidays

def test_1912():
    nyse = NYSEExchangeCalendar()
    holidays_1912 = [
        pd.Timestamp('1912-01-01', tz='UTC'),
        pd.Timestamp('1912-02-12', tz='UTC'),
        pd.Timestamp('1912-02-22', tz='UTC'),
        pd.Timestamp('1912-04-05', tz='UTC'),
        pd.Timestamp('1912-05-30', tz='UTC'),
        pd.Timestamp('1912-07-04', tz='UTC'),
        pd.Timestamp('1912-08-31', tz='UTC'),
        pd.Timestamp('1912-09-02', tz='UTC'),           
        pd.Timestamp('1912-10-12', tz='UTC'),
        pd.Timestamp('1912-11-02', tz='UTC'),
        pd.Timestamp('1912-11-05', tz='UTC'),
        pd.Timestamp('1912-11-28', tz='UTC'),
        pd.Timestamp('1912-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1912-01-01', '1912-12-31')
    for h in holidays_1912:
        assert h not in valid_days
        assert h in all_holidays

def test_1913():
    nyse = NYSEExchangeCalendar()
    holidays_1913 = [
        pd.Timestamp('1913-01-01', tz='UTC'),
        pd.Timestamp('1913-02-12', tz='UTC'),
        pd.Timestamp('1913-02-22', tz='UTC'),
        pd.Timestamp('1913-03-21', tz='UTC'),
        pd.Timestamp('1913-03-22', tz='UTC'),
        pd.Timestamp('1913-05-30', tz='UTC'),
        pd.Timestamp('1913-05-31', tz='UTC'),
        pd.Timestamp('1913-07-04', tz='UTC'),
        pd.Timestamp('1913-07-05', tz='UTC'),
        pd.Timestamp('1913-08-30', tz='UTC'),
        pd.Timestamp('1913-09-01', tz='UTC'),
        pd.Timestamp('1913-10-13', tz='UTC'),
        pd.Timestamp('1913-11-04', tz='UTC'),
        pd.Timestamp('1913-11-27', tz='UTC'),
        pd.Timestamp('1913-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1913-01-01', '1913-12-31')
    for h in holidays_1913:
        assert h not in valid_days
        assert h in all_holidays

def test_1914():
    nyse = NYSEExchangeCalendar()
    holidays_1914 = [
        pd.Timestamp('1914-01-01', tz='UTC'),
        pd.Timestamp('1914-02-12', tz='UTC'),
        pd.Timestamp('1914-02-23', tz='UTC'),
        pd.Timestamp('1914-04-10', tz='UTC'),
        pd.Timestamp('1914-05-30', tz='UTC'),
        pd.Timestamp('1914-07-04', tz='UTC'),
        pd.Timestamp('1914-07-31', tz='UTC'),
        pd.Timestamp('1914-08-01', tz='UTC'),
        pd.Timestamp('1914-08-03', tz='UTC'),
        pd.Timestamp('1914-08-04', tz='UTC'),
        pd.Timestamp('1914-08-05', tz='UTC'),
        pd.Timestamp('1914-08-06', tz='UTC'),
        pd.Timestamp('1914-08-07', tz='UTC'),
        pd.Timestamp('1914-08-08', tz='UTC'),
        pd.Timestamp('1914-08-10', tz='UTC'),
        pd.Timestamp('1914-08-11', tz='UTC'),
        pd.Timestamp('1914-08-12', tz='UTC'),
        pd.Timestamp('1914-08-13', tz='UTC'),
        pd.Timestamp('1914-08-14', tz='UTC'),
        pd.Timestamp('1914-08-15', tz='UTC'),
        pd.Timestamp('1914-08-17', tz='UTC'),
        pd.Timestamp('1914-08-18', tz='UTC'),
        pd.Timestamp('1914-08-19', tz='UTC'),
        pd.Timestamp('1914-08-20', tz='UTC'),
        pd.Timestamp('1914-08-21', tz='UTC'),
        pd.Timestamp('1914-08-22', tz='UTC'),
        pd.Timestamp('1914-08-24', tz='UTC'),
        pd.Timestamp('1914-08-25', tz='UTC'),
        pd.Timestamp('1914-08-26', tz='UTC'),
        pd.Timestamp('1914-08-27', tz='UTC'),
        pd.Timestamp('1914-08-28', tz='UTC'),
        pd.Timestamp('1914-08-29', tz='UTC'),
        pd.Timestamp('1914-08-31', tz='UTC'),
        pd.Timestamp('1914-09-01', tz='UTC'),
        pd.Timestamp('1914-09-02', tz='UTC'),
        pd.Timestamp('1914-09-03', tz='UTC'),
        pd.Timestamp('1914-09-04', tz='UTC'),
        pd.Timestamp('1914-09-05', tz='UTC'),
        pd.Timestamp('1914-09-07', tz='UTC'),
        pd.Timestamp('1914-09-07', tz='UTC'),
        pd.Timestamp('1914-09-08', tz='UTC'),
        pd.Timestamp('1914-09-09', tz='UTC'),
        pd.Timestamp('1914-09-10', tz='UTC'),
        pd.Timestamp('1914-09-11', tz='UTC'),
        pd.Timestamp('1914-09-12', tz='UTC'),
        pd.Timestamp('1914-09-14', tz='UTC'),
        pd.Timestamp('1914-09-15', tz='UTC'),
        pd.Timestamp('1914-09-16', tz='UTC'),
        pd.Timestamp('1914-09-17', tz='UTC'),
        pd.Timestamp('1914-09-18', tz='UTC'),
        pd.Timestamp('1914-09-19', tz='UTC'),
        pd.Timestamp('1914-09-21', tz='UTC'),
        pd.Timestamp('1914-09-22', tz='UTC'),
        pd.Timestamp('1914-09-23', tz='UTC'),
        pd.Timestamp('1914-09-24', tz='UTC'),
        pd.Timestamp('1914-09-25', tz='UTC'),
        pd.Timestamp('1914-09-26', tz='UTC'),
        pd.Timestamp('1914-09-28', tz='UTC'),
        pd.Timestamp('1914-09-29', tz='UTC'),
        pd.Timestamp('1914-09-30', tz='UTC'),
        pd.Timestamp('1914-10-01', tz='UTC'),
        pd.Timestamp('1914-10-02', tz='UTC'),
        pd.Timestamp('1914-10-03', tz='UTC'),
        pd.Timestamp('1914-10-05', tz='UTC'),
        pd.Timestamp('1914-10-06', tz='UTC'),
        pd.Timestamp('1914-10-07', tz='UTC'),
        pd.Timestamp('1914-10-08', tz='UTC'),
        pd.Timestamp('1914-10-09', tz='UTC'),
        pd.Timestamp('1914-10-10', tz='UTC'),
        pd.Timestamp('1914-10-12', tz='UTC'),
        pd.Timestamp('1914-10-12', tz='UTC'),
        pd.Timestamp('1914-10-13', tz='UTC'),
        pd.Timestamp('1914-10-14', tz='UTC'),
        pd.Timestamp('1914-10-15', tz='UTC'),
        pd.Timestamp('1914-10-16', tz='UTC'),
        pd.Timestamp('1914-10-17', tz='UTC'),
        pd.Timestamp('1914-10-19', tz='UTC'),
        pd.Timestamp('1914-10-20', tz='UTC'),
        pd.Timestamp('1914-10-21', tz='UTC'),
        pd.Timestamp('1914-10-22', tz='UTC'),
        pd.Timestamp('1914-10-23', tz='UTC'),
        pd.Timestamp('1914-10-24', tz='UTC'),
        pd.Timestamp('1914-10-26', tz='UTC'),
        pd.Timestamp('1914-10-27', tz='UTC'),
        pd.Timestamp('1914-10-28', tz='UTC'),
        pd.Timestamp('1914-10-29', tz='UTC'),
        pd.Timestamp('1914-10-30', tz='UTC'),
        pd.Timestamp('1914-10-31', tz='UTC'),
        pd.Timestamp('1914-11-02', tz='UTC'),
        pd.Timestamp('1914-11-03', tz='UTC'),
        pd.Timestamp('1914-11-03', tz='UTC'),
        pd.Timestamp('1914-11-04', tz='UTC'),
        pd.Timestamp('1914-11-05', tz='UTC'),
        pd.Timestamp('1914-11-06', tz='UTC'),
        pd.Timestamp('1914-11-07', tz='UTC'),
        pd.Timestamp('1914-11-09', tz='UTC'),
        pd.Timestamp('1914-11-10', tz='UTC'),
        pd.Timestamp('1914-11-11', tz='UTC'),
        pd.Timestamp('1914-11-12', tz='UTC'),
        pd.Timestamp('1914-11-13', tz='UTC'),
        pd.Timestamp('1914-11-14', tz='UTC'),
        pd.Timestamp('1914-11-16', tz='UTC'),
        pd.Timestamp('1914-11-17', tz='UTC'),
        pd.Timestamp('1914-11-18', tz='UTC'),
        pd.Timestamp('1914-11-19', tz='UTC'),
        pd.Timestamp('1914-11-20', tz='UTC'),
        pd.Timestamp('1914-11-21', tz='UTC'),
        pd.Timestamp('1914-11-23', tz='UTC'),
        pd.Timestamp('1914-11-24', tz='UTC'),
        pd.Timestamp('1914-11-25', tz='UTC'),
        pd.Timestamp('1914-11-26', tz='UTC'),
        pd.Timestamp('1914-11-26', tz='UTC'),
        pd.Timestamp('1914-11-27', tz='UTC'),
        pd.Timestamp('1914-11-28', tz='UTC'),
        pd.Timestamp('1914-11-30', tz='UTC'),
        pd.Timestamp('1914-12-01', tz='UTC'),
        pd.Timestamp('1914-12-02', tz='UTC'),
        pd.Timestamp('1914-12-03', tz='UTC'),
        pd.Timestamp('1914-12-04', tz='UTC'),
        pd.Timestamp('1914-12-05', tz='UTC'),
        pd.Timestamp('1914-12-07', tz='UTC'),
        pd.Timestamp('1914-12-08', tz='UTC'),
        pd.Timestamp('1914-12-09', tz='UTC'),
        pd.Timestamp('1914-12-10', tz='UTC'),
        pd.Timestamp('1914-12-11', tz='UTC'),
        pd.Timestamp('1914-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1914-01-01', '1914-12-31')
    for h in holidays_1914:
        assert h not in valid_days
        assert h in all_holidays

def test_1915():
    nyse = NYSEExchangeCalendar()
    holidays_1915 = [
        pd.Timestamp('1915-01-01', tz='UTC'),
        pd.Timestamp('1915-02-12', tz='UTC'),
        pd.Timestamp('1915-02-22', tz='UTC'),
        pd.Timestamp('1915-04-02', tz='UTC'),
        pd.Timestamp('1915-05-31', tz='UTC'),
        pd.Timestamp('1915-07-05', tz='UTC'),
        pd.Timestamp('1915-09-06', tz='UTC'),
        pd.Timestamp('1915-10-12', tz='UTC'),
        pd.Timestamp('1915-11-02', tz='UTC'),
        pd.Timestamp('1915-11-25', tz='UTC'),
        pd.Timestamp('1915-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1915-01-01', '1915-12-31')
    for h in holidays_1915:
        assert h not in valid_days
        assert h in all_holidays

def test_1916():
    nyse = NYSEExchangeCalendar()
    holidays_1916 = [
        pd.Timestamp('1916-01-01', tz='UTC'),
        pd.Timestamp('1916-02-12', tz='UTC'),
        pd.Timestamp('1916-02-22', tz='UTC'),
        pd.Timestamp('1916-04-21', tz='UTC'),
        pd.Timestamp('1916-05-30', tz='UTC'),
        pd.Timestamp('1916-07-04', tz='UTC'),
        pd.Timestamp('1916-09-04', tz='UTC'),
        pd.Timestamp('1916-10-12', tz='UTC'),
        pd.Timestamp('1916-11-07', tz='UTC'),
        pd.Timestamp('1916-11-30', tz='UTC'),
        pd.Timestamp('1916-12-25', tz='UTC'),
        pd.Timestamp('1916-12-30', tz='UTC')
    ]
    valid_days = nyse.valid_days('1916-01-01', '1916-12-31')
    for h in holidays_1916:
        assert h not in valid_days
        assert h in all_holidays
        
        
def test_1917():
    nyse = NYSEExchangeCalendar()
    holidays_1917 = [
        pd.Timestamp('1917-01-01', tz='UTC'),
        pd.Timestamp('1917-02-12', tz='UTC'),
        pd.Timestamp('1917-02-22', tz='UTC'),
        pd.Timestamp('1917-04-06', tz='UTC'),
        pd.Timestamp('1917-05-30', tz='UTC'),
        pd.Timestamp('1917-06-05', tz='UTC'),
        pd.Timestamp('1917-07-04', tz='UTC'),
        pd.Timestamp('1917-08-04', tz='UTC'),
        pd.Timestamp('1917-09-01', tz='UTC'),
        pd.Timestamp('1917-09-03', tz='UTC'),
        pd.Timestamp('1917-10-12', tz='UTC'),
        pd.Timestamp('1917-10-13', tz='UTC'),
        pd.Timestamp('1917-11-06', tz='UTC'),
        pd.Timestamp('1917-11-29', tz='UTC'),
        pd.Timestamp('1917-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1917-01-01', '1917-12-31')
    for h in holidays_1917:
        assert h not in valid_days
        assert h in all_holidays        

    # early closes we expect:
    early_closes_1917 = [
        pd.Timestamp(' 1917-08-29' , tz='UTC'),
        pd.Timestamp(' 1917-10-24' , tz='UTC'),
    ]
    expected = nyse.early_closes(nyse.schedule('1917-01-01', '1917-12-31'))
    for early_close_h in early_closes_1917:
        assert early_close_h in expected.index

def test_1918():
    nyse = NYSEExchangeCalendar()
    holidays_1918 = [
        pd.Timestamp('1918-01-01', tz='UTC'),
        pd.Timestamp('1918-01-28', tz='UTC'),
        pd.Timestamp('1918-02-04', tz='UTC'),
        pd.Timestamp('1918-02-11', tz='UTC'),
        pd.Timestamp('1918-02-12', tz='UTC'),
        pd.Timestamp('1918-02-22', tz='UTC'),
        pd.Timestamp('1918-03-29', tz='UTC'),
        pd.Timestamp('1918-05-30', tz='UTC'),
        pd.Timestamp('1918-07-04', tz='UTC'),
        pd.Timestamp('1918-09-02', tz='UTC'),
        pd.Timestamp('1918-09-12', tz='UTC'),
        pd.Timestamp('1918-10-12', tz='UTC'),
        pd.Timestamp('1918-11-05', tz='UTC'),
        pd.Timestamp('1918-11-11', tz='UTC'),
        pd.Timestamp('1918-11-28', tz='UTC'),
        pd.Timestamp('1918-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1918-01-01', '1918-12-31')
    for h in holidays_1918:
        assert h not in valid_days
        assert h in all_holidays        

    # early closes we expect:
    early_closes_1918 = [
        pd.Timestamp('1918-11-07')
    ]
    expected = nyse.early_closes(nyse.schedule('1918-01-01', '1918-12-31'))
    for early_close_h in early_closes_1918:
        assert early_close_h in expected.index 
       
        
def test_1919():
    nyse = NYSEExchangeCalendar()
    holidays_1919 = [
        pd.Timestamp('1919-01-01', tz='UTC'),
        pd.Timestamp('1919-02-12', tz='UTC'),
        pd.Timestamp('1919-02-22', tz='UTC'),
        pd.Timestamp('1919-03-25', tz='UTC'),
        pd.Timestamp('1919-04-18', tz='UTC'),
        pd.Timestamp('1919-05-06', tz='UTC'),
        pd.Timestamp('1919-05-30', tz='UTC'),
        pd.Timestamp('1919-05-31', tz='UTC'),
        pd.Timestamp('1919-07-04', tz='UTC'),
        pd.Timestamp('1919-07-05', tz='UTC'),
        pd.Timestamp('1919-07-19', tz='UTC'),
        pd.Timestamp('1919-08-02', tz='UTC'),
        pd.Timestamp('1919-08-16', tz='UTC'),
        pd.Timestamp('1919-08-30', tz='UTC'),
        pd.Timestamp('1919-09-01', tz='UTC'),
        pd.Timestamp('1919-09-10', tz='UTC'),
        pd.Timestamp('1919-10-13', tz='UTC'),
        pd.Timestamp('1919-11-04', tz='UTC'),
        pd.Timestamp('1919-11-27', tz='UTC'),
        pd.Timestamp('1919-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1919-01-01', '1919-12-31')
    for h in holidays_1919:
        assert h not in valid_days
        assert h in all_holidays        

    # early closes we expect:
    early_closes_1919 = [
        pd.Timestamp('1919-01-07')
    ]
    expected = nyse.early_closes(nyse.schedule('1919-01-01', '1919-12-31'))
    for early_close_h in early_closes_1919:
        assert early_close_h in expected.index        
   
def test_1920():
    nyse = NYSEExchangeCalendar()
    holidays_1920 = [
        pd.Timestamp('1920-01-01', tz='UTC'),
        pd.Timestamp('1920-02-12', tz='UTC'),
        pd.Timestamp('1920-02-23', tz='UTC'),
        pd.Timestamp('1920-04-02', tz='UTC'),
        pd.Timestamp('1920-04-03', tz='UTC'),
        pd.Timestamp('1920-05-01', tz='UTC'),
        pd.Timestamp('1920-05-31', tz='UTC'),
        pd.Timestamp('1920-07-03', tz='UTC'),
        pd.Timestamp('1920-07-05', tz='UTC'),
        pd.Timestamp('1920-09-04', tz='UTC'),
        pd.Timestamp('1920-09-06', tz='UTC'),
        pd.Timestamp('1920-10-12', tz='UTC'),
        pd.Timestamp('1920-11-02', tz='UTC'),
        pd.Timestamp('1920-11-25', tz='UTC'),
        pd.Timestamp('1920-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1920-01-01', '1920-12-31')
    for h in holidays_1920:
        assert h not in valid_days
        assert h in all_holidays        

    # early closes we expect:
    early_closes_1920 = [
        pd.Timestamp('1920-09-16')
    ]
    expected = nyse.early_closes(nyse.schedule('1920-01-01', '1920-12-31'))
    for early_close_h in early_closes_1920:
        assert early_close_h in expected.index  
 
def test_1921():
    nyse = NYSEExchangeCalendar()
    holidays_1921 = [
        pd.Timestamp('1921-01-01', tz='UTC'),
        pd.Timestamp('1921-02-12', tz='UTC'),
        pd.Timestamp('1921-02-22', tz='UTC'),
        pd.Timestamp('1921-03-25', tz='UTC'),
        pd.Timestamp('1921-05-28', tz='UTC'),
        pd.Timestamp('1921-05-30', tz='UTC'),
        pd.Timestamp('1921-07-02', tz='UTC'),
        pd.Timestamp('1921-07-04', tz='UTC'),
        pd.Timestamp('1921-09-03', tz='UTC'),
        pd.Timestamp('1921-09-05', tz='UTC'),
        pd.Timestamp('1921-10-12', tz='UTC'),
        pd.Timestamp('1921-11-08', tz='UTC'),
        pd.Timestamp('1921-11-11', tz='UTC'),
        pd.Timestamp('1921-11-24', tz='UTC'),
        pd.Timestamp('1921-12-26', tz='UTC')
    ]
    valid_days = nyse.valid_days('1921-01-01', '1921-12-31')
    for h in holidays_1921:
        assert h not in valid_days
        assert h in all_holidays            
 
def test_1922():
    nyse = NYSEExchangeCalendar()
    holidays_1922 = [
        pd.Timestamp('1922-01-02', tz='UTC'),
        pd.Timestamp('1922-02-13', tz='UTC'),
        pd.Timestamp('1922-02-22', tz='UTC'),
        pd.Timestamp('1922-04-14', tz='UTC'),
        pd.Timestamp('1922-05-30', tz='UTC'),
        pd.Timestamp('1922-07-04', tz='UTC'),
        pd.Timestamp('1922-09-04', tz='UTC'),
        pd.Timestamp('1922-10-12', tz='UTC'),
        pd.Timestamp('1922-11-07', tz='UTC'),
        pd.Timestamp('1922-11-30', tz='UTC'),
        pd.Timestamp('1922-12-23', tz='UTC'),
        pd.Timestamp('1922-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1922-01-01', '1922-12-31')
    for h in holidays_1922:
        assert h not in valid_days
        assert h in all_holidays            

def test_1923():
    nyse = NYSEExchangeCalendar()
    holidays_1923 = [
        pd.Timestamp('1923-01-01', tz='UTC'),
        pd.Timestamp('1923-02-12', tz='UTC'),
        pd.Timestamp('1923-02-22', tz='UTC'),
        pd.Timestamp('1923-03-30', tz='UTC'),
        pd.Timestamp('1923-05-30', tz='UTC'),
        pd.Timestamp('1923-07-04', tz='UTC'),
        pd.Timestamp('1923-08-03', tz='UTC'),
        pd.Timestamp('1923-08-10', tz='UTC'),
        pd.Timestamp('1923-09-03', tz='UTC'),
        pd.Timestamp('1923-10-12', tz='UTC'),
        pd.Timestamp('1923-11-06', tz='UTC'),
        pd.Timestamp('1923-11-29', tz='UTC'),
        pd.Timestamp('1923-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1923-01-01', '1923-12-31')
    for h in holidays_1923:
        assert h not in valid_days
        assert h in all_holidays            
        
def test_1924():
    nyse = NYSEExchangeCalendar()
    holidays_1924 = [
        pd.Timestamp('1924-01-01', tz='UTC'),
        pd.Timestamp('1924-02-12', tz='UTC'),
        pd.Timestamp('1924-02-22', tz='UTC'),
        pd.Timestamp('1924-04-18', tz='UTC'),
        pd.Timestamp('1924-05-30', tz='UTC'),
        pd.Timestamp('1924-05-31', tz='UTC'),
        pd.Timestamp('1924-07-04', tz='UTC'),
        pd.Timestamp('1924-09-01', tz='UTC'),
        pd.Timestamp('1924-10-13', tz='UTC'),
        pd.Timestamp('1924-11-04', tz='UTC'),
        pd.Timestamp('1924-11-27', tz='UTC'),
        pd.Timestamp('1924-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1924-01-01', '1924-12-31')
    for h in holidays_1924:
        assert h not in valid_days
        assert h in all_holidays        

    # early closes we expect:
    early_closes_1924 = [
        pd.Timestamp('1924-02-06')
    ]
    expected = nyse.early_closes(nyse.schedule('1924-01-01', '1924-12-31'))
    for early_close_h in early_closes_1924:
        assert early_close_h in expected.index         
        
def test_1925():
    nyse = NYSEExchangeCalendar()
    holidays_1925 = [
        pd.Timestamp('1924-01-01', tz='UTC'),
        pd.Timestamp('1924-02-12', tz='UTC'),
        pd.Timestamp('1924-02-22', tz='UTC'),
        pd.Timestamp('1924-04-18', tz='UTC'),
        pd.Timestamp('1924-05-30', tz='UTC'),
        pd.Timestamp('1924-05-31', tz='UTC'),
        pd.Timestamp('1924-07-04', tz='UTC'),
        pd.Timestamp('1924-09-01', tz='UTC'),
        pd.Timestamp('1924-10-13', tz='UTC'),
        pd.Timestamp('1924-11-04', tz='UTC'),
        pd.Timestamp('1924-11-27', tz='UTC'),
        pd.Timestamp('1924-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1925-01-01', '1925-12-31')
    for h in holidays_1925:
        assert h not in valid_days
        assert h in all_holidays        

    # early closes we expect:
    early_closes_1925 = [
        pd.Timestamp('1925-09-18')
    ]
    expected = nyse.early_closes(nyse.schedule('1925-01-01', '1925-12-31'))
    for early_close_h in early_closes_1925:
        assert early_close_h in expected.index    

    # late opens we expect:
    late_opens_1925 = [
            pd.Timestamp('1925-01-24', tz='UTC'),
    ]
    expected = nyse.late_opens(nyse.schedule('1925-01-01', '1925-12-31'))
    for lo in late_opens_1925:
        assert lo in expected.index          

def test_1926():
    nyse = NYSEExchangeCalendar()
    holidays_1926 = [
        pd.Timestamp('1926-01-01', tz='UTC'),
        pd.Timestamp('1926-02-12', tz='UTC'),
        pd.Timestamp('1926-02-22', tz='UTC'),
        pd.Timestamp('1926-04-02', tz='UTC'),
        pd.Timestamp('1926-05-29', tz='UTC'),
        pd.Timestamp('1926-05-31', tz='UTC'),
        pd.Timestamp('1926-07-03', tz='UTC'),
        pd.Timestamp('1926-07-05', tz='UTC'),
        pd.Timestamp('1926-09-04', tz='UTC'),
        pd.Timestamp('1926-09-06', tz='UTC'),
        pd.Timestamp('1926-10-12', tz='UTC'),
        pd.Timestamp('1926-11-02', tz='UTC'),
        pd.Timestamp('1926-11-25', tz='UTC'),
        pd.Timestamp('1926-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1926-01-01', '1926-12-31')
    for h in holidays_1926:
        assert h not in valid_days
        assert h in all_holidays            
        
def test_1927():
    nyse = NYSEExchangeCalendar()
    holidays_1927 = [
        pd.Timestamp('1927-01-01', tz='UTC'),
        pd.Timestamp('1927-02-12', tz='UTC'),
        pd.Timestamp('1927-02-22', tz='UTC'),
        pd.Timestamp('1927-04-15', tz='UTC'),
        pd.Timestamp('1927-05-30', tz='UTC'),
        pd.Timestamp('1927-06-13', tz='UTC'),
        pd.Timestamp('1927-07-04', tz='UTC'),
        pd.Timestamp('1927-09-05', tz='UTC'),
        pd.Timestamp('1927-10-12', tz='UTC'),
        pd.Timestamp('1927-11-08', tz='UTC'),
        pd.Timestamp('1927-11-24', tz='UTC'),
        pd.Timestamp('1927-12-26', tz='UTC')
    ]
    valid_days = nyse.valid_days('1927-01-01', '1927-12-31')
    for h in holidays_1927:
        assert h not in valid_days
        assert h in all_holidays                    
        
        
def test_1928():
    nyse = NYSEExchangeCalendar()
    holidays_1928 = [
        pd.Timestamp('1928-01-02', tz='UTC'),
        pd.Timestamp('1928-02-13', tz='UTC'),
        pd.Timestamp('1928-02-22', tz='UTC'),
        pd.Timestamp('1928-04-06', tz='UTC'),
        pd.Timestamp('1928-04-07', tz='UTC'),
        pd.Timestamp('1928-04-21', tz='UTC'),
        pd.Timestamp('1928-05-05', tz='UTC'),
        pd.Timestamp('1928-05-12', tz='UTC'),
        pd.Timestamp('1928-05-19', tz='UTC'),
        pd.Timestamp('1928-05-26', tz='UTC'),
        pd.Timestamp('1928-05-30', tz='UTC'),
        pd.Timestamp('1928-07-04', tz='UTC'),
        pd.Timestamp('1928-09-03', tz='UTC'),
        pd.Timestamp('1928-10-12', tz='UTC'),
        pd.Timestamp('1928-11-06', tz='UTC'),
        pd.Timestamp('1928-11-24', tz='UTC'),
        pd.Timestamp('1928-11-29', tz='UTC'),
        pd.Timestamp('1928-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1928-01-01', '1928-12-31')
    for h in holidays_1928:
        assert h not in valid_days
        assert h in all_holidays        

    # early closes we expect:
    early_closes_1928 = pd.date_range('1928-05-21', 
                                      '1928-05-25', 
                                       freq=CustomBusinessDay(weekmask = 'Mon Tue Wed Thu Fri Sat'),
                                       tz='UTC').to_list()
    expected = nyse.early_closes(nyse.schedule('1928-01-01', '1928-12-31'))
    for ec in early_closes_1928:
        assert ec in expected.index        
        
def test_1929():
    nyse = NYSEExchangeCalendar()
    holidays_1929 = [
        pd.Timestamp('1929-01-01', tz='UTC'),
        pd.Timestamp('1929-02-09', tz='UTC'),
        pd.Timestamp('1929-02-12', tz='UTC'),
        pd.Timestamp('1929-02-22', tz='UTC'),
        pd.Timestamp('1929-02-23', tz='UTC'),
        pd.Timestamp('1929-03-29', tz='UTC'),
        pd.Timestamp('1929-03-30', tz='UTC'),
        pd.Timestamp('1929-05-30', tz='UTC'),
        pd.Timestamp('1929-07-04', tz='UTC'),
        pd.Timestamp('1929-08-31', tz='UTC'),
        pd.Timestamp('1929-09-02', tz='UTC'),
        pd.Timestamp('1929-10-12', tz='UTC'),
        pd.Timestamp('1929-11-01', tz='UTC'),
        pd.Timestamp('1929-11-02', tz='UTC'),
        pd.Timestamp('1929-11-05', tz='UTC'),
        pd.Timestamp('1929-11-09', tz='UTC'),
        pd.Timestamp('1929-11-16', tz='UTC'),
        pd.Timestamp('1929-11-23', tz='UTC'),
        pd.Timestamp('1929-11-28', tz='UTC'),
        pd.Timestamp('1929-11-29', tz='UTC'),
        pd.Timestamp('1929-11-30', tz='UTC'),
        pd.Timestamp('1929-12-25', tz='UTC')
    ]
    valid_days = nyse.valid_days('1929-01-01', '1929-12-31')
    for h in holidays_1929:
        assert h not in valid_days
        assert h in all_holidays        

    # early closes we expect:
    early_closes_1929 = [
            pd.Timestamp('1929-11-06', tz='UTC'),
            pd.Timestamp('1929-11-07', tz='UTC'),
            pd.Timestamp('1929-11-08', tz='UTC'),
            pd.Timestamp('1929-11-11', tz='UTC'),
            pd.Timestamp('1929-11-12', tz='UTC'),
            pd.Timestamp('1929-11-13', tz='UTC'),
            pd.Timestamp('1929-11-14', tz='UTC'),
            pd.Timestamp('1929-11-15', tz='UTC'),
            pd.Timestamp('1929-11-18', tz='UTC'),
            pd.Timestamp('1929-11-19', tz='UTC'),
            pd.Timestamp('1929-11-20', tz='UTC'),
            pd.Timestamp('1929-11-21', tz='UTC'),
            pd.Timestamp('1929-11-22', tz='UTC')
    ]
    expected = nyse.early_closes(nyse.schedule('1929-01-01', '1929-12-31'))
    for ec in early_closes_1929:
        assert ec in expected.index          
        
    # late opens we expect:
    late_opens_1929 = [
            pd.Timestamp('1929-10-31', tz='UTC'),
    ]
    expected = nyse.late_opens(nyse.schedule('1929-01-01', '1929-12-31'))
    for lo in late_opens_1929:
        assert lo in expected.index          