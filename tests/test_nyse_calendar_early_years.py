import os
import pytz

import pandas as pd
from pandas.testing import assert_index_equal
from pandas.tseries.offsets import CustomBusinessDay

from pandas_market_calendars.exchange_calendar_nyse import NYSEExchangeCalendar

all_holidays = pd.DatetimeIndex(NYSEExchangeCalendar().holidays().holidays)
nyse = NYSEExchangeCalendar()

def test_time_zone():
    assert NYSEExchangeCalendar().tz == pytz.timezone('America/New_York')
    assert NYSEExchangeCalendar().name == 'NYSE'


def test_open_time_tz():
    assert nyse.open_time.tzinfo == nyse.tz


def test_close_time_tz():
    assert nyse.close_time.tzinfo == nyse.tz

def _test_holidays(holidays, start, end):
    df = pd.DataFrame(nyse.holidays().holidays, columns=['holidays'])
    mask = df['holidays'].isin(pd.date_range(start,end,freq='D'))   
    df = df[mask]
    assert len(holidays) == len(df) #Catches duplicate entries from overlapping rules
    valid_days = nyse.valid_days(start, end )
    for h in holidays:
        assert h not in valid_days
        assert h in all_holidays    

def _test_no_special_opens(start, end):   
    assert len(nyse.late_opens(nyse.schedule(start, end))) == 0
    
def _test_no_special_closes(start, end):
    assert len(nyse.early_closes(nyse.schedule(start, end))) == 0

def _test_no_special_opens_closes(start, end):
    _test_no_special_opens(start, end)
    _test_no_special_closes(start, end)
    
def _test_has_late_opens(late_opens, start, end):
    expected = nyse.late_opens(nyse.schedule(start, end))
    assert len(expected) == len(late_opens)
    for lo in late_opens:
        assert lo in expected.index
    
def _test_has_early_closes(early_closes, start, end):
    expected = nyse.early_closes(nyse.schedule(start, end))
    assert len(expected) == len(early_closes)
    for ec in early_closes:
        assert ec in expected.index
                           

def test_1885():
    start = '1885-01-01'
    end   = '1885-12-31'
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)
        
    #ensure labor day is a valid trading day
    assert pd.Timestamp('1885-09-07' , tz='UTC') in nyse.valid_days(start,end)

def test_1886():
    start = '1886-01-01'
    end   = '1886-12-31'    
    holidays = [
        pd.Timestamp('1886-01-01' , tz='UTC'),
        pd.Timestamp('1886-02-22' , tz='UTC'),
        pd.Timestamp('1886-04-23' , tz='UTC'),
        pd.Timestamp('1886-05-31' , tz='UTC'),
        pd.Timestamp('1886-07-05' , tz='UTC'),
        pd.Timestamp('1886-11-02' , tz='UTC'),
        pd.Timestamp('1886-11-25' , tz='UTC'),
        pd.Timestamp('1886-12-25' , tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1887():
    start = '1887-01-01'
    end   = '1887-12-31'        
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)



def test_1888():
    start = '1888-01-01'
    end   = '1888-12-31'            
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1889():
    start = '1889-01-01'
    end   = '1889-12-31'                
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1890():
    start = '1890-01-01'
    end   = '1890-12-31'                    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1891():
    start = '1891-01-01'
    end   = '1891-12-31'            
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)
        

