from datetime import time
from typing import Any, List, Literal, Union

from pandas import DatetimeIndex, Timedelta, Timestamp, date_range
from pandas.tseries.offsets import CustomBusinessDay
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendar_utils import Day_Anchor, Month_Anchor
from pandas_market_calendars.market_calendar import FRIDAY, MarketCalendar


TASEClosedDay = [
    # 2019
    Timestamp("2019-03-21", tz="Asia/Jerusalem"),
    Timestamp("2019-04-09", tz="Asia/Jerusalem"),
    Timestamp("2019-04-25", tz="Asia/Jerusalem"),
    Timestamp("2019-04-26", tz="Asia/Jerusalem"),
    Timestamp("2019-05-08", tz="Asia/Jerusalem"),
    Timestamp("2019-05-09", tz="Asia/Jerusalem"),
    Timestamp("2019-06-09", tz="Asia/Jerusalem"),
    Timestamp("2019-08-11", tz="Asia/Jerusalem"),
    Timestamp("2019-09-17", tz="Asia/Jerusalem"),
    Timestamp("2019-09-29", tz="Asia/Jerusalem"),
    Timestamp("2019-09-30", tz="Asia/Jerusalem"),
    Timestamp("2019-10-01", tz="Asia/Jerusalem"),
    Timestamp("2019-10-08", tz="Asia/Jerusalem"),
    Timestamp("2019-10-09", tz="Asia/Jerusalem"),
    Timestamp("2019-10-13", tz="Asia/Jerusalem"),
    Timestamp("2019-10-14", tz="Asia/Jerusalem"),
    Timestamp("2019-10-20", tz="Asia/Jerusalem"),
    Timestamp("2019-10-21", tz="Asia/Jerusalem"),
    # 2020
    Timestamp("2020-03-02", tz="Asia/Jerusalem"),
    Timestamp("2020-03-10", tz="Asia/Jerusalem"),
    Timestamp("2020-04-08", tz="Asia/Jerusalem"),
    Timestamp("2020-04-09", tz="Asia/Jerusalem"),
    Timestamp("2020-04-14", tz="Asia/Jerusalem"),
    Timestamp("2020-04-15", tz="Asia/Jerusalem"),
    Timestamp("2020-04-28", tz="Asia/Jerusalem"),
    Timestamp("2020-04-29", tz="Asia/Jerusalem"),
    Timestamp("2020-05-28", tz="Asia/Jerusalem"),
    Timestamp("2020-05-29", tz="Asia/Jerusalem"),
    Timestamp("2020-07-30", tz="Asia/Jerusalem"),
    Timestamp("2020-09-20", tz="Asia/Jerusalem"),
    Timestamp("2020-09-27", tz="Asia/Jerusalem"),
    Timestamp("2020-09-28", tz="Asia/Jerusalem"),
    # 2021
    Timestamp("2021-02-26", tz="Asia/Jerusalem"),
    Timestamp("2021-03-28", tz="Asia/Jerusalem"),
    Timestamp("2021-04-02", tz="Asia/Jerusalem"),
    Timestamp("2021-04-14", tz="Asia/Jerusalem"),
    Timestamp("2021-04-15", tz="Asia/Jerusalem"),
    Timestamp("2021-05-16", tz="Asia/Jerusalem"),
    Timestamp("2021-05-17", tz="Asia/Jerusalem"),
    Timestamp("2021-07-18", tz="Asia/Jerusalem"),
    Timestamp("2021-09-06", tz="Asia/Jerusalem"),
    Timestamp("2021-09-07", tz="Asia/Jerusalem"),
    Timestamp("2021-09-08", tz="Asia/Jerusalem"),
    Timestamp("2021-09-15", tz="Asia/Jerusalem"),
    Timestamp("2021-09-16", tz="Asia/Jerusalem"),
    Timestamp("2021-09-20", tz="Asia/Jerusalem"),
    Timestamp("2021-09-21", tz="Asia/Jerusalem"),
    Timestamp("2021-09-27", tz="Asia/Jerusalem"),
    Timestamp("2021-09-28", tz="Asia/Jerusalem"),
    # 2022
    Timestamp("2022-03-17", tz="Asia/Jerusalem"),
    Timestamp("2022-03-18", tz="Asia/Jerusalem"),
    Timestamp("2022-04-15", tz="Asia/Jerusalem"),
    Timestamp("2022-04-21", tz="Asia/Jerusalem"),
    Timestamp("2022-04-22", tz="Asia/Jerusalem"),
    Timestamp("2022-05-05", tz="Asia/Jerusalem"),
    Timestamp("2022-06-05", tz="Asia/Jerusalem"),
    Timestamp("2022-08-07", tz="Asia/Jerusalem"),
    Timestamp("2022-09-25", tz="Asia/Jerusalem"),
    Timestamp("2022-09-26", tz="Asia/Jerusalem"),
    Timestamp("2022-09-27", tz="Asia/Jerusalem"),
    Timestamp("2022-10-04", tz="Asia/Jerusalem"),
    Timestamp("2022-10-05", tz="Asia/Jerusalem"),
    Timestamp("2022-10-09", tz="Asia/Jerusalem"),
    Timestamp("2022-10-10", tz="Asia/Jerusalem"),
    Timestamp("2022-10-16", tz="Asia/Jerusalem"),
    Timestamp("2022-10-17", tz="Asia/Jerusalem"),
    Timestamp("2022-11-01", tz="Asia/Jerusalem"),
    # 2023
    Timestamp("2023-03-07", tz="Asia/Jerusalem"),
    Timestamp("2023-03-08", tz="Asia/Jerusalem"),
    Timestamp("2023-04-05", tz="Asia/Jerusalem"),
    Timestamp("2023-04-06", tz="Asia/Jerusalem"),
    Timestamp("2023-04-11", tz="Asia/Jerusalem"),
    Timestamp("2023-04-12", tz="Asia/Jerusalem"),
    Timestamp("2023-04-25", tz="Asia/Jerusalem"),
    Timestamp("2023-04-26", tz="Asia/Jerusalem"),
    Timestamp("2023-05-25", tz="Asia/Jerusalem"),
    Timestamp("2023-05-26", tz="Asia/Jerusalem"),
    Timestamp("2023-07-27", tz="Asia/Jerusalem"),
    Timestamp("2023-09-15", tz="Asia/Jerusalem"),
    Timestamp("2023-09-17", tz="Asia/Jerusalem"),
    Timestamp("2023-09-24", tz="Asia/Jerusalem"),
    Timestamp("2023-09-25", tz="Asia/Jerusalem"),
    Timestamp("2023-09-29", tz="Asia/Jerusalem"),
    Timestamp("2023-10-06", tz="Asia/Jerusalem"),
    Timestamp("2023-10-31", tz="Asia/Jerusalem"),
    # 2024
    Timestamp("2024-03-24", tz="Asia/Jerusalem"),
    Timestamp("2024-03-25", tz="Asia/Jerusalem"),
    Timestamp("2024-04-22", tz="Asia/Jerusalem"),
    Timestamp("2024-04-23", tz="Asia/Jerusalem"),
    Timestamp("2024-04-28", tz="Asia/Jerusalem"),
    Timestamp("2024-04-29", tz="Asia/Jerusalem"),
    Timestamp("2024-05-13", tz="Asia/Jerusalem"),
    Timestamp("2024-05-14", tz="Asia/Jerusalem"),
    Timestamp("2024-06-11", tz="Asia/Jerusalem"),
    Timestamp("2024-06-12", tz="Asia/Jerusalem"),
    Timestamp("2024-08-13", tz="Asia/Jerusalem"),
    Timestamp("2024-10-02", tz="Asia/Jerusalem"),
    Timestamp("2024-10-03", tz="Asia/Jerusalem"),
    Timestamp("2024-10-04", tz="Asia/Jerusalem"),
    Timestamp("2024-10-11", tz="Asia/Jerusalem"),
    Timestamp("2024-10-16", tz="Asia/Jerusalem"),
    Timestamp("2024-10-17", tz="Asia/Jerusalem"),
    Timestamp("2024-10-23", tz="Asia/Jerusalem"),
    Timestamp("2024-10-24", tz="Asia/Jerusalem"),
    # 2025
    Timestamp("2025-03-14", tz="Asia/Jerusalem"),
    Timestamp("2025-04-13", tz="Asia/Jerusalem"),
    Timestamp("2025-04-18", tz="Asia/Jerusalem"),
    Timestamp("2025-04-30", tz="Asia/Jerusalem"),
    Timestamp("2025-05-01", tz="Asia/Jerusalem"),
    Timestamp("2025-06-01", tz="Asia/Jerusalem"),
    Timestamp("2025-06-02", tz="Asia/Jerusalem"),
    Timestamp("2025-08-03", tz="Asia/Jerusalem"),
    Timestamp("2025-09-22", tz="Asia/Jerusalem"),
    Timestamp("2025-09-23", tz="Asia/Jerusalem"),
    Timestamp("2025-09-24", tz="Asia/Jerusalem"),
    Timestamp("2025-10-01", tz="Asia/Jerusalem"),
    Timestamp("2025-10-02", tz="Asia/Jerusalem"),
    Timestamp("2025-10-06", tz="Asia/Jerusalem"),
    Timestamp("2025-10-07", tz="Asia/Jerusalem"),
    Timestamp("2025-10-13", tz="Asia/Jerusalem"),
    Timestamp("2025-10-14", tz="Asia/Jerusalem"),
    # 2026 (Monday-Friday trading week from 2026-01-05)
    Timestamp("2026-03-03", tz="Asia/Jerusalem"),
    Timestamp("2026-04-01", tz="Asia/Jerusalem"),
    Timestamp("2026-04-02", tz="Asia/Jerusalem"),
    Timestamp("2026-04-07", tz="Asia/Jerusalem"),
    Timestamp("2026-04-08", tz="Asia/Jerusalem"),
    Timestamp("2026-04-21", tz="Asia/Jerusalem"),
    Timestamp("2026-04-22", tz="Asia/Jerusalem"),
    Timestamp("2026-05-21", tz="Asia/Jerusalem"),
    Timestamp("2026-05-22", tz="Asia/Jerusalem"),
    Timestamp("2026-07-23", tz="Asia/Jerusalem"),
    Timestamp("2026-09-11", tz="Asia/Jerusalem"),
    Timestamp("2026-09-18", tz="Asia/Jerusalem"),
    Timestamp("2026-09-21", tz="Asia/Jerusalem"),
    Timestamp("2026-09-25", tz="Asia/Jerusalem"),
    Timestamp("2026-10-02", tz="Asia/Jerusalem"),
    # 2027
    Timestamp("2027-03-23", tz="Asia/Jerusalem"),
    Timestamp("2027-04-21", tz="Asia/Jerusalem"),
    Timestamp("2027-04-22", tz="Asia/Jerusalem"),
    Timestamp("2027-04-27", tz="Asia/Jerusalem"),
    Timestamp("2027-04-28", tz="Asia/Jerusalem"),
    Timestamp("2027-05-11", tz="Asia/Jerusalem"),
    Timestamp("2027-05-12", tz="Asia/Jerusalem"),
    Timestamp("2027-06-10", tz="Asia/Jerusalem"),
    Timestamp("2027-06-11", tz="Asia/Jerusalem"),
    Timestamp("2027-08-12", tz="Asia/Jerusalem"),
    Timestamp("2027-10-01", tz="Asia/Jerusalem"),
    Timestamp("2027-10-08", tz="Asia/Jerusalem"),
    Timestamp("2027-10-11", tz="Asia/Jerusalem"),
    Timestamp("2027-10-15", tz="Asia/Jerusalem"),
    Timestamp("2027-10-22", tz="Asia/Jerusalem"),
]


class TASEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for TASE Stock Exchange

    TASE moved from a Sunday-Thursday to a Monday-Friday trading week effective
    2026-01-05; the last Sunday session was 2026-01-04. Friday sessions close
    early, ahead of Shabbat.
    https://www.tase.co.il/en/content/knowledge_center/trading_vacation_schedule/

    Note the dates before 2026 are only checked against 2020 and 2021
    https://info.tase.co.il/Eng/about_tase/corporate/Pages/vacation_schedule.aspx

    Opening times for the regular trading of equities (not including closing auction call)
    Open Time: 10:00 AM Asia/Jerusalem
    Close Time: 3:59 PM Asia/Jerusalem

    Daylight Saving Time in Israel comes into effect on the Friday before the last Sunday in March, and lasts until the
    last Sunday in October.
    During the Daylight Saving time period the clock will be UTC+3, and for the rest of the year UTC+2.

    Regularly-Observed Holidays (not necessarily in order):
    - Purim
    - Passover_I_Eve
    - Passover_I
    - Passover_II_Eve
    - Passover_II
    - Independence_Day
    - Yom_HaZikaron
    - Shavuot_Eve
    - Shavuot
    - Tisha_beAv
    - Jewish_New_Year_Eve
    - Jewish_New_Year_I
    - Jewish_New_Year_II
    - Yom_Kippur_Eve
    - Yom_Kippur
    - Sukkoth_Eve
    - Sukkoth
    - Simchat_Tora_Eve
    - Simchat_Tora
    """

    aliases = ["TASE"]
    regular_market_times = {
        "market_open": ((None, time(10)),),
        "market_close": ((None, time(15, 59)),),
    }

    # Last session of the Sunday-Thursday trading week; Monday-Friday trading
    # started 2026-01-05
    _sunday_end = Timestamp("2026-01-04", tz="UTC")

    @property
    def name(self) -> str:
        return "TASE"

    @property
    def full_name(self) -> str:
        return "Tel Aviv Stock Exchange"

    @property
    def tz(self) -> Any:
        return ZoneInfo("Asia/Jerusalem")

    @property
    def adhoc_holidays(self) -> List[Any]:
        return TASEClosedDay

    @property
    def weekmask(self) -> str:
        return "Mon Tue Wed Thu Fri"

    @property
    def weekmask_pre_2026(self) -> str:
        return "Sun Mon Tue Wed Thu"

    def holidays_pre_2026(self) -> CustomBusinessDay:
        """
        TASE traded Sunday-Thursday before the move to a Monday-Friday trading
        week effective 2026-01-05 (the last Sunday session was 2026-01-04).
        CustomBusinessDay object that can be used in place of holidays() for
        dates prior to the crossover.

        :return: CustomBusinessDay object of holidays
        """
        if hasattr(self, "_holidays_pre_2026"):
            return self._holidays_pre_2026

        self._holidays_pre_2026 = CustomBusinessDay(
            holidays=self.adhoc_holidays,
            weekmask=self.weekmask_pre_2026,
        )
        return self._holidays_pre_2026

    @property
    def special_closes(self) -> List[Any]:
        # Friday sessions (from 2026-01-05) end at 13:34, before Shabbat
        return [(time(13, 34), FRIDAY)]

    def valid_days(self, start_date: Any, end_date: Any, tz: Any = "UTC") -> DatetimeIndex:
        """
        Get a DatetimeIndex of valid open business days.

        Handles the trading week change from Sunday-Thursday to Monday-Friday
        effective 2026-01-05.

        :param start_date: start date
        :param end_date: end date
        :param tz: time zone in either string or pytz.timezone
        :return: DatetimeIndex of valid business days
        """
        start_date = Timestamp(start_date)
        end_date = Timestamp(end_date)
        start_date = start_date.tz_convert(tz) if start_date.tz else start_date.tz_localize(tz)
        end_date = end_date.tz_convert(tz) if end_date.tz else end_date.tz_localize(tz)

        if tz is None:
            sunday_end = self._sunday_end.tz_localize(None)
        else:
            sunday_end = self._sunday_end

        # Entirely within the Monday-Friday trading week. Call super.
        if start_date > sunday_end:
            return super().valid_days(start_date, end_date, tz=tz)

        # Entirely within the Sunday-Thursday trading week. Augment the super call.
        if end_date <= sunday_end:
            return date_range(
                start_date,
                end_date,
                freq=self.holidays_pre_2026(),
                normalize=True,
                tz=tz,
            )

        # Range is split across the crossover. Concatenate two date_range calls.
        days_pre = date_range(
            start_date,
            sunday_end,
            freq=self.holidays_pre_2026(),
            normalize=True,
            tz=tz,
        )
        days_post = date_range(sunday_end, end_date, freq=self.holidays(), normalize=True, tz=tz)
        return days_pre.union(days_post)

    def date_range_htf(
        self,
        frequency: Union[str, Timedelta, int, float],
        start: Union[str, Timestamp, int, float, None] = None,
        end: Union[str, Timestamp, int, float, None] = None,
        periods: Union[int, None] = None,
        closed: Union[Literal["left", "right"], None] = "right",
        *,
        day_anchor: Day_Anchor = "SAT",  # Change the default day anchor
        month_anchor: Month_Anchor = "JAN",
    ) -> DatetimeIndex:
        return super().date_range_htf(
            frequency,
            start,
            end,
            periods,
            closed,
            day_anchor=day_anchor,
            month_anchor=month_anchor,
        )
