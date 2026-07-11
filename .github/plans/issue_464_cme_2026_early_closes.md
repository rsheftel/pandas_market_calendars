# Issue 464 CME 2026 Early-Close Plan

## Current Step

4. Run the focused calendar tests, formatter, and diff checks. Completed.

## Plan

1. Reproduce the five reported close times on the current `dev` branch and identify the holiday rules that emit them. Completed.
2. Add 2026-only holiday rules so the correction doesn't change other calendar years. Completed.
3. Add focused regression coverage through the public `CMEGlobex_GC` and `CMEGlobex_MCL` aliases. Completed.
4. Run the focused calendar tests, formatter, and diff checks. Completed.

## Assumptions

- The five dates and close times reported in issue #464 are the authoritative 2026 values.
- This change applies only to the Energy and Metals calendar family.

## Validation

- Energy and Metals test file: 12 passed.
- CME Globex calendar test files: 1070 passed.
- Ruff formatting and lint checks passed for the changed Python files.
- The full fast suite reached 1254 passing tests before stopping at the existing timezone-sensitive `test_valid_days_tz_aware` assertion in `tests/test_nyse_calendar.py`.
