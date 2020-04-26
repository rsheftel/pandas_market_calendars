import pandas as pd
import pytz
from itertools import chain

from pandas_market_calendars.exchange_calendar_lse import LSEExchangeCalendar


def test_time_zone():
    assert LSEExchangeCalendar().tz == pytz.timezone('Europe/London')


def test_2012_holidays():
    # 2012/06/04 - Bank Holiday
    # 2012/06/05 - Queen's Diamond Jubilee
    lse = LSEExchangeCalendar()
    good_dates = lse.valid_days('2012-01-01', '2012-12-31')
    for date in ["2012-06-04", "2012-06-05"]:
        assert pd.Timestamp(date, tz='UTC') not in good_dates


def test_2016_holidays():
    # 2016/01/01 - New Years Day (observed on first business day on/after)
    # 2016/03/25 - Good Friday
    # 2016/03/28 - Easter Monday
    # 2016/05/02 - Early May Bank Holiday (first Monday in May)
    # 2016/05/30 - Spring Bank Holiday (last Monday in May)
    # 2016/08/29 - Summer Bank Holiday (last Monday in August)
    # 2016/12/27 - Dec. 27th (Christmas is on a weekend)
    # 2016/12/26 - Boxing Day
    lse = LSEExchangeCalendar()
    good_dates = lse.valid_days('2016-01-01', '2016-12-31')
    for date in ["2016-01-01", "2016-03-25", "2016-03-28", '2016-05-02', '2016-05-30',
                 '2016-08-29', '2016-12-27', '2016-12-26']:
        assert pd.Timestamp(date, tz='UTC') not in good_dates


def test_2016_early_closes():
    # Christmas Eve: 2016-12-23
    # New Year's Eve: 2016-12-30

    lse = LSEExchangeCalendar()
    schedule = lse.schedule('2016-01-01', '2017-12-31')
    early_closes = lse.early_closes(schedule).index

    for date in ["2016-12-23", "2016-12-30", '2017-12-22', '2017-12-29']:
        dt = pd.Timestamp(date, tz='UTC')
        assert dt in early_closes

        market_close = schedule.loc[dt].market_close
        assert market_close.tz_convert(lse.tz).hour == 12
        assert market_close.tz_convert(lse.tz).minute == 30


def test_unique_holidays():
    England_unique_hols_names = [
                                "VE_50", "VE_75", 
                                "QEII_Jubilee_25", "QEII_Jubilee_50", "QEII_Jubilee_60",
                                "Royal_Wedding_Anne_1973", "Royal_Wedding_Charles_1981", "Royal_Wedding_William_2011",
                                "3rd_Millenium_Eve",
                            ]
    England_unique_hols = {i: {"closed": None, "open": None} for i in England_unique_hols_names}

    #=====================================================
    # One-off holiday additions and removals in England
    #=====================================================
    
    ## VE-Day Anniversary
    # 50th Anniversary
    England_unique_hols["VE_50"]["closed"] = [pd.Timestamp("1995-05-08")]      
    England_unique_hols["VE_50"]["open"] = [pd.Timestamp("1995-05-01")]     # Early May bank holiday removed
    # 75th Anniversary
    England_unique_hols["VE_75"]["closed"] = [pd.Timestamp("2020-05-08")]      
    England_unique_hols["VE_75"]["open"] = [pd.Timestamp("2020-05-04")]     # Early May bank holiday removed
    
    ## Queen Elizabeth II Jubilees
    # Silver Jubilee
    England_unique_hols["QEII_Jubilee_25"]["closed"] = [pd.Timestamp("1977-06-07")]
    # Golden Jubilee
    England_unique_hols["QEII_Jubilee_50"]["closed"] = [pd.Timestamp("2002-06-03"), pd.Timestamp("2002-06-04")]    
    England_unique_hols["QEII_Jubilee_50"]["open"] = [pd.Timestamp("2002-05-27")]                                   # Spring bank holiday removed
    # Diamond Jubilee
    England_unique_hols["QEII_Jubilee_60" ]["closed"] = [pd.Timestamp("2012-06-04"), pd.Timestamp("2012-06-05")]    # Already added in ecd8ec4
    England_unique_hols["QEII_Jubilee_60" ]["open"] = [pd.Timestamp("2012-05-28")]                                  # Spring bank holiday removed (Not removed as of release 1.2)
    
    ## Royal Weddings
    # Wedding Day of Princess Anne and Mark Phillips
    England_unique_hols["Royal_Wedding_Anne_1973"]["closed"] = [pd.Timestamp("1973-11-14")]      
    # Wedding Day of Prince Charles and Diana Spencer
    England_unique_hols["Royal_Wedding_Charles_1981"]["closed"] = [pd.Timestamp("1981-07-29")]     
    # Wedding Day of Prince William and Catherine Middleton
    England_unique_hols["Royal_Wedding_William_2011"]["closed"] = [pd.Timestamp("2011-04-29")]  
    
    ## Miscellaneous
    # Eve of 3rd Millenium A.D.
    England_unique_hols["3rd_Millenium_Eve"]["closed"] = [pd.Timestamp("1999-12-31")] 
    
    
    #=====================================================
    # Test of closed dates
    #=====================================================

    lse = LSEExchangeCalendar()
    # get all the closed dates
    closed_days = [England_unique_hols[k].get('closed') for k in England_unique_hols]
    good_dates = lse.valid_days('1990-01-01', '2020-12-31')
    for date in chain.from_iterable(closed_days):
        assert pd.Timestamp(date, tz='UTC') not in good_dates
