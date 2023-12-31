import datetime

from dateutil.relativedelta import MO, TH, FR
from pandas import DateOffset, Timestamp
from pandas.tseries.holiday import Holiday, Easter, nearest_workday
from pandas.tseries.offsets import Day

#########
# Martin Luther King
#########
USMartinLutherKingJrAfter1998Before2022 = Holiday(
    "Dr. Martin Luther King Jr. Day",
    month=1,
    day=1,
    # The US markets didn't observe MLK day as a holiday until 1998.
    start_date=Timestamp("1998-01-01"),
    end_date=Timestamp("2021-12-31"),
    offset=DateOffset(weekday=MO(3)),
)

USMartinLutherKingJrAfter1998Before2015 = Holiday(
    "Dr. Martin Luther King Jr. Day",
    month=1,
    day=1,
    # The US markets didn't observe MLK day as a holiday until 1998.
    start_date=Timestamp("1998-01-01"),
    end_date=Timestamp("2014-12-31"),
    offset=DateOffset(weekday=MO(3)),
)

USMartinLutherKingJrAfter2015 = Holiday(
    "Dr. Martin Luther King Jr. Day",
    month=1,
    day=1,
    # The US markets didn't observe MLK day as a holiday until 1998.
    start_date=Timestamp("2015-01-01"),
    offset=DateOffset(weekday=MO(3)),
)

USMartinLutherKingJrAfter1998Before2016FridayBefore = Holiday(
    "Dr. Martin Luther King Jr. Day",
    month=1,
    day=1,
    start_date=Timestamp("1998-01-01"),
    end_date=Timestamp("2015-12-31"),
    offset=[DateOffset(weekday=MO(3)), DateOffset(weekday=FR(-1))],
)

#########
# President's Day
#########
USPresidentsDayBefore2022 = Holiday(
    "President" "s Day",
    start_date=Timestamp("1971-01-01"),
    end_date=Timestamp("2021-12-31"),
    month=2,
    day=1,
    offset=DateOffset(weekday=MO(3)),
)
USPresidentsDayBefore2015 = Holiday(
    "President" "s Day",
    start_date=Timestamp("1971-01-01"),
    end_date=Timestamp("2014-12-31"),
    month=2,
    day=1,
    offset=DateOffset(weekday=MO(3)),
)

USPresidentsDayAfter2015 = Holiday(
    "President" "s Day",
    start_date=Timestamp("2015-01-01"),
    month=2,
    day=1,
    offset=DateOffset(weekday=MO(3)),
)

USPresidentsDayBefore2016FridayBefore = Holiday(
    "President" "s Day",
    start_date=Timestamp("1971-01-01"),
    end_date=Timestamp("2015-12-31"),
    month=2,
    day=1,
    offset=[DateOffset(weekday=MO(3)), DateOffset(weekday=FR(-1))],
)

#########
# Good Friday
#########


GoodFridayBefore2021 = Holiday(
    "Good Friday",
    month=1,
    day=1,
    offset=[Easter(), Day(-2)],
    end_date=Timestamp("2020-12-31"),
)

# On some years (i.e. 2010,2012,2015) there is a special close for equities at 08:15
# so here it is made sure that those are not full holidays
easter = Easter()
daymin2 = Day(-2)


def not_0815_close(dt):
    if dt.year in (2010, 2012, 2015):
        return None
    else:
        return dt + easter + daymin2


GoodFridayBefore2021NotEarlyClose = Holiday(
    "Good Friday",
    month=1,
    day=1,
    observance=not_0815_close,
    end_date=Timestamp("2020-12-31"),
)

# CME Interest Rate Products have this odd close
GoodFriday2009 = Holiday(
    "Good Friday",
    month=1,
    day=1,
    offset=[Easter(), Day(-3)],
    start_date=Timestamp("2009-01-01"),
    end_date=Timestamp("2009-12-31"),
)

GoodFriday2021 = Holiday(
    "Good Friday",
    month=1,
    day=1,
    offset=[Easter(), Day(-2)],
    start_date=Timestamp("2021-01-01"),
    end_date=Timestamp("2021-12-31"),
)
GoodFridayAfter2021 = Holiday(
    "Good Friday",
    month=1,
    day=1,
    offset=[Easter(), Day(-2)],
    start_date=Timestamp("2022-01-01"),
)
GoodFriday2022 = Holiday(
    "Good Friday",
    month=1,
    day=1,
    offset=[Easter(), Day(-2)],
    start_date=Timestamp("2022-01-01"),
    end_date=Timestamp("2022-12-31"),
)
GoodFridayAfter2022 = Holiday(
    "Good Friday",
    month=1,
    day=1,
    offset=[Easter(), Day(-2)],
    start_date=Timestamp("2023-01-01"),
)
# Dates when equities closed at 08:15
GoodFriday2010 = Holiday(
    "Good Friday",
    month=1,
    day=1,
    offset=[Easter(), Day(-2)],
    start_date=Timestamp("2010-01-01"),
    end_date=Timestamp("2010-12-31"),
)
GoodFriday2012 = Holiday(
    "Good Friday",
    month=1,
    day=1,
    offset=[Easter(), Day(-2)],
    start_date=Timestamp("2012-01-01"),
    end_date=Timestamp("2012-12-31"),
)

GoodFriday2015 = Holiday(
    "Good Friday",
    month=1,
    day=1,
    offset=[Easter(), Day(-2)],
    start_date=Timestamp("2015-01-01"),
    end_date=Timestamp("2015-12-31"),
)

#########
# Memorial Day
#########

