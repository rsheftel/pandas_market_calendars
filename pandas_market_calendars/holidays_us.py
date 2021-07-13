from dateutil.relativedelta import (MO, TH, TU)
from pandas import (DateOffset, Timestamp, date_range)
from datetime import datetime, timedelta
from pandas.tseries.holiday import (Holiday, nearest_workday, sunday_to_monday, Easter)
from pandas.tseries.offsets import Day, CustomBusinessDay

from pandas_market_calendars.market_calendar import (FRIDAY, SATURDAY, SUNDAY, MONDAY, THURSDAY, TUESDAY, WEDNESDAY)

#Monday = 0, Sunday=6
def previous_saturday(dt):
    """
    If holiday falls on Sunday, Monday or Tuesday, Saturday there is no trading
    """
    if dt.weekday() == 0:
        return dt - timedelta(2)
    elif dt.weekday() == 1:
        return dt - timedelta(3)
    elif dt.weekday() == 6:
        return dt - timedelta(1)
    return dt

def next_saturday(dt):
    """
    If holiday falls on Thursday or Friday, the next Saturday there is no trading
    """
    if dt.weekday() == 3:
        return dt + timedelta(2)
    elif dt.weekday() == 4:
        return dt + timedelta(1)
    return dt


#############################################################################
# Saturday Trading Thru 1952
#   NYSE was open on Saturdays thru 5/24/1952
#   anyone maintaining this code after 2050 will need to update the end date
#############################################################################
Post1952May24Saturdays = date_range('1952-05-25', 
                                    '2050-12-31', 
                                    freq='W-SAT',
                                    tz='UTC'
)
# Every Saturday was an early close
Pre1952May24SatEarlyClose = date_range('1885-01-01', 
                                    '1952-05-25', 
                                    freq='W-SAT',
                                    tz='UTC'
)
# Adhoc Saturday Closes
Pre1952MaySatClosesAdhoc = [
    Timestamp('1901-04-27', tz='UTC'), # Moved to temporary quarters in Produce Exchange
    Timestamp('1901-05-11', tz='UTC')  # Enlarged Produce Exchange
    ]

####################################################
# US New Years Day Jan 1
#    Closed every year since the stock market opened
#####################################################
USNewYearsDay = Holiday(
    'New Years Day',
    month=1,
    day=1,
    # When Jan 1 is a Sunday, US markets observe the subsequent Monday.
    # When Jan 1 is a Saturday (as in 2005 and 2011), no holiday is observed.
    observance=sunday_to_monday
)
# Not every Saturday before/after Christmas is a holiday
SatBeforeNewYearsAdhoc = [
    Timestamp('1916-12-30', tz='UTC')
]

USMartinLutherKingJrAfter1998 = Holiday(
    'Dr. Martin Luther King Jr. Day',
    month=1,
    day=1,
    # The US markets didn't observe MLK day as a holiday until 1998.
    start_date=Timestamp('1998-01-01'),
    offset=DateOffset(weekday=MO(3)),
)
#########################################################################
# US Presidents Day Feb 
#    Lincoln's birthday closed every year 1896-1953
#    Washington's birthday closed every year. Observed Mondays since 1971
#    Grant's birthday was celebrated once in 1897
##########################################################################
# http://www.ltadvisors.net/Info/research/closings.pdf
USPresidentsDay = Holiday('President''s Day',
                          start_date=Timestamp('1971-01-01'),
                          month=2, day=1,
                          offset=DateOffset(weekday=MO(3)))
USWashingtonsBirthDayBefore1964 = Holiday(
    'Washington''s Birthday',
    month=2,
    day=22,
    start_date=Timestamp('1880-01-01'),
    end_date=Timestamp('1963-12-31'),
    observance=sunday_to_monday,
)
USWashingtonsBirthDay1964to1970 = Holiday(
    'Washington''s Birthday',
    month=2,
    day=22,
    start_date=Timestamp('1964-01-01'),
    end_date=Timestamp('1970-12-31'),
    observance=nearest_workday,
)
# Not all Saturdays before Washingtons birthday were holidays (e.g. 1920)
SatBeforeWashingtonsBirthdayAdhoc = [
    Timestamp('1903-02-21', tz='UTC'),
    ]
