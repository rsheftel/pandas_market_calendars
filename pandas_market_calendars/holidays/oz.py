# OZ Holidays

from pandas import DateOffset, Timestamp
from pandas.tseries.holiday import (
    Holiday,
    MO,
    next_monday_or_tuesday,
    weekend_to_monday,
)

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
    day=26,
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
    observance=next_monday_or_tuesday,
)

# One-off holiday additions and removals in Australia

UniqueCloses = []

# National Day of Mourning for Her Majesty the Queen
UniqueCloses.append(Timestamp("2022-09-22", tz="UTC"))
