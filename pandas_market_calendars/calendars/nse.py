"""
National Stock Exchange of India (NSE, XNSE).
"""

from datetime import time
from typing import Any, List

from pandas import Timestamp
from zoneinfo import ZoneInfo

from pandas_market_calendars.holidays.nse import NSEClosedDay
from pandas_market_calendars.market_calendar import MarketCalendar


class NSEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for the National Stock Exchange of India (NSE, XNSE).

    Coverage is 1996 through 2026. Holidays and special sessions are curated
    from NSE circulars, contemporaneous press coverage of exchange
    announcements, and observed market activity. Outside this range no
    holidays or special sessions are defined and the nearest era's regular
    hours apply.

    Regular hours are era-dependent: a 9:55 AM IST open until 2010, 9:00 AM
    during the 2010 pre-open-auction pilot, 9:15 AM since 2010-10-18, and
    several short-lived 1997-1999 changes. Times cover the continuous
    session only; the pre-open call auction and post-close session fall
    outside the open/close times.

    Muhurat trading dates are not holidays: NSE holds an evening session on
    Diwali with times announced fresh each year, modeled as special opens
    and closes. Weekend sessions -- Muhurat dates falling on Saturday or
    Sunday, union-budget sessions at regular hours, and announced special
    live sessions -- are listed in adhoc_sessions.

    Interruptions model the 2021-02-24 telecom failure (halted 11:40 AM,
    reopened 3:45-5:00 PM) and the two-window Saturday sessions on
    2004-04-17 and 2004-10-09.
    """

    aliases = ["NSE", "XNSE"]
    regular_market_times = {
        "market_open": (
            (None, time(10, 0)),
            ("1997-07-30", time(9, 30)),
            ("1997-08-07", time(9, 0)),
            ("1997-08-14", time(9, 30)),
            ("1998-07-01", time(10, 0)),
            ("1998-11-18", time(9, 55)),
            ("2010-01-04", time(9, 0)),
            ("2010-10-18", time(9, 15)),
        ),
        "market_close": (
            (None, time(15, 30)),
            ("1997-07-30", time(15, 0)),
            ("1997-08-07", time(14, 30)),
            ("1997-08-14", time(15, 0)),
            ("1997-09-29", time(15, 30)),
            ("1997-10-10", time(16, 0)),
            ("1998-05-18", time(15, 30)),
            ("1998-11-18", time(15, 45)),
            ("1999-06-09", time(15, 30)),
        ),
    }

    @property
    def name(self) -> str:
        return "NSE"

    @property
    def full_name(self) -> str:
        return "National Stock Exchange of India"

    @property
    def tz(self) -> Any:
        return ZoneInfo("Asia/Calcutta")

    @property
    def adhoc_holidays(self) -> List[Any]:
        return NSEClosedDay

    @property
    def adhoc_sessions(self) -> List[Any]:
        return [
            Timestamp("1996-11-10"),
            Timestamp("1997-03-01"),
            Timestamp("1997-04-12"),
            Timestamp("1998-10-31"),
            Timestamp("1998-11-21"),
            Timestamp("1998-11-28"),
            Timestamp("1999-02-27"),
            Timestamp("1999-04-17"),
            Timestamp("1999-11-07"),
            Timestamp("2003-02-01"),
            Timestamp("2003-03-22"),
            Timestamp("2003-10-25"),
            Timestamp("2003-11-15"),
            Timestamp("2004-04-17"),
            Timestamp("2004-10-09"),
            Timestamp("2005-06-04"),
            Timestamp("2005-11-26"),
            Timestamp("2006-04-29"),
            Timestamp("2006-06-25"),
            Timestamp("2006-10-21"),
            Timestamp("2009-10-17"),
            Timestamp("2010-02-06"),
            Timestamp("2012-01-07"),
            Timestamp("2012-03-03"),
            Timestamp("2012-04-28"),
            Timestamp("2012-09-08"),
            Timestamp("2013-05-11"),
            Timestamp("2013-11-03"),
            Timestamp("2014-03-22"),
            Timestamp("2015-02-28"),
            Timestamp("2016-10-30"),
            Timestamp("2019-10-27"),
            Timestamp("2020-02-01"),
            Timestamp("2020-11-14"),
            Timestamp("2023-11-12"),
            Timestamp("2024-01-20"),
            Timestamp("2025-02-01"),
            Timestamp("2026-02-01"),
        ]

    @property
    def special_opens_adhoc(self) -> List[Any]:
        # Muhurat and weekend special sessions. Times are the announced
        # continuous session (NSE press releases / circulars, or
        # contemporaneous press coverage of the announcement); dates without
        # a surviving announcement use the observed session bounds.
        return [
            (time(10, 30), ["2005-06-04", "2005-11-26", "2006-04-29", "2006-06-25"]),
            (time(10, 35), ["1998-11-21"]),
            (
                time(11, 0),
                [
                    "2003-03-22",
                    "2003-11-15",
                    "2004-04-17",
                    "2004-10-09",
                    "2010-02-06",
                ],
            ),
            (time(11, 1), ["2003-02-01"]),
            (
                time(11, 15),
                [
                    "2012-01-07",
                    "2012-03-03",
                    "2012-04-28",
                    "2012-09-08",
                    "2013-05-11",
                    "2014-03-22",
                ],
            ),
            (time(11, 37), ["1998-10-31"]),
            (time(13, 45), ["2025-10-21"]),
            (time(15, 45), ["2012-11-13"]),
            (time(16, 45), ["2011-10-26"]),
            (time(17, 0), ["2001-11-14", "2002-11-04"]),
            (time(17, 28), ["1998-10-19"]),
            (time(17, 30), ["2004-11-12", "2018-11-07"]),
            (time(17, 45), ["2015-11-11"]),
            (time(18, 0), ["2007-11-09", "2024-11-01"]),
            (time(18, 4), ["1996-11-10"]),
            (time(18, 5), ["2005-11-01"]),
            (time(18, 10), ["2003-10-25"]),
            (
                time(18, 15),
                [
                    "2006-10-21",
                    "2008-10-28",
                    "2009-10-17",
                    "2010-11-05",
                    "2013-11-03",
                    "2019-10-27",
                    "2020-11-14",
                    "2021-11-04",
                    "2022-10-24",
                    "2023-11-12",
                ],
            ),
            (time(18, 30), ["2000-10-26", "2014-10-23", "2016-10-30", "2017-10-19"]),
            (time(19, 2), ["1999-11-07"]),
        ]

    @property
    def special_closes_adhoc(self) -> List[Any]:
        # Alongside Muhurat sessions, this includes 1996-1999 weekday
        # closes that deviate from the era schedule: ad-hoc trading-hour
        # extensions and early closes on weekly buy-in auction days. No
        # announcements survive from this period; times are the observed
        # continuous-session bounds. Eight further dates with early-ending
        # activity (1996-12-20, 1997-01-03, 1997-02-28, 1997-08-06,
        # 1997-09-29, 1998-03-23, 1998-03-26, 1998-06-24) are deliberately
        # not listed: truncated records and scheduled early closes are
        # indistinguishable, so the era close stands.
        return [
            (time(11, 30), ["2006-06-25"]),
            (time(11, 54), ["2003-02-01"]),
            (time(12, 30), ["2010-02-06"]),
            (time(12, 38), ["1998-11-21"]),
            (
                time(12, 45),
                [
                    "2012-01-07",
                    "2012-03-03",
                    "2012-04-28",
                    "2012-09-08",
                    "2013-05-11",
                    "2014-03-22",
                ],
            ),
            (time(13, 0), ["2003-03-22", "2003-11-15"]),
            (time(13, 15), ["1997-08-13"]),
            (time(13, 30), ["2005-06-04", "2005-11-26", "2006-04-29"]),
            (time(13, 32), ["1998-10-31"]),
            (time(14, 0), ["1997-04-12", "2004-04-17"]),
            (time(14, 40), ["2004-10-09"]),
            (time(14, 45), ["2025-10-21"]),
            (time(15, 29), ["1997-08-05"]),
            (
                time(15, 30),
                [
                    "1997-10-15",
                    "1997-10-22",
                    "1997-10-29",
                    "1997-11-06",
                    "1997-11-12",
                    "1997-11-20",
                    "1997-11-26",
                    "1997-12-03",
                    "1997-12-10",
                    "1997-12-17",
                    "1997-12-24",
                    "1997-12-31",
                    "1998-01-07",
                    "1998-01-14",
                    "1998-01-21",
                    "1998-01-29",
                    "1998-02-05",
                    "1998-02-11",
                    "1998-02-18",
                    "1998-02-25",
                    "1998-03-05",
                ],
            ),
            (time(15, 35), ["1997-07-04"]),
            (time(15, 36), ["1996-07-09", "1998-10-20"]),
            (time(15, 39), ["1997-07-08", "1997-07-29"]),
            (time(15, 40), ["1997-06-13"]),
            (time(15, 46), ["1998-09-17", "1999-04-17"]),
            (time(15, 47), ["1996-01-23"]),
            (time(15, 57), ["1996-09-30", "1996-10-03", "1997-02-03"]),
            (
                time(15, 58),
                [
                    "1996-05-21",
                    "1996-05-30",
                    "1996-10-01",
                    "1996-10-04",
                    "1996-10-07",
                    "1996-10-08",
                    "1998-09-25",
                    "1998-09-28",
                    "1998-09-29",
                    "1998-10-05",
                    "1998-10-06",
                    "1998-10-07",
                    "1998-10-08",
                ],
            ),
            (
                time(15, 59),
                [
                    "1996-01-09",
                    "1996-01-16",
                    "1996-01-30",
                    "1996-02-06",
                    "1996-02-14",
                    "1998-09-30",
                    "1998-10-09",
                ],
            ),
            (
                time(16, 0),
                [
                    "1997-03-12",
                    "1997-03-13",
                    "1997-03-14",
                    "1997-03-17",
                    "1997-03-18",
                ],
            ),
            (time(16, 13), ["1996-03-13"]),
            (
                time(16, 14),
                [
                    "1996-03-08",
                    "1996-03-11",
                    "1996-03-12",
                    "1996-03-14",
                    "1996-03-15",
                    "1996-03-18",
                ],
            ),
            (time(16, 16), ["1999-02-27", "1999-05-24"]),
            (time(16, 19), ["1999-04-16"]),
            (time(16, 23), ["1999-03-09"]),
            (time(16, 24), ["1999-03-10", "1999-03-11", "1999-03-12", "1999-03-18"]),
            (time(16, 25), ["1999-03-08", "1999-03-17", "1999-03-19"]),
            (time(16, 26), ["1999-02-24", "1999-03-16"]),
            (time(16, 27), ["1999-03-15", "1999-06-28"]),
            (
                time(16, 28),
                [
                    "1996-04-25",
                    "1996-05-01",
                    "1996-07-11",
                    "1996-07-31",
                    "1996-08-01",
                    "1998-03-16",
                    "1998-03-18",
                ],
            ),
            (
                time(16, 29),
                [
                    "1996-02-09",
                    "1998-03-09",
                    "1998-03-10",
                    "1998-03-12",
                    "1998-03-17",
                ],
            ),
            (time(16, 30), ["1999-05-21"]),
            (time(16, 35), ["1997-04-01"]),
            (time(16, 56), ["1998-07-13"]),
            (time(16, 57), ["1997-01-06"]),
            (time(16, 58), ["1996-08-08"]),
            (time(16, 59), ["1998-03-24"]),
            (time(17, 0), ["2012-11-13", "2021-02-24"]),
            (time(17, 14), ["1997-05-30"]),
            (time(17, 28), ["1996-05-20"]),
            (time(18, 0), ["2011-10-26"]),
            (time(18, 15), ["2001-11-14", "2002-11-04"]),
            (time(18, 30), ["1996-07-22", "1998-06-01", "2018-11-07"]),
            (time(18, 45), ["2004-11-12", "2015-11-11"]),
            (time(19, 0), ["2007-11-09", "2024-11-01"]),
            (
                time(19, 15),
                [
                    "2008-10-28",
                    "2009-10-17",
                    "2010-11-05",
                    "2019-10-27",
                    "2020-11-14",
                    "2021-11-04",
                    "2022-10-24",
                    "2023-11-12",
                ],
            ),
            (time(19, 20), ["2005-11-01"]),
            (time(19, 25), ["2003-10-25"]),
            (time(19, 29), ["1998-10-19"]),
            (
                time(19, 30),
                [
                    "2006-10-21",
                    "2013-11-03",
                    "2014-10-23",
                    "2016-10-30",
                    "2017-10-19",
                ],
            ),
            (time(19, 45), ["2000-10-26"]),
            (time(19, 58), ["1996-11-10"]),
            (time(20, 27), ["1999-11-07"]),
        ]

    @property
    def interruptions(self) -> List[Any]:
        return [
            ("2004-04-17", time(12, 4), time(12, 34)),
            ("2004-10-09", time(11, 25), time(12, 5)),
            ("2021-02-24", time(11, 40), time(15, 45)),
        ]
