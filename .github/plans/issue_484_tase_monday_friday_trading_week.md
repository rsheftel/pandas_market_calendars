# Issue 484 TASE Monday-Friday Trading Week Plan

## Current Step

5. Run the TASE tests, the full fast suite, and the formatter checks. Completed.

## Plan

1. Confirm the trading week change (Sunday-Thursday to Monday-Friday effective 2026-01-05, last Sunday session 2026-01-04) and the 2026 closure dates against the exchange schedule, and cross-check both against the upstream `exchange_calendars` XTAE calendar. Completed.
2. Change the weekmask to Monday-Friday and handle the crossover in `valid_days`, following the NYSE pre/post-1952 Saturday pattern so pre-2026 schedules are unchanged. Completed.
3. Add the 2026 and 2027 closures to `TASEClosedDay` (the list ended at 2025-10-14). Completed.
4. Add the Friday 13:34 early close through `special_closes` with the weekday form. Completed.
5. Add native TASE tests (`tests/test_tase_calendar.py`), run the full fast suite, and run ruff format and check. Completed.

## Assumptions

- The exchange's published schedule is authoritative: Monday-Friday trading from 2026-01-05, Friday sessions 9:59-13:34, and a Friday before a Sunday holiday or holiday eve is closed.
- The 2027 closures follow the same rules; election days or other one-off closures are added when announced.
- The regular Monday-Thursday close time (15:59) is left as is; it predates this change and is noted in the issue.

## Validation

- `tests/test_tase_calendar.py`: 6 passed.
- Full fast suite on the `dev` base: 1497 passed.
- 2026-2027 session sets identical to the upstream `exchange_calendars` XTAE calendar (492 sessions each, no differences).
- 2019-2025 schedule output hash-identical to the unmodified branch.
- Ruff format and check passed for the changed Python files.
