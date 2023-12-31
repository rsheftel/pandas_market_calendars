from dateutil.relativedelta import MO, TH, TU
from pandas import DateOffset, Timestamp, date_range
from pandas.tseries.holiday import Holiday, nearest_workday, sunday_to_monday
from pandas.tseries.offsets import Day

from pandas_market_calendars.market_calendar import (
    FRIDAY,
    MONDAY,
    THURSDAY,
    TUESDAY,
    WEDNESDAY,
)


# These have the same definition, but are used in different places because the
# NYSE closed at 2:00 PM on Christmas Eve until 1993.


def following_tuesday_every_four_years_observance(dt):
    return dt + DateOffset(years=(4 - (dt.year % 4)) % 4, weekday=TU(1))


ChristmasEveBefore1993 = Holiday(
    "Christmas Eve",
    month=12,
    day=24,
    end_date=Timestamp("1993-01-01"),
    # When Christmas is a Saturday, the 24th is a full holiday.
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY),
)
ChristmasEveInOrAfter1993 = Holiday(
    "Christmas Eve",
    month=12,
    day=24,
    start_date=Timestamp("1993-01-01"),
    # When Christmas is a Saturday, the 24th is a full holiday.
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY),
)
USNewYearsDay = Holiday(
    "New Years Day",
    month=1,
    day=1,
    # When Jan 1 is a Sunday, US markets observe the subsequent Monday.
    # When Jan 1 is a Saturday (as in 2005 and 2011), no holiday is observed.
    observance=sunday_to_monday,
)
USMartinLutherKingJrAfter1998 = Holiday(
    "Dr. Martin Luther King Jr. Day",
    month=1,
    day=1,
    # The US markets didn't observe MLK day as a holiday until 1998.
    start_date=Timestamp("1998-01-01"),
    offset=DateOffset(weekday=MO(3)),
)
USLincolnsBirthDayBefore1954 = Holiday(
    "Lincoln" "s Birthday",
    month=2,
    day=12,
    start_date=Timestamp("1874-01-01"),
    end_date=Timestamp("1953-12-31"),
    observance=sunday_to_monday,
)
USWashingtonsBirthDayBefore1964 = Holiday(
    "Washington" "s Birthday",
    month=2,
    day=22,
    start_date=Timestamp("1880-01-01"),
    end_date=Timestamp("1963-12-31"),
    observance=sunday_to_monday,
)
USWashingtonsBirthDay1964to1970 = Holiday(
    "Washington" "s Birthday",
    month=2,
    day=22,
    start_date=Timestamp("1964-01-01"),
    end_date=Timestamp("1970-12-31"),
    observance=nearest_workday,
)
USPresidentsDay = Holiday(
    "President" "s Day",
    start_date=Timestamp("1971-01-01"),
    month=2,
    day=1,
    offset=DateOffset(weekday=MO(3)),
)
# http://www.tradingtheodds.com/nyse-full-day-closings/
USThanksgivingDayBefore1939 = Holiday(
    "Thanksgiving Before 1939",
    start_date=Timestamp("1864-01-01"),
    end_date=Timestamp("1938-12-31"),
    month=11,
    day=30,
    offset=DateOffset(weekday=TH(-1)),
)
# http://www.tradingtheodds.com/nyse-full-day-closings/
USThanksgivingDay1939to1941 = Holiday(
    "Thanksgiving 1939 to 1941",
    start_date=Timestamp("1939-01-01"),
    end_date=Timestamp("1941-12-31"),
    month=11,
    day=30,
    offset=DateOffset(weekday=TH(-2)),
)
USThanksgivingDay = Holiday(
    "Thanksgiving",
    start_date=Timestamp("1942-01-01"),
    month=11,
    day=1,
    offset=DateOffset(weekday=TH(4)),
)
# http://www.tradingtheodds.com/nyse-full-day-closings/
USMemorialDayBefore1964 = Holiday(
    "Memorial Day",
    month=5,
    day=30,
    end_date=Timestamp("1963-12-31"),
    observance=sunday_to_monday,
)
# http://www.tradingtheodds.com/nyse-full-day-closings/
USMemorialDay1964to1969 = Holiday(
    "Memorial Day",
    month=5,
    day=30,
    start_date=Timestamp("1964-01-01"),
    end_date=Timestamp("1969-12-31"),
    observance=nearest_workday,
)
USMemorialDay = Holiday(
    # NOTE: The definition for Memorial Day is incorrect as of pandas 0.16.0.
    # See https://github.com/pydata/pandas/issues/9760.
    "Memorial Day",
    month=5,
    day=25,
    start_date=Timestamp("1971-01-01"),
    offset=DateOffset(weekday=MO(1)),
)
# http://www.tradingtheodds.com/nyse-full-day-closings/
USIndependenceDayBefore1954 = Holiday(
    "July 4th",
    month=7,
    day=4,
    end_date=Timestamp("1953-12-31"),
    observance=sunday_to_monday,
)
USIndependenceDay = Holiday(
    "July 4th",
    month=7,
    day=4,
    start_date=Timestamp("1954-01-01"),
    observance=nearest_workday,
)
# http://www.tradingtheodds.com/nyse-full-day-closings/
USElectionDay1848to1967 = Holiday(
    "Election Day",
    month=11,
    day=2,
    start_date=Timestamp("1848-1-1"),
    end_date=Timestamp("1967-12-31"),
    offset=DateOffset(weekday=TU(1)),
)
# http://www.tradingtheodds.com/nyse-full-day-closings/
USElectionDay1968to1980 = Holiday(
    "Election Day",
    month=11,
    day=2,
    start_date=Timestamp("1968-01-01"),
    end_date=Timestamp("1980-12-31"),
    observance=following_tuesday_every_four_years_observance,
)
# http://www.tradingtheodds.com/nyse-full-day-closings/
USVeteransDay1934to1953 = Holiday(
    "Veteran Day",
    month=11,
    day=11,
    start_date=Timestamp("1934-1-1"),
    end_date=Timestamp("1953-12-31"),
    observance=sunday_to_monday,
)
# http://www.tradingtheodds.com/nyse-full-day-closings/
USColumbusDayBefore1954 = Holiday(
    "Columbus Day",
    month=10,
    day=12,
    end_date=Timestamp("1953-12-31"),
    observance=sunday_to_monday,
)
ChristmasBefore1954 = Holiday(
    "Christmas",
    month=12,
    day=25,
    end_date=Timestamp("1953-12-31"),
    observance=sunday_to_monday,
)
Christmas = Holiday(
    "Christmas",
    month=12,
    day=25,
    start_date=Timestamp("1954-01-01"),
    observance=nearest_workday,
)

