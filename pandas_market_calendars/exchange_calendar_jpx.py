from datetime import time
from itertools import chain

from pandas.tseries.holiday import AbstractHolidayCalendar
from pytz import timezone

from pandas_market_calendars.holidays_jp import *
from pandas_market_calendars.holidays_us import USNewYearsDay
from .market_calendar import MarketCalendar


# TODO:
# From 1949 to 1972 the TSE was open on all non-holiday Saturdays for a half day
# From 1973 to 1984 the TSE was open on all non-holiday Saturdays except the third Saturday of the month
# need to add support for weekmask to make this work properly

class JPXExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for JPX

    Open Time: 9:31 AM, Asia/Tokyo
    LUNCH BREAK :facepalm: : 11:30 AM - 12:30 PM Asia/Tokyo
    Close Time: 4:00 PM, Asia/Tokyo
    """
    aliases = ['JPX']
    regular_market_times = {
        "market_open": ((None, time(9)),),
        "market_close": ((None, time(15)),),
        "break_start": ((None, time(11, 30)),),
        "break_end": ((None, time(12,30)),)
    }
    regular_early_close = time(13)

    @property
    def name(self):
        return "JPX"

    @property
    def tz(self):
        return timezone('Asia/Tokyo')

    @property
    def adhoc_holidays(self):
        return list(chain(
            AscensionDays,
            MarriageDays,
            FuneralShowa,
            EnthronementDays,
            AutumnalCitizenDates,
            NoN225IndexPrices
        ))

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
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
            JapanMarineDay,
            JapanMountainDay2016to2019,
            JapanMountainDay2020,
            JapanMountainDay,
            JapanRespectForTheAgedDay1966To1972,
            JapanRespectForTheAgedDay1973To2002,
            JapanRespectForTheAgedDay,
            JapanAutumnalEquinox,
            JapanHealthAndSportsDay1966To1972,
            JapanHealthAndSportsDay1973To1999,
            JapanHealthAndSportsDay2000To2019,
            JapanSportsDay2020,
            JapanSportsDay,
            JapanCultureDayUntil1972,
            JapanCultureDay,
            JapanLaborThanksgivingDayUntil1972,
            JapanLaborThanksgivingDay,
            JapanEmperorAkahitosBirthday,
            JapanDecember29Until1988,
            JapanDecember30Until1988,
            JapanBeforeNewYearsDay,
        ])
