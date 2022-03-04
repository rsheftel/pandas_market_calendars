from datetime import time

from pandas.tseries.holiday import AbstractHolidayCalendar

from pandas_market_calendars.exchange_calendar_cme_globex_base import CMEGlobexBaseExchangeCalendar
from pandas_market_calendars.holidays_cme import (
    USMartinLutherKingJrAfter1998Before2022,
    USPresidentsDayBefore2022,
    GoodFridayBefore2021,
    GoodFriday2021,
    GoodFridayAfter2021,
    USMemorialDay2021AndPrior,
    USIndependenceDayBefore2022,
    USLaborDayStarting1887Before2022,
    USThanksgivingBefore2022,
    USThanksgivingFriday,
)
from pandas_market_calendars.holidays_us import (
    USNewYearsDay,
    ChristmasEveInOrAfter1993,
    Christmas,
)

_1015 = time(10, 15)
_1200 = time(12, 0)
_1215 = time(12, 15)


class CMEGlobexFXExchangeCalendar(CMEGlobexBaseExchangeCalendar):
    aliases = ['CME_Currency']

    # Using CME Globex trading times eg AUD/USD, EUR/GBP, and BRL/USD
    # https://www.cmegroup.com/markets/fx/g10/australian-dollar.contractSpecs.html
    # https://www.cmegroup.com/markets/fx/cross-rates/euro-fx-british-pound.contractSpecs.html
    # https://www.cmegroup.com/markets/fx/emerging-market/brazilian-real.contractSpecs.html
    # CME "NZD spot" has its own holiday schedule; this is a niche product (via "FX Link") and is not handled in this
    # class; however, its regular hours follow the same schedule (see
    # https://www.cmegroup.com/trading/fx/files/fx-product-guide-2021-us.pdf)
    regular_market_times = {
        "market_open": ((None, time(17), -1),),  # offset by -1 day
        "market_close": ((None, time(16, 00)),)
    }

    aliases = ['CMEGlobex_FX', 'CME_FX', 'CME_Currency']

    @property
    def name(self):
        return "CMEGlobex_FX"

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            GoodFridayBefore2021,
            GoodFridayAfter2021,
            Christmas,
        ])

    @property
    def special_closes(self):
        """
        Accurate 2020-2022 inclusive
        TODO - enhance/verify prior to 2020
        TODO - Add 2023+ once known
        """
        # Source https://www.cmegroup.com/tools-information/holiday-calendar.html
        return [
            (_1015, AbstractHolidayCalendar(rules=[GoodFriday2021])),
            (_1200, AbstractHolidayCalendar(rules=[
                USMartinLutherKingJrAfter1998Before2022,
                USPresidentsDayBefore2022,
                USMemorialDay2021AndPrior,
                USIndependenceDayBefore2022,
                USLaborDayStarting1887Before2022,
                USThanksgivingBefore2022,
            ])),
            (_1215, AbstractHolidayCalendar(rules=[USThanksgivingFriday, ChristmasEveInOrAfter1993])),
        ]
