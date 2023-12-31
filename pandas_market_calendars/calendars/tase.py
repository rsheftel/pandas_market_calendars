from datetime import time

from pandas import Timestamp
from pytz import timezone

from pandas_market_calendars.market_calendar import MarketCalendar

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
]


class TASEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for TASE Stock Exchange

    Note these dates are only checked against 2020 and 2021
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

    @property
    def name(self):
        return "TASE"

    @property
    def tz(self):
        return timezone("Asia/Jerusalem")

    @property
    def adhoc_holidays(self):
        return TASEClosedDay

    @property
    def weekmask(self):
        return "Sun Mon Tue Wed Thu"
