from dateutil.relativedelta import MO, TH
from pandas import DateOffset, Timestamp
from pandas.tseries.holiday import (
    Holiday,
    nearest_workday,
    next_monday,
    sunday_to_monday,
    previous_workday,
    Easter,
)
from pandas.tseries.offsets import Day

from pandas_market_calendars.market_calendar import (
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
)

####################################################
# US New Years Day Jan 1
# When Jan 1 is a Sunday, US markets observe the subsequent Monday.
# When Jan 1 is a Saturday (as in 2005 and 2011), no holiday is observed.
#####################################################
USNewYearsDay = Holiday(
    "New Years Day US",
    month=1,
    day=1,
    days_of_week=(
        MONDAY,
        TUESDAY,
        WEDNESDAY,
        THURSDAY,
        FRIDAY,
    ),
    observance=sunday_to_monday,
)

USNewYearsEve2pmEarlyClose = Holiday(
    "New Years Eve US",
    month=1,
    day=1,
    days_of_week=(
        MONDAY,
        TUESDAY,
        WEDNESDAY,
        THURSDAY,
        FRIDAY,
    ),
    observance=previous_workday,
)

#########################################################################
# Martin Luther King Jr
##########################################################################
MartinLutherKingJr = Holiday(
    "Dr. Martin Luther King Jr. Day",
    month=1,
    day=1,
    days_of_week=(
        MONDAY,
        TUESDAY,
        WEDNESDAY,
        THURSDAY,
        FRIDAY,
    ),
    offset=DateOffset(weekday=MO(3)),
)

#########################################################################
# US Presidents Day Feb
##########################################################################
USPresidentsDay = Holiday(
    "President" "s Day",
    start_date=Timestamp("1971-01-01"),
    month=2,
    day=1,
    days_of_week=(
        MONDAY,
        TUESDAY,
        WEDNESDAY,
        THURSDAY,
        FRIDAY,
    ),
    offset=DateOffset(weekday=MO(3)),
)

############################################################
# Good Friday
############################################################
GoodFridayThru2020 = Holiday(
    "Good Friday 1908+",
    end_date=Timestamp("2020-12-31"),
    month=1,
    day=1,
    offset=[Easter(), Day(-2)],
)

# 2021 is early close.
# 2022 is a full holiday.
# 2023 is early close.
# 2024 is a full holiday
GoodFridayAdHoc = [
    Timestamp("2022-04-15", tz="UTC"),
    Timestamp("2024-03-29", tz="UTC"),
]

GoodFriday2pmEarlyCloseAdHoc = [
    Timestamp("2021-04-02", tz="UTC"),
    Timestamp("2023-04-07", tz="UTC"),
]

DayBeforeGoodFriday2pmEarlyCloseThru2020 = Holiday(
    "Day Before Good Friday Thru 2020",
    end_date=Timestamp("2020-12-31"),
    month=1,
    day=1,
    offset=[Easter(), Day(-3)],
)

DayBeforeGoodFriday2pmEarlyCloseAdHoc = [
    Timestamp("2022-04-14", tz="UTC"),
    Timestamp("2024-03-28", tz="UTC"),
]

##################################################
# US Memorial Day (Decoration Day) May 30
#    Closed every year since 1873
#    Observed on Monday since 1971
##################################################
USMemorialDay = Holiday(
    "Memorial Day",
    month=5,
    day=25,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
    offset=DateOffset(weekday=MO(1)),
)

DayBeforeUSMemorialDay2pmEarlyClose = Holiday(
    "Day Before Memorial Day",
    month=5,
    day=25,
    offset=[DateOffset(weekday=MO(1)), Day(-3)],
)

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

#######################################
# US Independence Day July 4
#######################################
USIndependenceDay = Holiday(
    "July 4th",
    month=7,
    day=4,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
    observance=nearest_workday,
)

# Day before Independence Day
DayBeforeUSIndependenceDay2pmEarlyClose = Holiday(
    "Day Before Independence Day",
    month=7,
    day=4,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
    observance=previous_workday,
)

# When July 4th is a Saturday, the previous Friday is a holiday
# and the previous Thursday is an early close
ThursdayBeforeUSIndependenceDay2pmEarlyClose = Holiday(
    "Thursday Before Independence Day",
    month=7,
    day=2,
    days_of_week=(THURSDAY,),
)

