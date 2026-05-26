from datetime import time
from itertools import chain

import pandas as pd
from pandas.tseries.holiday import (
    MO,
    AbstractHolidayCalendar,
    DateOffset,
    GoodFriday,
    Holiday,
    weekend_to_monday,
)
from pandas_market_calendars.market_calendar import MarketCalendar
from pandas.tseries.offsets import BusinessDay
from zoneinfo import ZoneInfo

from pandas_market_calendars.holidays.uk import (
    BoxingDay,
    WeekendBoxingDay,
    WeekendChristmas,
)

from pandas_market_calendars.holidays.my import (
    ChineseNewYear1,
    ChineseNewYear2,
    Thaipusam,
    WesakDay,
    HariRayaPuasa1,
    HariRayaPuasa2,
    NuzulAlQuran,
    HariRayaHaji,
    MaalHijrah,
    MaulidNabi,
    Deepavali,
    NewYearsDay,
    LabourDay,
    YangDiPertuanAgongBirthday,
    NationalDay,
    MalaysiaDay,
    ChristmasDay,
)


class BursaMalaysiaBaseExchangeCalendar(MarketCalendar):
    """
    Base Exchange calendar for Bursa Malaysia

    The days follow a variety of the following:
    - Open
    - "Intraday pause" (typically 1h30 minute break, different per market)
    - Reopen
    - Close
    - T+1 session reopen
    - Close

    As this library only supports one break per day, and the T+1 session is janky,
    I'm ignoring T+1 session for now.

    Regularly-Observed Holidays:
        Fixed-date
        ----------
        - New Year's Day              (1 Jan; Sun → Mon)
        - Labour Day                  (1 May; Sun → Mon)
        - Yang Di-Pertuan Agong B'day (1st Mon of Jun)
        - National Day                (31 Aug; Sun → Mon)
        - Malaysia Day                (16 Sep; Sun → Mon)
        - Christmas Day               (25 Dec; Sun → Mon)

        Lunar / Islamic (ad-hoc per year, subject to moon sighting)
        -----------------------------------------------------------
        - Chinese New Year Day 1 & Day 2
        - Thaipusam
        - Nuzul Al-Quran
        - Hari Raya Puasa (Aidilfitri) Day 1 & Day 2
        - Wesak Day (Vesak)
        - Hari Raya Haji (Aidiladha)
        - Awal Muharram (Islamic New Year)
        - Birthday of Prophet Muhammad (Maulidur Rasul)
        - Deepavali

    Notes:
        - Eid/Islamic dates depend on moon sighting and may change at short
          notice.  Always cross-check against official Bursa announcements
          before use.
        - Federal Territory Day (1 Feb) applies to Labuan/KL offices but
          Bursa Malaysia does NOT close the exchange for it.
        - Source: https://www.bursamalaysia.com/about_bursa/about_us/calendar
    """

    @property
    def tz(self):
        return ZoneInfo("Asia/Kuala_Lumpur")

    @property
    def regular_holidays(self):
        # Collect all ad-hoc lunar/Islamic dates as Holiday rules
        adhoc_rules = []
        for cal in [
            ChineseNewYear1,
            ChineseNewYear2,
            Thaipusam,
            WesakDay,
            HariRayaPuasa1,
            HariRayaPuasa2,
            NuzulAlQuran,
            HariRayaHaji,
            MaalHijrah,
            MaulidNabi,
            Deepavali,
        ]:
            adhoc_rules.extend(cal.rules)

        return AbstractHolidayCalendar(
            rules=[
                NewYearsDay,
                LabourDay,
                YangDiPertuanAgongBirthday,
                NationalDay,
                MalaysiaDay,
                ChristmasDay,
                *adhoc_rules,
            ]
        )


class BursaMalaysiaFCPOExchangeCalendar(BursaMalaysiaBaseExchangeCalendar):
    aliases = [
        "BURSAMY_FCPO",
    ]

    @property
    def name(self):
        return "BURSAMY_FCPO"

    @property
    def full_name(self):
        return "Bursa Malaysi FCPO"

    regular_market_times = {
        "market_open": ((None, time(10, 30)),),
        "break_start": ((None, time(12, 30)),),
        "break_end": ((None, time(14, 30)),),
        "market_close": ((None, time(18)),),
        # T+1 session - 21:00 -> 23:00 except on fridays
    }


class BursaMalaysiaFKLIExchangeCalendar(BursaMalaysiaBaseExchangeCalendar):
    aliases = [
        "BURSAMY_FKLI",
    ]

    @property
    def name(self):
        return "BURSAMY_FKLI"

    @property
    def full_name(self):
        return "Bursa Malaysi FKLI"

    regular_market_times = {
        "market_open": ((None, time(8, 45)),),
        "break_start": ((None, time(12, 45)),),
        "break_end": ((None, time(14, 30)),),
        "market_close": ((None, time(17, 15)),),
        # T+1 session - 21:00 -> 02:30 T+1 except on fridays
    }