def test_1892():
    start = '1892-01-01'
    end   = '1892-12-31'                
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1893():
    start = '1893-01-01'
    end   = '1893-12-31'                    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1894():
    start = '1894-01-01'
    end   = '1894-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1895():
    start = '1895-01-01'
    end   = '1895-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1896():
    start = '1896-01-01'
    end   = '1896-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1897():
    start = '1897-01-01'
    end   = '1897-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1898():
    start = '1898-01-01'
    end   = '1898-12-31'        
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1899():
    start = '1899-01-01'
    end   = '1899-12-31'
    holidays = [
        pd.Timestamp('1899-01-02', tz='UTC'),
        pd.Timestamp('1899-02-11', tz='UTC'),
        pd.Timestamp('1899-02-13', tz='UTC'),
        pd.Timestamp('1899-02-22', tz='UTC'),
        pd.Timestamp('1899-03-31', tz='UTC'),
        pd.Timestamp('1899-05-29', tz='UTC'),
        pd.Timestamp('1899-05-30', tz='UTC'),
        pd.Timestamp('1899-07-03', tz='UTC'),
        pd.Timestamp('1899-07-04', tz='UTC'),
        pd.Timestamp('1899-09-04', tz='UTC'),
        pd.Timestamp('1899-09-29', tz='UTC'),
        pd.Timestamp('1899-09-30', tz='UTC'),
        pd.Timestamp('1899-11-07', tz='UTC'),
        pd.Timestamp('1899-11-25', tz='UTC'),
        pd.Timestamp('1899-11-30', tz='UTC'),
        pd.Timestamp('1899-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1900():
    start = '1900-01-01'
    end   = '1900-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1901():
    start = '1901-01-01'
    end   = '1901-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1902():
    start = '1902-01-01'
    end   = '1902-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1903():
    start = '1903-01-01'
    end   = '1903-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1904():
    start = '1904-01-01'
    end   = '1904-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1905():
    start = '1905-01-01'
    end   = '1905-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1906():
    start = '1906-01-01'
    end   = '1906-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1907():
    start = '1907-01-01'
    end   = '1907-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1908():
    start = '1908-01-01'
    end   = '1908-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)
        
    # early closes we expect:
    early_closes = [
        pd.Timestamp(' 1908-06-26' , tz='UTC') # Grover Cleveland funeral
    ]
    _test_has_early_closes(early_closes, start, end )
        
        

def test_1909():
    start = '1909-01-01'
    end   = '1909-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1910():
    start = '1910-01-01'
    end   = '1910-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
        
    # early closes:
    early_closes = [
        pd.Timestamp('1910-05-07' , tz='UTC') #King Edward VII death
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens:
    late_opens= [
        pd.Timestamp('1910-05-20' , tz='UTC') # King Edward VII funderal
    ]
    _test_has_late_opens(late_opens, start, end)
        
        
def test_1911():
    start = '1911-01-01'
    end   = '1911-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1912():
    start = '1912-01-01'
    end   = '1912-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1913():
    start = '1913-01-01'
    end   = '1913-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_closes(start, end)

    # late opens:
    late_opens = [
        pd.Timestamp('1913-04-14' , tz='UTC'), # JP Morgan Funeral
        pd.Timestamp('1913-09-22' , tz='UTC')  # Mayor William J. Gaynor Funeral
    ]
    _test_has_late_opens(late_opens, start, end)

    
def test_1914():
    start = '1914-01-01'
    end   = '1914-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1915():
    start = '1915-01-01'
    end   = '1915-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1916():
    start = '1916-01-01'
    end   = '1916-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)
       
        
def test_1917():
    start = '1917-01-01'
    end   = '1917-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp(' 1917-08-29' , tz='UTC'), # Parade of National Guard
        pd.Timestamp(' 1917-10-24' , tz='UTC'), # Liberty Day
    ]
    _test_has_early_closes(early_closes, start, end)

def test_1918():
    start = '1918-01-01'
    end   = '1918-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp('1918-04-26'), # Liberty Day
        pd.Timestamp('1918-11-07'), # False armistice report        
    ]
    _test_has_early_closes(early_closes, start, end)       
        
def test_1919():
    start = '1919-01-01'
    end   = '1919-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
 
    # early closes we expect:
    early_closes = [
        pd.Timestamp('1919-01-07')
    ]
    _test_has_early_closes(early_closes, start, end)        
    
    # late opens we expect:
    late_opens = [
            pd.Timestamp('1919-12-30', tz='UTC'), # Traffic block
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1920():
    start = '1920-01-01'
    end   = '1920-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
 
    # early closes we expect:
    early_closes= [
        pd.Timestamp('1920-09-16') # Wall Street explosion
    ]
    _test_has_early_closes(early_closes, start, end)
        
    # late opens we expect:
    late_opens = [
            pd.Timestamp('1920-02-06', tz='UTC'), # traffic block
    ]
    _test_has_late_opens(late_opens, start, end)    
 
def test_1921():
    start = '1921-01-01'
    end   = '1921-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_closes(start, end)
         
    # late opens we expect:
    late_opens = [
            pd.Timestamp('1921-08-08', tz='UTC'), # fire in annunciator board
    ]
    _test_has_late_opens(late_opens, start, end)
 
def test_1922():
    start = '1922-01-01'
    end   = '1922-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)


def test_1923():
    start = '1923-01-01'
    end   = '1923-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1924():
    start = '1924-01-01'
    end   = '1924-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp('1924-02-06') # Former President Woodrow Wilson funeral
    ]
    _test_has_early_closes(early_closes, start, end)

        
def test_1925():
    start = '1925-01-01'
    end   = '1925-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
 
    # early closes we expect:
    early_closes = [
        pd.Timestamp('1925-09-18') # Seymour L. Cromwell funeral
    ]
    _test_has_early_closes(early_closes, start, end)

    # late opens we expect:
    late_opens = [
            pd.Timestamp('1925-01-24', tz='UTC'), # Eclipse of sun
    ]
    _test_has_late_opens(late_opens, start, end)


def test_1926():
    start = '1926-01-01'
    end   = '1926-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1927():
    start = '1927-01-01'
    end   = '1927-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)
        
        
def test_1928():
    start = '1928-01-01'
    end   = '1928-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = pd.date_range('1928-05-21', # Backlog catch up
                                 '1928-05-25', 
                                  freq=CustomBusinessDay(weekmask = 'Mon Tue Wed Thu Fri Sat'),
                                   tz='UTC').to_list()
    _test_has_early_closes(early_closes, start, end)
    
        
