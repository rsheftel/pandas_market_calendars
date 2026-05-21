from datetime import time
from itertools import chain

import pandas as pd
from pandas.tseries.holiday import (
    MO,
    AbstractHolidayCalendar,
    DateOffset,
    GoodFriday,
    Holiday,
)
from pandas.tseries.offsets import BusinessDay
from zoneinfo import ZoneInfo

from pandas_market_calendars.holidays.uk import (
    BoxingDay,
    WeekendBoxingDay,
    WeekendChristmas,
)

from pandas_market_calendars.market_calendar import (
    FRIDAY,
    MONDAY,
    THURSDAY,
    TUESDAY,
    WEDNESDAY,
    MarketCalendar,
)
from pandas_market_calendars.holidays.ca import (
    NewYears, FamilyDay, VictoriaDay, CanadaDay, CivicHoliday, LaborDay, Thanksgiving, Christmas,
    TruthAndReconiliationDay, RemembranceDay, DayBeforeCanadaDay, DayBeforeFamilyDay, DayBeforeLaborDay, 
    DayBeforeCivicHoliday, DayBeforeChristmas, DayBeforeNewYears,DayBeforeRemembranceDay, DayBeforeThanksgiving,
    DayBeforeTruthAndReconiliationDay, DayBeforeVictoriaDay, DayBeforeGoodFriday
)


from .tsx import ChristmasEveEarlyClose2010Onwards




class MonExBaseExchangeCalendar(MarketCalendar):
    """
    Base Exchange calendar for the TMX Montreal Exchange.

    Regularly-Observed Holidays:
    - New Years Day (observed on first business day on/after)
    - Family Day (Third Monday in February, starting in 2008)
    - Good Friday
    - Victoria Day (Monday before May 25th)
    - Canada Day (July 1st, observed first business day after)
    - Civic Holiday (First Monday in August)
    - Labor Day (First Monday in September)
    - Thanksgiving (Second Monday in October)
    - Christmas Day
        - Dec. 26th if Christmas is on a Sunday
        - Dec. 27th if Christmas is on a weekend
    - Boxing Day
        - Dec. 27th if Christmas is on a Sunday
        - Dec. 28th if Boxing Day is on a weekend

    Early closes:
    - Starting in 2010, if Christmas Eve falls on a weekday, the market
      closes at 1:00 pm that day. If it falls on a weekend, there is no
      early close.
    """
    @property
    def tz(self):
        return ZoneInfo("Canada/Eastern")

    @property
    def _regular_holidays(self):
        return [
            NewYears,
            FamilyDay,
            GoodFriday,
            VictoriaDay,
            CanadaDay,
            CivicHoliday,
            LaborDay,
            Thanksgiving,
            Christmas,
            WeekendChristmas,
            BoxingDay,
            WeekendBoxingDay,
        ]

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=self._regular_holidays
        )

    @property
    def special_closes(self):
        return [
            (
                self.regular_early_close,
                AbstractHolidayCalendar(rules=[ChristmasEveEarlyClose2010Onwards]),
            )
        ]

    regular_early_close = time(13, 0)



class MonExRatesExchangeCalendar(MonExBaseExchangeCalendar):

    regular_early_close = time(13, 30)

    @property
    def _regular_holidays(self):
        return super()._regular_holidays + [TruthAndReconiliationDay, RemembranceDay]

    @property
    def special_closes(self):
        return [
            (
                self.regular_early_close, 
                AbstractHolidayCalendar(rules=[
                    DayBeforeFamilyDay,
                    DayBeforeGoodFriday,
                    DayBeforeVictoriaDay,
                    DayBeforeCanadaDay,
                    DayBeforeCivicHoliday,
                    DayBeforeLaborDay, 
                    DayBeforeTruthAndReconiliationDay,
                    DayBeforeThanksgiving,
                    DayBeforeRemembranceDay,
                    DayBeforeChristmas,
                    DayBeforeNewYears,
                    
                ])
            )
        ]


class MonExBondExchangeCalendar(MonExRatesExchangeCalendar):
    aliases = ["TMX_Bond", "MonEx_Bond", "CDE_Bond"]

    regular_market_times = {
        "market_open": ((None, time(20, 0), -1),),
        "market_close": ((None, time(16, 30)),),
    }

    @property
    def name(self):
        return "MonEx_Bonds"

    @property
    def full_name(self):
        return "Montreal Exchange Bonds"


class MonExStirExchangeCalendar(MonExRatesExchangeCalendar):
    aliases = ["TMX_STIR", "MonEx_STIR", "CDE_STIR"]

    regular_market_times = {
        "market_open": ((None, time(2, 0)),),
        "market_close": ((None, time(16, 30)),),
    }

    @property
    def name(self):
        return "MonEx_STIR"

    @property
    def full_name(self):
        return "Montreal Exchange STIR futures"



class MonExIndexExchangeCalendar(MonExBaseExchangeCalendar):
    aliases = ["TMX_Index", "MonEx_Index", "CDE_Index"]

    regular_market_times = {
        "market_open": ((None, time(9, 30)),),
        "market_close": ((None, time(16, 30)),),
    }

    @property
    def name(self):
        return "MonEx_Index"

    @property
    def full_name(self):
        return "Montreal Exchange Index futures"

