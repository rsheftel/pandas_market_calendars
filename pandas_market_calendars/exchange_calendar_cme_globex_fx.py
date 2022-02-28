from datetime import time

from pandas.tseries.holiday import AbstractHolidayCalendar, GoodFriday

from pandas_market_calendars.exchange_calendar_cme import CMEBaseExchangeCalendar
from pandas_market_calendars.holidays_us import USNewYearsDay, Christmas, USThanksgivingFriday


class CMECurrencyExchangeCalendar(CMEBaseExchangeCalendar):
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

    @property
    def name(self):
        return "CME_Currency"

    @property
    def special_close_time(self):
        return time(12, 15)

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            GoodFriday,
            Christmas,
        ])

    @property
    def special_closes(self):
        # Currency futures are typically fully closed or they trade normal hours; Thanksgiving Friday is the exception
        return [(
            self.special_close_time,
            AbstractHolidayCalendar(rules=[
                USThanksgivingFriday,
            ])
        )]