def test_1929():
    start = '1929-01-01'
    end   = '1929-12-31'    
    holidays = [
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
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [ # All backlog relief
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
    _test_has_early_closes(early_closes, start, end)
        
    # late opens we expect:
    late_opens = [
            pd.Timestamp('1929-10-31', tz='UTC'), # Backlog relief
    ]
    _test_has_late_opens(late_opens, start, end)

        
def test_1930():
    start = '1930-01-01'
    end   = '1930-12-31'    
    holidays = [
        pd.Timestamp('1930-01-01', tz='UTC'),
        pd.Timestamp('1930-02-12', tz='UTC'),
        pd.Timestamp('1930-02-22', tz='UTC'),
        pd.Timestamp('1930-04-18', tz='UTC'),
        pd.Timestamp('1930-04-19', tz='UTC'),
        pd.Timestamp('1930-05-30', tz='UTC'),
        pd.Timestamp('1930-05-31', tz='UTC'),
        pd.Timestamp('1930-07-04', tz='UTC'),
        pd.Timestamp('1930-07-05', tz='UTC'),
        pd.Timestamp('1930-08-30', tz='UTC'),
        pd.Timestamp('1930-09-01', tz='UTC'),
        pd.Timestamp('1930-10-13', tz='UTC'),
        pd.Timestamp('1930-11-04', tz='UTC'),
        pd.Timestamp('1930-11-27', tz='UTC'),
        pd.Timestamp('1930-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
            pd.Timestamp('1930-03-11', tz='UTC'), # Taft funeral
    ]
    _test_has_early_closes(early_closes, start, end)

        
def test_1931():
    start = '1931-01-01'
    end   = '1931-12-31'    
    holidays = [
        pd.Timestamp('1931-01-01', tz='UTC'),
        pd.Timestamp('1931-02-12', tz='UTC'),
        pd.Timestamp('1931-02-23', tz='UTC'),
        pd.Timestamp('1931-04-03', tz='UTC'),
        pd.Timestamp('1931-05-30', tz='UTC'),
        pd.Timestamp('1931-07-04', tz='UTC'),
        pd.Timestamp('1931-09-05', tz='UTC'),
        pd.Timestamp('1931-09-07', tz='UTC'),
        pd.Timestamp('1931-10-12', tz='UTC'),
        pd.Timestamp('1931-11-03', tz='UTC'),
        pd.Timestamp('1931-11-26', tz='UTC'),
        pd.Timestamp('1931-12-25', tz='UTC'),
        pd.Timestamp('1931-12-26', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1932():
    start = '1932-01-01'
    end   = '1932-12-31'    
    holidays = [
        pd.Timestamp('1932-01-01', tz='UTC'),
        pd.Timestamp('1932-02-12', tz='UTC'),
        pd.Timestamp('1932-02-22', tz='UTC'),
        pd.Timestamp('1932-03-25', tz='UTC'),
        pd.Timestamp('1932-05-30', tz='UTC'),
        pd.Timestamp('1932-07-02', tz='UTC'),
        pd.Timestamp('1932-07-04', tz='UTC'),
        pd.Timestamp('1932-09-05', tz='UTC'),
        pd.Timestamp('1932-10-12', tz='UTC'),
        pd.Timestamp('1932-11-08', tz='UTC'),
        pd.Timestamp('1932-11-24', tz='UTC'),
        pd.Timestamp('1932-12-26', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1933():
    start = '1933-01-01'
    end   = '1933-12-31'    
    holidays = [
        pd.Timestamp('1933-01-02', tz='UTC'),
        pd.Timestamp('1933-01-07', tz='UTC'),
        pd.Timestamp('1933-02-13', tz='UTC'),
        pd.Timestamp('1933-02-22', tz='UTC'),
        pd.Timestamp('1933-03-04', tz='UTC'),
        pd.Timestamp('1933-03-06', tz='UTC'),
        pd.Timestamp('1933-03-07', tz='UTC'),
        pd.Timestamp('1933-03-08', tz='UTC'),
        pd.Timestamp('1933-03-09', tz='UTC'),
        pd.Timestamp('1933-03-10', tz='UTC'),
        pd.Timestamp('1933-03-11', tz='UTC'),
        pd.Timestamp('1933-03-12', tz='UTC'),
        pd.Timestamp('1933-03-13', tz='UTC'),
        pd.Timestamp('1933-03-14', tz='UTC'),
        pd.Timestamp('1933-04-14', tz='UTC'),
        pd.Timestamp('1933-05-30', tz='UTC'),
        pd.Timestamp('1933-07-04', tz='UTC'),
        pd.Timestamp('1933-07-29', tz='UTC'),
        pd.Timestamp('1933-08-05', tz='UTC'),
        pd.Timestamp('1933-08-12', tz='UTC'),
        pd.Timestamp('1933-08-19', tz='UTC'),
        pd.Timestamp('1933-08-26', tz='UTC'),
        pd.Timestamp('1933-09-02', tz='UTC'),
        pd.Timestamp('1933-09-04', tz='UTC'),
        pd.Timestamp('1933-10-12', tz='UTC'),
        pd.Timestamp('1933-11-07', tz='UTC'),
        pd.Timestamp('1933-11-30', tz='UTC'),
        pd.Timestamp('1933-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp('1933-07-26', tz='UTC'), # Volume
        pd.Timestamp('1933-07-27', tz='UTC'), # Volume
        pd.Timestamp('1933-07-28', tz='UTC'), # Volume
        pd.Timestamp('1933-08-04', tz='UTC'), # Volume
        pd.Timestamp('1933-09-13', tz='UTC')  # NRA demonstration
    ]
    _test_has_early_closes(early_closes, start, end)
        
    # late opens we expect:
    late_opens = [
        pd.Timestamp('1933-07-24', tz='UTC'), # Volume
        pd.Timestamp('1933-07-25', tz='UTC'), # Volume
        pd.Timestamp('1933-07-26', tz='UTC'), # Volume
        pd.Timestamp('1933-07-27', tz='UTC'), # Volume
        pd.Timestamp('1933-07-28', tz='UTC'), # Volume
    ]
    _test_has_late_opens(late_opens, start, end)

        
def test_1934():
    start = '1934-01-01'
    end   = '1934-12-31'    
    holidays = [
        pd.Timestamp('1934-01-01', tz='UTC'),
        pd.Timestamp('1934-02-12', tz='UTC'),
        pd.Timestamp('1934-02-22', tz='UTC'),
        pd.Timestamp('1934-03-30', tz='UTC'),
        pd.Timestamp('1934-05-30', tz='UTC'),
        pd.Timestamp('1934-07-04', tz='UTC'),
        pd.Timestamp('1934-09-03', tz='UTC'),
        pd.Timestamp('1934-10-12', tz='UTC'),
        pd.Timestamp('1934-11-06', tz='UTC'),
        pd.Timestamp('1934-11-12', tz='UTC'),
        pd.Timestamp('1934-11-29', tz='UTC'),
        pd.Timestamp('1934-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
        
    # late opens we expect:
    late_opens = [
        pd.Timestamp('1934-02-20', tz='UTC') # snow
    ]
    _test_has_late_opens(late_opens, start, end)
       
        
def test_1935():
    start = '1935-01-01'
    end   = '1935-12-31'    
    holidays = [
       pd.Timestamp('1935-01-01', tz='UTC'),
        pd.Timestamp('1935-02-12', tz='UTC'),
        pd.Timestamp('1935-02-22', tz='UTC'),
        pd.Timestamp('1935-04-19', tz='UTC'),
        pd.Timestamp('1935-05-30', tz='UTC'),
        pd.Timestamp('1935-07-04', tz='UTC'),
        pd.Timestamp('1935-09-02', tz='UTC'),
        pd.Timestamp('1935-10-12', tz='UTC'),
        pd.Timestamp('1935-11-05', tz='UTC'),
        pd.Timestamp('1935-11-11', tz='UTC'),
        pd.Timestamp('1935-11-28', tz='UTC'),
        pd.Timestamp('1935-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1936():
    start = '1936-01-01'
    end   = '1936-12-31'    
    holidays = [
        pd.Timestamp('1936-01-01', tz='UTC'),
        pd.Timestamp('1936-02-12', tz='UTC'),
        pd.Timestamp('1936-02-22', tz='UTC'),
        pd.Timestamp('1936-04-10', tz='UTC'),
        pd.Timestamp('1936-05-30', tz='UTC'),
        pd.Timestamp('1936-07-04', tz='UTC'),
        pd.Timestamp('1936-09-07', tz='UTC'),
        pd.Timestamp('1936-10-12', tz='UTC'),
        pd.Timestamp('1936-11-03', tz='UTC'),
        pd.Timestamp('1936-11-11', tz='UTC'),
        pd.Timestamp('1936-11-26', tz='UTC'),
        pd.Timestamp('1936-12-25', tz='UTC'),
        pd.Timestamp('1936-12-26', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
        
    # late opens we expect:
    late_opens = [
        pd.Timestamp('1936-01-28', tz='UTC') # King George V funeral
    ]
    _test_has_late_opens(late_opens, start, end)
        
def test_1937():
    start = '1937-01-01'
    end   = '1937-12-31'    
    holidays = [
        pd.Timestamp('1937-01-01', tz='UTC'),
        pd.Timestamp('1937-02-12', tz='UTC'),
        pd.Timestamp('1937-02-22', tz='UTC'),
        pd.Timestamp('1937-03-26', tz='UTC'),
        pd.Timestamp('1937-05-29', tz='UTC'),
        pd.Timestamp('1937-05-31', tz='UTC'),
        pd.Timestamp('1937-07-03', tz='UTC'),
        pd.Timestamp('1937-07-05', tz='UTC'),
        pd.Timestamp('1937-09-06', tz='UTC'),
        pd.Timestamp('1937-10-12', tz='UTC'),
        pd.Timestamp('1937-11-02', tz='UTC'),
        pd.Timestamp('1937-11-11', tz='UTC'),
        pd.Timestamp('1937-11-25', tz='UTC'),
        pd.Timestamp('1937-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1938():
    start = '1938-01-01'
    end   = '1938-12-31'    
    holidays = [
        pd.Timestamp('1938-01-01', tz='UTC'),
        pd.Timestamp('1938-02-12', tz='UTC'),
        pd.Timestamp('1938-02-22', tz='UTC'),
        pd.Timestamp('1938-04-15', tz='UTC'),
        pd.Timestamp('1938-05-30', tz='UTC'),
        pd.Timestamp('1938-07-04', tz='UTC'),
        pd.Timestamp('1938-09-05', tz='UTC'),
        pd.Timestamp('1938-10-12', tz='UTC'),
        pd.Timestamp('1938-11-08', tz='UTC'),
        pd.Timestamp('1938-11-11', tz='UTC'),
        pd.Timestamp('1938-11-24', tz='UTC'),
        pd.Timestamp('1938-12-26', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)
              
        
def test_1939():
    start = '1939-01-01'
    end   = '1939-12-31'    
    holidays = [
        pd.Timestamp('1939-01-02', tz='UTC'),
        pd.Timestamp('1939-02-13', tz='UTC'),
        pd.Timestamp('1939-02-22', tz='UTC'),
        pd.Timestamp('1939-04-07', tz='UTC'),
        pd.Timestamp('1939-05-30', tz='UTC'),
        pd.Timestamp('1939-07-04', tz='UTC'),
        pd.Timestamp('1939-09-04', tz='UTC'),
        pd.Timestamp('1939-10-12', tz='UTC'),
        pd.Timestamp('1939-11-07', tz='UTC'),
        pd.Timestamp('1939-11-11', tz='UTC'),
        pd.Timestamp('1939-11-23', tz='UTC'),
        pd.Timestamp('1939-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1940():
    start = '1940-01-01'
    end   = '1940-12-31'    
    holidays = [
         pd.Timestamp('1940-01-01', tz='UTC'),
        pd.Timestamp('1940-02-12', tz='UTC'),
        pd.Timestamp('1940-02-22', tz='UTC'),
        pd.Timestamp('1940-03-22', tz='UTC'),
        pd.Timestamp('1940-05-30', tz='UTC'),
        pd.Timestamp('1940-07-04', tz='UTC'),
        pd.Timestamp('1940-09-02', tz='UTC'),
        pd.Timestamp('1940-10-12', tz='UTC'),
        pd.Timestamp('1940-11-05', tz='UTC'),
        pd.Timestamp('1940-11-11', tz='UTC'),
        pd.Timestamp('1940-11-21', tz='UTC'),
        pd.Timestamp('1940-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1941():
    start = '1941-01-01'
    end   = '1941-12-31'    
    holidays = [
        pd.Timestamp('1941-01-01', tz='UTC'),
        pd.Timestamp('1941-02-12', tz='UTC'),
        pd.Timestamp('1941-02-22', tz='UTC'),
        pd.Timestamp('1941-04-11', tz='UTC'),
        pd.Timestamp('1941-05-30', tz='UTC'),
        pd.Timestamp('1941-07-04', tz='UTC'),
        pd.Timestamp('1941-09-01', tz='UTC'),
        pd.Timestamp('1941-10-13', tz='UTC'),
        pd.Timestamp('1941-11-04', tz='UTC'),
        pd.Timestamp('1941-11-11', tz='UTC'),
        pd.Timestamp('1941-11-20', tz='UTC'),
        pd.Timestamp('1941-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1942():
    start = '1942-01-01'
    end   = '1942-12-31'    
    holidays = [
        pd.Timestamp('1942-01-01', tz='UTC'),
        pd.Timestamp('1942-02-12', tz='UTC'),
        pd.Timestamp('1942-02-23', tz='UTC'),
        pd.Timestamp('1942-04-03', tz='UTC'),
        pd.Timestamp('1942-05-30', tz='UTC'),
        pd.Timestamp('1942-07-04', tz='UTC'),
        pd.Timestamp('1942-09-07', tz='UTC'),
        pd.Timestamp('1942-10-12', tz='UTC'),
        pd.Timestamp('1942-11-03', tz='UTC'),
        pd.Timestamp('1942-11-11', tz='UTC'),
        pd.Timestamp('1942-11-26', tz='UTC'),
        pd.Timestamp('1942-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1943():
    start = '1943-01-01'
    end   = '1943-12-31'    
    holidays = [
        pd.Timestamp('1943-01-01', tz='UTC'),
        pd.Timestamp('1943-02-12', tz='UTC'),
        pd.Timestamp('1943-02-22', tz='UTC'),
        pd.Timestamp('1943-04-23', tz='UTC'),
        pd.Timestamp('1943-05-31', tz='UTC'),
        pd.Timestamp('1943-07-05', tz='UTC'),
        pd.Timestamp('1943-09-06', tz='UTC'),
        pd.Timestamp('1943-10-12', tz='UTC'),
        pd.Timestamp('1943-11-02', tz='UTC'),
        pd.Timestamp('1943-11-11', tz='UTC'),
        pd.Timestamp('1943-11-25', tz='UTC'),
        pd.Timestamp('1943-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1944():
    start = '1944-01-01'
    end   = '1944-12-31'    
    holidays = [
        pd.Timestamp('1944-01-01', tz='UTC'),
        pd.Timestamp('1944-02-12', tz='UTC'),
        pd.Timestamp('1944-02-22', tz='UTC'),
        pd.Timestamp('1944-04-07', tz='UTC'),
        pd.Timestamp('1944-05-30', tz='UTC'),
        pd.Timestamp('1944-07-04', tz='UTC'),
        pd.Timestamp('1944-08-19', tz='UTC'),
        pd.Timestamp('1944-08-26', tz='UTC'),
        pd.Timestamp('1944-09-02', tz='UTC'),
        pd.Timestamp('1944-09-04', tz='UTC'),
        pd.Timestamp('1944-10-12', tz='UTC'),
        pd.Timestamp('1944-11-07', tz='UTC'),
        pd.Timestamp('1944-11-11', tz='UTC'),
        pd.Timestamp('1944-11-23', tz='UTC'),
        pd.Timestamp('1944-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1945():
    start = '1945-01-01'
    end   = '1945-12-31'    
    holidays = [
        pd.Timestamp('1945-01-01', tz='UTC'),
        pd.Timestamp('1945-02-12', tz='UTC'),
        pd.Timestamp('1945-02-22', tz='UTC'),
        pd.Timestamp('1945-03-30', tz='UTC'),
        pd.Timestamp('1945-04-14', tz='UTC'),
        pd.Timestamp('1945-05-30', tz='UTC'),
        pd.Timestamp('1945-07-04', tz='UTC'),
        pd.Timestamp('1945-07-07', tz='UTC'),
        pd.Timestamp('1945-07-14', tz='UTC'),
        pd.Timestamp('1945-07-21', tz='UTC'),
        pd.Timestamp('1945-07-28', tz='UTC'),
        pd.Timestamp('1945-08-04', tz='UTC'),
        pd.Timestamp('1945-08-11', tz='UTC'),
        pd.Timestamp('1945-08-15', tz='UTC'),
        pd.Timestamp('1945-08-16', tz='UTC'),
        pd.Timestamp('1945-08-18', tz='UTC'),
        pd.Timestamp('1945-08-25', tz='UTC'),
        pd.Timestamp('1945-09-01', tz='UTC'),
        pd.Timestamp('1945-09-03', tz='UTC'),
        pd.Timestamp('1945-10-12', tz='UTC'),
        pd.Timestamp('1945-10-13', tz='UTC'),
        pd.Timestamp('1945-10-27', tz='UTC'),
        pd.Timestamp('1945-11-06', tz='UTC'),
        pd.Timestamp('1945-11-12', tz='UTC'),
        pd.Timestamp('1945-11-22', tz='UTC'),
        pd.Timestamp('1945-12-24', tz='UTC'),
        pd.Timestamp('1945-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1946():
    start = '1946-01-01'
    end   = '1946-12-31'    
    holidays = [
        pd.Timestamp('1946-01-01', tz='UTC'),
        pd.Timestamp('1946-02-12', tz='UTC'),
        pd.Timestamp('1946-02-22', tz='UTC'),
        pd.Timestamp('1946-02-23', tz='UTC'),
        pd.Timestamp('1946-04-19', tz='UTC'),
        pd.Timestamp('1946-05-25', tz='UTC'),
        pd.Timestamp('1946-05-30', tz='UTC'),
        pd.Timestamp('1946-06-01', tz='UTC'),
        pd.Timestamp('1946-06-08', tz='UTC'),
        pd.Timestamp('1946-06-15', tz='UTC'),
        pd.Timestamp('1946-06-22', tz='UTC'),
        pd.Timestamp('1946-06-29', tz='UTC'),
        pd.Timestamp('1946-07-04', tz='UTC'),
        pd.Timestamp('1946-07-06', tz='UTC'),
        pd.Timestamp('1946-07-13', tz='UTC'),
        pd.Timestamp('1946-07-20', tz='UTC'),
        pd.Timestamp('1946-07-27', tz='UTC'),
        pd.Timestamp('1946-08-03', tz='UTC'),
        pd.Timestamp('1946-08-10', tz='UTC'),
        pd.Timestamp('1946-08-17', tz='UTC'),
        pd.Timestamp('1946-08-24', tz='UTC'),
        pd.Timestamp('1946-08-31', tz='UTC'),
        pd.Timestamp('1946-09-02', tz='UTC'),
        pd.Timestamp('1946-09-07', tz='UTC'),
        pd.Timestamp('1946-09-14', tz='UTC'),
        pd.Timestamp('1946-09-21', tz='UTC'),
        pd.Timestamp('1946-09-28', tz='UTC'),
        pd.Timestamp('1946-10-12', tz='UTC'),
        pd.Timestamp('1946-11-05', tz='UTC'),
        pd.Timestamp('1946-11-11', tz='UTC'),
        pd.Timestamp('1946-11-28', tz='UTC'),
        pd.Timestamp('1946-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1947():
    start = '1947-01-01'
    end   = '1947-12-31'    
    holidays = [
        pd.Timestamp('1947-01-01', tz='UTC'),
        pd.Timestamp('1947-02-12', tz='UTC'),
        pd.Timestamp('1947-02-22', tz='UTC'),
        pd.Timestamp('1947-04-04', tz='UTC'),
        pd.Timestamp('1947-05-30', tz='UTC'),
        pd.Timestamp('1947-05-31', tz='UTC'),
        pd.Timestamp('1947-06-07', tz='UTC'),
        pd.Timestamp('1947-06-14', tz='UTC'),
        pd.Timestamp('1947-06-21', tz='UTC'),
        pd.Timestamp('1947-06-28', tz='UTC'),
        pd.Timestamp('1947-07-04', tz='UTC'),
        pd.Timestamp('1947-07-05', tz='UTC'),
        pd.Timestamp('1947-07-12', tz='UTC'),
        pd.Timestamp('1947-07-19', tz='UTC'),
        pd.Timestamp('1947-07-26', tz='UTC'),
        pd.Timestamp('1947-08-02', tz='UTC'),
        pd.Timestamp('1947-08-09', tz='UTC'),
        pd.Timestamp('1947-08-16', tz='UTC'),
        pd.Timestamp('1947-08-23', tz='UTC'),
        pd.Timestamp('1947-08-30', tz='UTC'),
        pd.Timestamp('1947-09-01', tz='UTC'),
        pd.Timestamp('1947-09-06', tz='UTC'),
        pd.Timestamp('1947-09-13', tz='UTC'),
        pd.Timestamp('1947-09-20', tz='UTC'),
        pd.Timestamp('1947-09-27', tz='UTC'),
        pd.Timestamp('1947-10-13', tz='UTC'),
        pd.Timestamp('1947-11-04', tz='UTC'),
        pd.Timestamp('1947-11-11', tz='UTC'),
        pd.Timestamp('1947-11-27', tz='UTC'),
        pd.Timestamp('1947-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1948():
    start = '1948-01-01'
    end   = '1948-12-31'    
    holidays = [
        pd.Timestamp('1948-01-01', tz='UTC'),
        pd.Timestamp('1948-01-03', tz='UTC'),
        pd.Timestamp('1948-02-12', tz='UTC'),
        pd.Timestamp('1948-02-23', tz='UTC'),
        pd.Timestamp('1948-03-26', tz='UTC'),
        pd.Timestamp('1948-05-29', tz='UTC'),
        pd.Timestamp('1948-05-31', tz='UTC'),
        pd.Timestamp('1948-06-05', tz='UTC'),
        pd.Timestamp('1948-06-12', tz='UTC'),
        pd.Timestamp('1948-06-19', tz='UTC'),
        pd.Timestamp('1948-06-26', tz='UTC'),
        pd.Timestamp('1948-07-03', tz='UTC'),
        pd.Timestamp('1948-07-05', tz='UTC'),
        pd.Timestamp('1948-07-10', tz='UTC'),
        pd.Timestamp('1948-07-17', tz='UTC'),
        pd.Timestamp('1948-07-24', tz='UTC'),
        pd.Timestamp('1948-07-31', tz='UTC'),
        pd.Timestamp('1948-08-07', tz='UTC'),
        pd.Timestamp('1948-08-14', tz='UTC'),
        pd.Timestamp('1948-08-21', tz='UTC'),
        pd.Timestamp('1948-08-28', tz='UTC'),
        pd.Timestamp('1948-09-04', tz='UTC'),
        pd.Timestamp('1948-09-06', tz='UTC'),
        pd.Timestamp('1948-09-11', tz='UTC'),
        pd.Timestamp('1948-09-18', tz='UTC'),
        pd.Timestamp('1948-09-25', tz='UTC'),
        pd.Timestamp('1948-10-12', tz='UTC'),
        pd.Timestamp('1948-11-02', tz='UTC'),
        pd.Timestamp('1948-11-11', tz='UTC'),
        pd.Timestamp('1948-11-25', tz='UTC'),
        pd.Timestamp('1948-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1949():
    start = '1949-01-01'
    end   = '1949-12-31'    
    holidays = [
        pd.Timestamp('1949-01-01', tz='UTC'),
        pd.Timestamp('1949-02-12', tz='UTC'),
        pd.Timestamp('1949-02-22', tz='UTC'),
        pd.Timestamp('1949-04-15', tz='UTC'),
        pd.Timestamp('1949-05-28', tz='UTC'),
        pd.Timestamp('1949-05-30', tz='UTC'),
        pd.Timestamp('1949-06-04', tz='UTC'),
        pd.Timestamp('1949-06-11', tz='UTC'),
        pd.Timestamp('1949-06-18', tz='UTC'),
        pd.Timestamp('1949-06-25', tz='UTC'),
        pd.Timestamp('1949-07-02', tz='UTC'),
        pd.Timestamp('1949-07-04', tz='UTC'),
        pd.Timestamp('1949-07-09', tz='UTC'),
        pd.Timestamp('1949-07-16', tz='UTC'),
        pd.Timestamp('1949-07-23', tz='UTC'),
        pd.Timestamp('1949-07-30', tz='UTC'),
        pd.Timestamp('1949-08-06', tz='UTC'),
        pd.Timestamp('1949-08-13', tz='UTC'),
        pd.Timestamp('1949-08-20', tz='UTC'),
        pd.Timestamp('1949-08-27', tz='UTC'),
        pd.Timestamp('1949-09-03', tz='UTC'),
        pd.Timestamp('1949-09-05', tz='UTC'),
        pd.Timestamp('1949-09-10', tz='UTC'),
        pd.Timestamp('1949-09-17', tz='UTC'),
        pd.Timestamp('1949-09-24', tz='UTC'),
        pd.Timestamp('1949-10-12', tz='UTC'),
        pd.Timestamp('1949-11-08', tz='UTC'),
        pd.Timestamp('1949-11-11', tz='UTC'),
        pd.Timestamp('1949-11-24', tz='UTC'),
        pd.Timestamp('1949-12-24', tz='UTC'),
        pd.Timestamp('1949-12-26', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)
        
def test_1950():
    start = '1950-01-01'
    end   = '1950-12-31'    
    holidays = [
        pd.Timestamp('1950-01-02', tz='UTC'),
        pd.Timestamp('1950-02-13', tz='UTC'),
        pd.Timestamp('1950-02-22', tz='UTC'),
        pd.Timestamp('1950-04-07', tz='UTC'),
        pd.Timestamp('1950-05-30', tz='UTC'),
        pd.Timestamp('1950-06-03', tz='UTC'),
        pd.Timestamp('1950-06-10', tz='UTC'),
        pd.Timestamp('1950-06-17', tz='UTC'),
        pd.Timestamp('1950-06-24', tz='UTC'),
        pd.Timestamp('1950-07-01', tz='UTC'),
        pd.Timestamp('1950-07-04', tz='UTC'),
        pd.Timestamp('1950-07-08', tz='UTC'),
        pd.Timestamp('1950-07-15', tz='UTC'),
        pd.Timestamp('1950-07-22', tz='UTC'),
        pd.Timestamp('1950-07-29', tz='UTC'),
        pd.Timestamp('1950-08-05', tz='UTC'),
        pd.Timestamp('1950-08-12', tz='UTC'),
        pd.Timestamp('1950-08-19', tz='UTC'),
        pd.Timestamp('1950-08-26', tz='UTC'),
        pd.Timestamp('1950-09-02', tz='UTC'),
        pd.Timestamp('1950-09-04', tz='UTC'),
        pd.Timestamp('1950-09-09', tz='UTC'),
        pd.Timestamp('1950-09-16', tz='UTC'),
        pd.Timestamp('1950-09-23', tz='UTC'),
        pd.Timestamp('1950-09-30', tz='UTC'),
        pd.Timestamp('1950-10-12', tz='UTC'),
        pd.Timestamp('1950-11-07', tz='UTC'),
        pd.Timestamp('1950-11-11', tz='UTC'),
        pd.Timestamp('1950-11-23', tz='UTC'),
        pd.Timestamp('1950-12-23', tz='UTC'),
        pd.Timestamp('1950-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)

        
def test_1951():
    start = '1951-01-01'
    end   = '1951-12-31'    
    holidays = [
        pd.Timestamp('1951-01-01', tz='UTC'),
        pd.Timestamp('1951-02-12', tz='UTC'),
        pd.Timestamp('1951-02-22', tz='UTC'),
        pd.Timestamp('1951-03-23', tz='UTC'),
        pd.Timestamp('1951-05-30', tz='UTC'),
        pd.Timestamp('1951-06-02', tz='UTC'),
        pd.Timestamp('1951-06-09', tz='UTC'),
        pd.Timestamp('1951-06-16', tz='UTC'),
        pd.Timestamp('1951-06-23', tz='UTC'),
        pd.Timestamp('1951-06-30', tz='UTC'),
        pd.Timestamp('1951-07-04', tz='UTC'),
        pd.Timestamp('1951-07-07', tz='UTC'),
        pd.Timestamp('1951-07-14', tz='UTC'),
        pd.Timestamp('1951-07-21', tz='UTC'),
        pd.Timestamp('1951-07-28', tz='UTC'),
        pd.Timestamp('1951-08-04', tz='UTC'),
        pd.Timestamp('1951-08-11', tz='UTC'),
        pd.Timestamp('1951-08-18', tz='UTC'),
        pd.Timestamp('1951-08-25', tz='UTC'),
        pd.Timestamp('1951-09-01', tz='UTC'),
        pd.Timestamp('1951-09-03', tz='UTC'),
        pd.Timestamp('1951-09-08', tz='UTC'),
        pd.Timestamp('1951-09-15', tz='UTC'),
        pd.Timestamp('1951-09-22', tz='UTC'),
        pd.Timestamp('1951-09-29', tz='UTC'),
        pd.Timestamp('1951-10-12', tz='UTC'),
        pd.Timestamp('1951-11-06', tz='UTC'),
        pd.Timestamp('1951-11-12', tz='UTC'),
        pd.Timestamp('1951-11-22', tz='UTC'),
        pd.Timestamp('1951-12-25', tz='UTC')
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp('1951-12-24', tz='UTC'), # Christmas Eve
     ]
    _test_has_early_closes(early_closes, start, end)

        
def test_1952():
    start = '1952-01-01'
    end   = '1952-12-31'    
    holidays = [
        pd.Timestamp('1952-01-01', tz='UTC'),
        pd.Timestamp('1952-02-12', tz='UTC'),
        pd.Timestamp('1952-02-22', tz='UTC'),
        pd.Timestamp('1952-04-11', tz='UTC'),
        pd.Timestamp('1952-05-30', tz='UTC'),
        pd.Timestamp('1952-05-31', tz='UTC'),
        pd.Timestamp('1952-06-07', tz='UTC'),
        pd.Timestamp('1952-06-14', tz='UTC'),
        pd.Timestamp('1952-06-21', tz='UTC'),
        pd.Timestamp('1952-06-28', tz='UTC'),
        pd.Timestamp('1952-07-04', tz='UTC'),
        pd.Timestamp('1952-07-05', tz='UTC'),
        pd.Timestamp('1952-07-12', tz='UTC'),
        pd.Timestamp('1952-07-19', tz='UTC'),
        pd.Timestamp('1952-07-26', tz='UTC'),
        pd.Timestamp('1952-08-02', tz='UTC'),
        pd.Timestamp('1952-08-09', tz='UTC'),
        pd.Timestamp('1952-08-16', tz='UTC'),
        pd.Timestamp('1952-08-23', tz='UTC'),
        pd.Timestamp('1952-08-30', tz='UTC'),
        pd.Timestamp('1952-09-01', tz='UTC'),
        pd.Timestamp('1952-09-06', tz='UTC'),
        pd.Timestamp('1952-09-13', tz='UTC'),
        pd.Timestamp('1952-09-20', tz='UTC'),
        pd.Timestamp('1952-09-27', tz='UTC'),
        pd.Timestamp('1952-10-13', tz='UTC'),
        pd.Timestamp('1952-11-04', tz='UTC'),
        pd.Timestamp('1952-11-11', tz='UTC'),
        pd.Timestamp('1952-11-27', tz='UTC'),
        pd.Timestamp('1952-12-25', tz='UTC'),
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens_closes(start, end)
