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
import datetime as dt
from pytz import timezone

import pandas_market_calendars.market_calendar as mc
from pandas_market_calendars.market_calendar import clean_dates, _overwrite_special_dates

from pandas_market_calendars.holidays_us import (       
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
    ChristmasEvesAdhoc, DayAfterChristmasAdhoc, ChristmasEve1pmEarlyCloseAdhoc,
    USNationalDaysofMourning,
    # 1885    
    UlyssesGrantFuneral1885,
    # 1892
    ColumbianCelebration1892, 
    # 1889
    WashingtonInaugurationCentennialCelebration1889,
    # 1898
    CharterDay1898, WelcomeNavalCommander1898, 
    # 1899
    AdmiralDeweyCelebration1899, GarretHobartFuneral1899,
    # 1901
    McKinleyDeathAndFuneral1901, QueenVictoriaFuneral1901, 
    MovedToProduceExchange1901, EnlargedProduceExchange1901,
    # 1902
    KingEdwardVIIcoronation1902, 
    # 1903
    NYSEnewBuildingOpen1903, 
    # 1908
    GroverClevelandFuneral1pmClose1908,
    # 1909
    HudsonFultonCelebration1909, 
    # 1910
    KingEdwardDeath11amyClose1910, KingEdwardFuneral12pmOpen1910,
    # 1912
    JamesShermanFuneral1912,
    # 1913
    JPMorganFuneral12pmOpen1913, WilliamGaynorFuneral12pmOpen1913,
    # 1914
    OnsetOfWWI1914, 
    # 1917
    WeatherHeatClosing1917, ParadeOfNationalGuardEarlyClose1917,
     LibertyDay12pmEarlyClose1917,  DraftRegistrationDay1917, 
    # 1918
    WeatherNoHeatClosing1918, DraftRegistrationDay1918, 
    LibertyDay12pmEarlyClose1918, FalseArmisticeReport1430EarlyClose1918, 
    ArmisticeSigned1918,
    # 1919
    RooseveltFuneral1230EarlyClose1919, Homecoming27Division1919, 
    ParadeOf77thDivision1919,  BacklogRelief1919, GeneralPershingReturn1919,
    TrafficBlockLateOpen1919, 
    # 1920
    TrafficBlockLateOpen1920, OfficeLocationChange1920, 
    WallStreetExplosionEarlyClose1920,
    # 1921
    AnnunciatorBoardFire1pmLateOpen1921,
    # 1923
    HardingDeath1923, HardingFuneral1923,
    # 1924
    WoodrowWilsonFuneral1230EarlyClose1924, 
    # 1925
    EclipseOfSunLateOpen1925, CromwellFuneral1430EarlyClose1925,
    # 1927
    LindberghParade1927,
    # 1928
    BacklogRelief1928, BacklogRelief2pmEarlyClose1928,
    # 1929
    BacklogRelief1929, BacklogRelief1pmEarlyClose1929, BacklogRelief12pmLateOpen1929,
    # 1930
    TaftFuneral1230EarlyClose1930,
    # 1933
    BankHolidays1933, GasFumesOnTradingFloor1230EarlyClose1933,
    HeavyVolume1933, HeavyVolume12pmLateOpen1933, HeavyVolume11amLateOpen1933, 
    HeavyVolume2pmEarlyClose1933, NRAdemonstration12pmEarlyClose1933,
    # 1924
    Snow11amLateOpen1934,
    # 1936
    KingGeorgeVFuneral11amLateOpen1936,
    # 1944
    SatClosings1944,
    # 1945
    SatClosings1945, VJday1945, NavyDay1945,
    # 1946
    RailroadStrike1946, SatClosings1946,
    # 1947
    SatClosings1947, 
    # 1948
    SatClosings1948, SevereWeather1948,
    # 1949
    SatClosings1949, 
    # 1950
    SatClosings1950, 
    # 1951
    SatClosings1951, 
    # 1952
    SatClosings1952,
    
    USVetransDayAdHoc, SatAfterColumbusDayAdHoc,
     
    FirstLunarLandingClosing,
    
    PaperworkCrisis68, September11Closings,
    WeatherSnowClosing,  
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
    Exchange calendar for NYSE from 1885-01-01
        - Note: DJIA was first recorded 1885-02-16

    - https://web.archive.org/web/20141224054812/http://www.nyse.com/about/history/timeline_trading.html
    - https://www.marketwatch.com/story/a-brief-history-of-trading-hours-on-wall-street-2015-05-29
    - http://www.ltadvisors.net/Info/research/closings.pdf
    - https://github.com/rsheftel/pandas_market_calendars/files/6827110/Stocks.NYSE-Closings.pdf 
    
    - 1792: 5 securities traded
    - 1871: Continuous trading begins
    - 1885 to 1887: trading hours Mon-Sat 10am to variable 2pm thru 4pm (coded as 3pm)
    - 1887: trading hours Mon-Fri 10am-3pm Sat 10am-noon
    - 1952-09-29: trading hours Mon-Fri 10am-3:30pm, 
        - Sat trading removed after Sept 27
        - Last effective Saturday traded was May 24, 1952
    - 1974: trading hours Mon-Fri 10am-4pm
    - 1985: trading hours Mon-Fri 9:30am-4pm

    #######################################
    Regularly-Observed Holidays as of 2021:
    #######################################    
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

    ################################
    Regularly-Observed Early Closes:
    ################################
    - July 3rd (Mondays, Tuesdays, and Thursdays, 1995 onward)
    - July 5th (Fridays, 1995 onward, except 2013)
    - Christmas Eve (except on Fridays, when the exchange is closed entirely)
    - Day After Thanksgiving (aka Black Friday, observed from 1992 onward)

    NOTE: Until 1993, the standard early close time for the NYSE was 2:00 PM.
    From 1993 onward, it has been 1:00 PM.

    ####################################
    Retired Regularly-Observed Holidays:
    ####################################
    - Columbus Day (after 1953)
    - Armistice/Veterans Day (after 1953)

    #################################
    Irregularities Openings/Closings:
    #################################
    - Closed on Aug 8, 1885 (Sat): President Ulysses S. Grant funeral
    - Closed on Jul 2, 1887 (Sat): Saturday before Independence Day
    - Closed on Dec 24, 1887 (Sat): Christmas Eve
    - Closed on Mar 12-13, 1888 (Mon-Tue): Blizzard of 1888
    - Closed on Sep 1, 1888 (Sat): Saturday before Labor Day
    - Closed on Nov 30, 1888 (Fri): Friday after Thanksgiving
    - Closed on Apr 29 - May 1, 1889 (Mon-Wed): Centennial celbration of Washington's inauguration
    - Closed on Jul 5, 1890 (Sat): Saturday after Independence Day
    - Closed on Dec 26, 1891 (Sat): Saturday after Christmas
    - Closed on Jul 2, 1892 (Sat): Saturday before Independence Day
    - Closed on Oct 12, 1892 (Wed) Columbian Celebration (Columbus discovery of America)
    - Closed on Oct 21-22, 1892 (Fri-Sat): Columbian Celebration
    - Closed on Apr 27, 1893 (Thu): Columbian Celebration
    - Closed on Dec 26, 1896 (Sat): Saturday after Christmas
    - Closed on Apr 27, 1897 (Tue): Grant's birthday
    - Closed on May 4, 1898 (Wed): NYC Charter Day 
    - Closed on Jul 2, 1898 (Sat): Saturday before Independence Day
    - Closed on Aug 20, 1898 (Sat): Welcome of naval commanders
    - Closed on Sep 3, 1898 (Sat): Saturday before Labor Day
    - Closed on Dec 24, 1898 (Sat): Saturday before Christmas
    - Closed on Feb 11, 1899 (Sat): Saturday before Lincoln's birthday
    - Closed on May 29, 1899 (Mon): Monday before Decoration Day
    - Closed on Jul 3, 1899 (Mon): Monday before Independence Day
    - Closed on Sep 29-30, 1899 (Fri-Sat): Admiral Dewey Celebration
    - Closed on Nov 25, 1899 (Sat): Funeral of Vice-President Garret A. Hobart
    - Closed on Apr 14, 1900 (Sat): Saturday after Good Friday
    - Closed on Sep 1, 1900 (Sat): Saturday before Labor Day
    - Closed on Dec 24, 1900 (Mon): Christmas Eve
    - Closed on Feb 2, 1901 (Sat): Funderal of Queen Victoria of England
    - Closed on Feb 23, 1901 (Sat): Saturday after Washington's birthday
    - Closed on Apr 6, 1901 (Sat): Saturday after Good Friday
    - Closed on Apr 27, 1901 (Sat): Moved to temporary quarters in Produce Exchange
    - Closed on May 11, 1901 (Sat): Enlarged temporary quarters in Produce Exchange
    - Closed on Jul 5-6, 1901  (Fri-Sat): Days after Independence Day
    - Closed on Aug 31, 1901 (Sat): Saturday before Labor Day
    - Closed on Sep 14, 1901 (Sat): Death of President William McKinley
    - Closed on Sep 19, 1901 (Thu): Funeral of President William McKinley
    - Closed on Mar 29, 1902 (Sat): Saturday after Good Friday
    - Closed on May 31, 1902 (Sat): Saturday after Decoration Day
    - Closed on Jul 5, 1902 (Sat): Saturday after Independence Day
    - Closed on Aug 9, 1902 (Sat): Coronation of King Edward VII of England
    - Closed on Aug 30, 1902 (Sat): Saturday before Labor Day
    - Closed on Feb 21, 1903 (Sat): Saturday before Washington's birthday
    - Closed on Apr 11, 1903 (Sat): Saturday after Good Friday
    - Closed on Apr 22, 1903 (Wed): Opening of the new NYSE building
    - Closed on Sep 5, 1903 (Sat): Saturday before Labor Day
    - Closed on Dec 26, 1903 (Sat): Saturday after Christmas
    - Closed on May 28, 1904 (Sat): Saturday before Decoration Day
    - Closed on Jul 2, 1904 (Sat): Saturday before Independence Day
    - Closed on Sep 3, 1904 (Sat): Saturday before Labor Day
    - Closed on Dec 24, 1904 (Sat): Saturday before Christmas
    - Closed on Apr 22, 1905 (Sat): Saturday after Good Friday
    - Closed on Feb 23, 1907 (Sat): Saturday after Washington's birthday
    - Closed on Mar 30, 1907 (Sat): Saturday after Good Friday
    - Closed on Aug 31, 1907 (Sat): Saturday before Labor Day
    - Closed on Apr 18, 1908 (Sat): Saturday after Good Friday
    - Early Close 1pm on Jun 25, 1908 (Fri): Former President Grover Cleveland funeral
    - Closed on Sep 5, 1908 (Sat): Saturday before Labor Day
    - Closed on Dec 26, 1908 (Sat): Saturday after Christmas
    - Closed on Feb 13, 1909 (Sat): Saturday after Lincoln's birthday
    - Closed on Apr 10, 1909 (Sat): Saturday after Good Friday
    - Closed on May 29, 1909 (Sat): Saturday before Decoration Day
    - Closed on Jul 3, 1909 (Sat): Saturday before Independence Day
    - Closed on Sep 4, 1909 (Sat) Saturday before Labor Day
    - Closed on Sep 25, 1909 (Sat): Reception Day of the Hudson-Fulton Celebration
    - Closed on Mar 26, 1910 (Sat): Saturday after Good Friday
    - Early Close 11am on May 7, 1910 (Sat): King Edward VII of England Death
    - Late Open 12pm on May 20, 1910 (Fri): King Edward VII of England Funeral 
    - Closed on May 28, 1910 (Sat): Saturday before Decoration Day
    - Closed on Jul 2, 1910 (Sat): Saturday before Independence Day
    - Closed on Sep 3, 1910 (Sat): Saturday before Labor Day
    - Closed on Dec 24, 1910 (Sat): Saturday before Christmas
    - Closed on  Apr 15, 1911 (Sat): Saturday after Good Friday
    - Closed on Sep 2, 1911 (Sat): Saturday before Labor Day
    - Closed on Dec 23, 1911 (Sat): Saturday before Christmas
    - Closed on Aug 31, 1912 (Sat): Saturday before Labor Day
    - Closed on Nov 2, 1912 (Sat): Vice-President James S. Sherman funeral
    - Closed on Mar 22, 1913 (Sat): Saturday after Good Friday
    - Late Open 12pm on Apr 14, 1913 (Mon): JP Morgan funeral
    - Closed on May 31, 1913 (Sat): Saturday after Decoration Day
    - Closed on Jul 5, 1913 (Sat): Saturday after Independence Day
    - Closed on Aug 30, 1913 (Sat): Saturday before Labor Day
    - Late Open 12pm on Sep 22, 1913 (Mon): Mayor William J. Gaynor funeral
    - Closed on Jul 31-Dec 11, 1914: Pending outbreak of World War I. 
        - Bonds reopn Nov 28, 1914 for limited trading with restrictions
        - Stocks (limited in number) reopen Dec 12, 1914 with restrictions
        - Stocks (all stocks) reopen Dec 14, 1914 with restrictions
        - Restrictions removed on Apr 1, 1915
    - Closed on Dec 30, 1916 (Sat): Saturday before New Year's Day
    - Closed on Jun 5, 1917 (Tue): Draft Registraion Day
    - Closed on Aug 4, 1917 (Sat): Heat
    - Early Close 12pm on Aug 29, 1917 (Wed): Parade of National Guard
    - Closed on Sep 1, 1917 (Sat): Saturday before Labor Day
    - Closed on Oct 13, 1917 (Sat): Saturday after Columbus Day
    - Early Close 12pm on Oct 24, 1917 (Wed): Liberty Day
    - Closed on Jan 28, 1918 (Mon): Heatless day
    - Closed on Feb 4, 1918 (Mon): Heatless day
    - Closed on Feb 11, 1918 (Mon): Heatless day
    - Early Close 12pm on Apr 26, 1918 (Fri): Liberty Day
    - NOT IMPLEMENTED: Break from 11am to 12pm on Jul 11, 1918 (Thu): Former Mayor John Purroy Mitchell funeral
    - Closed on Sep 12, 1918 (Thu): Draft registration day
    - Early Close 2:30pm on Nov 7, 1918 (Thu): False armistice report
    - Closed on Nov 11, 1918 (Mon): Armistice signed
    - Early Close 12:30pm on Jan 7, 1919 (Tue): Former President Theodore Roosevelt funeral
    - Closed on Mar 25, 1919 (Tue): Homecoming of 27th Division
    - Closed on May 6, 1919 (Tue): Parade of 77th Division
    - Closed on May 31, 1919 (Sat): Saturday after Decoratin Day
    - Closed on Jul 5, 1919 (Sat): Saturday after Independence Day
    - Closed on Jul 19, 1919 (Sat): Heat and backlog catch up
    - Closed on Aug 2, 1919 (Sat): Backlog catch up
    - Closed on Aug 16, 1919 (Sat): Backlog catch up
    - Closed on Aug 30, 1919 (Sat): Saturday before Labor Day
    - Closed on Sep 10, 1919 (Wed): Return of General John J. Pershing
    - Late Open 10:30am on Dec 30, 1919 (Tue): Traffic block
    - Late Open 10:30am on Feb 6, 1920 (Fri): Traffic block
    - Closed on Apr 3, 1920 (Sat): Saturday after Good Friday
    - Closed on May 1, 1920 (Sat): Many firms changed office locations
    - Closed on Jul 3, 1920 (Sat): Saturday before Independence Day
    - Closed on Sep 4, 1920 (Sat): Saturday before Labor Day
    - Early Close 12pm on Sep 16, 1920 (Thu): Wall Street explosion
    - Closed on May 28, 1921 (Sat): Saturday before Decoration Day
    - Closed on Jul 2, 1921 (Sat): Saturday before Independence Day
    - Late Open 1pm on Aug 2, 1921 (Tue): Fire in annunciator board
    - Closed on Sep 3, 1921 (Sat): Saturday before Labor Day
    - Closed on Dec 23, 1922 (Sat): Saturday before Christmas
    - Closed on Aug 3, 1923 (Fri): President Warren G. Harding death
    - NOT IMPLEMENTED: Break 11am to 12:30pm on Aug 8, 1923 (Wed): President Warren G. Harding funeral
    - Closed on Aug 10, 1923 (Fri): President Warren G. Harding funeral
    - Early Close 12:30pm on Feb 6, 1924 (Wed): Former President Woodrow Wilson funderal
    - Closed on May 31, 1924 (Sat): Saturday after Decoration Day
    - Late Open 10:45am on Jan 24, 1925 (Sat): Eclipse of sun
    - Early Close 2:30pm on Sep 18, 1925 (Fri): Seymour L. Cromwell funeral (former NYSE president)
    - Closed on Dec 26, 1925 (Sat): Saturday after Christmas
    - Closed on May 29, 1926 (Sat): Saturday before Decoration Day
    - Closed on Jul 3, 1926 (Sat): Saturday before Independence Day
    - Closed on Sep 4, 1926 (Sat): Saturday before Labor Day
    - Closed on Jun 13, 1927 (Mon): Colonel Charles A. Lindberg parade
    - Closed on Apr 7, 1928 (Sat): Backlog catch up
    - Closed on Apr 21, 1928 (Sat): Backlog catch up
    - Closed on May 5, 1928 (Sat): Backlog catch up
    - Closed on May 12, 1928 (Sat): Backlog catch up
    - Closed on May 19, 1928 (Sat): Backlog catch up
    - Early Closes May 21-25, 1928 (Mon-Fri): Backlog catch up
    - Closed on May 26, 1928 (Sat): Backlog catch up
    - Closed on Nov 24, 1928 (Sat): Backlog catch up
    - Closed on Feb 9, 1929 (Sat): Backlog catch up
    - Closed on Feb 23, 1929 (Sat): Saturday after Washington's birthday
    - Closed on Mar 30, 1929 (Sat): Saturday after Good Friday
    - Closed on Aug 31, 1929 (Sat): Saturday before Labor Day
    - Late Open 12pm on Oct 31, 1929 (Thu): Backlog catch up and relieve personnel
    - Closed on Nov 1-2, 1929 (Fri-Sat): Backlog catch up and relieve personnel
    - Early Closes 1pm on Nov 6-8, 1929 (Wed-Fri): Backlog catch up and relieve personnel
    - Closed on Nov 9, 1929 (Sat): Backlog catch up and relieve personnel
    - Early Closes 1pm on Nov 11-15, 1929 (Mon-Fri): Backlog catch up and relieve personnel
    - Closed on Nov 16, 1929 (Sat): Backlog catch up and relieve personnel
    - Closed on Nov 18-22, 1929 (Mon-Fri): Backlog catch up and relieve personnel
    - Closed on Nov 23, 1929 (Sat): Backlog catch up and relieve personnel
    - Closed on Nov 29-30, 1929 (Fri-Sat): Backlog catch up and relieve personnel
    - Early Close 12:30pm on Mar 11, 1930 (Tue): Former President William Howard Taft funeral
    - Closed on Apr 19, 1930 (Sat): Saturday after Good Friday
    - Closed on May 31, 1930 (Sat): Saturday after Decoration Dday
    - Closed on Jul 5, 1930 (Sat): Saturday after Independence Day
    - Closed on Aug 30, 1930 (Sat): Saturday before Labor Day
    - Closed on Sep 5, 1931 (Sat): Saturday before Labor Day
    - Closed on Dec 26, 1931 (Sat): Saturday after Christmas
    - Closed on Jul 2, 1932 (Sat): Saturday before Independence Day
    - Closed on Jan 7, 1933 (Sat): Former President Calvin Coolidge funeral
    - Closed on Mar 4, 1933 (Sat): State banking holiday
    - Closed on Mar 6-14, 1933 (Mon-Tue): National banking holiday
    - Late Open 12pm on Jul 24-25, 1933 (Mon-Tue): Volume activity
    - Late Opens AND Early Closes on Jul 26-28, 1933 (Wed-Fri): Volume activity
    - Closed on July 29, 1933 (Sat): Volume activity
    - Early Close 12:30pm on Aug 4, 1933 (Fri): Gas fumes on trading floor
    - Closed on Aug 5, 1933 (Sat): Volume activity
    - Closed on Aug 12, 1933 (Sat): Volume activity
    - Closed on Aug 19, 1933 (Sat): Volume activity
    - Closed on Aug 26, 1933 (Sat): Volume activity
    - Closed on Sep 2, 1933 (Sat): Volume activity
    - Early Close 12pm on Sep 13, 1933 (Wed): NRA demonstration
    - Late Open 11am on Feb 20, 1934 (Tue): severe snowstorm
    - Late Open 11am on Jan 28, 1936 (Tue): King George V of England funeral
    - Closed on Dec 26, 1936 (Sat): Saturday after Christmas
    - Closed on May 29, 1937 (Sat): Saturday before Decoration Day
    - Closed on Jul 3, 1937 (Sat): Saturday before Independence Day
    - NOT IMPLEMENTED Break from 12-13:00 on May 18, 1942 (Mon): NYSE 150th anniversary
    - NOT IMPLEMENTED Break from 14:32-14:58 on Oct 22, 1942 (Thu): Civil Defense drill
    - NOT IMPLEMENTED Break from 14:38-14:59 on Oct 26, 1943 (Tue): Civil Defense drill
        - Reopened from 15:20-15:40 under special rule of the Board
    - Closed on Aug 19, 1944 (Sat)
    - Closed on Aug 26, 1944 (Sat)
    - Closed on Sep 2, 1944 (Sat)
    - Closed on Apr 14, 1945 (Sat): President Franklin D. Roosevelt National Day of mourning
    - NOT IMPLEMENTED Break 11:00-13:00 on Jun 19, 1945 (Tue): Parade for General Eisenhower
    - Closed on Saturdays Jul 7-Sep 1, 1945 
    - Closed on Aug 15-16, 1945 (Wed-Thu): VJ Day. End of World War II
    - Closed on Oct 13, 1945 (Sat): Saturday after Columbus Day
    - Closed on Oct 27, 1945 (Sat): Navy Day
    - Closed on Dec 24, 1945 (Mon): Christmas Eve 
    - Closed on Feb 23, 1946 (Sat): Saturday after Washington's birthday
    - Closed on May 25, 1946 (Sat): Railroad strike
    - Closed on Saturdays Jun 1-Sep 28, 1946 (Sat-Sat)
    - Closed on Saturdays May 31-Sep 27, 1947 (Sat-Sat)
    - Closed on Jan 3, 1948 (Sat): severe weather
    - Closed on Saturdays May 29-Sep 25, 1948 (Sat-Sat)
    - Closed on Saturdays May 28-Sep 4, 1948 (Sat-Sat)
    - Cosed on Dec 24, 1949 (Sat): Christmas Eve
    - Closed on Saturdays Jun 3-Sep 30, 1950 (Sat-Sat)
    - Closed on Dec 12, 1950 (Sat): Saturday before Christmas Eve
    - NOT IMPLEMENTED Break from 11:00-13:00 on Apr 20, 1951 (Fri): Parade for General MacArthur
    - Closed on Saturdays Jun 2-Sep 29, 1951 (Sat-Sat)
    - NOT IMPLEMENTED Break from 10:33-11:05 (Wed): Civil Defense Drill
    - Early Close 1pm on Dec 24, 1951 (Mon): Christmas Eve
    - Closed on Saturdays May 31-Sep 27, 1952 (Sat-Sat)
        - As of Sep 29, 1952 Saturdays were retired as trading days
        - As of Sep 29, 1952, M-F trading closes at 3:30pm (30 minutes longer)
    
    
    
    
    
    
    
    
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
    aliases = ['NYSE', 'stock', 'NASDAQ', 'BATS', 'DJIA', 'DOW']

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
            UlyssesGrantFuneral1885,
            ColumbianCelebration1892,
            GreatBlizzardOf1888,
            WashingtonInaugurationCentennialCelebration1889,
            CharterDay1898,
            WelcomeNavalCommander1898,
            AdmiralDeweyCelebration1899,
            GarretHobartFuneral1899,
            QueenVictoriaFuneral1901,
            MovedToProduceExchange1901,
            EnlargedProduceExchange1901,
            McKinleyDeathAndFuneral1901,
            KingEdwardVIIcoronation1902,
            NYSEnewBuildingOpen1903,
            HudsonFultonCelebration1909,
            JamesShermanFuneral1912,
            OnsetOfWWI1914,
            WeatherHeatClosing1917,
            DraftRegistrationDay1917,
            WeatherNoHeatClosing1918,
            DraftRegistrationDay1918,
            ArmisticeSigned1918,
            Homecoming27Division1919,
            ParadeOf77thDivision1919,
            BacklogRelief1919,
            GeneralPershingReturn1919,
            OfficeLocationChange1920,
            HardingDeath1923,
            HardingFuneral1923,
            LindberghParade1927,
            BacklogRelief1928,
            BacklogRelief1929,
            BankHolidays1933,
            HeavyVolume1933,
            SatClosings1944,
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
            
            
            FirstLunarLandingClosing,
            September11Closings,
            NewYorkCityBlackout77,
            HurricaneGloriaClosings,
            HurricaneSandyClosings,
            
                        
        ))

    @property
    def special_closes(self):
        return [
             (time(11), AbstractHolidayCalendar(rules=[
                KingEdwardDeath11amyClose1910,
            ])),
            (time(12), AbstractHolidayCalendar(rules=[
                ParadeOfNationalGuardEarlyClose1917,
                LibertyDay12pmEarlyClose1917,
                LibertyDay12pmEarlyClose1918,
                WallStreetExplosionEarlyClose1920,
                NRAdemonstration12pmEarlyClose1933,
            ])),
            (time(hour=12, minute=30), AbstractHolidayCalendar(rules=[
                RooseveltFuneral1230EarlyClose1919,
                WoodrowWilsonFuneral1230EarlyClose1924,
                TaftFuneral1230EarlyClose1930,
                GasFumesOnTradingFloor1230EarlyClose1933,
            ])),
            (time(13), AbstractHolidayCalendar(rules=[               
                MonTuesThursBeforeIndependenceDay,
                FridayAfterIndependenceDayPre2013,
                WednesdayBeforeIndependenceDayPost2013,
                GroverClevelandFuneral1pmClose1908,
                USBlackFridayInOrAfter1993,
                ChristmasEveInOrAfter1993,               
            ])),
            (time(14), AbstractHolidayCalendar(rules=[
                ChristmasEveBefore1993,
                USBlackFridayBefore1993,
            ])),
            (time(hour=14, minute=30), AbstractHolidayCalendar(rules=[
                FalseArmisticeReport1430EarlyClose1918,
                CromwellFuneral1430EarlyClose1925,
            ])),
 
        ]