#################################################
# US Labor Day
#################################################
USLaborDay = Holiday("Labor Day", month=9, day=1, offset=DateOffset(weekday=MO(1)))

#################################################
# Columbus Day
#################################################
USColumbusDay = Holiday(
    "Columbus Day",
    month=10,
    day=1,
    offset=DateOffset(weekday=MO(2)),
)

##########################################################
# Armistice/Veterans day
# When falls on Saturday, no holiday is observed.
# When falls on Sunday, the Monday following is a holiday.
##########################################################
USVeteransDay2022 = Holiday(
    "Veterans Day Prior to 2023",
    month=11,
    day=11,
    end_date=Timestamp("2022-12-31"),
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
    observance=sunday_to_monday,
)

USVeteransDay = Holiday(
    "Veterans Day",
    month=11,
    day=11,
    start_date=Timestamp("2023-12-31"),
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
    observance=sunday_to_monday,
)

################################################
# US Thanksgiving Nov 30
################################################
USThanksgivingDay = Holiday(
    "Thanksgiving", month=11, day=1, offset=DateOffset(weekday=TH(4))
)

DayAfterThanksgiving2pmEarlyClose = Holiday(
    "Black Friday",
    month=11,
    day=1,
    offset=[DateOffset(weekday=TH(4)), Day(1)],
)

################################
# Christmas Dec 25
################################
Christmas = Holiday(
    "Christmas",
    month=12,
    day=25,
    observance=nearest_workday,
)

ChristmasEve2pmEarlyClose = Holiday(
    "Christmas Eve",
    month=12,
    day=25,
    observance=previous_workday,
)

# When Christmas is on a Saturday it is observed on Friday the 24th
# Early close on Thursday 23rd
ChristmasEveThursday2pmEarlyClose = Holiday(
    "Christmas Eve on Thursday",
    month=12,
    day=23,
    days_of_week=(THURSDAY,),
)

############################################################################
# UK Specific Holidays
############################################################################

# Remarkably, in 2022 SIFMA recommended NO new year's day observance in the US (Saturday)
#             but in the UK it was observed on Monday requiring a different rule
UKNewYearsDay = Holiday(
    "New Years Day",
    month=1,
    day=1,
    observance=next_monday,
)

UKGoodFriday = Holiday("Good Friday", month=1, day=1, offset=[Easter(), Day(-2)])

UKEasterMonday = Holiday("Easter Monday", month=1, day=1, offset=[Easter(), Day(+1)])

# Observed first Monday in May
UKMayDay = Holiday(
    "May Day",
    month=5,
    day=1,
    offset=DateOffset(weekday=MO(1)),
)

# Almost always follows US Memorial Day except for
UKSpringBankAdHoc = [
    Timestamp("2022-06-02", tz="UTC"),
]

UKPlatinumJubilee2022 = [
    Timestamp("2022-06-03", tz="UTC"),
]

# Observed last Monday in August in England, Wales, and Northern Ireland
# Observed first Monday in August in Scotland
# Coded as last Monday
# https://www.timeanddate.com/holidays/uk/summer-bank-holiday
UKSummerBank = Holiday(
    "Summer Bank Holiday",
    month=8,
    day=30,
    offset=DateOffset(weekday=MO(-1)),
)

# UK observes Christmas on Tuesday when Boxing Day is on Monday
# UK observes Christmas on Monday when Christmas is on Saturday
UKChristmaEve = Holiday(
    "Christmas",
    month=12,
    day=24,
    days_of_week=(FRIDAY,),
)

UKChristmas = Holiday(
    "Christmas",
    month=12,
    day=25,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
)

# If christmas day is Saturday Monday 27th is a holiday
# If christmas day is sunday the Tuesday 27th is a holiday
UKWeekendChristmas = Holiday(
    "Weekend Christmas",
    month=12,
    day=27,
    days_of_week=(MONDAY, TUESDAY),
)

# Boxing day
UKBoxingDay = Holiday(
    "Boxing Day",
    month=12,
    day=26,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
)

# If boxing day is saturday then Monday 28th is a holiday
# If boxing day is sunday then Tuesday 28th is a holiday
UKWeekendBoxingDay = Holiday(
    "Weekend Boxing Day",
    month=12,
    day=28,
    days_of_week=(MONDAY, TUESDAY),
)