# Not all Saturdays after Washington's brithday were holidays (e.g. 1918)
SatAfterWashingtonsBirthdayAdhoc = [
    Timestamp('1901-02-23', tz='UTC'),
    Timestamp('1907-02-23', tz='UTC'),
    Timestamp('1929-02-23', tz='UTC')
]

USLincolnsBirthDayBefore1954 = Holiday(
    'Lincoln''s Birthday',
    month=2,
    day=12,
    start_date=Timestamp('1896-01-01'), 
    end_date=Timestamp('1953-12-31'),
    observance=sunday_to_monday,
)
# Not all Saturdays before/after Lincoln's birthday were holidays
SatBeforeAfterLincolnsBirthdayAdhoc = [
    Timestamp('1899-02-11', tz='UTC'),
    Timestamp('1909-02-13', tz='UTC')
    ]

# 1968-02-12. Offices were open but trading floor was closed
LincolnsBirthDayAdhoc = [Timestamp('1968-02-12', tz='UTC')]

GrantsBirthDayAdhoc   = [Timestamp('1897-04-27', tz='UTC')]

############################################################
# Good Friday 
#      closed every year except 1898, 1906, and 1907
############################################################
GoodFriday = Holiday(
    "Good Friday 1908+", 
    start_date=Timestamp('1908-01-01'), 
    month=1, 
    day=1, 
    offset=[Easter(), Day(-2)]
)
GoodFridayPre1898 = Holiday(
    "Good Friday Before 1898", 
    start_date=Timestamp('1885-01-01'),
    end_date=Timestamp('1897-12-31'), 
    month=1, 
    day=1, 
    offset=[Easter(), Day(-2)]
)
GoodFriday1899to1905 = Holiday(
    "Good Friday 1899 to 1905", 
    start_date=Timestamp('1899-01-01'),
    end_date=Timestamp('1905-12-31'), 
    month=1, 
    day=1, 
    offset=[Easter(), Day(-2)]
)
#Not every saturday after Good Friday is a holiday (e.g. 1904)
SatAfterGoodFridayAdhoc = [
    Timestamp("1900-04-14"),
    Timestamp("1901-04-06"),
    Timestamp("1902-03-29"),
    Timestamp("1903-04-11"),
    Timestamp("1905-04-22"),
    Timestamp("1907-03-30"),
    Timestamp("1908-04-18"),
    Timestamp("1909-04-10"),
    Timestamp("1910-03-26"),
    Timestamp("1911-04-15"),
    Timestamp("1913-03-22"),
    Timestamp("1920-04-03"),
    Timestamp("1929-03-30"),
    Timestamp("1930-04-19")
]


##################################################
# US Memorial Day (Decoration Day) May 30 
#    Closed every year since 1873
#    Observed on Monday since 1971
##################################################
# http://www.tradingtheodds.com/nyse-full-day-closings/
USMemorialDay = Holiday(
    'Memorial Day',
    month=5,
    day=25,
    start_date=Timestamp('1971-01-01'),
    offset=DateOffset(weekday=MO(1)),
)
USMemorialDayBefore1964 = Holiday(
    'Memorial Day',
    month=5,
    day=30,
    end_date=Timestamp('1963-12-31'),
    observance=sunday_to_monday,
)
# http://www.tradingtheodds.com/nyse-full-day-closings/
USMemorialDay1964to1969 = Holiday(
    'Memorial Day',
    month=5,
    day=30,
    start_date=Timestamp('1964-01-01'),
    end_date=Timestamp('1969-12-31'),
    observance=nearest_workday,
)

