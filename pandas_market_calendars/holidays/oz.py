# OZ Holidays

from pandas import DateOffset, Timestamp
from pandas.tseries.holiday import (
    MO,
    Holiday,
    next_monday_or_tuesday,
    previous_friday,
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

# Easter Tuesday / Public Holiday, as ANZAC Day fell on Easter Monday
UniqueCloses.append(Timestamp("2011-04-26", tz="UTC"))

# National Day of Mourning for Her Majesty the Queen
UniqueCloses.append(Timestamp("2022-09-22", tz="UTC"))


# Early closes
# Before 2022, a weekend Christmas Eve or New Year's Eve moved the early close to the previous Friday.
# From 2022, there is no early close when it falls on a weekend: ASX traded a full day on
# Friday 23 and 30 December 2022 and Friday 22 and 29 December 2023.

# Christmas Eve
ChristmasEveBefore2022 = Holiday(
    "Christmas Eve",
    month=12,
    day=24,
    end_date=Timestamp("2021-12-31"),
    observance=previous_friday,
)
ChristmasEveInOrAfter2022 = Holiday(
    "Christmas Eve",
    month=12,
    day=24,
    start_date=Timestamp("2022-01-01"),
)

# New Year's Eve
NewYearsEveBefore2022 = Holiday(
    "New Year's Eve",
    month=12,
    day=31,
    end_date=Timestamp("2021-12-31"),
    observance=previous_friday,
)
NewYearsEveInOrAfter2022 = Holiday(
    "New Year's Eve",
    month=12,
    day=31,
    start_date=Timestamp("2022-01-01"),
)
