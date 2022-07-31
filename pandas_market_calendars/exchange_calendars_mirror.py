"""
Imported calendars from the exchange_calendars project

GitHub: https://github.com/gerrymanoim/exchange_calendars
"""

from .market_calendar import MarketCalendar
import exchange_calendars


class TradingCalendar(MarketCalendar):
    """
    This class provides access to all the information on opens, breaks and closes that are available
    in the exchange_calendars package, it will receive the correctly formatted regular_market_times
    dictionary in the for-loop below.

    The initialization of calendars from exchange_calendars, is bypassed until the `.ec` property is used,
    which returns the initialized exchange_calendar calendar, which is only initialized the first time.
    """
    # flag indicating that offset still needs to be checked.
    # A class attribute so we only do this once per class and not per instance
    _FINALIZE_TRADING_CALENDAR = True

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        self._ec = super().__new__(cls._ec_class)
        # flag indicating that mirrored class is not initialized yet, which we only want to do
        # once per instance, if and only if the public `.ec` property is used.
        self._EC_NOT_INITIALIZED = True

        # offsets of exchange_calendar_mirrors are only available through the instance
        if cls._FINALIZE_TRADING_CALENDAR:
            if self._ec.open_offset:
                cls.regular_market_times._set("market_open", tuple(
                    (t[0], t[1], self._ec.open_offset) for t in cls.regular_market_times["market_open"]))

            if self._ec.close_offset:
                cls.regular_market_times._set("market_close", tuple(
                    (t[0], t[1], self._ec.close_offset) for t in cls.regular_market_times["market_close"]))
            cls._FINALIZE_TRADING_CALENDAR = False

        self.__init__(*args, **kwargs)
        return self

    def __init__(self, open_time=None, close_time=None):
        super().__init__(open_time, close_time)

    @property
    def ec(self):
        if self._EC_NOT_INITIALIZED:
            self._ec.__init__()
            self._EC_NOT_INITIALIZED = False

        return self._ec

    @property
    def name(self):
        return self._ec.name

    @property
    def tz(self):
        return self._ec.tz

    @property
    def regular_holidays(self):
        return self._ec.regular_holidays

    @property
    def adhoc_holidays(self):
        return self._ec.adhoc_holidays

    @property
    def special_opens(self):
        return self._ec.special_opens

    @property
    def special_opens_adhoc(self):
        return self._ec.special_opens_adhoc

    @property
    def special_closes(self):
        return self._ec.special_closes

    @property
    def special_closes_adhoc(self):
        return self._ec.special_closes_adhoc


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

    cal = type(exchange, (TradingCalendar,), {'_ec_class': calendars[exchange],
                                              'alias': [exchange],
                                              'regular_market_times': regular_market_times})
    locals()[exchange + 'ExchangeCalendar'] = cal