# Not all Saturdays before/after Decoration Day were observed
SatBeforeDecorationAdhoc = [
    Timestamp('1904-05-28', tz='UTC'),
    Timestamp('1909-05-29', tz='UTC'),    
    Timestamp('1910-05-28', tz='UTC'), 
    Timestamp('1921-05-28', tz='UTC'), 
    Timestamp('1926-05-29', tz='UTC'), 
    Timestamp('1937-05-29', tz='UTC'), 
]
SatAfterDecorationAdhoc = [
    Timestamp('1902-05-31', tz='UTC'),
    Timestamp('1913-05-31', tz='UTC'),  
    Timestamp('1919-05-31', tz='UTC'), 
    Timestamp('1924-05-31', tz='UTC'), 
    Timestamp('1930-05-31', tz='UTC'), 
]

DayBeforeDecorationAdhoc = [
    Timestamp('1899-05-29', tz='UTC'),
    Timestamp('1961-05-29', tz='UTC')
]


#######################################
# US Independence Day July 4
#######################################
USIndependenceDay = Holiday(
    'July 4th',
    month=7,
    day=4,
    start_date=Timestamp('1954-01-01'),
    observance=nearest_workday,
)
# http://www.tradingtheodds.com/nyse-full-day-closings/
USIndependenceDayBefore1954 = Holiday(
    'July 4th',
    month=7,
    day=4,
    end_date=Timestamp('1953-12-31'),
    observance=sunday_to_monday,
)

MonTuesThursBeforeIndependenceDay = Holiday(
    # When July 4th is a Tuesday, Wednesday, or Friday, the previous day is a
    # half day.
    'Mondays, Tuesdays, and Thursdays Before Independence Day',
    month=7,
    day=3,
    days_of_week=(MONDAY, TUESDAY, THURSDAY),
    start_date=Timestamp("1995-01-01"),
)

def july_5th_holiday_observance(datetime_index):
    return datetime_index[datetime_index.year < 2013]

FridayAfterIndependenceDayPre2013 = Holiday(
    # When July 4th is a Thursday, the next day is a half day prior to 2013.
    # Since 2013 the early close is on Wednesday and Friday is a full day
    "Fridays after Independence Day prior to 2013",
    month=7,
    day=5,
    days_of_week=(FRIDAY,),
    observance=july_5th_holiday_observance,
    start_date=Timestamp("1885-01-01"),
)

WednesdayBeforeIndependenceDayPost2013 = Holiday(
    # When July 4th is a Thursday, the next day is a half day prior to 2013.
    # Since 2013 the early close is on Wednesday and Friday is a full day
    "Wednesdays Before Independence Day including and after 2013",
    month=7,
    day=3,
    days_of_week=(WEDNESDAY,),
    start_date=Timestamp("2013-01-01"),
)
MonBeforeIndependenceDayAdhoc = [
    Timestamp('1899-07-03', tz='UTC'),
    ]
# Not all Saturdays before/after Independence day are observed
SatBeforeIndependenceDayAdhoc = [
    Timestamp('1887-07-02', tz='UTC'),
    Timestamp('1892-07-02', tz='UTC'),
    Timestamp('1898-07-02', tz='UTC'),
    Timestamp('1904-07-02', tz='UTC'),
    Timestamp('1909-07-03', tz='UTC'),
    Timestamp('1910-07-02', tz='UTC'),
    Timestamp('1920-07-03', tz='UTC'),
    Timestamp('1921-07-02', tz='UTC'),
    Timestamp('1926-07-03', tz='UTC'),
    Timestamp('1932-07-02', tz='UTC'),
    Timestamp('1937-07-03', tz='UTC'),    
    ]

