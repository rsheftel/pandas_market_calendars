# Issues #506 and #507: CME Agriculture Holiday Fixes

## Current Step

5. Add a concise entry to `docs/change_log.rst`, then run both focused test files, the fast test suite, and Ruff checks for any changed Python files. Completed.

## Plan

1. Treat the six Juneteenth dates listed in #506, including 2026-06-19, as authoritative. The current Globex rules have a 2026 gap; cover that date explicitly for Grains without broadening the behavior to other products. Confirmed by user.
2. Update only `CMEGlobexGrainsAndOilseedsExchangeCalendar` so its regular holidays include the verified Juneteenth dates. Prefer an existing holiday rule that covers the confirmed date range; avoid changing shared CME or US holiday rules unless the evidence requires it. Completed.
3. Update only `CMEAgricultureExchangeCalendar.adhoc_holidays` to exclude both 2018-12-05 and 2025-01-09 from full-day closures. Preserve the existing 2025-01-09 early close and leave shared mourning-day rules and other CME calendars unchanged. Completed.
4. Add or extend focused tests in `tests/test_exchange_calendar_cme_globex_grains.py` and `tests/test_cme_agriculture_calendar.py`. Assert all reported Juneteenth dates are absent from grains sessions, both mourning dates are valid agriculture sessions, and the 2025 agriculture session still closes at 12:15 CT. Check adjacent sessions remain unchanged. Completed.
5. Add a concise entry to `docs/change_log.rst`, then run both focused test files, the fast test suite, and Ruff checks for any changed Python files. Completed.

## Validation

- Focused CME Grains and CME Agriculture tests: 11 passed.
- Fast suite: 1588 passed, 1 skipped. It reported 12 existing pandas 3.1 timezone `.values` deprecation warnings in `tests/test_market_calendar.py`.
- Ruff check and format check passed for all changed Python files.

## Assumptions and Suggestions

- Treat all six dates listed in #506 as the requested CME Globex Grains closures, including 2026-06-19, as confirmed by the user.
- Keep both fixes scoped to the named calendars; do not broaden mourning-day or Juneteenth behavior to other CME products.
- The issues are related CME calendar corrections, so one implementation branch and pull request should be sufficient; separate tests and changelog wording will keep each fix traceable.
- No clarification is blocking the plan.

## Git Workflow

- Start from the latest `dev` branch and create a feature/fix branch from it; never switch to, merge into, or make changes on `master`.
- Current planning branch: `fix/issues-506-507-cme-holidays` (based on fetched `origin/dev`).