MonTuesThursBeforeIndependenceDay = Holiday(
    # When July 4th is a Tuesday, Wednesday, or Friday, the previous day is a
    # half day.
    "Mondays, Tuesdays, and Thursdays Before Independence Day",
    month=7,
    day=3,
    days_of_week=(MONDAY, TUESDAY, THURSDAY),
    start_date=Timestamp("1995-01-01"),
)
FridayAfterIndependenceDayPre2013 = Holiday(
    # When July 4th is a Thursday, the next day is a half day prior to 2013.
    # Since 2013 the early close is on Wednesday and Friday is a full day
    "Fridays after Independence Day prior to 2013",
    month=7,
    day=5,
    days_of_week=(FRIDAY,),
    start_date=Timestamp("1995-01-01"),
    end_date=Timestamp("2012-12-31"),
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
USBlackFridayBefore1993 = Holiday(
    "Black Friday",
    month=11,
    day=1,
    # Black Friday was not observed until 1992.
    start_date=Timestamp("1992-01-01"),
    end_date=Timestamp("1993-01-01"),
    offset=[DateOffset(weekday=TH(4)), Day(1)],
)
USBlackFridayInOrAfter1993 = Holiday(
    "Black Friday",
    month=11,
    day=1,
    start_date=Timestamp("1993-01-01"),
    offset=[DateOffset(weekday=TH(4)), Day(1)],
)
BattleOfGettysburg = Holiday(
    # All of the floor traders in Chicago were sent to PA
    "Markets were closed during the battle of Gettysburg",
    month=7,
    day=(1, 2, 3),
    start_date=Timestamp("1863-07-01"),
    end_date=Timestamp("1863-07-03"),
)

# http://www.tradingtheodds.com/nyse-full-day-closings/
November29BacklogRelief = [
    Timestamp("1929-11-01", tz="UTC"),
    Timestamp("1929-11-29", tz="UTC"),
]

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
August45VictoryOverJapan = date_range("1945-08-15", "1945-08-16", tz="UTC")

# http://www.tradingtheodds.com/nyse-full-day-closings/
ChristmasEvesAdhoc = [
    Timestamp("1945-12-24", tz="UTC"),
    Timestamp("1956-12-24", tz="UTC"),
]

# http://www.tradingtheodds.com/nyse-full-day-closings/
DayAfterChristmasAdhoc = [Timestamp("1958-12-26", tz="UTC")]

# http://www.tradingtheodds.com/nyse-full-day-closings/
DayBeforeDecorationAdhoc = [Timestamp("1961-05-29", tz="UTC")]

# http://www.tradingtheodds.com/nyse-full-day-closings/
LincolnsBirthDayAdhoc = [Timestamp("1968-02-12", tz="UTC")]

# http://www.tradingtheodds.com/nyse-full-day-closings/
PaperworkCrisis68 = [
    Timestamp("1968-06-12", tz="UTC"),
    Timestamp("1968-06-19", tz="UTC"),
    Timestamp("1968-06-26", tz="UTC"),
    Timestamp("1968-07-10", tz="UTC"),
    Timestamp("1968-07-17", tz="UTC"),
    Timestamp("1968-07-24", tz="UTC"),
    Timestamp("1968-07-31", tz="UTC"),
    Timestamp("1968-08-07", tz="UTC"),
    Timestamp("1968-08-14", tz="UTC"),
    Timestamp("1968-08-21", tz="UTC"),
    Timestamp("1968-08-28", tz="UTC"),
    Timestamp("1968-09-11", tz="UTC"),
    Timestamp("1968-09-18", tz="UTC"),
    Timestamp("1968-09-25", tz="UTC"),
    Timestamp("1968-10-02", tz="UTC"),
    Timestamp("1968-10-09", tz="UTC"),
    Timestamp("1968-10-16", tz="UTC"),
    Timestamp("1968-10-23", tz="UTC"),
    Timestamp("1968-10-30", tz="UTC"),
    Timestamp("1968-11-11", tz="UTC"),
    Timestamp("1968-11-20", tz="UTC"),
    Timestamp("1968-12-04", tz="UTC"),
    Timestamp("1968-12-11", tz="UTC"),
    Timestamp("1968-12-18", tz="UTC"),
    Timestamp("1968-12-25", tz="UTC"),
]

# http://www.tradingtheodds.com/nyse-full-day-closings/
DayAfterIndependenceDayAdhoc = [Timestamp("1968-07-05", tz="UTC")]

# http://www.tradingtheodds.com/nyse-full-day-closings/
WeatherSnowClosing = [Timestamp("1969-02-10", tz="UTC")]

# http://www.tradingtheodds.com/nyse-full-day-closings/
FirstLunarLandingClosing = [Timestamp("1969-07-21", tz="UTC")]

# http://www.tradingtheodds.com/nyse-full-day-closings/
NewYorkCityBlackout77 = [Timestamp("1977-07-14", tz="UTC")]

# http://en.wikipedia.org/wiki/Aftermath_of_the_September_11_attacks
September11Closings = [
    Timestamp("2001-09-11", tz="UTC"),
    Timestamp("2001-09-12", tz="UTC"),
    Timestamp("2001-09-13", tz="UTC"),
    Timestamp("2001-09-14", tz="UTC"),
]

# http://en.wikipedia.org/wiki/Hurricane_Gloria
HurricaneGloriaClosings = date_range("1985-09-27", "1985-09-27", tz="UTC")

# http://en.wikipedia.org/wiki/Hurricane_sandy
HurricaneSandyClosings = date_range("2012-10-29", "2012-10-30", tz="UTC")

# National Days of Mourning
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
    Timestamp("1963-11-25", tz="UTC"),
    Timestamp("1968-04-09", tz="UTC"),
    Timestamp("1969-03-31", tz="UTC"),
    Timestamp("1972-12-28", tz="UTC"),
    Timestamp("1973-01-25", tz="UTC"),
    Timestamp("1994-04-27", tz="UTC"),
    Timestamp("2004-06-11", tz="UTC"),
    Timestamp("2007-01-02", tz="UTC"),
    Timestamp("2018-12-05", tz="UTC"),
]

#######################################
# US Juneteenth (June 19th)
#######################################
USJuneteenthAfter2022 = Holiday(
    "Juneteenth Starting at 2022",
    start_date=Timestamp("2022-06-19"),
    month=6,
    day=19,
    observance=nearest_workday,
)
