from dateutil.relativedelta import (MO, TH, TU)
from pandas import (DateOffset, Timestamp, date_range)
from datetime import  timedelta
from pandas.tseries.holiday import (Holiday, nearest_workday, sunday_to_monday,  Easter)
from pandas.tseries.offsets import Day, CustomBusinessDay

from pandas_market_calendars.market_calendar import ( MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY)

################################################################################################
# main reference:     
#    https://github.com/rsheftel/pandas_market_calendars/files/6827110/Stocks.NYSE-Closings.pdf 
#
# See exchange_calendar_nyse.py for details
#################################################################################################

def previous_saturday(dt):
    """
    If holiday falls on Sunday, Monday or Tuesday, Saturday there is no trading
    """
    if dt.weekday() == MONDAY:
        return dt - timedelta(2)
    elif dt.weekday() == TUESDAY:
        return dt - timedelta(3)
    elif dt.weekday() == SUNDAY:
        return dt - timedelta(1)
    return dt

def next_saturday(dt):
    """
    If holiday falls on Thursday or Friday, the next Saturday there is no trading
    """
    if dt.weekday() == THURSDAY:
        return dt + timedelta(2)
    elif dt.weekday() == FRIDAY:
        return dt + timedelta(1)
    return dt

####################################################
# US New Years Day Jan 1
#    Closed every year since the stock market opened
#####################################################
USNewYearsDayNYSEpost1952 = Holiday(
    'New Years Day',
    month=1,
    day=1,
    start_date = Timestamp('1952-09-29'),
    # When Jan 1 is a Sunday, US markets observe the subsequent Monday.
    # When Jan 1 is a Saturday (as in 2005 and 2011), no holiday is observed.
    observance=sunday_to_monday,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY,)    
)

USNewYearsDayNYSEpre1952 = Holiday(
    'New Years Day Before Saturday Trading Ceased',
    month=1,
    day=1,
    end_date = Timestamp('1952-09-28'),
    observance=sunday_to_monday,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY,)
)

NewYearsEve1pmCloseAdhoc = [
    #Timestamp('1999-12-31', tz='UTC'), # Disputed. Not in reference source
]

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
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY,),
    offset=DateOffset(weekday=MO(3)),
)
#########################################################################
# US Presidents Day Feb 
#    Lincoln's birthday closed every year 1896-1953
#    Washington's birthday closed every year. Observed Mondays since 1971
#    Grant's birthday was celebrated once in 1897
##########################################################################
USPresidentsDay = Holiday('President''s Day',
                          start_date=Timestamp('1971-01-01'),
                          month=2, day=1,
                          days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY,),
                          offset=DateOffset(weekday=MO(3)))

USWashingtonsBirthDayBefore1952 = Holiday(
    'Washington''s Birthday',
    month=2,
    day=22,
    end_date=Timestamp('1952-09-28'),
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY,),
    observance=sunday_to_monday,
)
USWashingtonsBirthDay1952to1963 = Holiday(
    'Washington''s Birthday',
    month=2,
    day=22,
    start_date=Timestamp('1952-09-29'),
    end_date=Timestamp('1963-12-31'),
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY,),
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
    Timestamp('1929-02-23', tz='UTC'),
    Timestamp('1946-02-23', tz='UTC')
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
    Timestamp("1900-04-14", tz='UTC'),
    Timestamp("1901-04-06", tz='UTC'),
    Timestamp("1902-03-29", tz='UTC'),
    Timestamp("1903-04-11", tz='UTC'),
    Timestamp("1905-04-22", tz='UTC'),
    Timestamp("1907-03-30", tz='UTC'),
    Timestamp("1908-04-18", tz='UTC'),
    Timestamp("1909-04-10", tz='UTC'),
    Timestamp("1910-03-26", tz='UTC'),
    Timestamp("1911-04-15", tz='UTC'),
    Timestamp("1913-03-22", tz='UTC'),
    Timestamp("1920-04-03", tz='UTC'),
    Timestamp("1929-03-30", tz='UTC'),
    Timestamp("1930-04-19", tz='UTC')
]

##################################################
# US Memorial Day (Decoration Day) May 30 
#    Closed every year since 1873
#    Observed on Monday since 1971
##################################################
USMemorialDay = Holiday(
    'Memorial Day',
    month=5,
    day=25,
    start_date=Timestamp('1971-01-01'),
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
    offset=DateOffset(weekday=MO(1)),
)
USMemorialDayBefore1952 = Holiday(
    'Memorial Day',
    month=5,
    day=30,
    end_date=Timestamp('1952-09-28'),
    observance=sunday_to_monday,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY)
)
USMemorialDay1952to1964 = Holiday(
    'Memorial Day',
    month=5,
    day=30,
    start_date=Timestamp('1952-09-29'),
    end_date=Timestamp('1963-12-31'),
    observance=sunday_to_monday,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY)
)

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
# US Juneteenth (June 19th)
#######################################
USJuneteenthAfter2022 = Holiday(
    'Juneteenth Starting at 2022',
    start_date=Timestamp('2022-06-19'),
    month=6, day=19,
    observance=nearest_workday,
)