SatAfterIndependenceDayAdhoc = [
    Timestamp('1890-07-05', tz='UTC'),
    Timestamp('1902-07-05', tz='UTC'),
    Timestamp('1913-07-05', tz='UTC'),
    Timestamp('1919-07-05', tz='UTC'),
    Timestamp('1930-07-05', tz='UTC'),
    Timestamp('1902-07-05', tz='UTC'),
    ]

DaysAfterIndependenceDayAdhoc = [
    Timestamp('1901-07-05', tz='UTC'),
    Timestamp('1901-07-06', tz='UTC'),
    Timestamp('1968-07-05', tz='UTC')
    ]


#################################################
# US Labor Day Starting 1887
#################################################
# http://www.ltadvisors.net/Info/research/closings.pdf
USLaborDayStarting1887 = Holiday(
    "Labor Day", 
    month=9, 
    day=1, 
    start_date=Timestamp("1887-01-01"),
    offset=DateOffset(weekday=MO(1))
)
# Not every Saturday before Labor Day is observed. 1894 is an example.
SatBeforeLaborDayAdhoc = [
    Timestamp('1888-09-01', tz='UTC'),
    Timestamp('1898-09-03', tz='UTC'),
    Timestamp('1900-09-01', tz='UTC'),
    Timestamp('1901-08-31', tz='UTC'),
    Timestamp('1902-08-30', tz='UTC'),
    Timestamp('1903-09-05', tz='UTC'),
    Timestamp('1904-09-03', tz='UTC'),
    Timestamp('1907-08-31', tz='UTC'),
    Timestamp('1908-09-05', tz='UTC'),
    Timestamp('1909-09-04', tz='UTC'),
    Timestamp('1910-09-03', tz='UTC'),
    Timestamp('1911-09-02', tz='UTC'),
    Timestamp('1912-08-31', tz='UTC'),
    Timestamp('1913-08-30', tz='UTC'),
    Timestamp('1917-09-01', tz='UTC'),
    Timestamp('1919-08-30', tz='UTC'),
    Timestamp('1920-09-04', tz='UTC'),
    Timestamp('1921-09-03', tz='UTC'),
    Timestamp('1926-09-04', tz='UTC'),
    Timestamp('1929-08-31', tz='UTC'),
    Timestamp('1930-08-30', tz='UTC'),
    Timestamp('1931-09-05', tz='UTC'),
]

###################################################
# US Election Day Nov 2
###################################################
# http://www.tradingtheodds.com/nyse-full-day-closings/
USElectionDay1848to1967 = Holiday(
    'Election Day',
    month=11,
    day=2,
    start_date=Timestamp('1848-1-1'),
    end_date=Timestamp('1967-12-31'),
    offset=DateOffset(weekday=TU(1)),
)

def following_tuesday_every_four_years_observance(dt):
    return dt + DateOffset(years=(4 - (dt.year % 4)) % 4, weekday=TU(1))

USElectionDay1968to1980 = Holiday(
    'Election Day',
    month=11,
    day=2,
    start_date=Timestamp('1968-01-01'),
    end_date=Timestamp('1980-12-31'),
    observance=following_tuesday_every_four_years_observance
)
################################################
# US Thanksgiving Nov 30
################################################
# http://www.tradingtheodds.com/nyse-full-day-closings/
USThanksgivingDayBefore1939 = Holiday('Thanksgiving Before 1939',
                                      start_date=Timestamp('1864-01-01'),
                                      end_date=Timestamp('1938-12-31'),
                                      month=11, day=30,
                                      offset=DateOffset(weekday=TH(-1)))
# http://www.tradingtheodds.com/nyse-full-day-closings/
USThanksgivingDay1939to1941 = Holiday('Thanksgiving 1939 to 1941',
                                      start_date=Timestamp('1939-01-01'),
                                      end_date=Timestamp('1941-12-31'),
                                      month=11, day=30,
                                      offset=DateOffset(weekday=TH(-2)))
USThanksgivingDay = Holiday('Thanksgiving',
                            start_date=Timestamp('1942-01-01'),
                            month=11, day=1,
                            offset=DateOffset(weekday=TH(4)))