USMemorialDay2021AndPrior = Holiday(
    "Memorial Day",
    month=5,
    day=25,
    start_date=Timestamp("1971-01-01"),
    end_date=Timestamp("2021-12-31"),
    offset=DateOffset(weekday=MO(1)),
)  # Equity Products
USMemorialDay2013AndPrior = Holiday(
    "Memorial Day",
    month=5,
    day=25,
    start_date=Timestamp("1971-01-01"),
    end_date=Timestamp("2013-12-31"),
    offset=DateOffset(weekday=MO(1)),
)
USMemorialDayAfter2013 = Holiday(
    "Memorial Day",
    month=5,
    day=25,
    start_date=Timestamp("2014-01-01"),
    offset=DateOffset(weekday=MO(1)),
)
USMemorialDay2015AndPriorFridayBefore = Holiday(
    "Memorial Day",
    month=5,
    day=25,
    start_date=Timestamp("1971-01-01"),
    end_date=Timestamp("2015-12-31"),
    offset=[DateOffset(weekday=MO(1)), DateOffset(weekday=FR(-1))],
)

#######
# Independence Day
#######

USIndependenceDayBefore2022 = Holiday(
    "July 4th",
    month=7,
    day=4,
    start_date=Timestamp("1954-01-01"),
    end_date=Timestamp("2021-12-31"),
    observance=nearest_workday,
)
USIndependenceDayBefore2014 = Holiday(
    "July 4th",
    month=7,
    day=4,
    start_date=Timestamp("1954-01-01"),
    end_date=Timestamp("2013-12-31"),
    observance=nearest_workday,
)
USIndependenceDayAfter2014 = Holiday(
    "July 4th",
    month=7,
    day=4,
    start_date=Timestamp("2014-01-01"),
    observance=nearest_workday,
)


# Necessary for equities and crypto
def previous_workday_if_july_4th_is_tue_to_fri(dt):
    july4th = datetime.datetime(dt.year, 7, 4)
    if july4th.weekday() in (1, 2, 3, 4):
        return july4th - datetime.timedelta(days=1)
    # else None


USIndependenceDayBefore2022PreviousDay = Holiday(
    "July 4th",
    month=7,
    day=4,
    start_date=Timestamp("1954-01-01"),
    observance=previous_workday_if_july_4th_is_tue_to_fri,
)

#########
# Labor Day
#########

USLaborDayStarting1887Before2022 = Holiday(
    "Labor Day",
    month=9,
    day=1,
    start_date=Timestamp("1887-01-01"),
    end_date=Timestamp("2021-12-31"),
    offset=DateOffset(weekday=MO(1)),
)
USLaborDayStarting1887Before2014 = Holiday(
    "Labor Day",
    month=9,
    day=1,
    start_date=Timestamp("1887-01-01"),
    end_date=Timestamp("2013-12-31"),
    offset=DateOffset(weekday=MO(1)),
)
USLaborDayStarting1887Before2015FridayBefore = Holiday(
    "Labor Day",
    month=9,
    day=1,
    start_date=Timestamp("1887-01-01"),
    end_date=Timestamp("2014-12-31"),
    offset=[DateOffset(weekday=MO(1)), DateOffset(weekday=FR(-1))],
)
USLaborDayStarting1887After2014 = Holiday(
    "Labor Day",
    month=9,
    day=1,
    start_date=Timestamp("2014-01-01"),
    offset=DateOffset(weekday=MO(1)),
)

#########
# Thanksgiving
#########

USThanksgivingBefore2022 = Holiday(
    "ThanksgivingFriday",
    start_date=Timestamp("1942-01-01"),
    end_date=Timestamp("2021-12-31"),
    month=11,
    day=1,
    offset=DateOffset(weekday=TH(4)),
)
USThanksgivingBefore2014 = Holiday(
    "ThanksgivingFriday",
    start_date=Timestamp("1942-01-01"),
    end_date=Timestamp("2013-12-31"),
    month=11,
    day=1,
    offset=DateOffset(weekday=TH(4)),
)
USThanksgivingAfter2014 = Holiday(
    "ThanksgivingFriday",
    start_date=Timestamp("2014-01-01"),
    month=11,
    day=1,
    offset=DateOffset(weekday=TH(4)),
)


# The following Holidays shouldn't be set with the FR offset
# In 2013, Nov 1st is a friday, so the 4th Friday is before the 4th Thursday...
# the observance rule defined herafter fixes this

# USThanksgivingFridayBefore2022 = Holiday(
#     'ThanksgivingFriday',
#     start_date=Timestamp('1942-01-01'),
#     end_date=Timestamp('2021-12-31'),
#     month=11, day=1,
#     offset=DateOffset(weekday=FR(4)),
# )
#
# USThanksgivingFriday2022AndAfter = Holiday(
#     'ThanksgivingFriday',
#     start_date=Timestamp('2022-01-01'),
#     month=11, day=1,
#     offset=DateOffset(weekday=FR(4)),
# )
# USThanksgivingFriday = Holiday(
#     'ThanksgivingFriday',
#     month=11, day=1,
#     offset=DateOffset(weekday=FR(4)),
# )


def fri_after_4th_thu(dt):
    # dt will just be Nov 1st
    diff_to_thu = 3 - dt.weekday()
    if diff_to_thu < 0:
        diff_to_thu += 7
    return dt + datetime.timedelta(days=diff_to_thu + 22)


USThanksgivingFriday = Holiday(
    "ThanksgivingFriday",
    start_date=Timestamp("1942-01-01"),
    month=11,
    day=1,
    observance=fri_after_4th_thu,
)

USThanksgivingFriday2022AndAfter = Holiday(
    "ThanksgivingFriday",
    start_date=Timestamp("2022-01-01"),
    month=11,
    day=1,
    observance=fri_after_4th_thu,
)
# USThanksgivingFriday = Holiday(
#     'ThanksgivingFriday',
#     month=11, day=1,
#     observance= fri_after_4th_thu,
# )
