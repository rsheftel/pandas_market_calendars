from datetime import time
from typing import Any, List

from pandas.tseries.holiday import AbstractHolidayCalendar

from pandas_market_calendars.calendars.cme_globex_base import (
    CMEGlobexBaseExchangeCalendar,
)
from pandas_market_calendars.holidays.cme import (
    GoodFriday2021,
    GoodFriday2022,
    GoodFridayAfter2022JobsReport,
    GoodFridayAfter2022NoJobsReport,
    GoodFridayBefore2021,
    USIndependenceDayBefore2022,
    USLaborDayStarting1887Before2022,
    USMartinLutherKingJrAfter1998Before2022,
    USMemorialDay2021AndPrior,
    USPresidentsDayBefore2022,
    USThanksgivingBefore2022,
)
from pandas_market_calendars.holidays.cme_globex import (
    ChristmasEveFrom2024,
    ChristmasEveThrough2023,
    FridayAfterThanksgivingFrom2024,
    FridayAfterThanksgivingThrough2023,
)
from pandas_market_calendars.holidays.us import (
    Christmas,
    USNewYearsDay,
)


_1015 = time(10, 15)
_1200 = time(12, 0)
_1215 = time(12, 15)
_1245 = time(12, 45)
_1345 = time(13, 45)


class CMEGlobexFXExchangeCalendar(CMEGlobexBaseExchangeCalendar):
    aliases = ["CME_Currency"]

    # Using CME Globex trading times eg AUD/USD, EUR/GBP, and BRL/USD
    # https://www.cmegroup.com/markets/fx/g10/australian-dollar.contractSpecs.html
    # https://www.cmegroup.com/markets/fx/cross-rates/euro-fx-british-pound.contractSpecs.html
    # https://www.cmegroup.com/markets/fx/emerging-market/brazilian-real.contractSpecs.html
    # CME "NZD spot" has its own holiday schedule; this is a niche product (via "FX Link") and is not handled in this
    # class; however, its regular hours follow the same schedule (see
    # https://www.cmegroup.com/trading/fx/files/fx-product-guide-2021-us.pdf)
    regular_market_times = {
        "market_open": ((None, time(17), -1),),  # offset by -1 day
        "market_close": ((None, time(16, 00)),),
    }

    aliases = ["CMEGlobex_FX", "CME_FX", "CME_Currency"]

    @property
    def name(self) -> str:
        return "CMEGlobex_FX"

    @property
    def regular_holidays(self) -> Any:
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                GoodFridayBefore2021,
                GoodFriday2022,
                GoodFridayAfter2022NoJobsReport,
                Christmas,
            ]
        )

    @property
    def special_closes(self) -> List[Any]:
        """
        Accurate 2020-2022 inclusive
        TODO - enhance/verify prior to 2020
        TODO - Add 2023+ once known
        """
        # Source https://www.cmegroup.com/tools-information/holiday-calendar.html
        return [
            (
                _1015,
                AbstractHolidayCalendar(
                    rules=[
                        GoodFriday2021,
                        GoodFridayAfter2022JobsReport,
                    ]
                ),
            ),
            (
                _1200,
                AbstractHolidayCalendar(
                    rules=[
                        USMartinLutherKingJrAfter1998Before2022,
                        USPresidentsDayBefore2022,
                        USMemorialDay2021AndPrior,
                        USIndependenceDayBefore2022,
                        USLaborDayStarting1887Before2022,
                        USThanksgivingBefore2022,
                    ]
                ),
            ),
            (
                _1215,
                AbstractHolidayCalendar(rules=[FridayAfterThanksgivingThrough2023, ChristmasEveThrough2023]),
            ),
            (
                _1245,
                AbstractHolidayCalendar(rules=[ChristmasEveFrom2024]),
            ),
            (
                _1345,
                AbstractHolidayCalendar(rules=[FridayAfterThanksgivingFrom2024]),
            ),
        ]

    @property
    def special_closes_adhoc(self) -> List[Any]:
        # July 4th on a Friday, or observed on one
        return [(_1200, ["2025-07-04", "2026-07-03"])]