#######################################
# US Independence Day July 4
#######################################
USIndependenceDay = Holiday(
    'July 4th',
    month=7,
    day=4,
    start_date=Timestamp('1954-01-01'),
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
    observance=nearest_workday,
)
USIndependenceDayPre1952 = Holiday(
    'July 4th',
    month=7,
    day=4,
    end_date=Timestamp('1952-09-28'),
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY),
    observance=sunday_to_monday,
)
USIndependenceDay1952to1954 = Holiday(
    'July 4th',
    month=7,
    day=4,
    start_date=Timestamp('1952-09-29'),
    end_date=Timestamp('1953-12-31'),
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
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

FridayAfterIndependenceDayNYSEpre2013 = Holiday(
    # When July 4th is a Thursday, the next day is a half day prior to 2013.
    # Since 2013 the early close is on Wednesday and Friday is a full day
    "Fridays after Independence Day prior to 2013",
    month=7,
    day=5,
    days_of_week=(FRIDAY,),
    observance=july_5th_holiday_observance,
    start_date=Timestamp("1996-01-01"),
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
    ]

DaysAfterIndependenceDayAdhoc = [
    Timestamp('1901-07-05', tz='UTC'),
    Timestamp('1901-07-06', tz='UTC'),
    Timestamp('1968-07-05', tz='UTC')
    ]

DaysBeforeIndependenceDay1pmEarlyCloseAdhoc = [
    Timestamp('2013-07-03', tz='UTC')
    ]

#################################################
# US Labor Day Starting 1887
#################################################
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
USElectionDay1848to1967 = Holiday(
    'Election Day',
    month=11,
    day=2,
    start_date=Timestamp('1848-1-1'),
    end_date=Timestamp('1967-12-31'),
    offset=DateOffset(weekday=TU(1)),
)

USElectionDay1968to1980Adhoc = [
    Timestamp('1968-11-05', tz="UTC"),
    Timestamp('1972-11-07', tz="UTC"),
    Timestamp('1976-11-02', tz="UTC"),
    Timestamp('1980-11-04', tz="UTC")]

################################################
# US Thanksgiving Nov 30
################################################
USThanksgivingDay = Holiday(
    'Thanksgiving',
    start_date=Timestamp('1942-01-01'),
    month=11, day=1,
    offset=DateOffset(weekday=TH(4))
)

USThanksgivingDayBefore1939 = Holiday(
    'Thanksgiving Before 1939',
    start_date=Timestamp('1864-01-01'),
    end_date=Timestamp('1938-12-31'),
    month=11, day=30,
    offset=DateOffset(weekday=TH(-1))
)

USThanksgivingDay1939to1941 = Holiday(
    'Thanksgiving 1939 to 1941',
    start_date=Timestamp('1939-01-01'),
    end_date=Timestamp('1941-12-31'),
    month=11, day=30,
    offset=DateOffset(weekday=TH(-2))
)

DayAfterThanksgiving2pmEarlyCloseBefore1993 = Holiday(
    'Black Friday',
    month=11,
    day=1,
    # Black Friday was not observed until 1992.
    start_date=Timestamp('1992-01-01'),
    end_date=Timestamp('1993-01-01'),
    offset=[DateOffset(weekday=TH(4)), Day(1)],
)

DayAfterThanksgiving1pmEarlyCloseInOrAfter1993 = Holiday(
    'Black Friday',
    month=11,
    day=1,
    start_date=Timestamp('1993-01-01'),
    offset=[DateOffset(weekday=TH(4)), Day(1)],
)

FridayAfterThanksgivingAdHoc = [
    Timestamp('1888-11-30', tz='UTC'),
]

################################
# Christmas Dec 25
################################
ChristmasNYSE = Holiday(
    'Christmas',
    month=12,
    day=25,
    start_date=Timestamp('1999-01-01'),
    observance=nearest_workday, 
)

Christmas54to98NYSE = Holiday(
    'Christmas',
    month=12,
    day=25,
    start_date=Timestamp('1954-01-01'),
    end_date=Timestamp('1998-12-31'),
    observance=nearest_workday, 
)

ChristmasBefore1954 = Holiday(
    'Christmas',
    month=12,
    day=25,
    end_date=Timestamp('1953-12-31'),
    observance=sunday_to_monday,
)

# Only some Christmas Eve's were fully close
ChristmasEvesAdhoc = [
    Timestamp('1900-12-24', tz='UTC'),
    Timestamp('1945-12-24', tz='UTC'),
    Timestamp('1956-12-24', tz='UTC'),
]

DayAfterChristmasAdhoc = [
    Timestamp('1958-12-26', tz='UTC'),
]

DayAfterChristmas1pmEarlyCloseAdhoc = [
    Timestamp('1997-12-26', tz='UTC'),
    Timestamp('2003-12-26', tz='UTC'),
]

ChristmasEvePost1999Early1pmClose = Holiday(
    # When Christmas Eve is Mon-Thu it is a 1pm early close
    'Mondays, Tuesdays, Wednesdays, and Thursdays Before Christmas',
    month=12,
    day=24,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY),
    start_date=Timestamp("1999-01-01"),
)

