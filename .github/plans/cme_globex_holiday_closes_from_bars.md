# CME Globex Holiday Closes From Traded Bars Plan

## Current Step

5. Run the full suite and Ruff. Completed.

## Plan

1. Measure each holiday session from one-minute TRADES bars: the end of the last bar on each holiday and early-close day, per product. Completed.
2. Write failing tests for the closes that differ from the library, through the public calendars and aliases. Completed.
3. Good Friday: a short session only when the jobs report falls on it, matching CMEBondExchangeCalendar's lists. Completed.
4. Energy and Metals, FX, Crypto, Grains and Oilseeds: date-scoped rules for the closes the bars show. Completed.
5. Run the full suite and Ruff. Completed.

## Assumptions

- The end of the last traded one-minute bar on a liquid front month is the session's close. CL, GC, HG, NG, 6E, 6J, 6B, 6C, BTC, ETH, ZC, ZS and ZW all agree within each product family.
- FX and Crypto Thanksgiving Friday and Christmas Eve closes are verified up to 2022-2023 and for 2025. The 2024 boundary follows Energy and Metals, whose bars show the change in 2024.
- Good Friday 2025 has no bars here; it follows the jobs-report rule that 2021, 2023, 2024 and 2026 confirm.
- Energy and Metals years after 2026 continue the 2022-2026 pattern; no 2027 schedule was checked.
- FX's July 3 2026 close rests on 6L alone, the only FX contract with bars that day.
- Grains and Oilseeds early closes start in 2015; earlier years closed at 12:00 against a 13:15 regular close, which the calendar does not model.

## Validation

- Full suite: 1526 passed, 1 skipped, with warnings as errors.
- Ruff formatting and lint checks passed for the changed Python files.
