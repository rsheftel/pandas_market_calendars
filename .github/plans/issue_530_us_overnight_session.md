# Issue #530: Nasdaq and NYSE Arca 23/5 overnight session

## Problem
Nasdaq and NYSE Arca plan to start an overnight session on Sunday 2026-12-06: 21:00 to 04:00 ET,
Sunday to Thursday nights, with trades counting toward the next trading date. No calendar in the
library can express this for US equities today.

## Constraint from the maintainer (issue #530)
The change must be additive: do not alter existing tests, only add new ones, and do not change
anyone's existing workflow. So `"NASDAQ"` stays an alias of `NYSEExchangeCalendar`, and the new
calendars are registered under new names only.

## Sources
- SR-NASDAQ-2025-109 (Nasdaq 23/5 rule filing):
  https://listingcenter.nasdaq.com/assets/rulebook/nasdaq/filings/SR-NASDAQ-2025-109.pdf
- SR-NYSEArca-2026-53 (NYSE Arca overnight session rule filing):
  https://www.nyse.com/publicdocs/nyse/markets/nyse-arca/rule-filings/filings/2026/SR-NYSEArca-2026-53.pdf

## Steps
1. [x] Read AGENTS.md, CONTRIBUTING.md, the issue reply; record a green baseline of the fast suite.
2. [x] Add `tests/test_us_overnight_calendars.py` (schedule times on the first night, weeknights, no
   Friday night, holidays, both DST changeovers, `open_at_time`, default schedule equal to NYSE,
   moving the start date, registry and sources). Watch it fail.
3. [x] Add `pandas_market_calendars/calendars/us_overnight.py`: `OVERNIGHT_FROM`, a helper that adds
   an `overnight` market time to NYSE's times, and `NASDAQExchangeCalendar` /
   `NYSEArcaExchangeCalendar` subclasses of `NYSEExchangeCalendar`, registered as `"NASDAQ_23_5"` and
   `"NYSE_Arca"` / `"ARCA"` / `"ARCX"`. `"XNAS"` is avoided because `sources.get_sources` treats names
   starting with "X" as calendars mirrored from `exchange_calendars`.
4. [x] Import both classes in `calendar_registry.py`.
5. [x] Add `sources.py` entries keyed by each class's `name`.
6. [x] Add rows to `docs/calendars.rst` and a line to `docs/change_log.rst`.
7. [ ] Run ruff on the changed files and the full test suite; no new warnings.

## Design
- `overnight` is one new market time, counted as an open in `open_close_map`. Its value is
  `((None, time(4)), ("2026-12-07", time(21), -1))`: before trading date 2026-12-07 it equals `pre`
  (zero-length session, so history is unchanged); from then on it is 21:00 on the previous calendar day.
- `market_open` stays at 09:30, so the default `schedule()` columns match NYSE exactly.
- Holidays need no special code: a trading date D always opens at 21:00 on D-1, so Monday opens on
  Sunday evening, the day after a holiday opens on the holiday's evening, and a holiday has no row.
- Half-day overnight hours are not confirmed yet; exceptions can be added later through
  `special_overnight` / `special_overnight_adhoc`.

No change to `NYSEExchangeCalendar`, no change to existing tests, no new dependency.