FridayAfterThanksgivingAdHoc = [
    Timestamp('1888-11-30', tz='UTC'),
]
################################
# Christmas Dec 25
################################
Christmas = Holiday(
    'Christmas',
    month=12,
    day=25,
    start_date=Timestamp('1954-01-01'),
    observance=nearest_workday,
)
ChristmasBefore1954 = Holiday(
    'Christmas',
    month=12,
    day=25,
    end_date=Timestamp('1953-12-31'),
    observance=sunday_to_monday,
)
    # These have the same definition, but are used in different places because the
    # NYSE closed at 2:00 PM on Christmas Eve until 1993.
ChristmasEveBefore1993 = Holiday(
    'Christmas Eve',
    month=12,
    day=24,
    end_date=Timestamp('1993-01-01'),
    # When Christmas is a Saturday, the 24th is a full holiday.
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY),
)
ChristmasEveInOrAfter1993 = Holiday(
    'Christmas Eve',
    month=12,
    day=24,
    start_date=Timestamp('1993-01-01'),
    # When Christmas is a Saturday, the 24th is a full holiday.
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY),
)
# Not every Saturday before/after Christmas is a holiday
SatBeforeChristmasAdhoc = [
    Timestamp('1887-12-24', tz='UTC'),
    Timestamp('1898-12-24', tz='UTC'),
    Timestamp('1904-12-24', tz='UTC'),
    Timestamp('1910-12-24', tz='UTC'),
    Timestamp('1911-12-23', tz='UTC'),
    Timestamp('1922-12-23', tz='UTC'),
    Timestamp('1949-12-24', tz='UTC'),
    Timestamp('1950-12-23', tz='UTC'),
]
SatAfterChristmasAdhoc = [
    Timestamp('1891-12-26', tz='UTC'),
    Timestamp('1896-12-26', tz='UTC'),
    Timestamp('1903-12-26', tz='UTC'),
    Timestamp('1908-12-26', tz='UTC'),
    Timestamp('1925-12-26', tz='UTC'),
    Timestamp('1931-12-26', tz='UTC'),
    Timestamp('1936-12-26', tz='UTC'),
    ]

ChristmasEvesAdhoc = [
    Timestamp('1900-12-24', tz='UTC'),
    Timestamp('1945-12-24', tz='UTC'),
    Timestamp('1954-12-24', tz='UTC'),
    Timestamp('1956-12-24', tz='UTC'),
    Timestamp('1965-12-24', tz='UTC')
]

DayAfterChristmasAdhoc = [
    Timestamp('1958-12-26', tz='UTC'),
]

ChristmasEveEarlyCloseAdhoc = [
    Timestamp('1951-12-24', tz='UTC'),
    Timestamp('1974-12-24', tz='UTC'),
    Timestamp('1975-12-24', tz='UTC'),
    Timestamp('1990-12-24', tz='UTC'),
]


#####################################
# Retired holidays
#####################################
# http://www.tradingtheodds.com/nyse-full-day-closings/
USVeteransDay1934to1953 = Holiday(
    'Veteran Day',
    month=11,
    day=11,
    start_date=Timestamp('1934-1-1'),
    end_date=Timestamp('1953-12-31'),
    observance=sunday_to_monday,
)
USVetransDayAdHoc = [
    Timestamp("1921-11-11", tz="UTC")
]
# http://www.tradingtheodds.com/nyse-full-day-closings/
USColumbusDayBefore1954 = Holiday(
    'Columbus Day',
    month=10,
    day=12,
    start_date=Timestamp('1909-01-01'),
    end_date=Timestamp('1953-12-31'),
    observance=sunday_to_monday,
)
SatAfterColumbusDayAdHoc = [
    Timestamp("1917-10-13", tz="UTC"),
]
USBlackFridayBefore1993 = Holiday(
    'Black Friday',
    month=11,
    day=1,
    # Black Friday was not observed until 1992.
    start_date=Timestamp('1992-01-01'),
    end_date=Timestamp('1993-01-01'),
    offset=[DateOffset(weekday=TH(4)), Day(1)],
)
USBlackFridayInOrAfter1993 = Holiday(
    'Black Friday',
    month=11,
    day=1,
    start_date=Timestamp('1993-01-01'),
    offset=[DateOffset(weekday=TH(4)), Day(1)],
)