ChristmasEve1pmEarlyCloseAdhoc = [
    Timestamp('1951-12-24', tz='UTC'),
    Timestamp('1996-12-24', tz='UTC'),
    Timestamp('1997-12-24', tz='UTC'), 
    Timestamp('1998-12-24', tz='UTC'), 
    Timestamp('1999-12-24', tz='UTC'), 
]

# Only some Christmas Eve's were 2pm early close (1976-1979 were not)
ChristmasEve2pmEarlyCloseAdhoc = [
    Timestamp('1974-12-24', tz='UTC'),
    Timestamp('1975-12-24', tz='UTC'),
    Timestamp('1990-12-24', tz='UTC'),  #### This one was also in the 1pm list, in the tests you check for 2pm
    Timestamp('1991-12-24', tz='UTC'),
    Timestamp('1992-12-24', tz='UTC'),
]

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


#####################################
# Retired holidays
#####################################
# Armistice/Veterans day
USVeteransDay1934to1953 = Holiday(
    'Veteran Day',
    month=11,
    day=11,
    start_date=Timestamp('1934-1-1'),
    end_date=Timestamp('1953-12-31'),
    observance=sunday_to_monday,
)

USVetransDayAdHoc = [
    Timestamp("1921-11-11", tz="UTC"),
    Timestamp("1968-11-11", tz="UTC")
]

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
    Timestamp("1945-10-13", tz="UTC"),
]


##########################
# Non-recurring holidays
##########################

# 1885
UlyssesGrantFuneral1885 = [Timestamp('1885-08-08', tz='UTC')]

# 1888
GreatBlizzardOf1888 = [
    Timestamp('1888-03-12', tz='UTC'),
    Timestamp('1888-03-13', tz='UTC'),
]

# 1889
WashingtonInaugurationCentennialCelebration1889 = [
    Timestamp("1889-04-29", tz='UTC'),
    Timestamp("1889-04-30", tz='UTC'),
    Timestamp("1889-05-01", tz='UTC'),
]


# 1892
ColumbianCelebration1892 = [
    Timestamp("1892-10-12", tz='UTC'),
    Timestamp("1892-10-21", tz='UTC'),
    Timestamp("1892-10-22", tz='UTC'),
    Timestamp("1893-04-27", tz='UTC'),
]

# 1898
    # NYC's 5 boroughs founded as NYC
    # Not actually celebrated due to Spanish-American war but market was closed
CharterDay1898 = [Timestamp('1898-05-04', tz='UTC')]

WelcomeNavalCommander1898 = [Timestamp('1898-08-20', tz='UTC')]

# 1899
AdmiralDeweyCelebration1899 = [Timestamp('1899-09-29', tz='UTC'),
                              Timestamp('1899-09-30', tz='UTC') 
]

GarretHobartFuneral1899 = [Timestamp('1899-11-25', tz='UTC')]

# 1901
QueenVictoriaFuneral1901 = [Timestamp('1901-02-02', tz='UTC')]

MovedToProduceExchange1901 = [Timestamp('1901-04-27', tz='UTC')]

EnlargedProduceExchange1901 = [Timestamp('1901-05-11', tz='UTC')]

McKinleyDeathAndFuneral1901 = [Timestamp('1901-09-14', tz='UTC'), 
                              Timestamp('1901-09-19', tz='UTC'),]

# 1902
KingEdwardVIIcoronation1902 = [Timestamp('1902-08-09', tz='UTC')]

# 1903
NYSEnewBuildingOpen1903 = [Timestamp('1903-04-22', tz='UTC')]

# 1908
GroverClevelandFuneral1pmClose1908 = Holiday(
    'Funeral of Grover Cleveland 1908 1pm Close',
    month=6,
    day=26,
    start_date=Timestamp('1908-06-26'),
    end_date=Timestamp('1908-06-26'),
)

# 1909
    # 300th anniversary of Hudson discovering the Hudson river and
    # 100th anniversary of Fulton inventing the paddle steamer
HudsonFultonCelebration1909 = [Timestamp('1909-09-25', tz='UTC')]

# 1910
KingEdwardDeath11amyClose1910 = Holiday(
    'King Edward VII Death May 7, 1910',
    month=5,
    day=7,
    start_date=Timestamp('1910-05-07'),
    end_date=Timestamp('1910-05-07'),
)

KingEdwardFuneral12pmOpen1910 = Holiday(
    'King Edward VII Funeral 12pm late open May 20, 1910',
    month=5,
    day=20,
    start_date=Timestamp('1910-05-20'),
    end_date=Timestamp('1910-05-20'),
)

# 1912
JamesShermanFuneral1912 = [Timestamp('1912-11-02', tz='UTC')]

