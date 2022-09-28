# UK Holidays

import pandas as pd
from pandas import DateOffset, Timestamp
from pandas.tseries.holiday import Holiday, MO, previous_friday, weekend_to_monday

from pandas_market_calendars.market_calendar import MONDAY, TUESDAY

# New Year's Eve
LSENewYearsEve = Holiday(
    "New Year's Eve",
    month=12,
    day=31,
    observance=previous_friday,
)

# New Year's Day
LSENewYearsDay = Holiday(
    "New Year's Day",
    month=1,
    day=1,
    observance=weekend_to_monday,
)

# Early May bank holiday has two exceptions based on the 50th and 75th anniversary of VE-Day
# 1995-05-01 Early May bank holiday removed for VE-day 50th anniversary
# 2020-05-04 Early May bank holiday removed for VE-day 75th anniversary

# Early May bank holiday pre-1995
MayBank_pre_1995 = Holiday(
    "Early May Bank Holiday",
    month=5,
    offset=DateOffset(weekday=MO(1)),
    day=1,
    end_date=Timestamp('1994-12-31'),
)

# Early May bank holiday post-1995 and pre-2020
MayBank_post_1995_pre_2020 = Holiday(
    "Early May Bank Holiday",
    month=5,
    offset=DateOffset(weekday=MO(1)),
    day=1,
    start_date=Timestamp('1996-01-01'),
    end_date=Timestamp('2019-12-31'),
)

# Early May bank holiday post 2020
MayBank_post_2020 = Holiday(
    "Early May Bank Holiday",
    month=5,
    offset=DateOffset(weekday=MO(1)),
    day=1,
    start_date=Timestamp('2021-01-01')
)

# Spring bank holiday has two exceptions based on the Golden & Diamond Jubilee
# 2002-05-27 Spring bank holiday removed for Golden Jubilee
# 2012-05-28 Spring bank holiday removed for Diamond Jubilee
# 2022-05-31 Spring bank holiday removed for Platinum Jubilee

# Spring bank holiday
SpringBank_pre_2002 = Holiday(
    "Spring Bank Holiday",
    month=5,
    day=31,
    offset=DateOffset(weekday=MO(-1)),
    end_date=Timestamp('2001-12-31'),
)

SpringBank_post_2002_pre_2012 = Holiday(
    "Spring Bank Holiday",
    month=5,
    day=31,
    offset=DateOffset(weekday=MO(-1)),
    start_date=Timestamp('2003-01-01'),
    end_date=Timestamp('2011-12-31'),
)

SpringBank_post_2012_pre_2022 = Holiday(
    "Spring Bank Holiday",
    month=5,
    day=31,
    offset=DateOffset(weekday=MO(-1)),
    start_date=Timestamp('2013-01-01'),
    end_date=Timestamp('2021-12-31'),
)

SpringBank_post_2022 = Holiday(
    "Spring Bank Holiday",
    month=5,
    day=31,
    offset=DateOffset(weekday=MO(-1)),
    start_date=Timestamp('2022-01-01'),
)

# Summer bank holiday
SummerBank = Holiday(
    "Summer Bank Holiday",
    month=8,
    day=31,
    offset=DateOffset(weekday=MO(-1)),
)

# Christmas Eve
ChristmasEve = Holiday(
    'Christmas Eve',
    month=12,
    day=24,
    observance=previous_friday,
)

# Christmas
Christmas = Holiday(
    "Christmas",
    month=12,
    day=25,
)

# If christmas day is Saturday Monday 27th is a holiday
# If christmas day is sunday the Tuesday 27th is a holiday
WeekendChristmas = Holiday(
    "Weekend Christmas",
    month=12,
    day=27,
    days_of_week=(MONDAY, TUESDAY),
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

# One-off holiday additions and removals in England

UniqueCloses = []
# VE-Day Anniversary
UniqueCloses.append(pd.Timestamp("1995-05-08", tz='UTC'))  # 50th Anniversary
UniqueCloses.append(pd.Timestamp("2020-05-08", tz='UTC'))  # 75th Anniversary

# Queen Elizabeth II Jubilees
# Silver Jubilee
UniqueCloses.append(pd.Timestamp("1977-06-07", tz='UTC'))

# Golden Jubilee
UniqueCloses.append(pd.Timestamp("2002-06-03", tz='UTC'))
UniqueCloses.append(pd.Timestamp("2002-06-04", tz='UTC'))

# Diamond Jubilee
UniqueCloses.append(pd.Timestamp("2012-06-04", tz='UTC'))
UniqueCloses.append(pd.Timestamp("2012-06-05", tz='UTC'))

# Platinum Jubilee
UniqueCloses.append(pd.Timestamp("2022-06-02", tz='UTC'))
UniqueCloses.append(pd.Timestamp("2022-06-03", tz='UTC'))

# State Funeral of Queen Elizabeth II
UniqueCloses.append(pd.Timestamp("2022-09-19", tz='UTC'))

# Royal Weddings
UniqueCloses.append(pd.Timestamp("1973-11-14", tz='UTC'))     # Wedding Day of Princess Anne and Mark Phillips
UniqueCloses.append(pd.Timestamp("1981-07-29", tz='UTC'))     # Wedding Day of Prince Charles and Diana Spencer
UniqueCloses.append(pd.Timestamp("2011-04-29", tz='UTC'))     # Wedding Day of Prince William and Catherine Middleton

# Miscellaneous
UniqueCloses.append(pd.Timestamp("1999-12-31", tz='UTC'))     # Eve of 3rd Millenium A.D.
