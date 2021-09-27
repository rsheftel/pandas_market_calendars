"""
Imported calendars from the exchange_calendars project

GitHub: https://github.com/gerrymanoim/exchange_calendars
"""

from .market_calendar import MarketCalendar
import exchange_calendars


class TradingCalendar(MarketCalendar):
    _FINALIZE_TRADING_CALENDAR = True

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        self._tc = super().__new__(cls._tc_class)
        self._TC_NOT_INITIALIZED = True

        # offsets of exchange_calendar_mirrors are only available through the instance
        if cls._FINALIZE_TRADING_CALENDAR:
            if self._tc.open_offset:
                cls.regular_market_times._ALLOW_SETTING_TIMES = True
                cls.regular_market_times["market_open"] = tuple(
                    (t[0], t[1], self._tc.open_offset) for t in cls.regular_market_times["market_open"])

            if self._tc.close_offset:
                cls.regular_market_times._ALLOW_SETTING_TIMES = True
                cls.regular_market_times["market_close"] = tuple(
                    (t[0], t[1], self._tc.close_offset) for t in cls.regular_market_times["market_close"])
            cls._FINALIZE_TRADING_CALENDAR = False

        self.__init__(*args, **kwargs)
        return self

    def __init__(self, open_time=None, close_time=None):
        super().__init__(open_time, close_time)

    @property
    def tc(self):
        if self._TC_NOT_INITIALIZED:
            self._tc.__init__()
            self._TC_NOT_INITIALIZED = False

        return self._tc

    @property
    def name(self):
        return self._tc.name

    @property
    def tz(self):
        return self._tc.tz

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


calendars = exchange_calendars.calendar_utils._default_calendar_factories  # noqa

time_props = dict(open_times= "market_open",
                  close_times= "market_close",
                  break_start_times= "break_start",
                  break_end_times= "break_end")

for exchange in calendars:
    cal = calendars[exchange]

    # this loop will set up the newly required regular_market_times dictionary
    regular_market_times = {}
    for prop, new in time_props.items():
        times = getattr(cal, prop)
        if times is None or isinstance(times, property): continue
        regular_market_times[new] = times

    cal = type(exchange, (TradingCalendar,), {'_tc_class': calendars[exchange],
                                              'alias': [exchange],
                                              'regular_market_times': regular_market_times})
    locals()[exchange + 'ExchangeCalendar'] = cal





