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

from pandas_market_calendars.holidays_nyse import (    
    # Always Celebrated Holidays
    USNewYearsDayNYSEpost1952, USNewYearsDayNYSEpre1952, SatBeforeNewYearsAdhoc,
    
    USPresidentsDay, USWashingtonsBirthDay1964to1970, 
    USWashingtonsBirthDayBefore1952, USWashingtonsBirthDay1952to1963,
    USLincolnsBirthDayBefore1954, LincolnsBirthDayAdhoc, 
    SatBeforeWashingtonsBirthdayAdhoc, SatAfterWashingtonsBirthdayAdhoc, 
    SatBeforeAfterLincolnsBirthdayAdhoc,  GrantsBirthDayAdhoc,  
    
    USMartinLutherKingJrAfter1998,

    GoodFriday, GoodFridayPre1898, GoodFriday1899to1905, SatAfterGoodFridayAdhoc,
    
    USMemorialDay, USMemorialDayBefore1952, USMemorialDay1952to1964, USMemorialDay1964to1969,
    SatBeforeDecorationAdhoc, SatAfterDecorationAdhoc,
    DayBeforeDecorationAdhoc,

    USJuneteenthAfter2022,

    USIndependenceDay, USIndependenceDayPre1952, USIndependenceDay1952to1954,
    SatBeforeIndependenceDayAdhoc, SatAfterIndependenceDayAdhoc,
    MonTuesThursBeforeIndependenceDay, FridayAfterIndependenceDayNYSEpre2013,
    WednesdayBeforeIndependenceDayPost2013,
    MonBeforeIndependenceDayAdhoc, DaysAfterIndependenceDayAdhoc,
    # DaysBeforeIndependenceDay1pmEarlyCloseAdhoc,
    
    USColumbusDayBefore1954, USElectionDay1848to1967, 
    
    USLaborDayStarting1887, SatBeforeLaborDayAdhoc,
    
    USThanksgivingDay, USThanksgivingDay1939to1941,
    USThanksgivingDayBefore1939, 
    DayAfterThanksgiving2pmEarlyCloseBefore1993, 
    DayAfterThanksgiving1pmEarlyCloseInOrAfter1993,
    FridayAfterThanksgivingAdHoc, 
    
    USElectionDay1968to1980Adhoc,
    
    ChristmasNYSE, Christmas54to98NYSE, ChristmasBefore1954, 
    ChristmasEvesAdhoc, DayAfterChristmasAdhoc, DayAfterChristmas1pmEarlyCloseAdhoc,
    ChristmasEvePost1999Early1pmClose,
    ChristmasEve1pmEarlyCloseAdhoc, ChristmasEve2pmEarlyCloseAdhoc,
    SatBeforeChristmasAdhoc, SatAfterChristmasAdhoc,
    
    # Retired Holidays
    USVetransDayAdHoc, SatAfterColumbusDayAdHoc, USVeteransDay1934to1953,
    
    # Adhoc Holidays
    # 1885    
    UlyssesGrantFuneral1885,
    # 1892
    ColumbianCelebration1892, 
    # 1888
    GreatBlizzardOf1888,
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
    CoolidgeFuneral1933,
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
    RooseveltDayOfMourning1945, SatClosings1945, VJday1945, NavyDay1945,
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
    # 1960
    Snow11amLateOpening1960,
    # 1963
    KennedyAssassination1407EarlyClose,
    KennedyFuneral1963,
    # 1964
    HooverFuneral1400EarlyClose1964,
    # 1965
    PowerFail1105LateOpen,
    # 1966
    TransitStrike2pmEarlyClose1966,
    # 1967
    Snow1015LateOpen1967,
    Snow2pmEarlyClose1967,
    Backlog2pmEarlyCloses1967,
    # 1968
    Backlog2pmEarlyCloses1968,
    MLKdayOfMourning1968,
    PaperworkCrisis1968,
    # 1969 - 1970
    PaperworkCrisis2pmEarlyCloses1969,
    SnowClosing1969, Snow11amLateOpen1969,
    EisenhowerFuneral1969, Storm1045LateOpen1969,
    PaperworkCrisis230pmEarlyCloses1969, FirstLunarLandingClosing1969,
    PaperworkCrisis3pmEarlyCloses1969to1970,
    # 1972
    TrumanFuneral1972,
    # 1973
    JohnsonFuneral1973,
    Ice11amLateOpen1973,
    # 1974
    MerrillLynchComputer1015LateOpen1974, FireDrill1015LateOpen1974,
    # 1975
    Snow230EarlyClose1975,
    # 1976
    Storm1115LateOpen1976, FireDrill1015LateOpen1976,
    HurricaneWatch3pmEarlyClose1976,
    # 1977
    NewYorkCityBlackout77,
    # 1978
    Snow12pmLateOpen1978, Snow2pmEarlyClose1978, Snow11amLateOpen1978,
    # 1981
    ReaganAssassAttempt317pmEarlyClose1981,
    ConEdPowerFail328pmEarlyClose1981,
    # 1985
    HurricaneGloriaClosings1985,
    # 1987
    Backlog2pmEarlyCloses1987, Backlog230pmEarlyCloses1987,
    Backlog3pmEarlyCloses1987, Backlog330pmEarlyCloses1987,
    # 1989
    Fire11amLateOpen1989,
    # 1990
    ConEdXformer931amLateOpen1990,
    # 1991
    TroopsInGulf931LateOpens1991,
    # 1994
    Snow230pmEarlyClose1994,
    NixonFuneral1994,
    # 1995
    Computer1030LateOpen1995,
    # 1996
    Snow11amLateOpen1996,
    Snow2pmEarlyClose1996,
    # 1997
    CircuitBreakerTriggered330pmEarlyClose1997,
    # 2001
    September11Closings2001,
    Sept11MomentSilence933amLateOpen2001,
    EnduringFreedomMomentSilence931amLateOpen2001,
    # 2002
    Sept11Anniversary12pmLateOpen2002,
    # 2003
    IraqiFreedom932amLateOpen2003,
    # 2004
    ReaganMomentSilence932amLateOpen2004,
    ReaganMourning2004,
    # 2005
    SystemProb356pmEarlyClose2005,
    # 2006
    FordMomentSilence932amLateOpen2006,
    # 2007
    FordMourning2007,
    # 2012  
    HurricaneSandyClosings2012,
    # 2018
    GeorgeHWBushDeath2018
)
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

    REFERENCES:
    - https://web.archive.org/web/20141224054812/http://www.nyse.com/about/history/timeline_trading.html
    - https://www.marketwatch.com/story/a-brief-history-of-trading-hours-on-wall-street-2015-05-29
    - http://www.ltadvisors.net/Info/research/closings.pdf
    - https://github.com/rsheftel/pandas_market_calendars/files/6827110/Stocks.NYSE-Closings.pdf 
    
    NYSE OVERVIEW:
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
    - Washington's Birthday (February 22nd, before 1971 with rule change in 1964)
    - Washington's Birthday (aka President's Day, 3rd Monday in February, after 1970)
    - Good Friday (two days before Easter Sunday)
    - Memorial Day (May 30th, before 1970, with rule change in 1964)
    - Memorial Day (last Monday in May, after 1970)
    - Independence Day (July 4th Sunday to Monday, before 1954)
    - Independence Day (observed on the nearest weekday to July 4th, after 1953)
    - Election Day (First Tuesday starting on November 2nd, between 1848 and 1967)
    - Election Day (Every four years, first Tuesday starting on November 2nd, between 1968 and 1980)
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
    begin reference: https://github.com/rsheftel/pandas_market_calendars/files/6827110/Stocks.NYSE-Closings.pdf 
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
    - NOT IMPLEMENTED Break 10:02-10:32 on Jun 14, 1954 (Mon): Civil Defense drill
    - Closed on Dec 24, 1954 (Fri): Christmas Eve
    - NOT IMPLEMENTED Break 14:05-14:35 on Jun 15, 1955 (Wed): Civil Defense drill
    - Closed on Dec 24, 1956 (Mon): Christmas Eve
    - NOT IMPLEMENTED Break 13:45-14:15 on Jul 12, 1957 (Fri): Civil Defense drill
    - NOT IMPLEMENTED Break 10:30-10:50 on May 6, 1958 (Tue): Civil Defense drill
    - Closed on Dec 26, 1958 (Fri): Day after Christmas
    - NOT IMPLEMENTED Break 13:30-13:50 on Apr 17, 1959 (Fri): Civil Defense drill
    - NOT IMPLEMENTED Break 14:16-14:40 on May 3, 1960 (Tue): Civil Defense drill
    - Late Open 11:00 on Dec 12, 1960 (Mon): severe snowstorm
    - Closed on May 29, 1961 (Mon): Day before Decoration Day
    - Early Close 14:07 on Nov 22, 1963 (Fri): President John F. Kennedy assassintion
    - Closed on Nov 25, 1963 (Mon): President John F. Kennedy funeral
    - Early Close 14:00 on Oct 23, 1964 (Fri): Former President Herbert C. Hoover funeral
    - NOT IMPLEMENTED Break 11:00-11:02 on Jan 25, 1965 (Mon): Sir Winston Churchill 2 minutes of silence
    - Late Open 11:05 on Nov 10, 1965 (Wed): Power failure in NY grid supply
    - Closed on Dec 24, 1965 (Fri): Christmas Eve
    - Early Closes 14:00 on Jan 6-14, 1966 (Thu-Fri): Transit strike
    - NOT IMPLEMENTED Break 13:00-13:01 on Feb 3, 1967 (Fri): Apollo I disaster moment of silence
    - Late Open 10:15 AND Early Close 14:00 on Feb 7, 1967 (Tue): snowstorm 
    - NOT IMPLEMENTED Break 12:58-13:13 on May 17, 1967 (Wed): Vice President Humphrey spoke in honor of NYSE's 175th anniversary
    - Early Closes 14:00 on Aug 8-18, 1967 (Tue-Fri): Backlog catch up
    - Early Closes 14:00 on Jan 22-Mar 1, 1968 (Mon-Fri): Backlog catch up
    - Closed on Feb 12, 1968 (Mon): Lincoln's birthday (offices open, trading closed)
    - NOT IMPLEMENTED Break 11:00-11:01 on Apr 5, 1968 (Fri): Dr. Martin Luther King, Jr. moment of silence
    - Closed on Apr 9, 1968 (Tue): Martin Luther King, Jr. day or mourning
    - NOT IMPLEMENTED Break 11:00-11:02 on Jun 6, 1968 (Fri): Senator Robert F. Kennedy moment of silence
    - 4 day workweek Closed on a Wednesday OR Holiday from Jun 12-Dec 31, 1968: Paperwork crisis
    - Closed on July 5, 1968 (Fri): Day after Independence Day
    - Early Closes 14:00 on Jan 2-Jul 3, 1969: Paperwork Crisis
    - Closed on Feb 10, 1969 (Mon): heavy snow
    - Late open 11am on Feb 11, 1969 (Tue): heavy snow
    - NOT IMPLEMENTED Break 13:30-13:32 on Mar 28, 1969 (Fri): Former President Dwight D. Eisenhower moment of silence
    - Closed on Mar 31, 1969 (Mon): Former President Dwight D. Eisenhower funeral
    - Late Open 10:45 on Jun 2, 1969 (Mon): storm
    - Early Closes 14:30 on Jul 7-Sep 26,1969 (Mon-Fri): Paperwork Crisis
    - Closed on Jul 21, 1969 (Mon): National Day of Participation for lunar exploration
    - NOT IMPLEMENTED Break 12:35-13:05 on Sep 3, 1969 (Wed): power failure
    - Early Closes 15:00 on Sep 29, 1969 to May 1, 1970: Paperwork Crisis
    - Closed on Dec 28, 1972 (Thu): Former President Harry S. Truman funeral
    - Closed on Jan 25, 1973 (Thu): Former President Lyndon B. Johnson funeral
    - Late Open 11am on Dec 17, 1973 (Mon): ice storm
    - Late Open 10:15 on Jan 16, 1974 (Wed): Merrill Lynch computer trouble
    - NOT IMPLEMENTED Break 11:09-11:35 on Apr 10, 1974 (Wed): computer malfunction
    - NOT IMPLEMENTED Break 11:46-12:22 on Oct 15, 1974 (Wed): Ticker down at 11:37 to 12:22
    - Late Open 10:15 on Nov 22, 1974 (Fri): Fire drill
    - Early Close 14:00 on Dec 24, 1974 (Tue): Christmas Eve
    - NOT IMPLEMENTED Break 10:07-10:50 on Jan 7, 1975 (Tue): Computer stopped
    - NOT IMPLEMENTED Break 13:24-13:45 on Jan 15, 1975 (Wed): Computer stopped
    - NOT IMPLEMENTED Break 10:24-11:00 on Feb 7, 1975 (Fri): Computer failure
    - Early Close 14:30 on Feb 12, 1975 (Wed): snowstorm
    - NOT IMPLEMENTED Break 10:09-10:35 on Apr 9, 1975 (Wed): Computer stopped
    - Early Close 14:00 on Dec 24, 1975 (Wed): Christmas Eve    
    - Late Open 11:15 on Feb 2, 1976 (Mon): storm
    - Late Open UNKNOWN (coded as 10:15) on Jun 8, 1976 (Tue): fire drill
    - Early Close 15:00 on Aug 9, 1976 (Mon): hurricane watch
    - NOT IMPLEMENTED Break 1 minute time UNKNOWN on Nov 4, 1976 (Thu): Former NYSE Chair Gustave L. Levy moment of silence
    - NOT IMPLEMENTED Break 11:00-11:01 on Feb 24, 1977 (Thu): Former NYSE Chair John A. Coleman moment of silence
    - NOT IMPLEMENTED Break 10:24-11:45 on Mar 1, 1977 (Tue): Fire on moving ramp between trading floor and Blue Room
    - Closed on July 14, 1977 (Thu): Power failure in NYC
    - Late Open 12pm on Jan 20, 1978 (Fri): snowstorm
    - Early Close 2pm on Feb 6, 1978 (Mon): snowstorm
    - Late Open 11am on Feb 7, 1978 (Tue): snowstorm
    - NOT IMPLEMENTED Break 1 minute time UNKNOWN on Dec 13, 1979 (Thu): Former NYSE Chair Robert L. Stott minute of silence    
    - NOT IMPLEMENTED Break 11:11-12:04 on Oct 13, 1980 (Mon): Computer malfunction
    - NOT IMPLEMENTED Break 1 minute time UNKNOWN on Dec 30, 1980 (Tue): Former NYSE Chair James Crane Kellogg III moment of silence
    - Early Close 3:17pm on Mar 30, 1981 (Mon): President Reagan assassination attempt
    - Early Close 3:28pm on Sep 9, 1981 (Wed): Con Edison power failure
    - NOT IMPLEMENTED Break 12:26-12:45pm on Sep 16, 1981 (Wed): Fire alarm malfunction
    - NOT IMPLEMENTED Break 10:25-11:00am on Dec 28, 1982 (Tue): small fire
    - NOT IMPLEMENTED Break 13:51-15:30 on Oct 13, 1983 (Thu): low speed ticker malfunction
    - Closed on Sep 27, 1985 (Fri): Hurricane Gloria    
    - NOT IMPLEMENTED Break 11:00-11:01 on Jan 29, 1986 (Wed): Challenger space crew moment of silence    
    - Early Closes 2pm on Oct 23-30, 1987 (Fri-Fri): October 19th break volume
    - Early Closes 2:30pm on Nov 2-4, 1987 (Mon-Wed): reason not given volume assumed
    - Early Closes 3pm on Nov 5-6, 1987 (Thu-Fri): reason not given volume assumed
    - Early Closes 3:30pm on Nov 9-11, 1987 (Mon-Wed): Trading floor and clerical staff strike
    - Late Open 11am on Nov 10, 1989 (Fri): Electrical fire    
    - NOT IMPLEMENTED Break 9:41-11:15 on Nov 23, 1990 (Fri): Internal power failure    
    - Early Close 2pm on Dec 24, 1990 (Mon): Christmas Eve
    - Late Open 11am on Dec 27, 1990 (Thu): explosion of Con Edison transformer    
    - Late Open 9:31am on Jan 17, 1991 (Thu): American troops in Persian Gulf moment of silence
    - Late Open 9:31am on Feb 25, 1991 (Thu): American troops in Persian Gulf moment of silence
    - NOT IMPLEMENTED Break 10:21-10:45am on Oct 22, 1991 (Tue): power dip
    - Early Close 2pm on Dec 24, 1991 (Tue): Christmas Eve   
    - NOT IMPLEMENTED Break 1 minute time UNKNOWN on Mar 19, 1992 (Thu): Former NYSE Chair Bernard J. Lasker moment of silence
    - NOT IMPLEMENTED Break 1 minute time UNKNOWN on May 15, 1992 (Fri): Former NYSE President G. Keith Funston moment of silence
    - NOT IMPELMENTED Break 1 minute time UNKNOWN on Jun 15, 1992 (Mon): Former NYSE President Robert W. Haack moment of silence      
    - Early Close 2pm on Nov 27, 1992 (Fri): Day after Thanksgiving
    - Early Close 2pm on Dec 24, 1992 (Thu): Christmas Eve           
    - Early Close 1pm on Nov 26, 1993 (Fri): Day after Thanksgiving
    - Early Close 14:30 on Feb 11, 1994 (Fri): snowstorm
    - NOT IMPLEMENTED Break 12:00-12:02 on Apr 25, 1994 (Mon): Former President Richard M. Nixon moment of silence
    - Closed on Apr 27, 1994 (Wed): Former President Richard M. Nixon funderal
    - Early Close 1pm on Nov 25, 1994 (Fri): Day after Thanksgiving          
    - NOT IMPLEMENTED Break 10:02-10:03 on Apr 26, 1995 (Wed): Oklahoma City bombing victims moment of silence
    - Early Close 1pm on Jul 3, 1995 (Mon): Day before Independence Day
    - Early Close 1pm on Nov 24, 1995 (Fri): Day after Thanksgiving
    - Late Open 10:30am on Dec 18, 1995 (Mon): Computer system troubles
    - Late Open 11am AND Early Close 2pm on Jan 8, 1996 (Mon): snowstorm
    - NOT IMPLEMENTED Break time UNKNOWN on Apr 4, 1996 (Thu): Commerce Secretary Ron Brown and others killed in Balkans plane crash
    - Early Close 1pm on July 5, 1996 (Fri): Day after Independence Day
    - Early Close 1pm on Nov 29, 1996 (Fri): Day after Thanksgiving
    - Early Close 1pm on Dec 24, 1996 (Tue): Christmas Eve        
    - Early Close 1pm on Jul 3, 1997 (Thu): Day before Independence Day
    - NOT IMPLEMENTED Break 14:35-15:05 on Oct 27, 1997 (Mon): Circuit breaker triggered
    - Early Close 3:30pm on Oct 27, 1997 (Mon): Circuit breaker triggered
    - Early Close 1pm on Nov 28, 1997 (Fri): Day after Thanksgiving
    - Early Close 1pm on Dec 24, 1997 (Wed): Christmas Eve
    - Early Close 1pm on Dec 26, 1997 (Fri): Friday after Christmas        
    - NOT IMPLEMENTED Break time UNKNOWN on Jul 29, 1998 (Wed): Former NYSE President William McChesney Marting, Jr. moment of silence
    - NOT IMPLEMENTED Break 13:16-14:15 on Oct 26, 1998 (Mon): Computer switch malfunction
    - Early Close 1pm on Nov 27, 1998 (Fri): Day after Thanksgiving
    - Early Close 1pm on Dec 24, 1998 (Thu): Christmas Eve   
    - NOT IMPLEMENTED Break 10:00-10:02 on Mar 25, 1999 (Thu): NATO troops in Kosovo minute of silence
    - NOT IMPLEMENTED Break 12:00-12:02 on Apr 26, 1999 (Mon): Columbine High School killings moment of silence
    - Early Close 1pm on Nov 26, 1999 (Fri): Day after Thanksgiving
    - Early Close 1pm on Dec 24, 1999 (Fri): Christmas Eve       
    - NOT IMPLEMENTED Break 12:00-12:01 on Feb 16, 2000 (Wed): Former NYSE Chair Walter N. Frank moment of silence
    - NOT IMPLEMENTED Break 12:00-12:01 on May 4, 2000 (Thu): Archbishop of NY Cardinal John O'Connor moment of silence
    - Early Close 1pm on Jul 3, 2000 (Mon): Day before Independence Day
    - Early Close 1pm on Nov 24, 2000 (Fri): Day after Thanksgiving        
    - NOT IMPLEMENTED Break 10:10-11:35 on Jun 8, 2001 (Fri): computer systems connectivity problem
    - Early Close 1pm on Jul 3, 2001 (Tue): Day before Independence Day
    - Closed on Sep 11-14, 2001 (Tue-Fri): Terrorist attack on World Trade Center
    - Late Open 9:33am on Sep 17, 2001 (Mon): 2 minutes silence in honor of lives lost on 9/11
    - Late Open 9:31am on Oct 8, 2001 (Mon): 1 minute silence for troops engaged in Operation Enduring Freedom
    - Early Close 1pm on Nov 23, 2001 (Fri): Day after Thanksgiving
    - Early Close 1pm on Dec 24, 2001 (Mon): Christmas Eve    
    - NOT IMPLEMENTED Break 10:29-10:31 on May 30, 2002 (Thu): Commemorate end of recovery work at Ground Zero
    - Early Close 1pm on Jul 5, 2002 (Fri): Day after Independence Day    
    - Late Opening 12:00pm on Sep 11, 2002 (Wed): 1 year anniversary of 9/11 attack    
    - Early Close 1pm on Nov 29, 2002 (Fri): Day after Thanksgiving
    - Early Close 1pm on Dec 24, 2002 (Tue): Christmas Eve
    - NOT IMPLEMENTED Break 11:00-11:02 on Feb 3, 2002 (Mon): Columbia Space Shuttle lives lost moment of silence        
    - Late Opening 9:32am on Mar 20, 2003 (Thu): Operation Iraqi Freedom Troops moment of silence
    - Early Close 1pm on Jul 3, 2003 (Thu): Day before Independence Day
    - NOT IMPLEMENTED multiple 1-minute Breaks 9:59 and 10:29 on Sep 11, 2003 (Thu): 9/11 Commemoration
    - Early Close 1pm on Nov 28, 2003 (Fri): Day after Thanksgiving
    - Early Close 1pm on Dec 24, 2003 (Wed): Christmas Eve
    - Early Close 1pm on Dec 26, 2003 (Fri): Friday after Christmas        
    - Late Open 9:32am on Jun 7, 2004 (Mon): Former President Ronald Reagan death moment of silence
    - Closed on Jun 11, 2004 (Fri): Former President Ronald Reagan National Day of Mourning
    - Early Close 1pm on Nov 26, 2004 (Fri): Day after Thanksgiving    
    - Early Close 3:56pm on Jun 1, 2005 (Wed): Systems communication problem
    - Early Close 1pm on Nov 25, 2005 (Fri): Day after Thanksgiving       
    - Early Close 1pm on Jul 3, 2006 (Mon): Day before Independence Day        
    - Early Close 1pm on Nov 24, 2006 (Fri): Day after Thanksgiving
    - Late Open 9:32am on Dec 27, 2006 (Wed): Former President Gerald Ford moment of silence        
    - Closed on Jan 2, 2007 (Tue): Former President Gerald Ford National Day of Mourning
    - Early Close 1pm on Jul 3, 2007 (Tue): Day before Independence Day
    - Early Close 1pm on Nov 23, 2007 (Fri): Day after Thanksgiving
    - Early Close 1pm on Dec 24, 2007 (Mon): Christmas Eve        
    - Early Close 1pm on Jul 4, 2008 (Thu): Day before Independence Day
    - Early Close 1pm on Nov 28, 2008 (Fri): Day after Thanksgiving
    - Early Close 1pm on Dec 24, 2008 (Wed): Christmas Eve        
    - NOT IMPLEMENTED Extended Close 4:15pm on Jul 2, 2009 (Thu): Execute customer orders impacted by system irregularities
    - Early Close 1pm on Nov 27, 2009 (Fri): Day after Thanksgiving
    - Early Close 1pm on Dec 24, 2009 (Thu): Christmas Eve
    - Early Close 1pm on Nov 26, 2010 (Fri): Day after Thanksgiving    
    - NOT IMPLEMENTED Break 11:00-11:01 on Jan 10, 2011 (Mon): Arizona shooting victims moment of silence    

    end of reference: https://github.com/rsheftel/pandas_market_calendars/files/6827110/Stocks.NYSE-Closings.pdf 
    *******************************************************************
    
    https://www.streetinsider.com/Insiders+Blog/NYSE+Releases+2010+and+2011+Holiday+Calendar/4915576.html
    - Early Close 1pm on Nov 25, 2011 (Fri): Day after Thanksgiving    

    https://holidaystracker.com/stock-market/new-york-stock-exchange-holidays-2012/
    - Early Close 1pm on Jul 4, 2012 (Tue): Day before Independence Day
    - Closed on 10/29/2012 and 10/30/2012 due to Hurricane Sandy.
    - Early Close 1pm on Nov 23, 2012 (Fri): Day after Thanksgiving    
    - Early Close 1pm on Dec 24, 2012 (Mon): Christmas Eve

    https://holidaystracker.com/stock-market/new-york-stock-exchange-nyse-holidays-2013/    
    - Early Close 1pm on Jul 3, 2013 (Wed): Day before Independence Day
    - Early Close 1pm on Nov 29, 2013 (Fri): Day after Thanksgiving    
    - Early Close 1pm on Dec 24, 2013 (Tue): Christmas Eve
   
    https://www.streetinsider.com/Insiders+Blog/NYSE+2014+and+2015+Holiday+Hours/8999575.html    - Early Close 1pm on Jul 3, 2014 (Thu): Day before Independence Day
    - Early Close 1pm on Jul 3, 2014 (Thu): Day before Independence Day
    - Early Close 1pm on Nov 28, 2014 (Fri): Day after Thanksgiving    
    - Early Close 1pm on Dec 24, 2014 (Wed): Christmas Eve

    https://www.businesswire.com/news/home/20141208006349/en/NYSE-Group-2016-Holiday-Calendar-and-Early-Closings
    - Early Close 1pm on Nov 27, 2015 (Fri): Day after Thanksgiving    
    - Early Close 1pm on Dec 24, 2015 (Thu): Christmas Eve
    - Early Close 1pm on Nov 25, 2016 (Fri): Day after Thanksgiving    

    https://www.stockinvestor.com/30380/stock-market-holidays-2017/
    - Early Close 1pm on Jul 3, 2017 (Mon): Day before Independence Day
    - Early Close 1pm on Nov 24, 2017 (Fri): Day after Thanksgiving    
    - Early Close 1pm on Jul 3, 2018 (Tue): Day before Independence Day
    - Early Close 1pm on Nov 23, 2018 (Fri): Day after Thanksgiving    
    - Closed on 12/5/2018 due to George H.W. Bush's death.
    - Early Close 1pm on Dec 24, 2018 (Tue): Christmas Eve
    - Early Close 1pm on Jul 3, 2019 (Wed): Day before Independence Day
    - Early Close 1pm on Nov 29, 2019 (Fri): Day after Thanksgiving    
    - Early Close 1pm on Dec 24, 2019 (Wed): Christmas Eve

    https://holidaystracker.com/stock-market/new-york-stock-exchange-nyse-holidays-2020/
    - Early Close 1pm on Nov 27, 2020 (Fri): Day after Thanksgiving    
    - Early Close 1pm on Dec 24, 2020 (Thu): Christmas Eve
    

    NOTE: The exchange was **not** closed early on Friday December 26, 2008,
    nor was it closed on Friday December 26, 2014. The next Thursday Christmas
    will be in 2025.  If someone is still maintaining this code in 2025, then
    we've done alright...and we should check if it's a half day.
    
    """
    aliases = ['NYSE', 'stock', 'NASDAQ', 'BATS', 'DJIA', 'DOW']

    regular_market_times = {
        "pre": ((None, time(4)),),
        "market_open": ((None, time(10)),
                        ("1985-01-01", time(9, 30))),
        "market_close":((None, time(15)),
                        ("1952-09-29", time(15, 30)),
                        ("1974-01-01", time(16))),
        "post": ((None, time(20)),)
    }

    _saturday_close = time(12)
    _saturday_end = pd.Timestamp('1952-09-29', tz='UTC')

    @property
    def name(self):
        return "NYSE"

    @property
    def tz(self):
        return timezone("America/New_York")

    @property
    def weekmask(self):
        return "Mon Tue Wed Thu Fri Sat"    #Market open on Saturdays thru 5/24/1952

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USNewYearsDayNYSEpost1952,
            USNewYearsDayNYSEpre1952,
            USMartinLutherKingJrAfter1998,
            USPresidentsDay,
            USWashingtonsBirthDayBefore1952,
            USWashingtonsBirthDay1952to1963,
            USWashingtonsBirthDay1964to1970,
            USLincolnsBirthDayBefore1954,
            GoodFriday,
            GoodFridayPre1898,
            GoodFriday1899to1905,
            USMemorialDay,
            USMemorialDayBefore1952,
            USMemorialDay1952to1964,
            USMemorialDay1964to1969,
            USIndependenceDay,
            USIndependenceDayPre1952,
            USIndependenceDay1952to1954,
            USLaborDayStarting1887,
            USColumbusDayBefore1954,
            USElectionDay1848to1967,
            USVeteransDay1934to1953,
            USThanksgivingDay,
            USThanksgivingDayBefore1939,
            USThanksgivingDay1939to1941,
            ChristmasNYSE,
            Christmas54to98NYSE,
            ChristmasBefore1954,
            USJuneteenthAfter2022,
        ])

    @property
    def adhoc_holidays(self):
        return list(chain(
            # Recurring Holidays
            SatAfterGoodFridayAdhoc,
            MonBeforeIndependenceDayAdhoc,
            SatBeforeIndependenceDayAdhoc,
            SatAfterIndependenceDayAdhoc,
            DaysAfterIndependenceDayAdhoc,
            SatBeforeLaborDayAdhoc,
            USElectionDay1968to1980Adhoc,
            FridayAfterThanksgivingAdHoc,
            SatBeforeChristmasAdhoc,
            SatAfterChristmasAdhoc,
            ChristmasEvesAdhoc,
            DayAfterChristmasAdhoc,
            # Retired
            USVetransDayAdHoc,
            SatAfterColumbusDayAdHoc,
            LincolnsBirthDayAdhoc,
            GrantsBirthDayAdhoc,
            SatBeforeNewYearsAdhoc,
            SatBeforeWashingtonsBirthdayAdhoc,
            SatAfterWashingtonsBirthdayAdhoc,
            SatBeforeAfterLincolnsBirthdayAdhoc,
            SatBeforeDecorationAdhoc,
            SatAfterDecorationAdhoc,
            DayBeforeDecorationAdhoc,
           # Irregularities
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
            CoolidgeFuneral1933,
            BankHolidays1933,
            HeavyVolume1933,
            SatClosings1944,
            RooseveltDayOfMourning1945,
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
            KennedyFuneral1963,
            MLKdayOfMourning1968,
            PaperworkCrisis1968,
            SnowClosing1969,
            EisenhowerFuneral1969,
            FirstLunarLandingClosing1969,
            TrumanFuneral1972,
            JohnsonFuneral1973,
            NewYorkCityBlackout77,
            HurricaneGloriaClosings1985,
            NixonFuneral1994,
            ReaganMourning2004,
            FordMourning2007,
            September11Closings2001,
            HurricaneSandyClosings2012,
            GeorgeHWBushDeath2018,
        ))
#
    @property
    def special_closes(self):
        return [
             (time(11, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                KingEdwardDeath11amyClose1910,
            ])),
            (time(12, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                ParadeOfNationalGuardEarlyClose1917,
                LibertyDay12pmEarlyClose1917,
                LibertyDay12pmEarlyClose1918,
                WallStreetExplosionEarlyClose1920,
                NRAdemonstration12pmEarlyClose1933,
            ])),
            (time(hour=12, minute=30, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                RooseveltFuneral1230EarlyClose1919,
                WoodrowWilsonFuneral1230EarlyClose1924,
                TaftFuneral1230EarlyClose1930,
                GasFumesOnTradingFloor1230EarlyClose1933,
            ])),
            (time(13, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                FridayAfterIndependenceDayNYSEpre2013,
                MonTuesThursBeforeIndependenceDay,
                WednesdayBeforeIndependenceDayPost2013,
                DayAfterThanksgiving1pmEarlyCloseInOrAfter1993,
                ChristmasEvePost1999Early1pmClose,
                GroverClevelandFuneral1pmClose1908,
            ])),
            (time(14, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                DayAfterThanksgiving2pmEarlyCloseBefore1993,
                HooverFuneral1400EarlyClose1964,
                Snow2pmEarlyClose1967,
                Snow2pmEarlyClose1978,
                Snow2pmEarlyClose1996,
            ])),
            (time(14, 7, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                KennedyAssassination1407EarlyClose,
            ])),
            (time(hour=14, minute=30, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                FalseArmisticeReport1430EarlyClose1918,
                CromwellFuneral1430EarlyClose1925,
                Snow230EarlyClose1975,
                Snow230pmEarlyClose1994,
            ])),
            (time(15, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                HurricaneWatch3pmEarlyClose1976,
            ])),
            (time(15, 17, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                ReaganAssassAttempt317pmEarlyClose1981,
            ])),
            (time(15, 28, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
               ConEdPowerFail328pmEarlyClose1981,
            ])),
            (time(15, 30, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
               CircuitBreakerTriggered330pmEarlyClose1997,
            ])),
            (time(15, 56, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
               SystemProb356pmEarlyClose2005,
            ])),
        ]
#
    @property
    def special_closes_adhoc(self):
        def _union_many(indexes):
            # Merges a list of pd.DatetimeIndex objects, returns merged DatetimeIndex
            union_index = pd.DatetimeIndex([], tz="UTC")
            for index in indexes:
                union_index = union_index.union(index)
            return union_index

        return [
            (time(13, tzinfo=timezone('America/New_York')),
                # DaysBeforeIndependenceDay1pmEarlyCloseAdhoc # list
                ChristmasEve1pmEarlyCloseAdhoc
                + DayAfterChristmas1pmEarlyCloseAdhoc
                + BacklogRelief1pmEarlyClose1929
            ),
            (time(14, tzinfo=timezone('America/New_York')), _union_many(
                [pd.DatetimeIndex(
                 ChristmasEve2pmEarlyCloseAdhoc
                 + HeavyVolume2pmEarlyClose1933)] +
                                      
                [BacklogRelief2pmEarlyClose1928,
                 TransitStrike2pmEarlyClose1966, # index
                 Backlog2pmEarlyCloses1967, # index
                 Backlog2pmEarlyCloses1968, # index
                 PaperworkCrisis2pmEarlyCloses1969, # index
                 Backlog2pmEarlyCloses1987 ])# index
            ),
            (time(14, 30, tzinfo=timezone('America/New_York')), _union_many(
                                      
                [PaperworkCrisis230pmEarlyCloses1969,
                 Backlog230pmEarlyCloses1987]) # index
            ),
            (time(15, tzinfo=timezone('America/New_York')), _union_many(
                                      
                [PaperworkCrisis3pmEarlyCloses1969to1970,
                 Backlog3pmEarlyCloses1987]) # index
            ),
            (time(15, 30, tzinfo=timezone('America/New_York')),
                Backlog330pmEarlyCloses1987 # index
            ),
        ]

#
    @property
    def special_opens(self):
        return [
            (time(hour=9, minute=31, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                ConEdXformer931amLateOpen1990,
                EnduringFreedomMomentSilence931amLateOpen2001,
            ])),
            (time(hour=9, minute=32, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                IraqiFreedom932amLateOpen2003,
                ReaganMomentSilence932amLateOpen2004,
                FordMomentSilence932amLateOpen2006,
            ])),
            (time(hour=9, minute=33, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                Sept11MomentSilence933amLateOpen2001,
            ])),
            (time(hour=10, minute=15, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                Snow1015LateOpen1967,
                MerrillLynchComputer1015LateOpen1974,
                FireDrill1015LateOpen1974,
                FireDrill1015LateOpen1976,
            ])),
            (time(hour=10, minute=30, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                TrafficBlockLateOpen1919,
                TrafficBlockLateOpen1920,
                Computer1030LateOpen1995,
            ])),
            (time(hour=10, minute=45, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                EclipseOfSunLateOpen1925,
                Storm1045LateOpen1969,
            ])),
            (time(11, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                Snow11amLateOpen1934,
                KingGeorgeVFuneral11amLateOpen1936,
                Snow11amLateOpening1960,
                Snow11amLateOpen1969,
                Ice11amLateOpen1973,
                Snow11amLateOpen1978,
                Fire11amLateOpen1989,
                Snow11amLateOpen1996,
            ])),
            (time(11, 5, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                PowerFail1105LateOpen,
            ])),
            (time(11, 15, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                Storm1115LateOpen1976,
            ])),
            (time(12, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                KingEdwardFuneral12pmOpen1910,
                JPMorganFuneral12pmOpen1913,
                WilliamGaynorFuneral12pmOpen1913,
                Snow12pmLateOpen1978,
                Sept11Anniversary12pmLateOpen2002,
            ])),
            (time(13, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                AnnunciatorBoardFire1pmLateOpen1921,
            ])),
            ]

#
    @property
    def special_opens_adhoc(self):
        return [
            (time(9, 31, tzinfo=timezone('America/New_York')), TroopsInGulf931LateOpens1991
            ),
            (time(11, tzinfo=timezone('America/New_York')), HeavyVolume11amLateOpen1933
            ),
            (time(12, tzinfo=timezone('America/New_York')),
                BacklogRelief12pmLateOpen1929
                + HeavyVolume12pmLateOpen1933
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
        trading_days = super().valid_days(start_date, end_date, tz= 'UTC')

        # Starting Monday Sept. 29, 1952, no more saturday trading days
        above_cut_off = trading_days >= self._saturday_end
        if above_cut_off.any():
            above_and_saturday = (trading_days.weekday == 5) & above_cut_off
            trading_days = trading_days[~above_and_saturday]

        return trading_days.tz_convert(tz)


    def days_at_time(self, days, market_time, day_offset=0):
        days = super().days_at_time(days, market_time, day_offset= day_offset)

        if market_time == "market_close" and not self.is_custom(market_time):
            days = days.dt.tz_convert(self.tz)
            days = days.where(days.dt.weekday != 5, days.dt.normalize()+ self._tdelta(self._saturday_close))
            days = days.dt.tz_convert("UTC")
        return days

    def early_closes(self, schedule):
        """
        Get a DataFrame of the dates that are an early close.

        :param schedule: schedule DataFrame
        :return: schedule DataFrame with rows that are early closes
        """
        early = super().early_closes(schedule)

        # make sure saturdays are not considered early closes if they are >= 12pm
        mc = early.market_close.dt.tz_convert(self.tz)
        after_noon = (mc - mc.dt.normalize()).ge(self._tdelta(self._saturday_close))
        return early[~(mc.dt.weekday.eq(5) & after_noon)]
