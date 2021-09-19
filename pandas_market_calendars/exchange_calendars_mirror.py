"""
Imported calendars from the exchange_calendars project

GitHub: https://github.com/gerrymanoim/exchange_calendars
"""

from datetime import time
from .market_calendar import MarketCalendar
import exchange_calendars


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
        return self._tc.open_times[0][1].replace(tzinfo=self.tz)

    @property
    def close_time_default(self):
        return self._tc.close_times[0][1].replace(tzinfo=self.tz)

    @property
    def break_start(self):
        tc_time = self._tc.break_start_times
        return tc_time[0][1] if tc_time else None

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




# Convert the lists of tuples in exchange calendars to the new MarketCalendar format
def _exchange_calendars_times_to_market_calendars(times):
    times = dict(times)

    cut_offs = list(times.keys())
    cut_offs.remove(None)
    cut_offs.sort()
    cut_offs.insert(0, None)

    all_times = {None: times[cut_offs[-1]]}
    all_times.update({
        cut_offs[i + 1]: times[cut_off] for i, cut_off in enumerate(cut_offs[:-1])})
    return all_times



calendars = exchange_calendars.calendar_utils._default_calendar_factories  # noqa
time_props = dict(open_times= "market_open",
                  close_times= "market_close",
                  break_start_times= "break_start",
                  break_end_times= "break_end")

for exchange in calendars:
    cal = type(exchange, (TradingCalendar, ), {'_tc_class': calendars[exchange], 'alias': [exchange]})

    locals()[exchange + 'ExchangeCalendar'] = cal

    for prop, new in time_props.items():
        times = getattr(cal._tc_class, prop)
        if times is None: continue
        print(cal)
        print(times)
        cal._all_market_times[new] = _exchange_calendars_times_to_market_calendars(times)







