from datetime import time
from itertools import chain

from pandas.tseries.holiday import AbstractHolidayCalendar
from pytz import timezone

from pandas_market_calendars.holidays.jp import *
from pandas_market_calendars.holidays.us import USNewYearsDay
from pandas_market_calendars.market_calendar import MarketCalendar


# TODO:
# From 1949 to 1972 the TSE was open on all non-holiday Saturdays for a half day
# From 1973 to 1984 the TSE was open on all non-holiday Saturdays except the third Saturday of the month
# need to add support for weekmask to make this work properly


class JPXExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for JPX

    Open Time: 9:31 AM, Asia/Tokyo
    LUNCH BREAK :facepalm: : 11:30 AM - 12:30 PM Asia/Tokyo
    Close Time: 3:30 PM, Asia/Tokyo

    Market close of Japan changed from 3:00 PM to 3:30 PM on November 5, 2024
    Reference:
    https://www.jpx.co.jp/english/equities/trading/domestic/tvdivq0000006blj-att/tradinghours_eg.pdf
    """

    aliases = ["JPX", "XJPX"]
    regular_market_times = {
        "market_open": ((None, time(9)),),
        "market_close": ((None, time(15)), ("2024-11-05", time(15, 30))),
        "break_start": ((None, time(11, 30)),),
        "break_end": ((None, time(12, 30)),),
    }
    regular_early_close = time(13)

    @property
    def name(self):
        return "JPX"

    @property
    def tz(self):
        return timezone("Asia/Tokyo")

    @property
    def adhoc_holidays(self):
        return list(
            chain(
                AscensionDays,
                MarriageDays,
                FuneralShowa,
                EnthronementDays,
                AutumnalCitizenDates,
                NoN225IndexPrices,
                EquityTradingSystemFailure,
            )
        )

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                JapanNewYearsDay2,
                JapanNewYearsDay3,
                JapanComingOfAgeDay1951To1973,
                JapanComingOfAgeDay1974To1999,
                JapanComingOfAgeDay,
                JapanNationalFoundationDay1969To1973,
                JapanNationalFoundationDay,
                JapanEmperorsBirthday,
                JapanVernalEquinox,
                JapanShowaDayUntil1972,
                JapanShowaDay,
                JapanConstitutionMemorialDayUntil1972,
                JapanConstitutionMemorialDay,
                JapanGreeneryDay,
                JapanChildrensDayUntil1972,
                JapanChildrensDay,
                JapanGoldenWeekBonusDay,
                JapanMarineDay1996To2002,
                JapanMarineDay2003To2019,
                JapanMarineDay2020,
                JapanMarineDay2021,
                JapanMarineDay,
                JapanMountainDay2016to2019,
                JapanMountainDay2020,
                JapanMountainDay2021,
                JapanMountainDay2021NextDay,
                JapanMountainDay,
                JapanRespectForTheAgedDay1966To1972,
                JapanRespectForTheAgedDay1973To2002,
                JapanRespectForTheAgedDay,
                JapanAutumnalEquinox,
                JapanHealthAndSportsDay1966To1972,
                JapanHealthAndSportsDay1973To1999,
                JapanHealthAndSportsDay2000To2019,
                JapanSportsDay2020,
                JapanSportsDay2021,
                JapanSportsDay,
                JapanCultureDayUntil1972,
                JapanCultureDay,
                JapanLaborThanksgivingDayUntil1972,
                JapanLaborThanksgivingDay,
                JapanEmperorAkahitosBirthday,
                JapanDecember29Until1988,
                JapanDecember30Until1988,
                JapanBeforeNewYearsDay,
            ]
        )
