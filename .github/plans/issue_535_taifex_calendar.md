# Issue 535: Taiwan Futures Exchange (TAIFEX) calendar

## Current Step

6. Run the new tests with `-W error`, the fast suite, and ruff format and check on the changed files. Completed.

## Plan

1. Read AGENTS.md, CONTRIBUTING.md, `docs/new_market.rst` and the China futures calendars (PR #505); record the
   fast-suite baseline. Completed.
2. Add `tests/data/taifex_tx_session_exceptions.csv` (derived from TAIFEX's daily TX data) and
   `tests/test_taifex_calendar.py`. Watch the tests fail. Completed.
3. Add `pandas_market_calendars/holidays/taifex.py` with the dated facts: the after-hours start date, the closures
   that the XTAI rules miss, and the trading days that had no after-hours session. Completed.
4. Add `pandas_market_calendars/calendars/taifex.py` with `TAIFEXDayCalendar` (`TAIFEX_Day`) and
   `TAIFEXExchangeCalendar` (`TAIFEX`, `XTAF`, `TAIFEX_TX`), and import both in `calendar_registry.py`. Completed.
5. Add `sources.py` entries for `TAIFEX` and `TAIFEX_Day`, rows in `docs/calendars.rst` and a line in
   `docs/change_log.rst`. Completed.
6. Run the new tests with `-W error`, the fast suite, and ruff format and check on the changed files. Completed.

## Design

- Scope: the TAIEX futures and options group (TX, MTX, TMF, TXO and the sector index futures). They share the
  08:45-13:45 regular session and the 15:00-05:00 after-hours session. FX, gold, stock and TOPIX products have other
  hours and are left for later.
- `TAIFEX` follows `SHFE_BaseMetals`: `market_open` is the after-hours open at 15:00 on the previous trading day, then
  `night_close` 05:00 (a close in `open_close_map`), `day_open` 08:45 (an open) and `market_close` 13:45, Asia/Taipei.
  TAIFEX books after-hours trades to the next trading day.
- Unlike the China futures night sessions, the after-hours session also runs on the evening before a closure.
  So a trading day always opens at 15:00 on the previous trading day, however many days lie between them. Special
  opens are computed from `valid_days`: a day `k >= 2` calendar days after the previous trading day gets
  `market_open` at 15:00 with offset `-k` and `night_close` at 05:00 with offset `-k + 1`. Future holidays and new
  typhoon closures need no extra code.
- Days without an after-hours session open at 08:45 (`market_open`, `night_close` and `day_open` equal): every day
  before 2017-05-16, plus five listed days (2018-07-11 after Typhoon Maria, and the Mondays after the Saturday make-up
  sessions in 2017-2018). `night_close` gets its own special time on those days, so they are right with
  `force_special_times=False` too.
- `TAIFEX_Day` has only `market_open` 08:45 and `market_close` 13:45.
- History: 09:00-12:15 before 2001-01-02; after-hours from 2017-05-16 (session opened 15:00 on 2017-05-15).
- Holidays: the XTAI rules and ad hoc list (through the pmc mirror of exchange_calendars), plus the closures XTAI
  misses since 2002: 2005-05-02, 2011-05-02, 2022-02-04, 2023-01-18, the typhoon days 2024-10-31, 2026-07-10 and
  2026-10-23, and the announced 2027 closures 02-02, 02-03, 04-06 and 12-24. The XTAI mirror itself is not changed;
  the issue asks the maintainer where these closures should live.
- The name is `TAIFEX`, not `XTAF`: `sources.get_sources` treats names starting with "X" as mirrored calendars.

## Assumptions and limitations

- Saturday sessions cannot be modelled (weekmask Monday-Friday, see issue #480): Saturdays before 2001 and the
  make-up Saturdays from 2006-10-14 to 2018-12-22. Their trading days are missing from the calendar.
- The calendar is checked against TAIFEX data from 2002-01-01. Before 2002, XTAI is open on 24 weekdays on which
  TAIFEX and TWSE were closed, and closed on 2000-02-09, when both traded.
- The expiring contract's earlier close (13:30 on its last trading day) is contract-level and not modelled.

## Validation

- TAIFEX daily TX data, 2002-01-01 to 2026-11-26: 6,130 trading days; the calendar has 6,107, all of them in the
  data. The 23 missing days are all Saturday sessions.
- After-hours sessions, 2017-05-16 to 2026-11-26: the calendar agrees with the data on all 2,322 weekday trading days
  (2,317 with a session, 5 without), and every session opens at 15:00 on the previous trading day.
- 2026 and 2027 closures equal TAIFEX's published calendars.
- `uv run --no-sync pytest tests/test_taifex_calendar.py -W error`: 20 passed (collection error before the change).
- `uv run --no-sync pytest -m "not slow"`: 1636 passed, 1 skipped, 1 failed. The failure
  (`test_nyse_calendar.py::test_valid_days_tz_aware`) and the 12 warnings are the same on `dev`; the failure depends
  on the local time zone and passes with `TZ=UTC`.
- `uv run ruff format` and `uv run ruff check` on the changed Python files: clean.
