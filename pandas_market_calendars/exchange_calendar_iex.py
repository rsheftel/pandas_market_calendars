from datetime import time
from itertools import chain
from .exchange_calendar_nyse import NYSEExchangeCalendar 
from pandas.tseries.holiday import AbstractHolidayCalendar
from pytz import timezone 

from pandas_market_calendars.holidays_nyse import (
    USPresidentsDay,
    GoodFriday,
    USMemorialDay,
    USJuneteenthAfter2022,
    USIndependenceDay,
    USThanksgivingDay,
    ChristmasNYSE,
    USMartinLutherKingJrAfter1998,

    #Ad-Hoc
    DayAfterThanksgiving1pmEarlyCloseInOrAfter1993,
    DaysBeforeIndependenceDay1pmEarlyCloseAdhoc,
    ChristmasEvesAdhoc,
)

class IEXExchangeCalendar(NYSEExchangeCalendar):
    """
    Exchange calendar for the Investor's Exchange (IEX).

    IEX Exchange is a U.S. stock exchange focused on driving performance
    for broker-dealers and investors through innovative design and technology.

    Most of this class inherits from NYSEExchangeCalendar since 
    the holidays are the same. The only variation is (1) IEX began 
    operation in 2013, and (2) IEX has different hours of operation

    References: 
    - https://exchange.iex.io/
    - https://iexexchange.io/resources/trading/trading-hours-holidays/index.html
    """

    regular_market_times = {
        "pre": (('2013-03-25', time(8)),),
        "market_open": ((None, time(9, 30)),),
        "market_close":((None, time(16)),),
        "post": ((None, time(17)),)
    }

    aliases = ['IEX', 'Investors_Exchange']

    @property
    def name(self):
        return "IEX"
    
    @property
    def weekmask(self):
        return "Mon Tue Wed Thu Fri"
    
    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USPresidentsDay,
            GoodFriday,
            USMemorialDay,
            USJuneteenthAfter2022,
            USIndependenceDay,
            USThanksgivingDay,
            ChristmasNYSE,
            USMartinLutherKingJrAfter1998
        ])
    
    @property
    def adhoc_holidays(self):
        return list(chain(
            ChristmasEvesAdhoc,
        ))

    @property
    def special_closes(self):
        return [
            (time(hour=13, tzinfo=timezone('America/New_York')), AbstractHolidayCalendar(rules=[
                DayAfterThanksgiving1pmEarlyCloseInOrAfter1993,
            ]))
        ]

    """Override NYSE calendar special cases"""

    @property
    def special_closes_adhoc(self):
        return [
            (time(13, tzinfo=timezone('America/New_York')),
                DaysBeforeIndependenceDay1pmEarlyCloseAdhoc) 
        ]

    @property
    def special_opens(self):
        return []

    def valid_days(self, start_date, end_date, tz='UTC'):
        trading_days = super().valid_days(start_date, end_date, tz=tz) #all NYSE valid days
        return trading_days[~(trading_days <= '2013-08-25')]