##########################
# Non-recurring holidays
##########################

ColumbianCelebration1892 = [
    Timestamp("1892-10-12", tz='UTC'),
    Timestamp("1892-10-21", tz='UTC'),
    Timestamp("1892-10-22", tz='UTC'),
    Timestamp("1893-04-27", tz='UTC'),
]

GreatBlizzardOf1888 = [
    Timestamp('1888-03-12', tz='UTC'),
    Timestamp('1888-03-13', tz='UTC'),
]

WashingtonInaugurationCentennialCelebration1889 = [
    Timestamp("1889-04-29", tz='UTC'),
    Timestamp("1889-04-30", tz='UTC'),
    Timestamp("1889-05-01", tz='UTC'),
]

# NYC's 5 boroughs founded as NYC
# Not actually celebrated due to Spanish-American war but market was closed
CharterDay1898 = [Timestamp('1898-05-04', tz='UTC')]

WelcomeNavalCommander1898 = [Timestamp('1898-08-20', tz='UTC')]

AdmiralDeweyCelebration1899 = [Timestamp('1899-09-29', tz='UTC'),Timestamp('1899-09-30', tz='UTC') ]

KingEdwardVIIcoronation1902 = [Timestamp('1902-08-09', tz='UTC')]

NYSEnewBuildingOpen1903 = [Timestamp('1903-04-22', tz='UTC')]

FuneralOfGroverCleveland1908 = Holiday(
    'Funeral of Grover Cleveland 1908 1pm Close',
    month=6,
    day=26,
    start_date=Timestamp('1908-06-26'),
    end_date=Timestamp('1908-06-26'),
)

# 300th anniversary of Hudson discovering the Hudson river and
# 100th anniversary of Fulton inventing the paddle steamer
HudsonFultonCelebration1909 = [Timestamp('1909-09-25', tz='UTC')]

# Reopened for trading bonds (with restrictions) Nov 27, 1914
# Reopened for trading stocks (with restrictions) Dec 12, 1914
# Restrictions remained in place until April 1, 1915
OnsetOfWWI1914 =  date_range('1914-07-31', 
                             '1914-12-11', 
                             freq=CustomBusinessDay(weekmask = 'Mon Tue Wed Thu Fri Sat'),
                             tz='UTC'
)

DraftRegistrationDay1917 = [Timestamp('1917-06-05', tz='UTC')]
DraftRegistrationDay1918 = [Timestamp('1918-09-12', tz='UTC')]

ParadeOfNationalGuardEarlyClose1917 = Holiday(
    'Parade of National Guard 12pm Early Close Aug 29, 1917',
    month=8,
    day=29,
    start_date=Timestamp('1917-08-29'),
    end_date=Timestamp('1917-08-29'),
)

LibertyDayEarlyClose1917 = Holiday(
    'Liberty Day 12pm Early Close Oct 24, 1917',
    month=10,
    day=24,
    start_date=Timestamp('1917-10-24'),
    end_date=Timestamp('1917-10-24'),
)
LibertyDayEarlyClose1918 = Holiday(
    'Liberty Day 12pm Early Close April 26, 1918',
    month=4,
    day=26,
    start_date=Timestamp('1918-04-26'),
    end_date=Timestamp('1918-04-26'),
)
FalseArmisticeReportEarlyClose1918 = Holiday(
    'False Armistice Report 2:30pm Early Close Nov 7, 1918',
    month=11,
    day=7,
    start_date=Timestamp('1918-11-07'),
    end_date=Timestamp('1918-11-07'),
)
ArmisticeSigned1918 = [Timestamp('1918-11-11', tz='UTC')]