# 1913
JPMorganFuneral12pmOpen1913 = Holiday(
    'JP Morgan Funeral 12pm late open April 14, 1913',
    month=4,
    day=14,
    start_date=Timestamp('1913-04-14'),
    end_date=Timestamp('1913-04-14'),
)

WilliamGaynorFuneral12pmOpen1913 = Holiday(
    'Mayor William J. Gaynor Funeral 12pm late open Sept 22, 1913',
    month=9,
    day=22,
    start_date=Timestamp('1913-09-22'),
    end_date=Timestamp('1913-09-22'),
)

# 1914

# Reopened for trading bonds (with restrictions) Nov 27, 1914
# Reopened for trading stocks (with restrictions) Dec 12, 1914
# Restrictions remained in place until April 1, 1915
OnsetOfWWI1914 =  date_range('1914-07-31', 
                             '1914-12-11', 
                             freq=CustomBusinessDay(weekmask = 'Mon Tue Wed Thu Fri Sat'),
                             tz='UTC'
)

# 1917
DraftRegistrationDay1917 = [Timestamp('1917-06-05', tz='UTC')]

WeatherHeatClosing1917 = [Timestamp('1917-08-04', tz='UTC')]

ParadeOfNationalGuardEarlyClose1917 = Holiday(
    'Parade of National Guard 12pm Early Close Aug 29, 1917',
    month=8,
    day=29,
    start_date=Timestamp('1917-08-29'),
    end_date=Timestamp('1917-08-29'),
)

LibertyDay12pmEarlyClose1917 = Holiday(
    'Liberty Day 12pm Early Close Oct 24, 1917',
    month=10,
    day=24,
    start_date=Timestamp('1917-10-24'),
    end_date=Timestamp('1917-10-24'),
)

# 1918
WeatherNoHeatClosing1918 = [
    Timestamp('1918-01-28', tz='UTC'),
    Timestamp('1918-02-04', tz='UTC'),
    Timestamp('1918-02-11', tz='UTC'),
    
    ]

LibertyDay12pmEarlyClose1918 = Holiday(
    'Liberty Day 12pm Early Close April 26, 1918',
    month=4,
    day=26,
    start_date=Timestamp('1918-04-26'),
    end_date=Timestamp('1918-04-26'),
)

DraftRegistrationDay1918 = [Timestamp('1918-09-12', tz='UTC')]

FalseArmisticeReport1430EarlyClose1918 = Holiday(
    'False Armistice Report 2:30pm Early Close Nov 7, 1918',
    month=11,
    day=7,
    start_date=Timestamp('1918-11-07'),
    end_date=Timestamp('1918-11-07'),
)
ArmisticeSigned1918 = [Timestamp('1918-11-11', tz='UTC')]

