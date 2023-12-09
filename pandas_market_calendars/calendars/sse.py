from datetime import time, timedelta
from functools import partial

from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, next_monday
from pytz import timezone

from pandas_market_calendars.holidays.cn import *
from pandas_market_calendars.market_calendar import MarketCalendar


class SSEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for Shanghai Stock Exchange

    Open Time: 9:30 AM, Asia/Shanghai
    LUNCH BREAK :facepalm: : 11:30 AM - 1:00 PM Asia/Shanghai
    Close Time: 3:00 PM, Asia/Shanghai
    """

    aliases = ["SSE"]
    regular_market_times = {
        "market_open": ((None, time(9, 30)),),
        "market_close": ((None, time(15)),),
        "break_start": ((None, time(11, 30)),),
        "break_end": ((None, time(13)),),
    }

    @property
    def name(self):
        return "SSE"

    @property
    def tz(self):
        return timezone("Asia/Shanghai")

    @property
    def regular_holidays(self):
        """
        Rules are guesses based on observations of recent year.
        Rectify accordingly once the next year's holidays arrangement is published by the government.
        """
        # Since all past holidays are adhoc, start_year should always be a year in the future.
        # For example: Holiday arrangements for 2022 are now included,
        # then our guesswork starts from the next year so start_year = 2023
        start_year = 2024

        return AbstractHolidayCalendar(
            rules=[
                Holiday(
                    name="New Year's Day",
                    month=1,
                    day=1,
                    observance=next_monday,
                    start_date=Timestamp(start_year, 1, 1),
                ),
                Holiday(
                    name="New Year's Day",
                    month=1,
                    day=2,
                    observance=partial(second_day_in_lieu),
                    start_date=Timestamp(start_year, 1, 2),
                ),
                Holiday(
                    name="New Year's Day",
                    month=1,
                    day=3,
                    observance=partial(third_day_in_lieu),
                    start_date=Timestamp(start_year, 1, 3),
                ),
                Holiday(
                    name="Spring Festival",
                    month=1,
                    day=20,
                    observance=partial(lunisolar, mapping=sf_mapping, delta=-1),
                    start_date=Timestamp(start_year, 1, 20),
                ),
                Holiday(
                    name="Spring Festival",
                    month=1,
                    day=21,
                    observance=partial(lunisolar, mapping=sf_mapping, delta=0),
                    start_date=Timestamp(start_year, 1, 21),
                ),
                Holiday(
                    name="Spring Festival",
                    month=1,
                    day=21,
                    observance=partial(lunisolar, mapping=sf_mapping, delta=1),
                    start_date=Timestamp(start_year, 1, 22),
                ),
                Holiday(
                    name="Spring Festival",
                    month=1,
                    day=21,
                    observance=partial(lunisolar, mapping=sf_mapping, delta=2),
                    start_date=Timestamp(start_year, 1, 23),
                ),
                Holiday(
                    name="Spring Festival",
                    month=1,
                    day=21,
                    observance=partial(lunisolar, mapping=sf_mapping, delta=3),
                    start_date=Timestamp(start_year, 1, 24),
                ),
                Holiday(
                    name="Spring Festival",
                    month=1,
                    day=21,
                    observance=partial(lunisolar, mapping=sf_mapping, delta=4),
                    start_date=Timestamp(start_year, 1, 25),
                ),
                Holiday(
                    name="Spring Festival",
                    month=1,
                    day=21,
                    observance=partial(lunisolar, mapping=sf_mapping, delta=5),
                    start_date=Timestamp(start_year, 1, 26),
                ),
                Holiday(
                    name="Labour Day",
                    month=5,
                    day=1,
                    observance=next_monday,
                    start_date=Timestamp(start_year, 5, 1),
                ),
                Holiday(
                    name="Labour Day",
                    month=5,
                    day=2,
                    observance=second_day_in_lieu,
                    start_date=Timestamp(start_year, 5, 2),
                ),
                Holiday(
                    name="Labour Day",
                    month=5,
                    day=3,
                    observance=third_day_in_lieu,
                    start_date=Timestamp(start_year, 5, 3),
                ),
                Holiday(
                    name="Tomb-sweeping Day",
                    month=4,
                    day=4,
                    observance=partial(
                        lunisolar, mapping=tsd_mapping, func=next_monday
                    ),
                    start_date=Timestamp(start_year, 4, 4),
                ),
                Holiday(
                    name="Tomb-sweeping Day",
                    month=4,
                    day=5,
                    observance=partial(
                        lunisolar, mapping=tsd_mapping, func=second_day_in_lieu, delta=1
                    ),
                    start_date=Timestamp(start_year, 4, 4),
                ),
                Holiday(
                    name="Tomb-sweeping Day",
                    month=4,
                    day=6,
                    observance=partial(
                        lunisolar, mapping=tsd_mapping, func=third_day_in_lieu, delta=2
                    ),
                    start_date=Timestamp(start_year, 4, 4),
                ),
                Holiday(
                    name="Dragon Boat Festival",
                    month=5,
                    day=27,
                    observance=partial(
                        lunisolar, mapping=dbf_mapping, func=next_monday
                    ),
                    start_date=Timestamp(start_year, 5, 27),
                ),
                Holiday(
                    name="Dragon Boat Festival",
                    month=5,
                    day=28,
                    observance=partial(
                        lunisolar, mapping=dbf_mapping, func=second_day_in_lieu, delta=1
                    ),
                    start_date=Timestamp(start_year, 5, 27),
                ),
                Holiday(
                    name="Dragon Boat Festival",
                    month=5,
                    day=29,
                    observance=partial(
                        lunisolar, mapping=dbf_mapping, func=third_day_in_lieu, delta=2
                    ),
                    start_date=Timestamp(start_year, 5, 27),
                ),
                Holiday(
                    name="Mid-autumn Festival",
                    month=9,
                    day=7,
                    observance=partial(
                        lunisolar, mapping=maf_mapping, func=next_monday
                    ),
                    start_date=Timestamp(start_year, 9, 7),
                ),
                Holiday(
                    name="Mid-autumn Festival",
                    month=9,
                    day=8,
                    observance=partial(
                        lunisolar, mapping=maf_mapping, func=second_day_in_lieu, delta=1
                    ),
                    start_date=Timestamp(start_year, 9, 7),
                ),
                Holiday(
                    name="Mid-autumn Festival",
                    month=9,
                    day=9,
                    observance=partial(
                        lunisolar, mapping=maf_mapping, func=third_day_in_lieu, delta=2
                    ),
                    start_date=Timestamp(start_year, 9, 7),
                ),
                Holiday(
                    name="National Day",
                    month=10,
                    day=1,
                    start_date=Timestamp(start_year, 10, 1),
                ),
                Holiday(
                    name="National Day",
                    month=10,
                    day=2,
                    start_date=Timestamp(start_year, 10, 2),
                ),
                Holiday(
                    name="National Day",
                    month=10,
                    day=3,
                    start_date=Timestamp(start_year, 10, 3),
                ),
                Holiday(
                    name="National Day",
                    month=10,
                    day=4,
                    start_date=Timestamp(start_year, 10, 4),
                ),
                Holiday(
                    name="National Day",
                    month=10,
                    day=5,
                    start_date=Timestamp(start_year, 10, 5),
                ),
                Holiday(
                    name="National Day",
                    month=10,
                    day=6,
                    start_date=Timestamp(start_year, 10, 6),
                ),
                Holiday(
                    name="National Day",
                    month=10,
                    day=7,
                    start_date=Timestamp(start_year, 10, 7),
                ),
            ]
        )

    @property
    def adhoc_holidays(self):
        return all_holidays


def second_day_in_lieu(dt):
    dow = dt.weekday()
    if dow == 0:  # Holiday is Sunday, use Saturday
        return dt - timedelta(2)
    elif dow == 1:  # Holiday is Monday, use Saturday
        return dt - timedelta(3)
    elif dow == 2:  # Holiday is Tuesday, use Sunday
        return dt - timedelta(3)
    elif dow == 3:  # Holiday is Wednesday, use Saturday
        return dt - timedelta(5)

    return dt


def third_day_in_lieu(dt):
    dow = dt.weekday()
    if dow == 0:  # Holiday is Saturday, use Sunday
        return dt - timedelta(1)
    elif dow == 1:  # Holiday is Sunday, use Sunday
        return dt - timedelta(2)
    elif dow == 2:  # Holiday is Monday, use Sunday
        return dt - timedelta(3)
    elif dow == 3:  # Holiday is Tuesday, use Monday
        return dt - timedelta(3)
    elif dow == 4:  # Holiday is Wednesday, use Sunday
        return dt - timedelta(5)

    return dt


def lunisolar(dt, mapping, func=None, delta=None):
    if mapping and (dt.year in mapping):
        new_dt = mapping[dt.year]
    else:
        new_dt = dt
    if delta:
        new_dt = new_dt + timedelta(delta)
    if func:
        return func(new_dt)
    else:
        return new_dt