RooseveltFuneralEarlyClose1919 = Holiday(
    'Former President Roosevelt funeral 12:30pm Early Close Jan 7, 1919',
    month=1,
    day=7,
    start_date=Timestamp('1919-01-07'),
    end_date=Timestamp('1919-01-07'),
)

Homecoming27Division1919 = [Timestamp('1919-03-25', tz='UTC')]

ParadeOf77thDivision1919 = [Timestamp('1919-05-06', tz='UTC')]

BacklogRelief1919 = [
    Timestamp('1919-07-19', tz='UTC'),
    Timestamp('1919-08-02', tz='UTC'),
    Timestamp('1919-08-16', tz='UTC'),
    ]

GeneralPershingReturn1919 = [Timestamp('1919-09-10', tz='UTC')]

OfficeLocationChange1920 = [Timestamp('1920-05-01', tz='UTC')]

WallStreetExplosionEarlyClose1920 = Holiday(
    'Wall Street Explosion 12:00 Early Close Sept 16, 1920',
    month=9,
    day=16,
    start_date=Timestamp('1920-09-16'),
    end_date=Timestamp('1920-09-16'),
)

BattleOfGettysburg = Holiday(
    # All of the floor traders in Chicago were sent to PA
    'Markets were closed during the battle of Gettysburg',
    month=7,
    day=(1, 2, 3),
    start_date=Timestamp("1863-07-01"),
    end_date=Timestamp("1863-07-03")
)

# http://www.tradingtheodds.com/nyse-full-day-closings/

November29BacklogRelief = [Timestamp('1929-11-01', tz='UTC'),
                           Timestamp('1929-11-29', tz='UTC')]

# https://en.wikipedia.org/wiki/March_1933#March_6,_1933_(Monday)
March33BankHoliday = [
    Timestamp("1933-03-06", tz="UTC"),
    Timestamp("1933-03-07", tz="UTC"),
    Timestamp("1933-03-08", tz="UTC"),
    Timestamp("1933-03-09", tz="UTC"),
    Timestamp("1933-03-10", tz="UTC"),
    Timestamp("1933-03-13", tz="UTC"),
    Timestamp("1933-03-14", tz="UTC"),
]

# http://www.tradingtheodds.com/nyse-full-day-closings/
August45VictoryOverJapan = date_range('1945-08-15', '1945-08-16', tz='UTC')



# http://www.tradingtheodds.com/nyse-full-day-closings/
PaperworkCrisis68 = [Timestamp('1968-06-12', tz='UTC'),
                     Timestamp('1968-06-19', tz='UTC'),
                     Timestamp('1968-06-26', tz='UTC'),
                     Timestamp('1968-07-10', tz='UTC'),
                     Timestamp('1968-07-17', tz='UTC'),
                     Timestamp('1968-07-24', tz='UTC'),
                     Timestamp('1968-07-31', tz='UTC'),
                     Timestamp('1968-08-07', tz='UTC'),
                     Timestamp('1968-08-14', tz='UTC'),
                     Timestamp('1968-08-21', tz='UTC'),
                     Timestamp('1968-08-28', tz='UTC'),
                     Timestamp('1968-09-11', tz='UTC'),
                     Timestamp('1968-09-18', tz='UTC'),
                     Timestamp('1968-09-25', tz='UTC'),
                     Timestamp('1968-10-02', tz='UTC'),
                     Timestamp('1968-10-09', tz='UTC'),
                     Timestamp('1968-10-16', tz='UTC'),
                     Timestamp('1968-10-23', tz='UTC'),
                     Timestamp('1968-10-30', tz='UTC'),
                     Timestamp('1968-11-11', tz='UTC'),
                     Timestamp('1968-11-20', tz='UTC'),
                     Timestamp('1968-12-04', tz='UTC'),
                     Timestamp('1968-12-11', tz='UTC'),
                     Timestamp('1968-12-18', tz='UTC'),
                     Timestamp('1968-12-25', tz='UTC')]


