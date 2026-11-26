"""
Dated facts of the Taiwan Futures Exchange (TAIFEX) calendar.

TAIFEX index futures and options trade on the trading days of the Taiwan Stock Exchange (TWSE), so the TAIFEX
calendars reuse the XTAI holiday rules of exchange_calendars. This module holds what those rules do not cover:

* The after-hours session (15:00-05:00 Taipei time) started on the evening of 2017-05-15. Its trades belong to the
  NEXT trading day, so 2017-05-16 is the first trading day with one.
* Closures missing from XTAI. TAIFEX's and TWSE's daily data agree on every trading day since 1998-07-21; these are
  the weekdays since 2002 on which both were closed but XTAI is open, plus the announced 2027 closures XTAI lacks.
* Trading days since 2017-05-16 that had no after-hours session.

All dates were checked against TAIFEX's daily TX data (https://www.taifex.com.tw/cht/3/dlFutDailyMarketView),
which agrees with TWSE's daily trading summary. Typhoon closures also cite TAIFEX's notices
(https://www.taifex.com.tw/cht/11/newsDetail?newsType=1&idx=<N>, numbers below).
"""

from pandas import Timestamp


# First trading day with an after-hours session (the session opened at 15:00 on 2017-05-15). TAIFEX press release:
# https://www.taifex.com.tw/cht/11/newsDetail?newsType=1&idx=7834
AFTER_HOURS_FROM = "2017-05-16"

# Weekdays on which TAIFEX (and TWSE) did not trade but the XTAI calendar is open.
TAIFEX_ADHOC_CLOSURES = [
    Timestamp("2005-05-02"),  # Labour Day (Sunday 2005-05-01) observed
    Timestamp("2011-05-02"),  # Labour Day (Sunday 2011-05-01) observed
    Timestamp("2022-02-04"),  # Lunar New Year bridge holiday (make-up workday Saturday 2022-01-22)
    Timestamp("2023-01-18"),  # first no-trading day after the last trading day (2023-01-17) before Lunar New Year
    Timestamp("2024-10-31"),  # Typhoon Kong-rey, notice idx=15446
    Timestamp("2026-07-10"),  # Typhoon Bavi, notice idx=17137
    Timestamp("2026-10-23"),  # Typhoon Champi, notice idx=17441
    # 2027 closures announced on 2026-11-10 (TAIFEX letter 1150003597; 2027 trading calendar)
    Timestamp("2027-02-02"),  # no trading: the two days after the last trading day (2027-02-01) before Lunar New Year
    Timestamp("2027-02-03"),
    Timestamp("2027-04-06"),  # Children's Day (Sunday 2027-04-04) observed
    Timestamp("2027-12-24"),  # Constitution Day (Saturday 2027-12-25) observed
]

# Trading days since AFTER_HOURS_FROM without an after-hours session on the evening before. Until 2018 TAIFEX
# traded on Saturday make-up workdays: the Friday evening session counted toward the Saturday, and nothing ran
# on the Saturday evening, so the following Monday had no after-hours session. Saturday sessions themselves
# cannot be modelled with a Monday-Friday weekmask.
NO_AFTER_HOURS = [
    Timestamp("2017-06-05"),  # Monday after the Saturday session on 2017-06-03
    Timestamp("2017-10-02"),  # Monday after the Saturday session on 2017-09-30
    Timestamp("2018-04-02"),  # Monday after the Saturday session on 2018-03-31
    Timestamp("2018-07-11"),  # the 2018-07-10 evening session was closed for Typhoon Maria, notice idx=8805
    Timestamp("2018-12-24"),  # Monday after the Saturday session on 2018-12-22
]
