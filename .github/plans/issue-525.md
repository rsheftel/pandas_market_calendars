# Issue #525: EUREX_Bond open time change on 2018-12-10 goes the wrong way

## Problem
`EUREXFixedIncomeCalendar.regular_market_times["market_open"]` had the two eras swapped:
it opened at 01:10 before 2018-12-10 and at 08:00 from then on. Eurex actually moved the
open of the fixed income futures (Bund, Bobl, Schatz, Buxl) *earlier*, into the Asian time
zone, on Monday 10 December 2018.

## Sources
- Eurex circular 063/18 (launch of extended trading hours on Monday, 10 December 2018; open
  moved forward to 01:00 CET):
  https://www.eurex.com/ex-en/find/circulars/No.-063-18-Extension-of-trading-hours-for-selected-benchmark-futures-and-MSCI-futures-219526
- Eurex trading-hour-extension archive (lists FGBX, FGBL, FGBM, FGBS):
  https://www.eurex.com/ex-en/support/initiatives/archive/trading-hour-extension
- Current product pages show continuous trading from 01:10 CET.

## Change
- `pandas_market_calendars/calendars/eurex_fixed_income.py`: swap the open times to
  `((None, time(8, 0)), ("2018-12-10", time(1, 10)))` and cite the circular in a comment.
- `tests/test_eurex_fixed_income_calendar.py`: add a schedule test for 2018-12-06..11 asserting
  08:00 opens before the change, 01:10 opens from 2018-12-10, and 22:00 closes throughout.

Small bug fix: no public API change, no new dependency.