# 1919
RooseveltFuneral1230EarlyClose1919 = Holiday(
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

TrafficBlockLateOpen1919 = Holiday(
    'Traffic Block 10:30am late open Dec. 30, 1919',
    month=12,
    day=30,
    start_date=Timestamp('1919-12-30'),
    end_date=Timestamp('1919-12-30'),
)

# 1920
TrafficBlockLateOpen1920 = Holiday(
    'Traffic Block 10:30am late open Feb. 6, 1920',
    month=2,
    day=6,
    start_date=Timestamp('1920-02-06'),
    end_date=Timestamp('1920-02-06'),
)

OfficeLocationChange1920 = [Timestamp('1920-05-01', tz='UTC')]

WallStreetExplosionEarlyClose1920 = Holiday(
    'Wall Street Explosion 12:00 Early Close Sept 16, 1920',
    month=9,
    day=16,
    start_date=Timestamp('1920-09-16'),
    end_date=Timestamp('1920-09-16'),
)

# 1921
AnnunciatorBoardFire1pmLateOpen1921 = Holiday(
    'Annunciator Board Fire 1pm late open Aug 8, 1921',
    month=8,
    day=2,
    start_date=Timestamp('1921-08-02'),
    end_date=Timestamp('1921-08-02'),
)

# 1923
HardingDeath1923 = [Timestamp('1923-08-03', tz='UTC')]

HardingFuneral1923 = [Timestamp('1923-08-10', tz='UTC')]

# 1924
WoodrowWilsonFuneral1230EarlyClose1924 = Holiday(
    'Former President Woodrow Wilson Funeral 12:30 Early Close Feb 6, 1924',
    month=2,
    day=6,
    start_date=Timestamp('1924-02-06'),
    end_date=Timestamp('1924-02-06'),
)

# 1925
EclipseOfSunLateOpen1925 = Holiday(
    'Eclipse of Sun 10:45am late open Jan 25, 1925',
    month=1,
    day=24,
    start_date=Timestamp('1925-01-24'),
    end_date=Timestamp('1925-01-24'),
)

CromwellFuneral1430EarlyClose1925 = Holiday(
    'Former NYSE President Seymour L. Cromwell Funeral 2:30pm Early Close Sept 18, 1925',
    month=9,
    day=18,
    start_date=Timestamp('1925-09-18'),
    end_date=Timestamp('1925-09-18'),
)

# 1927
LindberghParade1927 = [Timestamp('1927-06-13', tz='UTC')]

# 1928
BacklogRelief1928 = [
    Timestamp('1928-04-07', tz='UTC'),
    Timestamp('1928-04-21', tz='UTC'),
    Timestamp('1928-05-05', tz='UTC'),
    Timestamp('1928-05-12', tz='UTC'),
    Timestamp('1928-05-19', tz='UTC'),
    Timestamp('1928-05-26', tz='UTC'),
    Timestamp('1928-11-24', tz='UTC'),
]

BacklogRelief2pmEarlyClose1928 =  date_range('1928-05-21', 
                                          '1928-05-25', 
                                          freq=CustomBusinessDay(weekmask = 'Mon Tue Wed Thu Fri Sat'),
                                          tz='UTC'
)

# 1929
BacklogRelief1929 = [
    Timestamp('1929-02-09', tz='UTC'),
    Timestamp('1929-11-01', tz='UTC'),
    Timestamp('1929-11-02', tz='UTC'),
    Timestamp('1929-11-09', tz='UTC'),
    Timestamp('1929-11-16', tz='UTC'),
    Timestamp('1929-11-23', tz='UTC'),
    Timestamp('1929-11-29', tz='UTC'),
    Timestamp('1929-11-30', tz='UTC'),
]

BacklogRelief1pmEarlyClose1929 = [
    Timestamp('1929-11-06', tz='UTC'),
    Timestamp('1929-11-07', tz='UTC'),
    Timestamp('1929-11-08', tz='UTC'),
    Timestamp('1929-11-11', tz='UTC'),
    Timestamp('1929-11-12', tz='UTC'),
    Timestamp('1929-11-13', tz='UTC'),
    Timestamp('1929-11-14', tz='UTC'),
    Timestamp('1929-11-15', tz='UTC'),
    Timestamp('1929-11-18', tz='UTC'),
    Timestamp('1929-11-19', tz='UTC'),
    Timestamp('1929-11-20', tz='UTC'),
    Timestamp('1929-11-21', tz='UTC'),
    Timestamp('1929-11-22', tz='UTC')
]

BacklogRelief12pmLateOpen1929 = [
    Timestamp('1929-10-31', tz='UTC'),
]

# 1930
TaftFuneral1230EarlyClose1930 = Holiday(
    'Former President William Howard Taft Funeral 12:30pm Early Close Mar 11, 1930',
    month=3,
    day=11,
    start_date=Timestamp('1930-03-11'),
    end_date=Timestamp('1930-03-11'),
)

# 1933
CoolidgeFuneral1933 = [Timestamp('1933-01-07', tz='UTC'),]

BankHolidays1933 = [
    Timestamp('1933-03-04', tz='UTC'),
    Timestamp('1933-03-06', tz='UTC'),
    Timestamp('1933-03-07', tz='UTC'),
    Timestamp('1933-03-08', tz='UTC'),
    Timestamp('1933-03-09', tz='UTC'),
    Timestamp('1933-03-10', tz='UTC'),
    Timestamp('1933-03-11', tz='UTC'),
    Timestamp('1933-03-12', tz='UTC'),
    Timestamp('1933-03-13', tz='UTC'),
    Timestamp('1933-03-14', tz='UTC'),
]

GasFumesOnTradingFloor1230EarlyClose1933 = Holiday(
    'Gas Fumes on Trading Floor 12:30pm Early Close Aug 4, 1933',
    month=8,
    day=4,
    start_date=Timestamp('1933-08-04'),
    end_date=Timestamp('1933-08-04'),
)


HeavyVolume1933 = [
    Timestamp('1933-07-29', tz='UTC'),
    Timestamp('1933-08-05', tz='UTC'),
    Timestamp('1933-08-12', tz='UTC'),
    Timestamp('1933-08-19', tz='UTC'),
    Timestamp('1933-08-26', tz='UTC'),
    Timestamp('1933-09-02', tz='UTC'),
]


HeavyVolume12pmLateOpen1933 = [
    Timestamp('1933-07-24', tz='UTC'),
    Timestamp('1933-07-25', tz='UTC'),
]

HeavyVolume11amLateOpen1933 = [
    Timestamp('1933-07-26', tz='UTC'),
    Timestamp('1933-07-27', tz='UTC'),
    Timestamp('1933-07-28', tz='UTC'),
]

HeavyVolume2pmEarlyClose1933 = [
    Timestamp('1933-07-26', tz='UTC'),
    Timestamp('1933-07-27', tz='UTC'),
    Timestamp('1933-07-28', tz='UTC'),
]

NRAdemonstration12pmEarlyClose1933 = Holiday(
    'NRA Demonstration 12:00 noon Early Close Sept 13, 1933',
    month=9,
    day=13,
    start_date=Timestamp('1933-09-13'),
    end_date=Timestamp('1933-09-13'),
)

# 1934
Snow11amLateOpen1934 = Holiday(
    'Severe Snowstorm 11:00am late open Feb 20, 1934',
    month=2,
    day=20,
    start_date=Timestamp('1934-02-20'),
    end_date=Timestamp('1934-02-20'),
)

# 1936
KingGeorgeVFuneral11amLateOpen1936 = Holiday(
    'King George V of England 11:00am late open Jan 28, 1936',
    month=1,
    day=28,
    start_date=Timestamp('1936-01-28'),
    end_date=Timestamp('1936-01-28'),
)

# 1944
SatClosings1944 = [
    Timestamp('1944-08-19', tz='UTC'),
    Timestamp('1944-08-26', tz='UTC'),
    Timestamp('1944-09-02', tz='UTC'),
]

# 1945
RooseveltDayOfMourning1945 = [Timestamp('1945-04-14', tz='UTC'),]

    # Starting in 1945, no Saturday trading over the summer
SatClosings1945 = date_range('1945-07-07', 
                             '1945-09-01', 
                             freq='W-SAT',
                             tz='UTC')

VJday1945 = [
    Timestamp('1945-08-15', tz='UTC'),
    Timestamp('1945-08-16', tz='UTC'),
]

NavyDay1945 = [
    Timestamp('1945-10-27', tz='UTC'),
]

RailroadStrike1946 = [
    Timestamp('1946-05-25', tz='UTC'),
]

# 1946
SatClosings1946 = date_range('1946-06-01', 
                             '1946-09-28', 
                             freq='W-SAT',
                             tz='UTC'
)

# 1947
SatClosings1947 = date_range('1947-05-31', 
                             '1947-09-27', 
                             freq='W-SAT',
                             tz='UTC'
)

# 1948
SevereWeather1948 = [
    Timestamp('1948-01-03', tz='UTC'),
]

SatClosings1948 = date_range('1948-05-29', 
                             '1948-09-25', 
                             freq='W-SAT',
                             tz='UTC'
)

# 1949
SatClosings1949 = date_range('1949-05-28', 
                             '1949-09-24', 
                             freq='W-SAT',
                             tz='UTC'
)

# 1950
SatClosings1950 = date_range('1950-06-03', 
                             '1950-09-30', 
                             freq='W-SAT',
                             tz='UTC'
)

# 1951
SatClosings1951 = date_range('1951-06-02', 
                             '1951-09-29', 
                             freq='W-SAT',
                             tz='UTC'
)

# 1952
SatClosings1952 = date_range('1952-05-31', 
                             '1952-09-27', 
                             freq='W-SAT',
                             tz='UTC'
)

# 1960
Snow11amLateOpening1960 = Holiday(
    'Severe Snow 11am Late Opening on Dec 12, 1960',
    month=12,
    day=12,
    start_date=Timestamp('1960-12-12'),
    end_date=Timestamp('1960-12-12'),
)

# 1963
KennedyAssassination1407EarlyClose = Holiday(
    'President John F. Kennedy Assassination',
    month=11,
    day=22,
    start_date=Timestamp('1963-11-22'),
    end_date=Timestamp('1963-11-22'),
)

KennedyFuneral1963 = [Timestamp('1963-11-25', tz='UTC')]

# 1964
HooverFuneral1400EarlyClose1964 = Holiday(
    'Former President Herbert C. Hoover Funeral',
    month=10,
    day=23,
    start_date=Timestamp('1964-10-23'),
    end_date=Timestamp('1964-10-23'),
)

# 1965
PowerFail1105LateOpen = Holiday(
    'Power Failure in NY grid supply',
    month=11,
    day=10,
    start_date=Timestamp('1965-11-10'),
    end_date=Timestamp('1965-11-10'),
)

# 1966
TransitStrike2pmEarlyClose1966 = date_range('1966-01-06', '1966-01-14', 
                 freq=CustomBusinessDay(weekmask = 'Mon Tue Wed Thu Fri'),
                 tz='UTC')

# 1967
Snow1015LateOpen1967 = Holiday(
    'Late Open due to snow',
    month=2,
    day=7,
    start_date=Timestamp('1967-02-07'),
    end_date=Timestamp('1967-02-07'),
)
Snow2pmEarlyClose1967 = Holiday(
    'Late Open due to snow',
    month=2,
    day=7,
    start_date=Timestamp('1967-02-07'),
    end_date=Timestamp('1967-02-07'),
)
Backlog2pmEarlyCloses1967 =  date_range('1967-08-09', '1967-08-18', 
                 freq=CustomBusinessDay(weekmask = 'Mon Tue Wed Thu Fri'),
                 tz='UTC')

# 1968
Backlog2pmEarlyCloses1968 =  date_range('1968-01-22', '1968-03-01', 
                  freq=CustomBusinessDay(weekmask = 'Mon Tue Wed Thu Fri'),
                  tz='UTC')


MLKdayOfMourning1968 = [Timestamp('1968-04-09', tz='UTC'),]


PaperworkCrisis1968 = [Timestamp('1968-06-12', tz='UTC'),
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
                     Timestamp('1968-11-20', tz='UTC'),
                     Timestamp('1968-12-04', tz='UTC'),
                     Timestamp('1968-12-11', tz='UTC'),
                     Timestamp('1968-12-18', tz='UTC'),]


# 1969
PaperworkCrisis2pmEarlyCloses1969 =  date_range('1969-01-01', '1969-07-03', 
                 freq=CustomBusinessDay(weekmask = 'Mon Tue Wed Thu Fri'),
                 tz='UTC')

SnowClosing1969 = [Timestamp('1969-02-10', tz='UTC')]

Snow11amLateOpen1969 = Holiday(
    'Late Open due to snow',
    month=2,
    day=11,
    start_date=Timestamp('1969-02-11'),
    end_date=Timestamp('1969-02-11'),
)

EisenhowerFuneral1969 = [Timestamp('1969-03-31', tz='UTC'),]

Storm1045LateOpen1969 = Holiday(
    'Late Open due to storm',
    month=6,
    day=2,
    start_date=Timestamp('1969-06-02'),
    end_date=Timestamp('1969-06-02'),
)

PaperworkCrisis230pmEarlyCloses1969 =  date_range('1969-07-07', '1969-09-26', 
                 freq=CustomBusinessDay(weekmask = 'Mon Tue Wed Thu Fri'),
                 tz='UTC')

FirstLunarLandingClosing1969 = [Timestamp('1969-07-21', tz='UTC')]

PaperworkCrisis3pmEarlyCloses1969to1970 =  date_range('1969-09-29', '1970-05-01', 
                 freq=CustomBusinessDay(weekmask = 'Mon Tue Wed Thu Fri'),
                 tz='UTC')

# 1972
TrumanFuneral1972 = [Timestamp('1972-12-28', tz='UTC'),]

# 1973
JohnsonFuneral1973 = [Timestamp('1973-01-25', tz='UTC'),]

Ice11amLateOpen1973 = Holiday(
    'Late Open due to storm',
    month=12,
    day=17,
    start_date=Timestamp('1973-12-17'),
    end_date=Timestamp('1973-12-17'),
)

# 1974
MerrillLynchComputer1015LateOpen1974 = Holiday(
    'Late Open due to Merrill Lynch Computer trouble',
    month=1,
    day=16,
    start_date=Timestamp('1974-01-16'),
    end_date=Timestamp('1974-01-16'),
)
FireDrill1015LateOpen1974 = Holiday(
    'Late Open due to Merrill Lynch Computer trouble',
    month=11,
    day=22,
    start_date=Timestamp('1974-11-22'),
    end_date=Timestamp('1974-11-22'),
)

# 1975
Snow230EarlyClose1975 = Holiday(
    'Early Close at 2:30pm due to snow',
    month=2,
    day=12,
    start_date=Timestamp('1975-02-12'),
    end_date=Timestamp('1975-02-12'),
)

# 1976
Storm1115LateOpen1976 = Holiday(
    'Late Open 11:15am due to storm',
    month=2,
    day=2,
    start_date=Timestamp('1976-02-02'),
    end_date=Timestamp('1976-02-02'),
)

FireDrill1015LateOpen1976 = Holiday(
    'Late Open 10:15am due to fire drill',
    month=6,
    day=8,
    start_date=Timestamp('1976-06-08'),
    end_date=Timestamp('1976-06-08'),
)

HurricaneWatch3pmEarlyClose1976 = Holiday(
    'Early Close 3pm for Hurricane Watch',
    month=8,
    day=9,
    start_date=Timestamp('1976-08-09'),
    end_date=Timestamp('1976-08-09'),
)

# 1977
NewYorkCityBlackout77 = [Timestamp('1977-07-14', tz='UTC')]

# 1978
Snow12pmLateOpen1978 = Holiday(
    'Late Open due to snow',
    month=1,
    day=20,
    start_date=Timestamp('1978-01-20'),
    end_date=Timestamp('1978-01-20'),
)

Snow2pmEarlyClose1978 = Holiday(
    'Early close due to snow',
    month=2,
    day=6,
    start_date=Timestamp('1978-02-06'),
    end_date=Timestamp('1978-02-06'),
)

Snow11amLateOpen1978 = Holiday(
    'Late Open due to snow',
    month=2,
    day=7,
    start_date=Timestamp('1978-02-07'),
    end_date=Timestamp('1978-02-07'),
)

# 1981
ReaganAssassAttempt317pmEarlyClose1981 = Holiday(
    'President Reagan Assassination Attempt',
    month=3,
    day=30,
    start_date=Timestamp('1981-03-30'),
    end_date=Timestamp('1981-03-30'),
)

ConEdPowerFail328pmEarlyClose1981 = Holiday(
    'Con Edison power failure',
    month=9,
    day=9,
    start_date=Timestamp('1981-09-09'),
    end_date=Timestamp('1981-09-09'),
)

# http://en.wikipedia.org/wiki/Hurricane_Gloria
HurricaneGloriaClosings1985= [Timestamp('1985-09-27', tz='UTC')]


# 1987
Backlog2pmEarlyCloses1987   = date_range('1987-10-23', '1987-10-30', tz='UTC') 
Backlog230pmEarlyCloses1987 = date_range('1987-11-02', '1987-11-04', tz='UTC')
Backlog3pmEarlyCloses1987   = date_range('1987-11-05', '1987-11-06', tz='UTC') 
Backlog330pmEarlyCloses1987 = date_range('1987-11-09', '1987-11-11', tz='UTC') 

# 1989
Fire11amLateOpen1989 = Holiday(
    'Electrical Fire',
    month=11,
    day=10,
    start_date=Timestamp('1989-11-10'),
    end_date=Timestamp('1989-11-10'),
)

# 1990

ConEdXformer931amLateOpen1990 = Holiday(
    'Con Edison transformer explosion',
    month=12,
    day=27,
    start_date=Timestamp('1990-12-27'),
    end_date=Timestamp('1990-12-27'),
)

# 1991
TroopsInGulf931LateOpens1991 = [
    Timestamp("1991-01-17", tz='UTC'),
    Timestamp("1991-02-25", tz='UTC')
]

# 1994
Snow230pmEarlyClose1994 = Holiday(
    'Snowstorm',
    month=2,
    day=11,
    start_date=Timestamp('1994-02-11'),
    end_date=Timestamp('1994-02-11'),
)

NixonFuneral1994 = [Timestamp('1994-04-27', tz='UTC'),]

# 1995
Computer1030LateOpen1995 = Holiday(
    'Computer Systems Troubles',
    month=12,
    day=18,
    start_date=Timestamp('1995-12-18'),
    end_date=Timestamp('1995-12-18'),
)

# 1996
Snow11amLateOpen1996 = Holiday(
    'Snow',
    month=1,
    day=8,
    start_date=Timestamp('1996-01-08'),
    end_date=Timestamp('1996-01-08'),
)

Snow2pmEarlyClose1996 = Holiday(
    'Snow',
    month=1,
    day=8,
    start_date=Timestamp('1996-01-08'),
    end_date=Timestamp('1996-01-08'),
)

CircuitBreakerTriggered330pmEarlyClose1997 =  Holiday(
    'Oct 27 1997 Stock Market Drop Circuit Breaker Triggered',
    month=10,
    day=27,
    start_date=Timestamp('1997-10-27'),
    end_date=Timestamp('1997-10-27'),
)

# 2001
# http://en.wikipedia.org/wiki/Aftermath_of_the_September_11_attacks
September11Closings2001 = [
    Timestamp("2001-09-11", tz='UTC'),
    Timestamp("2001-09-12", tz='UTC'),
    Timestamp("2001-09-13", tz='UTC'),
    Timestamp("2001-09-14", tz='UTC')
]

Sept11MomentSilence933amLateOpen2001 =  Holiday(
    'Moment of silence for terrorist attacks on 9/11',
    month=9,
    day=17,
    start_date=Timestamp('2001-09-17'),
    end_date=Timestamp('2001-09-17'),
)

EnduringFreedomMomentSilence931amLateOpen2001 =  Holiday(
    'Moment of silence for Enduring Freedom troops',
    month=10,
    day=8,
    start_date=Timestamp('2001-10-08'),
    end_date=Timestamp('2001-10-08'),
)
# 2002
Sept11Anniversary12pmLateOpen2002 =  Holiday(
    '1 year anniversary of terrorist attacks on 9/11',
    month=9,
    day=11,
    start_date=Timestamp('2002-09-11'),
    end_date=Timestamp('2002-09-11'),
)

# 2003
IraqiFreedom932amLateOpen2003 =  Holiday(
    'Operation Iraqi freedom moment of silence',
    month=3,
    day=20,
    start_date=Timestamp('2003-03-20'),
    end_date=Timestamp('2003-03-20'),
)

# 2004
ReaganMomentSilence932amLateOpen2004 =  Holiday(
    'Death of Former President Ronald Reagan moment of silence',
    month=6,
    day=7,
    start_date=Timestamp('2004-06-07'),
    end_date=Timestamp('2004-06-07'),
)

ReaganMourning2004 =  [Timestamp('2004-06-11', tz="UTC")]

# 2005
SystemProb356pmEarlyClose2005 =  Holiday(
    'Systems Communication Problem',
    month=6,
    day=1,
    start_date=Timestamp('2005-06-01'),
    end_date=Timestamp('2005-06-01'),
)

# 2006
FordMomentSilence932amLateOpen2006 =  Holiday(
    'Former President Gerald Ford moment of silence',
    month=12,
    day=27,
    start_date=Timestamp('2006-12-27'),
    end_date=Timestamp('2006-12-27'),
)

# 2007
FordMourning2007 = [Timestamp('2007-01-02', tz='UTC'),]

# 2012
# http://en.wikipedia.org/wiki/Hurricane_sandy
HurricaneSandyClosings2012 = [Timestamp('2012-10-29', tz='UTC'),
                              Timestamp('2012-10-30', tz='UTC')]

# 2018
GeorgeHWBushDeath2018 = [Timestamp('2018-12-05', tz='UTC'),]

