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

import pandas as pd
from pandas.tseries.holiday import AbstractHolidayCalendar
from pytz import timezone

from pandas_market_calendars.market_calendar import clean_dates, days_at_time, _overwrite_special_dates

from pandas_market_calendars.holidays_us import (
    Pre1952May24SatEarlyClose, Post1952May24Saturdays, Pre1952MaySatClosesAdhoc,
    
    USNewYearsDay, SatBeforeNewYearsAdhoc,
    
    USPresidentsDay, USWashingtonsBirthDay1964to1970, 
    USWashingtonsBirthDayBefore1964, 
    SatBeforeWashingtonsBirthdayAdhoc, SatAfterWashingtonsBirthdayAdhoc, 
    LincolnsBirthDayAdhoc, SatBeforeAfterLincolnsBirthdayAdhoc, GrantsBirthDayAdhoc,  
    
    GoodFriday, GoodFridayPre1898, GoodFriday1899to1905, SatAfterGoodFridayAdhoc,
    
    USMemorialDay, USMemorialDay1964to1969,
    USMemorialDayBefore1964,  SatBeforeDecorationAdhoc, SatAfterDecorationAdhoc,
    DayBeforeDecorationAdhoc,
    
    USIndependenceDay,SatBeforeIndependenceDayAdhoc, SatAfterIndependenceDayAdhoc,
    USIndependenceDayBefore1954, FridayAfterIndependenceDayPre2013, 
    MonTuesThursBeforeIndependenceDay, WednesdayBeforeIndependenceDayPost2013,
    MonBeforeIndependenceDayAdhoc, DaysAfterIndependenceDayAdhoc,
    
    USBlackFridayBefore1993, USBlackFridayInOrAfter1993,
    USColumbusDayBefore1954, USElectionDay1848to1967,
    USElectionDay1968to1980,  USLincolnsBirthDayBefore1954,
    USMartinLutherKingJrAfter1998, 
    USLaborDayStarting1887, SatBeforeLaborDayAdhoc,
    USThanksgivingDay, USThanksgivingDay1939to1941,
    USThanksgivingDayBefore1939, FridayAfterThanksgivingAdHoc, USVeteransDay1934to1953,
    Christmas, ChristmasBefore1954, ChristmasEveBefore1993, ChristmasEveInOrAfter1993, 
    SatBeforeChristmasAdhoc, SatAfterChristmasAdhoc,
    ChristmasEvesAdhoc, DayAfterChristmasAdhoc, ChristmasEveEarlyCloseAdhoc,
    USNationalDaysofMourning,
    ColumbianCelebration1892, WashingtonInaugurationCentennialCelebration1889,
    CharterDay1898, WelcomeNavalCommander1898, AdmiralDeweyCelebration1899,
    KingEdwardVIIcoronation1902, NYSEnewBuildingOpen1903, FuneralOfGroverCleveland1908,
    HudsonFultonCelebration1909, OnsetOfWWI1914, 
    ParadeOfNationalGuardEarlyClose1917, LibertyDayEarlyClose1917, 
    DraftRegistrationDay1917, DraftRegistrationDay1918,
    LibertyDayEarlyClose1918,
    FalseArmisticeReportEarlyClose1918, ArmisticeSigned1918,
    RooseveltFuneralEarlyClose1919, Homecoming27Division1919, ParadeOf77thDivision1919,
    BacklogRelief1919, GeneralPershingReturn1919,
    TrafficBlockLateOpen1919, TrafficBlockLateOpen1920,
    OfficeLocationChange1920, WallStreetExplosionEarlyClose1920,
    WoodrowWilsonFuneralEarlyClose1924, 
    AunnciatorBoardFireLateOpen1921,
    EclipseOfSunLateOpen1925, CromwellFuneralEarlyClose1925,
    LindberghParade1927, BacklogRelief1928, BacklogReliefEarlyClose1928,
    BacklogRelief1929, BacklogReliefEarlyClose1929, BacklogReliefLateOpen1929,
    TaftFuneralEarlyClose1930,
    BankHolidays1933, 
    HeavyVolume1933, HeavyVolume12pmLateOpen1933, HeavyVolume11amLateOpen1933, 
    HeavyVolume2pmEarlyClose1933, GasFumesOnTradingFloorEarlyClose1933,
    NRAdemonstrationEarlyClose1933,Snow11amLateOpen1934,
    SatClosings1945, VJday1945, NavyDay1945,
    RailroadStrike1946, SatClosings1946,
    SatClosings1947, SatClosings1948, SevereWeather1948,
    SatClosings1949, SatClosings1950, SatClosings1951, SatClosings1952,
    
    USVetransDayAdHoc, SatAfterColumbusDayAdHoc,
     
    FirstLunarLandingClosing,
    
    PaperworkCrisis68, September11Closings,
    WeatherSnowClosing, WeatherHeatClosing, WeatherNoHeatClosing,
    GreatBlizzardOf1888, HurricaneGloriaClosings,
    HurricaneSandyClosings, NewYorkCityBlackout77 )
