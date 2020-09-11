"""
Imported calendars from the trading_calendars project

GitHub: www.tradcing.com

Subtracts 1 minute from the start time as listed in the trading_calendars project
"""

from datetime import time
from .market_calendar import MarketCalendar
import trading_calendars


class TradingCalendar(MarketCalendar):
    def __init__(self, open_time=None, close_time=None):
        self._tc = self._tc_class()  # _tc.class is defined in the class generator below
        super().__init__(open_time, close_time)

    @property
    def name(self):
        return self._tc.name

    @property
    def tz(self):
        return self._tc.tz

    @property
    def open_time_default(self):
        tc_time = self._tc.open_times[0][1]
        return time(tc_time.hour, max(tc_time.minute - 1, 0))  # aligns the open time standard with mcal

    @property
    def close_time_default(self):
        return self._tc.close_times[0][1]

    @property
    def regular_holidays(self):
        return self._tc.regular_holidays

    @property
    def adhoc_holidays(self):
        return self._tc.adhoc_holidays

    @property
    def special_opens(self):
        return self._tc.special_opens

    @property
    def special_opens_adhoc(self):
        return self._tc.special_opens_adhoc

    @property
    def special_closes(self):
        return self._tc.special_closes

    @property
    def special_closes_adhoc(self):
        return self._tc.special_closes_adhoc


calendars = trading_calendars.calendar_utils._default_calendar_factories  # noqa

# TODO: add the aliases from their alias dict (watch out for collision, actually, best to not do this right now
for exchange in calendars:
    locals()[exchange + 'ExchangeCalendar'] = type(exchange, (TradingCalendar, ),
                                                   {'_tc_class': calendars[exchange], 'alias': [exchange]})
