# Issue 477 CME Equity Market Pause Plan

## Current Step

4. Run focused plus full validation. Completed.

## Plan

1. Reproduce the obsolete post-cutover pause and confirm the historical boundary. Completed.
2. Add focused schedule, open-state, and intraday-grid regression tests around the cutover. Completed.
3. Add a date-effective CME equity-hours transition that preserves the pre-2021 pause. Completed.
4. Run focused plus full validation. Completed.

## Assumptions

- CME's June 2021 Globex notice is authoritative for the June 28, 2021 trade-date cutover.
- Historical sessions before the cutover must retain the 15:15-15:30 CT pause.
- A zero-length break at the former 15:15 CT pause boundary preserves the established schedule schema without
  removing any tradable time.

## Validation

- The two new regression tests failed before the implementation and passed afterward.
- Focused CME equity and source tests: 25 passed.
- Fast suite: 1492 passed and 1 failed; the only failure was the existing timezone-sensitive
  `test_valid_days_tz_aware` NYSE baseline already documented on `dev`.
- Ruff lint and format checks passed for all changed Python files.
- `git diff --check` passed with CRLF treated as a valid line ending.