#
    @property
    def special_closes_adhoc(self):
        return [            
            (time(13), [
                '1997-12-26',
                '1999-12-31',
                '2003-12-26',
                '2013-07-03'
            ]),
            (time(14), [t.strftime("%Y-%m-%d") for t in ChristmasEve1pmEarlyCloseAdhoc]
             + BacklogRelief2pmEarlyClose1928.strftime("%Y-%m-%d").tolist()
             + [t.strftime("%Y-%m-%d") for t in BacklogRelief1pmEarlyClose1929]
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
                KingGeorgeVFuneral11amLateOpen1936,
            ])),
            (time(12), AbstractHolidayCalendar(rules=[
                KingEdwardFuneral12pmOpen1910,
                JPMorganFuneral12pmOpen1913,
                WilliamGaynorFuneral12pmOpen1913,
            ])),
            (time(13), AbstractHolidayCalendar(rules=[
                AnnunciatorBoardFire1pmLateOpen1921,
            ])),
            ]

#
    @property
    def special_opens_adhoc(self):
        return [                       
            (time(11), [t.strftime("%Y-%m-%d") for t in HeavyVolume11amLateOpen1933]                     
            ),     
            (time(12), [t.strftime("%Y-%m-%d") for t in BacklogRelief12pmLateOpen1929]
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
        # Starting Monday Sept. 29, 1952, no more saturday trading days
        trading_days = pd.date_range(start_date, end_date, freq=self.holidays(), normalize=True, tz=tz)
        ts_start_date = pd.Timestamp(start_date, tz='UTC')
        ts_end_date = pd.Timestamp(end_date, tz='UTC')
        if ts_start_date < pd.Timestamp('1952-09-29', tz='UTC'):
            if ts_end_date   <  pd.Timestamp('1952-09-29', tz='UTC'):
                return trading_days
            if ts_end_date   >=  pd.Timestamp('1952-09-29', tz='UTC'):
                saturdays = pd.date_range('1952-09-29', end_date, freq='W-SAT', tz='UTC')
        else: 
            saturdays = pd.date_range(start_date, end_date, freq='W-SAT', tz='UTC')         
                    
        drop_days = []
        for s in saturdays:
            if s in trading_days:
                drop_days.append(s)
        return trading_days.drop(drop_days)
       

    def days_at_time_open(self, days, tz, day_offset=0):
        """
        Create an index of days at time ``t``, interpreted in timezone ``tz``. 
        The returned index is localized to UTC.
        
        Rewritten from market_calendar.py due to variable open times    
        
        :param days: DatetimeIndex An index of dates (represented as midnight).
        :param t: datetime.time The time to apply as an offset to each day in ``days``.
        :param tz: pytz.timezone The timezone to use to interpret ``t``.
        :param day_offset: int The number of days we want to offset @days by
        :return: DatetimeIndex of date with the time t
        """
        if len(days) == 0:
            return pd.DatetimeIndex(days).tz_localize(tz).tz_convert('UTC')
    
        # Offset days without tz to avoid timezone issues.
        days = pd.DatetimeIndex(days).tz_localize(None)
        
        # Prior to 1985 trading began at 10am
        # After 1985 trading begins at 9:30am
        dti = []
        for d in days:
            if d >= pd.Timestamp('1985-01-01'):
                t = time(9,30)
            else:
                t = time(10)
            
            # TODO: Figure out why dates before 1901-12-14 have a 4 minute time shift
            if(d < pd.Timestamp('1901-12-14')):
                d = d + pd.Timedelta(minutes=4)
                           
            delta =  pd.Timedelta(
                        days=day_offset,
                        hours=t.hour,
                        minutes=t.minute,
                        seconds=t.second)
        
            dti.append( (d + delta).tz_localize(tz).tz_convert('UTC') )
                
        return pd.DatetimeIndex(dti)
    

    def days_at_time_close(self, days, tz, day_offset=0):
        """
        Create an index of days at time ``t``, interpreted in timezone ``tz``. 
        The returned index is localized to UTC.
        
        Rewritten from market_calendar.py due to variable close times    
        
        :param days: DatetimeIndex An index of dates (represented as midnight).
        :param t: datetime.time The time to apply as an offset to each day in ``days``.
        :param tz: pytz.timezone The timezone to use to interpret ``t``.
        :param day_offset: int The number of days we want to offset @days by
        :return: DatetimeIndex of date with the time t
        """
        if len(days) == 0:
            return pd.DatetimeIndex(days).tz_localize(tz).tz_convert('UTC')
    
        # Offset days without tz to avoid timezone issues.
        days = pd.DatetimeIndex(days).tz_localize(None)
        
        # Prior to 1952-09-29 close was Mon-Fri 3pm and Sat noon
        # 1952-1973 close was Mon-Fri 3:30pm (no saturday trades)
        # 1974+ close is 4pm 
        # TODO: Vectorize

        #tmp = pd.DatetimeIndex(days.to_series().apply(lambda d: self.normal_close_time(d, self.tz)))
        #print("tmp= \n", tmp)
        
        dti = []
        for d in days:
            if d < pd.Timestamp('1952-09-29'):
                t = time(15)
            elif ( d >= pd.Timestamp('1952-09-29') and d < pd.Timestamp('1974-01-01')):
                t = time(15,30)
            else:
                t = time(16)
                           
            # Saturday close    
            if d.dayofweek == 5:
                t = time(12)
            
            
            delta =  pd.Timedelta(
                        days=day_offset,
                        hours=t.hour,
                        minutes=t.minute,
                        seconds=t.second)

            # dates before 1901-12-14 have a 4 minute time shift. rounding removes it
            dti.append( (d + delta).tz_localize(tz).tz_convert('UTC').round('15min') )
                
        return pd.DatetimeIndex(dti)
    
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

        opens =  self.days_at_time_open(_all_days, self.tz, self.open_offset).tz_convert(tz)        
        closes = self.days_at_time_close(_all_days, self.tz, self.close_offset).tz_convert(tz)

        # `DatetimeIndex`s of nonstandard opens/closes
        _special_opens = self._calculate_special_opens(start_date, end_date)
        _special_closes = self._calculate_special_closes(start_date, end_date)
        
        print("special closes= ", _special_closes)

        # Overwrite the special opens and closes on top of the standard ones.
        _overwrite_special_dates(_all_days, opens, _special_opens)
        _overwrite_special_dates(_all_days, closes, _special_closes)

        result = pd.DataFrame(index=_all_days.tz_localize(None), columns=['market_open', 'market_close'],
                            data={'market_open': opens, 'market_close': closes})

        #TODO: TEST
        if self.break_start:
            result['break_start'] = self.days_at_time(_all_days, self.break_start, self.tz).tz_convert(tz)
            temp = result[['market_open', 'break_start']].max(axis=1)
            result['break_start'] = temp
            result['break_end'] = self.days_at_time(_all_days, self.break_end, self.tz).tz_convert(tz)
            temp = result[['market_close', 'break_end']].min(axis=1)
            result['break_end'] = temp

        return result
    
    def early_closes(self, schedule):
        """
        Get a DataFrame of the dates that are an early close.
        
        NOTE: Dates before 1901-12-14 convert with 4 minute time shift. 
              Rounding removes this

        :param schedule: schedule DataFrame
        :return: schedule DataFrame with rows that are early closes
        """
        # Prior to 1952-09-29 close was Mon-Fri 3pm and Sat noon
        # 1952-1973 close was Mon-Fri 3:30pm (no saturday trades)
        # 1974+ close is 4pm 
        # dates before 1901-12-14 have a 4 minute time shift. rounding removes it
              
        close3pm = schedule['market_close'].apply(lambda x: (x.tz_convert(self.tz).round('15min').time() != time(15)) &
                                                            (x < pd.Timestamp('1952-09-29', tz='UTC')) &
                                                            (x.dayofweek != 5)) 
        
        
        close12Sat  = schedule['market_close'].apply(lambda x: (x.tz_convert(self.tz).round('15min').time() != time(12)) &
                                                               (x.dayofweek == 5))
        
        close330pm = schedule['market_close'].apply(lambda x: (x.tz_convert(self.tz).round('15min').time() != time(15,30)) &
                                                              (x >= pd.Timestamp('1952-09-29', tz='UTC')) &
                                                              (x < pd.Timestamp('1974-01-01', tz='UTC')) 
                                                    )
        
        close4pm = schedule['market_close'].apply(lambda x: (x.tz_convert(self.tz).round('15min').time() != time(16)) &                                                              
                                                              (x >= pd.Timestamp('1974-01-01', tz='UTC'))
                                                    )
        
        mask = close3pm | close330pm | close4pm | close12Sat

        return schedule[mask]
 
 

    def late_opens(self, schedule):
        """
        Get a DataFrame of the dates that are an late opens.

        :param schedule: schedule DataFrame
        :return: schedule DataFrame with rows that are late opens
        """
        # Prior to 1985 trading began at 10am
        # After 1985 trading begins at 9:30am 
        # dates before 1901-12-14 have a 4 minute time shift. rounding removes it
        open10am = schedule['market_open'].apply(lambda x: (x.tz_convert(self.tz).round('15min').time() != time(10)) &
                                                            (x < pd.Timestamp('1985-01-01', tz='UTC')) )
                                                           
        open930am = schedule['market_open'].apply(lambda x: (x.tz_convert(self.tz).round('15min').time() != time(9,30)) &
                                                            (x >= pd.Timestamp('1985-01-01', tz='UTC')) )
        
        mask = open10am | open930am

        return schedule[mask]