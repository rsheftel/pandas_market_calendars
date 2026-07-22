from pandas.tseries.holiday import DateOffset, Holiday, MO, Easter, weekend_to_monday, previous_friday
from pandas.tseries.offsets import BusinessDay, Day

NewYears = Holiday("New Years Day", month=1, day=1, observance=weekend_to_monday)


# Ontario Family Day
FamilyDay = Holiday(
    "Family Day",
    month=2,
    day=1,
    offset=DateOffset(weekday=MO(3)),
    start_date="2008-01-01",
)
DayBeforeFamilyDay = Holiday(
    "Family Day",
    month=2,
    day=1,
    offset=[DateOffset(weekday=MO(3)), BusinessDay(-1)],
    start_date="2008-01-01",
)

# Victoria Day
# https://www.timeanddate.com/holidays/canada/victoria-day
VictoriaDay = Holiday(
    "Victoria Day",
    month=5,
    day=24,
    offset=DateOffset(weekday=MO(-1)),
)
DayBeforeVictoriaDay = Holiday(
    "Victoria Day",
    month=5,
    day=24,
    offset=[DateOffset(weekday=MO(-1)), BusinessDay(-1)],
)

# Canada Day
CanadaDay = Holiday(
    "Canada Day",
    month=7,
    day=1,
    observance=weekend_to_monday,
)
DayBeforeCanadaDay = Holiday(
    "Canada Day",
    month=6,
    day=30,
    observance=previous_friday,
)

# Civic Holiday
CivicHoliday = Holiday(
    "Civic Holiday", # AKA Terry Fox day
    month=8,
    day=1,
    offset=DateOffset(weekday=MO(1)),
)
DayBeforeCivicHoliday = Holiday(
    "Day before Civic Holiday",
    month=8,
    day=1,
    offset=[DateOffset(weekday=MO(1)), BusinessDay(-1)],
)

# Labor Day
LaborDay = Holiday(
    "Labor Day",
    month=9,
    day=1,
    offset=DateOffset(weekday=MO(1)),
)
DayBeforeLaborDay = Holiday(
    "Day before Labor Day",
    month=9,
    day=1,
    offset=[DateOffset(weekday=MO(1)), BusinessDay(-1)],
)

# Thanksgiving
Thanksgiving = Holiday(
    "Thanksgiving",
    month=10,
    day=1,
    offset=DateOffset(weekday=MO(2)),
)
DayBeforeThanksgiving = Holiday(
    "Day before Thanksgiving",
    month=10,
    day=1,
    offset=[DateOffset(weekday=MO(2)), BusinessDay(-1)],
)

TruthAndReconciliationDay = Holiday(
    "Canada Truth and Reconciliation Day", month=9, day=30, observance=weekend_to_monday, start_date="2021-01-01"
)
DayBeforeTruthAndReconciliationDay = Holiday(
    "Canada Truth and Reconciliation Day", month=9, day=29, observance=previous_friday, start_date="2021-01-01"
)

RemembranceDay = Holiday("Canada Remembrance Day", month=11, day=11, observance=weekend_to_monday)
DayBeforeRemembranceDay = Holiday("Day before Remembrance Day", month=11, day=10, observance=previous_friday)

DayBeforeChristmas = Holiday("Day before Christmas", month=12, day=24, observance=previous_friday)
Christmas = Holiday("Christmas", month=12, day=25, observance=weekend_to_monday)


DayBeforeNewYears = Holiday("Day before New years", month=12, day=31, observance=previous_friday)


DayBeforeGoodFriday = Holiday("Day before good friday", month=1, day=1, offset=[Easter(), Day(-3)])
