"""
Night-session facts shared by the mainland China futures exchange calendars.

Closure dates themselves are the same for all mainland exchanges (State Council holiday
notice + CSRC arrangement), so the futures calendars reuse ``pandas_market_calendars.holidays.cn``.
What differs from the stock exchanges is the night session, which this module documents:

* A night session (starting 21:00 Beijing time) belongs to the NEXT trading day. Friday evening's
  session is Monday's trading day; there is no night session on the evening before a holiday
  closure, so the first trading day after a holiday is day-session only.
* Night trading was suspended from the first trading day after the 2020 Spring Festival until it
  resumed on the evening of 2020-05-06 (resumption notices published by SHFE, INE, DCE and CZCE at the
  end of April 2020).

Cross-checked against the exchange holiday notices collected at https://marketsopen.today
(open data, CC BY 4.0) for 2026.
"""

from pandas import Timestamp


# Trading days whose night session was suspended because of COVID-19: the first trading day after the
# extended 2020 Spring Festival closure up to and including 2020-05-06 (night trading resumed the
# evening of 2020-05-06, which belongs to the 2020-05-07 trading day).
NIGHT_SESSION_SUSPENDED_FROM = Timestamp("2020-02-03")
NIGHT_SESSION_SUSPENDED_TO = Timestamp("2020-05-06")

# First trading day with a night session, per product group (used as the cut-over date for the
# regular market times, so earlier history is modelled as day-session only).
SHFE_PRECIOUS_METALS_NIGHT_FROM = "2013-07-05"  # gold, silver
SHFE_BASE_METALS_NIGHT_FROM = "2013-12-20"  # copper, aluminium, zinc, lead (later: nickel, tin, stainless, alumina)
SHFE_INDUSTRIALS_NIGHT_FROM = "2014-12-26"  # rebar, hot-rolled coil, rubber, bitumen (fuel oil 2018, pulp 2018)
DCE_NIGHT_FROM = "2014-07-04"
CZCE_NIGHT_FROM = "2014-12-12"
INE_CRUDE_NIGHT_FROM = "2018-03-26"  # product launch
INE_INDUSTRIALS_NIGHT_FROM = "2019-08-12"  # TSR 20 rubber launch (low-sulphur fuel oil 2020-06-22)
INE_COPPER_NIGHT_FROM = "2020-11-19"  # product launch
