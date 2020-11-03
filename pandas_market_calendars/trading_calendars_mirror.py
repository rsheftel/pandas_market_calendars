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
        self._tc = self._tc_class()  # noqa: _tc.class is defined in the class generator below
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
        return time(tc_time.hour, max(tc_time.minute - 1, 0), tzinfo=self.tz)  # aligns tc standard with mcal

    @property
    def close_time_default(self):
        return self._tc.close_times[0][1].replace(tzinfo=self.tz)

    @property
    def break_start(self):
        tc_time = self._tc.break_start_times
        if not tc_time:
            return None
        tc_time = tc_time[0][1]
        return time(tc_time.hour, tc_time.minute - 1, tzinfo=self.tz)  # aligns tc standard with mcal

    @property
    def break_end(self):
        tc_time = self._tc.break_end_times
        return tc_time[0][1] if tc_time else None

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

for exchange in calendars:
    locals()[exchange + 'ExchangeCalendar'] = type(exchange, (TradingCalendar, ),
                                                   {'_tc_class': calendars[exchange], 'alias': [exchange]})