from .market_calendar import MarketCalendar

# Useful resources for making changes to this file:
# http://www.nyse.com/pdfs/closings.pdf
# http://www.stevemorse.org/jcal/whendid.html

# Overwrite the default holiday calendar start_date of 1/1/70 
AbstractHolidayCalendar.start_date = '1885-01-01'


class NYSEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for NYSE

    Open Time: 9:30 AM, US/Eastern
    Close Time: 4:00 PM, US/Eastern
    
    From 1887 to 5/24/1952 the Market was open most Saturdays 10am-noon
    - https://www.marketwatch.com/story/a-brief-history-of-trading-hours-on-wall-street-2015-05-29
    - http://www.ltadvisors.net/Info/research/closings.pdf

    Regularly-Observed Holidays:
    - New Years Day (observed on monday when Jan 1 is a Sunday)
    - Martin Luther King Jr. Day (3rd Monday in January, only after 1998)
    - Lincoln's Birthday (February 12th, only before 1954 starting in 1896)
    - Washington's Birthday (February 22nd, before 1971 with rule change in
      1964)
    - Washington's Birthday (aka President's Day, 3rd Monday in February,
      after 1970)
    - Good Friday (two days before Easter Sunday)
    - Memorial Day (May 30th, before 1970, with rule change in 1964)
    - Memorial Day (last Monday in May, after 1970)
    - Independence Day (July 4th Sunday to Monday, before 1954)
    - Independence Day (observed on the nearest weekday to July 4th, after
      1953)
    - Election Day (First Tuesday starting on November 2nd, between 1848 and
      1967)
    - Election Day (Every four years, first Tuesday starting on November 2nd,
      between 1968 and 1980)
    - Veterans Day (November 11th, between 1934 and 1953)
    - Columbus Day (October 12th, before 1954)
    - Labor Day (first Monday in September)
    - Thanksgiving (last Thursday in November, before 1939)
    - Thanksgiving (second to last Thursday in November, between 1939 and 1941)
    - Thanksgiving (fourth Thursday in November, after 1941)
    - Christmas (December 25th, Sunday to Monday, before 1954)
    - Christmas (observed on nearest weekday to December 25, after 1953)

    NOTE: The NYSE does not observe the following US Federal Holidays:
    - Columbus Day (after 1953)
    - Veterans Day (after 1953)

    Regularly-Observed Early Closes:
    - July 3rd (Mondays, Tuesdays, and Thursdays, 1995 onward)
    - July 5th (Fridays, 1995 onward, except 2013)
    - Christmas Eve (except on Fridays, when the exchange is closed entirely)
    - Day After Thanksgiving (aka Black Friday, observed from 1992 onward)

    NOTE: Until 1993, the standard early close time for the NYSE was 2:00 PM.
    From 1993 onward, it has been 1:00 PM.

    Additional Irregularities:
    - Closed on 11/1/1929 and 11/29/1929 for backlog relief.
    - Closed between 3/6/1933 and 3/14/1933 due to bank holiday.
    - Closed on 8/15/1945 and 8/16/1945 following victory over Japan.
    - Closed on Christmas Eve in 1945 and 1946.
    - Closed on December 26th in 1958.
    - Closed the day before Memorial Day in 1961.
    - Closed on 11/25/1963 due to John F. Kennedy's death.
    - Closed for Lincoln's Birthday in 1968.
    - Closed a number of days between June 12th and  December 24th in 1968
      due to paperwork crisis.
    - Closed on 4/9/1968 due to Martin Luther King's death.
    - Closed the day after Independence Day in 1968.
    - Closed on 2/10/1969 due to weather (snow).
    - Closed on 3/31/1969 due to Dwight D. Eisenhower's death.
    - Closed on 7/21/1969 following the first lunar landing.
    - Closed on 12/28/1972 due to Harry S. Truman's death.
    - Closed on 1/25/1973 due to Lyndon B. Johnson's death.
    - Closed on 7/14/1977 due to New York City blackout.
    - Closed on 9/27/1985 due to Hurricane Gloria.
    - Closed on 4/27/1994 due to Richard Nixon's death.
    - Closed from 9/11/2001 to 9/16/2001 due to terrorist attacks in NYC.
    - Closed on 6/11/2004 due to Ronald Reagan's death.
    - Closed on 1/2/2007 due to Gerald Ford's death.
    - Closed on 10/29/2012 and 10/30/2012 due to Hurricane Sandy.
    - Closed on 12/5/2018 due to George H.W. Bush's death.
    - Closed at 1:00 PM on Wednesday, July 3rd, 2013
    - Closed at 1:00 PM on Friday, December 31, 1999
    - Closed at 1:00 PM on Friday, December 26, 1997
    - Closed at 1:00 PM on Friday, December 26, 2003

    NOTE: The exchange was **not** closed early on Friday December 26, 2008,
    nor was it closed on Friday December 26, 2014. The next Thursday Christmas
    will be in 2025.  If someone is still maintaining this code in 2025, then
    we've done alright...and we should check if it's a half day.
    """
    aliases = ['NYSE', 'stock', 'NASDAQ', 'BATS']
    regular_early_close = time(13)
    regular_late_open = time(10)

    @property
    def name(self):
        return "NYSE"
    
    @property
    def weekmask(self):
        return "Mon Tue Wed Thu Fri Sat"    #Market open on Saturdays thru 5/24/1952

    @property
    def tz(self):
        return timezone('America/New_York')

    @property
    def open_time_default(self):
        return time(9, 30, tzinfo=self.tz)

    @property
    def close_time_default(self):
        return time(16, tzinfo=self.tz)

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            USMartinLutherKingJrAfter1998,
            USPresidentsDay,
            USWashingtonsBirthDayBefore1964,
            USWashingtonsBirthDay1964to1970,
            USLincolnsBirthDayBefore1954,
            GoodFriday,
            GoodFridayPre1898,
            GoodFriday1899to1905, 
            USMemorialDay,
            USMemorialDayBefore1964,
            USMemorialDay1964to1969,
            USIndependenceDayBefore1954,
            USIndependenceDay,
            USLaborDayStarting1887,
            USThanksgivingDayBefore1939,
            USThanksgivingDay1939to1941,
            USThanksgivingDay,
            USElectionDay1848to1967,
            USElectionDay1968to1980,
            USVeteransDay1934to1953,
            USColumbusDayBefore1954,
            Christmas,
            ChristmasBefore1954,
        ])

    @property
    def adhoc_holidays(self):
        return list(chain(
            #Post1952May24Saturdays,
            Pre1952MaySatClosesAdhoc,
            SatBeforeNewYearsAdhoc,
            SatBeforeWashingtonsBirthdayAdhoc,
            SatAfterWashingtonsBirthdayAdhoc,
            SatBeforeAfterLincolnsBirthdayAdhoc,
            SatBeforeDecorationAdhoc,
            SatAfterDecorationAdhoc,
            DayBeforeDecorationAdhoc,
            SatAfterGoodFridayAdhoc,
            MonBeforeIndependenceDayAdhoc,
            SatBeforeIndependenceDayAdhoc,
            SatAfterIndependenceDayAdhoc,
            DaysAfterIndependenceDayAdhoc,
            SatBeforeLaborDayAdhoc,
            FridayAfterThanksgivingAdHoc,
            SatBeforeChristmasAdhoc,
            SatAfterChristmasAdhoc,
            ChristmasEvesAdhoc,
            DayAfterChristmasAdhoc,
           
            USNationalDaysofMourning,
            ColumbianCelebration1892,
            GreatBlizzardOf1888,
            WashingtonInaugurationCentennialCelebration1889,
            CharterDay1898,
            WelcomeNavalCommander1898,
            AdmiralDeweyCelebration1899,
            KingEdwardVIIcoronation1902,
            NYSEnewBuildingOpen1903,
            HudsonFultonCelebration1909,
            OnsetOfWWI1914,
            DraftRegistrationDay1917,
            DraftRegistrationDay1918,
            ArmisticeSigned1918,
            Homecoming27Division1919,
            ParadeOf77thDivision1919,
            BacklogRelief1919,
            GeneralPershingReturn1919,
            OfficeLocationChange1920,
            LindberghParade1927,
            BacklogRelief1928,
            BacklogRelief1929,
            BankHolidays1933,
            HeavyVolume1933,
            SatClosings1945,
            VJday1945,
            NavyDay1945,
            RailroadStrike1946,
            SatClosings1946,
            SatClosings1947,
            SatClosings1948,
            SevereWeather1948,
            SatClosings1949,
            SatClosings1950,
            SatClosings1951,
            SatClosings1952,
            
            USVetransDayAdHoc,
            SatAfterColumbusDayAdHoc,            
            LincolnsBirthDayAdhoc,
            GrantsBirthDayAdhoc,
            PaperworkCrisis68,
            WeatherSnowClosing,
            WeatherHeatClosing,
            WeatherNoHeatClosing,
            FirstLunarLandingClosing,
            September11Closings,
            NewYorkCityBlackout77,
            HurricaneGloriaClosings,
            HurricaneSandyClosings,
            
                        
        ))


    @property
    def special_closes(self):
        return [
            (self.regular_early_close, 
             AbstractHolidayCalendar(rules=[
                MonTuesThursBeforeIndependenceDay,
                FridayAfterIndependenceDayPre2013,
                WednesdayBeforeIndependenceDayPost2013,
                USBlackFridayInOrAfter1993,
                ChristmasEveInOrAfter1993,
            ])),
             (time(12), AbstractHolidayCalendar(rules=[
                ParadeOfNationalGuardEarlyClose1917,
                LibertyDayEarlyClose1917,
                LibertyDayEarlyClose1918,
                WallStreetExplosionEarlyClose1920,
                NRAdemonstrationEarlyClose1933,
            ])),
            (time(hour=12, minute=30), AbstractHolidayCalendar(rules=[
                RooseveltFuneralEarlyClose1919,
                WoodrowWilsonFuneralEarlyClose1924,
                TaftFuneralEarlyClose1930,
                GasFumesOnTradingFloorEarlyClose1933,
            ])),
            (time(13), AbstractHolidayCalendar(rules=[
                FuneralOfGroverCleveland1908,
            ])),
            (time(14), AbstractHolidayCalendar(rules=[
                ChristmasEveBefore1993,
                USBlackFridayBefore1993,
            ])),
            (time(hour=14, minute=30), AbstractHolidayCalendar(rules=[
                FalseArmisticeReportEarlyClose1918,
                CromwellFuneralEarlyClose1925,
            ])),
 
        ]
#
    @property
    def special_closes_adhoc(self):
        return [
            (self.regular_early_close, [
                '1997-12-26',
                '1999-12-31',
                '2003-12-26',
                '2013-07-03'
            ]),
            (time(12), Pre1952May24SatEarlyClose.strftime("%Y-%m-%d").tolist()
             ),
            (time(14), [t.strftime("%Y-%m-%d") for t in ChristmasEveEarlyCloseAdhoc]
             + BacklogReliefEarlyClose1928.strftime("%Y-%m-%d").tolist()
             + [t.strftime("%Y-%m-%d") for t in BacklogReliefEarlyClose1929]
             + [t.strftime("%Y-%m-%d") for t in HeavyVolume2pmEarlyClose1933]
            ),
        ]

            
    @property
    def special_opens(self):
        return [
            (time(hour=10, minute=30), AbstractHolidayCalendar(rules=[
                TrafficBlockLateOpen1919,
                TrafficBlockLateOpen1920,
            ])),
            (time(hour=10, minute=45), AbstractHolidayCalendar(rules=[
                EclipseOfSunLateOpen1925,
            ])),
            (time(11), AbstractHolidayCalendar(rules=[
                Snow11amLateOpen1934,
            ])),
            (time(13), AbstractHolidayCalendar(rules=[
                AunnciatorBoardFireLateOpen1921,
            ])),
            ]

#
    @property
    def special_opens_adhoc(self):
        return [                       
            (time(11), [t.strftime("%Y-%m-%d") for t in HeavyVolume11amLateOpen1933]                     
            ),     
            (time(12), [t.strftime("%Y-%m-%d") for t in BacklogReliefLateOpen1929]
                     + [t.strftime("%Y-%m-%d") for t in HeavyVolume12pmLateOpen1933]
            ),            
        ]
 
    # Override market_calendar.py
    def valid_days(self, start_date, end_date, tz='UTC'):
        """
        Get a DatetimeIndex of valid open business days.

        :param start_date: start date
        :param end_date: end date
        :param tz: time zone in either string or pytz.timezone
        :return: DatetimeIndex of valid business days
        """
        # Remove saturday as trading day after Sept 27, 1952
        trading_days = pd.date_range(start_date, end_date, freq=self.holidays(), normalize=True, tz=tz)
        ts_start_date = pd.Timestamp(start_date, tz='UTC')
        ts_end_date = pd.Timestamp(end_date, tz='UTC')
        if ts_end_date <= pd.Timestamp('1952-09-27', tz='UTC'):
            return trading_days
        elif (ts_start_date <= pd.Timestamp('1952-09-27', tz='UTC') and
              ts_end_date   >  pd.Timestamp('1952-09-27', tz='UTC')):
            saturdays = pd.date_range('1952-09-28', end_date, freq='W-SAT', tz='UTC')            
        else:
            saturdays = pd.date_range(start_date, end_date, freq='W-SAT', tz='UTC')
        
        drop_days = []
        for s in saturdays:
            if s in trading_days:
                drop_days.append(s)
        #return trading_days
        return trading_days.drop(drop_days)
    
    
    # Override parent method so that derived valid_days is called            
    def schedule(self, start_date, end_date, tz='UTC'):
        """
        Generates the schedule DataFrame. The resulting DataFrame will have all the valid business days as the index
        and columns for the market opening datetime (market_open) and closing datetime (market_close). All time zones
        are set to UTC by default. Setting the tz parameter will convert the columns to the desired timezone,
        such as 'America/New_York'

        :param start_date: start date
        :param end_date: end date
        :param tz: timezone
        :return: schedule DataFrame
        """
        start_date, end_date = clean_dates(start_date, end_date)
        if not (start_date <= end_date):
            raise ValueError('start_date must be before or equal to end_date.')

        # Setup all valid trading days
        _all_days = self.valid_days(start_date, end_date)
        
        # If no valid days return an empty DataFrame
        if len(_all_days) == 0:
            return pd.DataFrame(columns=['market_open', 'market_close'], index=pd.DatetimeIndex([], freq='C'))

        # `DatetimeIndex`s of standard opens/closes for each day.
        opens =  days_at_time(_all_days, self.open_time, self.tz, self.open_offset).tz_convert(tz)
        closes = days_at_time(_all_days, self.close_time, self.tz, self.close_offset).tz_convert(tz)

        # `DatetimeIndex`s of nonstandard opens/closes
        _special_opens = self._calculate_special_opens(start_date, end_date)
        _special_closes = self._calculate_special_closes(start_date, end_date)

        # Overwrite the special opens and closes on top of the standard ones.
        _overwrite_special_dates(_all_days, opens, _special_opens)
        _overwrite_special_dates(_all_days, closes, _special_closes)

        result = pd.DataFrame(index=_all_days.tz_localize(None), columns=['market_open', 'market_close'],
                            data={'market_open': opens, 'market_close': closes})

        if self.break_start:
            result['break_start'] = days_at_time(_all_days, self.break_start, self.tz).tz_convert(tz)
            temp = result[['market_open', 'break_start']].max(axis=1)
            result['break_start'] = temp
            result['break_end'] = days_at_time(_all_days, self.break_end, self.tz).tz_convert(tz)
            temp = result[['market_close', 'break_end']].min(axis=1)
            result['break_end'] = temp

        return result