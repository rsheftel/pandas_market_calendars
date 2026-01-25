"""
Imported calendars from the exchange_calendars project

GitHub: https://github.com/gerrymanoim/exchange_calendars
"""

import exchange_calendars
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay

from pandas_market_calendars.market_calendar import MarketCalendar


DAYMASKS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# XTAE (Tel Aviv Stock Exchange) changed from Sun-Thu to Mon-Fri on Jan 5, 2026
XTAE_TRANSITION_DATE = pd.Timestamp("2026-01-05")
XTAE_WEEKMASK_OLD = "Sun Mon Tue Wed Thu"  # Before Jan 5, 2026
XTAE_WEEKMASK_NEW = "Mon Tue Wed Thu Fri"  # From Jan 5, 2026


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
                cls.regular_market_times._set(
                    "market_open",
                    tuple((t[0], t[1], self._ec.open_offset) for t in cls.regular_market_times["market_open"]),
                )

            if self._ec.close_offset:
                cls.regular_market_times._set(
                    "market_close",
                    tuple((t[0], t[1], self._ec.close_offset) for t in cls.regular_market_times["market_close"]),
                )
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
    def full_name(self):
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

    @property
    def weekmask(self):
        if hasattr(self._ec, "weekmask"):
            if "1" in self._ec.weekmask or "0" in self._ec.weekmask:
                # Convert 1s & 0s to Day Abbreviations
                return " ".join([DAYMASKS[i] for i, val in enumerate(self._ec.weekmask) if val == "1"])
            else:
                return self._ec.weekmask
        else:
            return "Mon Tue Wed Thu Fri"


calendars = exchange_calendars.calendar_utils._default_calendar_factories

time_props = {
    "open_times": "market_open",
    "close_times": "market_close",
    "break_start_times": "break_start",
    "break_end_times": "break_end",
}

for exchange in calendars:
    cal = calendars[exchange]

    # this loop will set up the newly required regular_market_times dictionary
    regular_market_times = {}
    for prop, new in time_props.items():
        times = getattr(cal, prop)
        if times is None or isinstance(times, property):
            continue
        regular_market_times[new] = times

    cal = type(
        exchange,
        (TradingCalendar,),
        {
            "_ec_class": calendars[exchange],
            "alias": [exchange],
            "regular_market_times": regular_market_times,
        },
    )
    locals()[f"{exchange}ExchangeCalendar"] = cal


class XTAEExchangeCalendar(TradingCalendar):
    """
    Custom XTAE (Tel Aviv Stock Exchange) calendar that handles the weekmask transition.

    TASE changed its trading week from Sunday-Thursday to Monday-Friday on January 5, 2026
    to align with international markets. This calendar properly handles both schedules
    based on the requested date range.

    See: https://github.com/gerrymanoim/exchange_calendars/issues/518
    """

    _ec_class = calendars["XTAE"]
    aliases = ["XTAE"]  # Note: must be "aliases" (plural) for registry to pick it up

    # Get regular_market_times from the exchange_calendars XTAE
    regular_market_times = {}
    for prop, new in time_props.items():
        times = getattr(calendars["XTAE"], prop)
        if times is not None and not isinstance(times, property):
            regular_market_times[new] = times

    @property
    def weekmask(self):
        # Default to the new weekmask (Mon-Fri) for the base property
        # The actual date-dependent logic is in valid_days
        return XTAE_WEEKMASK_NEW

    def _get_holidays_for_weekmask(self, weekmask: str) -> CustomBusinessDay:
        """Create a CustomBusinessDay with the specified weekmask."""
        return CustomBusinessDay(
            holidays=self.adhoc_holidays,
            calendar=self.regular_holidays,
            weekmask=weekmask,
        )

    def valid_days(self, start_date, end_date, tz="UTC") -> pd.DatetimeIndex:
        """
        Get a DatetimeIndex of valid open business days, handling the XTAE weekmask transition.

        Before Jan 5, 2026: Sunday-Thursday
        From Jan 5, 2026: Monday-Friday

        :param start_date: start date
        :param end_date: end date
        :param tz: time zone in either string or pytz.timezone
        :return: DatetimeIndex of valid business days
        """
        start_date = pd.Timestamp(start_date).normalize()
        end_date = pd.Timestamp(end_date).normalize()

        # If entirely before transition, use old weekmask
        if end_date < XTAE_TRANSITION_DATE:
            holidays = self._get_holidays_for_weekmask(XTAE_WEEKMASK_OLD)
            return pd.date_range(start_date, end_date, freq=holidays, normalize=True, tz=tz)

        # If entirely after transition, use new weekmask
        if start_date >= XTAE_TRANSITION_DATE:
            holidays = self._get_holidays_for_weekmask(XTAE_WEEKMASK_NEW)
            return pd.date_range(start_date, end_date, freq=holidays, normalize=True, tz=tz)

        # Spans the transition - need to combine both
        holidays_old = self._get_holidays_for_weekmask(XTAE_WEEKMASK_OLD)
        holidays_new = self._get_holidays_for_weekmask(XTAE_WEEKMASK_NEW)

        # Get days before transition (up to and including last day before transition)
        days_before = pd.date_range(
            start_date,
            XTAE_TRANSITION_DATE - pd.Timedelta(days=1),
            freq=holidays_old,
            normalize=True,
            tz=tz,
        )

        # Get days from transition onwards
        days_after = pd.date_range(
            XTAE_TRANSITION_DATE,
            end_date,
            freq=holidays_new,
            normalize=True,
            tz=tz,
        )

        # Combine and return
        return days_before.union(days_after)
