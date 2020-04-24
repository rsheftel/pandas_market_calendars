# OZ Holidays

from pandas import DateOffset
from pandas.tseries.holiday import Holiday, MO, weekend_to_monday

from pandas_market_calendars.market_calendar import MONDAY, TUESDAY

# New Year's Day
OZNewYearsDay = Holiday(
    "New Year's Day",
    month=1,
    day=1,
    observance=weekend_to_monday,
)

# Australia Day
AustraliaDay = Holiday(
    "Australia Day",
    month=1,
    day=27,
    observance=weekend_to_monday,
)

# ANZAC Day
AnzacDay = Holiday(
    "ANZAC Day",
    month=4,
    day=25,
)

# Queen's Birthday
QueensBirthday = Holiday(
    "Queen's Birthday",
    month=6,
    day=1,
    offset=DateOffset(weekday=MO(2)),
)

# Christmas
Christmas = Holiday(
    "Christmas",
    month=12,
    day=25,
    observance=weekend_to_monday,
)


# Boxing day
BoxingDay = Holiday(
    "Boxing Day",
    month=12,
    day=26,
)

# If boxing day is saturday then Monday 28th is a holiday
# If boxing day is sunday then Tuesday 28th is a holiday
WeekendBoxingDay = Holiday(
    "Weekend Boxing Day",
    month=12,
    day=28,
    days_of_week=(MONDAY, TUESDAY),
)
