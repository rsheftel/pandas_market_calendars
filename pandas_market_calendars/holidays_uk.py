# UK Holidays

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

# Early May bank holiday
MayBank = Holiday(
    "Early May Bank Holiday",
    month=5,
    offset=DateOffset(weekday=MO(1)),
    day=1,
)

# Spring bank holiday
SpringBank = Holiday(
    "Spring Bank Holiday",
    month=5,
    day=31,
    offset=DateOffset(weekday=MO(-1)),
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

BankHoliday = [Timestamp('2012-06-04', tz='UTC')]

QueensJubilee = [Timestamp('2012-06-05', tz='UTC')]
