from dateutil.relativedelta import (MO, FR)
from dateutil.relativedelta import (TH)
from pandas import (DateOffset, Timestamp)
from pandas.tseries.holiday import (Holiday, Easter)
from pandas.tseries.holiday import (nearest_workday)
from pandas.tseries.offsets import (Day)

USMartinLutherKingJrAfter1998Before2022 = Holiday(
    'Dr. Martin Luther King Jr. Day',
    month=1,
    day=1,
    # The US markets didn't observe MLK day as a holiday until 1998.
    start_date=Timestamp('1998-01-01'),
    end_date=Timestamp('2021-12-31'),
    offset=DateOffset(weekday=MO(3)),
)

USPresidentsDayBefore2022 = Holiday(
    'President''s Day',
    start_date=Timestamp('1971-01-01'),
    end_date=Timestamp('2021-12-31'),
    month=2, day=1,
    offset=DateOffset(weekday=MO(3)),
)

GoodFridayBefore2021 = Holiday(
    "Good Friday",
    month=1, day=1,
    offset=[Easter(), Day(-2)],
    end_date=Timestamp('2020-12-31'),
)
GoodFriday2021 = Holiday(
    "Good Friday",
    month=1, day=1,
    offset=[Easter(), Day(-2)],
    start_date=Timestamp('2021-01-01'),
    end_date=Timestamp('2021-12-31'),
)
GoodFridayAfter2021 = Holiday(
    "Good Friday",
    month=1, day=1,
    offset=[Easter(), Day(-2)],
    start_date=Timestamp('2022-01-01'),
)

USMemorialDay2021AndPrior = Holiday(
    'Memorial Day',
    month=5,
    day=25,
    start_date=Timestamp('1971-01-01'),
    end_date=Timestamp('2021-12-31'),
    offset=DateOffset(weekday=MO(1)),
)

USIndependenceDayBefore2022 = Holiday(
    'July 4th',
    month=7,
    day=4,
    start_date=Timestamp('1954-01-01'),
    end_date=Timestamp('2021-12-31'),
    observance=nearest_workday,
)

USLaborDayStarting1887Before2022 = Holiday(
    "Labor Day",
    month=9,
    day=1,
    start_date=Timestamp("1887-01-01"),
    end_date=Timestamp('2021-12-31'),
    offset=DateOffset(weekday=MO(1))
)


USThanksgivingBefore2022 = Holiday(
    'ThanksgivingFriday',
    start_date=Timestamp('1942-01-01'),
    end_date=Timestamp('2021-12-31'),
    month=11, day=1,
    offset=DateOffset(weekday=TH(4)),
)
USThanksgivingFridayBefore2022 = Holiday(
    'ThanksgivingFriday',
    start_date=Timestamp('1942-01-01'),
    end_date=Timestamp('2021-12-31'),
    month=11, day=1,
    offset=DateOffset(weekday=FR(4)),
)
USThanksgivingFriday2022AndAfter = Holiday(
    'ThanksgivingFriday',
    start_date=Timestamp('2022-01-01'),
    month=11, day=1,
    offset=DateOffset(weekday=FR(4)),
)
USThanksgivingFriday = Holiday(
    'ThanksgivingFriday',
    month=11, day=1,
    offset=DateOffset(weekday=FR(4)),
)