# http://www.tradingtheodds.com/nyse-full-day-closings/
WeatherSnowClosing = [Timestamp('1969-02-10', tz='UTC')]

WeatherHeatClosing = [Timestamp('1917-08-04', tz='UTC')]

WeatherNoHeatClosing = [
    Timestamp('1918-01-28', tz='UTC'),
    Timestamp('1918-02-04', tz='UTC'),
    Timestamp('1918-02-11', tz='UTC'),
    
    ]

# http://www.tradingtheodds.com/nyse-full-day-closings/
FirstLunarLandingClosing = [Timestamp('1969-07-21', tz='UTC')]

# http://www.tradingtheodds.com/nyse-full-day-closings/
NewYorkCityBlackout77 = [Timestamp('1977-07-14', tz='UTC')]

# http://en.wikipedia.org/wiki/Aftermath_of_the_September_11_attacks
September11Closings = [
    Timestamp("2001-09-11", tz='UTC'),
    Timestamp("2001-09-12", tz='UTC'),
    Timestamp("2001-09-13", tz='UTC'),
    Timestamp("2001-09-14", tz='UTC')
]

# http://en.wikipedia.org/wiki/Hurricane_Gloria
HurricaneGloriaClosings = date_range(
    '1985-09-27',
    '1985-09-27',
    tz='UTC'
)

# http://en.wikipedia.org/wiki/Hurricane_sandy
HurricaneSandyClosings = date_range(
    '2012-10-29',
    '2012-10-30',
    tz='UTC'
)



# National Days of Mourning
# - President Ulysses S Grant Funeral - August 8, 1885
# - Vice-President Garret A. Hobart - November 25, 1899
# - Queen Victoria of England Funderal - February 2, 1901
# - President William McKinley Death - September 14, 1901
# - President William McKinley Funderal - September 19, 1901
# - Vice-President James S. Sherman - November 2, 1912
# - President Warren G. Harding Death - August 3, 1923
# - President Warren G. Harding Funeral - August 10, 1923
# - President John F. Kennedy - November 25, 1963
# - Martin Luther King - April 9, 1968
# - President Dwight D. Eisenhower - March 31, 1969
# - President Harry S. Truman - December 28, 1972
# - President Lyndon B. Johnson - January 25, 1973
# - President Richard Nixon - April 27, 1994
# - President Ronald W. Reagan - June 11, 2004
# - President Gerald R. Ford - Jan 2, 2007
# - President George H.W. Bush - Dec 5, 2018
USNationalDaysofMourning = [
    Timestamp('1885-08-08', tz='UTC'), 
    Timestamp('1899-11-25', tz='UTC'), 
    Timestamp('1901-02-02', tz='UTC'), 
    Timestamp('1901-09-14', tz='UTC'),
    Timestamp('1901-09-19', tz='UTC'),
    Timestamp('1912-11-02', tz='UTC'),
    Timestamp('1923-08-03', tz='UTC'),
    Timestamp('1923-08-10', tz='UTC'),
    Timestamp('1963-11-25', tz='UTC'),
    Timestamp('1968-04-09', tz='UTC'),
    Timestamp('1969-03-31', tz='UTC'),
    Timestamp('1972-12-28', tz='UTC'),
    Timestamp('1973-01-25', tz='UTC'),
    Timestamp('1994-04-27', tz='UTC'),
    Timestamp('2004-06-11', tz='UTC'),
    Timestamp('2007-01-02', tz='UTC'),
    Timestamp('2018-12-05', tz='UTC'),
]
