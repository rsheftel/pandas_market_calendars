# Package-Wide Type Hint Plan

Date: 2026-05-25

## Status Update (2026-05-26)

- Current phase: Holiday-module typing cleanup in progress after calendar sweep completion.
- Type-check baseline has improved to `32` diagnostics via annotation-only changes.
- Calendar annotation coverage:
   - Missing return annotations in `pandas_market_calendars/calendars/*.py`: `0`
   - Missing non-`self`/`cls` parameter annotations in `pandas_market_calendars/calendars/*.py`: `0`
- Recent validation:
   - Focused file check: `uv run ty check pandas_market_calendars/calendars/iex.py` passed.
   - Targeted behavior test: `uv run --no-sync pytest -q tests/test_iex_calendar.py` passed (`4 passed`).
   - Holiday-focused checks: missing helper annotations in `pandas_market_calendars/holidays/*.py` reduced to `0` returns and `0` parameters.
   - Holiday-focused type-check remains at existing stub-related baseline (`14` diagnostics, no net new errors).
   - Targeted holiday-related tests passed: `uv run --no-sync pytest -q tests/test_jpx_calendar.py tests/test_nyse_calendar.py tests/test_sifma_calendars.py` (`60 passed`).
   - Full fast suite passed: `uv run --no-sync pytest -q -m "not slow"` (`1489 passed`).
   - Ruff check passed for touched holiday files.
   - Package-wide type baseline reconfirmed and improved: `uv run ty check pandas_market_calendars` (`Found 32 diagnostics`).
   - Core regression checks passed: `uv run --no-sync pytest -q tests/test_utils.py tests/test_date_range.py tests/test_market_calendar.py tests/test_class_registry.py` (`78 passed`).

## Goal

Add or improve type hints across `pandas_market_calendars` so the package is clearer and passes Pylance cleanly, without changing runtime behavior or refactoring unrelated logic.

## Constraints

1. Preserve runtime behavior and public APIs.
2. Prefer plain inline annotations first.
3. Introduce `TypeVar` only when a return type depends on an input type or multiple inputs must share the same type.
4. Introduce `@overload` only when call shapes or `None` handling materially change the return type.
5. Prefer built-in generics and modern union syntax compatible with Python 3.10+.
6. Keep imports minimal and use `TYPE_CHECKING` only when required to avoid import cycles.
7. Keep edits local and validate after each file group.

## File Groups

1. Core package modules
   - `pandas_market_calendars/__init__.py`
   - `pandas_market_calendars/market_calendar.py`
   - `pandas_market_calendars/calendar_utils.py`
   - `pandas_market_calendars/calendar_registry.py`
   - `pandas_market_calendars/class_registry.py`
   - `pandas_market_calendars/sources.py`
2. Shared calendar infrastructure
   - `pandas_market_calendars/calendars/cme_market_times.py`
   - `pandas_market_calendars/calendars/cme_globex_base.py`
   - `pandas_market_calendars/calendars/__init__.py`
3. Calendar families
   - CME and Globex calendars first
   - Single-exchange calendars with lighter inheritance next
   - Historically complex calendars such as NYSE/XNYS and SIFMA last
4. Holiday modules
   - `pandas_market_calendars/holidays/*.py`

## Baseline Findings

Baseline completed on 2026-05-25.

### Baseline Command

- Canonical typing baseline: `uv run ty check pandas_market_calendars`
- VS Code `get_errors` did not surface the typing backlog for this package, so `ty` should be treated as the source of truth for this work.

### Current Diagnostic Summary

- `39` type diagnostics across `13` files.
- Error categories:
  - `unresolved-import`: 12
  - `unknown-argument`: 12
  - `unsupported-operator`: 5
  - `invalid-assignment`: 4
  - `no-matching-overload`: 3
  - `invalid-return-type`: 2
  - `invalid-method-override`: 1
- Highest-concentration files:
  - `pandas_market_calendars/calendar_utils.py`: 10
  - `pandas_market_calendars/holidays/nyse.py`: 9
  - `pandas_market_calendars/market_calendar.py`: 5
  - `pandas_market_calendars/class_registry.py`: 2
  - `pandas_market_calendars/calendars/bmf.py`: 2
  - `pandas_market_calendars/calendars/six.py`: 2
  - `pandas_market_calendars/calendars/tsx.py`: 2

### Annotation Backlog Summary

- Missing return annotations: `289`
- Missing non-`self`/`cls` parameter annotations: `173`
- Largest backlog by file:
  - `pandas_market_calendars/market_calendar.py`: 60 missing returns, 93 missing parameters
  - `pandas_market_calendars/class_registry.py`: 10 missing returns, 16 missing parameters
  - `pandas_market_calendars/calendar_utils.py`: 21 missing parameters plus the largest concentration of live checker failures
  - `pandas_market_calendars/calendars/cme.py`: 21 missing returns
  - `pandas_market_calendars/calendars/nyse.py`: 20 missing returns
  - `pandas_market_calendars/calendars/sifma.py`: 17 missing returns

### Baseline Issue Inventory

1. `calendar_utils.py`
   - Date-like unions are too wide for direct comparison against `Timestamp` values.
   - Several pandas-stubs overloads do not match current call shapes for `pd.cut` and `pd.date_range`.
   - Some helper return annotations are narrower than the values inferred from pandas objects.

2. `market_calendar.py` and `class_registry.py`
   - Metaclass-driven assignment patterns are not typed precisely enough for `ty`.
   - `ProtectedDict` class attributes need explicit shape treatment.
   - `HolidayCalendar.holidays` currently conflicts with the pandas stub overloads.
   - `CustomBusinessDay(weekmask=...)` calls are valid at runtime but missing from current stubs.

3. NYSE and mirror-style calendar logic
   - `weekmask` keyword usage triggers stub mismatches in both calendar and holiday modules.
   - Historically complex calendar logic will require careful narrowing without altering behavior.

4. Import and stub mismatches in holiday and exchange modules
   - `pandas.tseries.holiday` members such as `Easter`, `Day`, `MO`, and `DateOffset` are available at runtime but unresolved in current stubs.
   - These are concentrated in `calendars/bmf.py`, `calendars/six.py`, `calendars/tsx.py`, `holidays/cme.py`, `holidays/cme_globex.py`, `holidays/nyse.py`, `holidays/oz.py`, `holidays/sifma.py`, and `holidays/uk.py`.

5. Broad annotation backlog in public APIs
   - Most remaining work is still straightforward annotation coverage, especially calendar property overrides and helper methods across exchange modules.

### Import-Cycle Risk Notes

- `calendar_registry.py` imports calendar modules for metaclass registration side effects; avoid adding new runtime imports there for typing.
- `market_calendar.py` already depends on `calendar_utils`, `class_registry`, and `sources`; any new typing-only references to concrete calendar modules should stay behind `TYPE_CHECKING`.
- `class_registry.py` mutates class attributes dynamically in the metaclass, so typing helpers should be added without introducing imports back into calendar modules.

## Execution Plan

1. Establish a typing baseline.
   - Status: Completed.
   - Completed on 2026-05-25.
   - Package-level `ty` diagnostics have been collected and grouped by file and error category.
   - Import-cycle risks are limited to side-effect-heavy registry modules and can be managed with `TYPE_CHECKING` imports.
   - Exit criterion satisfied.

2. Type the core public surface first.
   - Status: In progress.
   - Start with `calendar_utils.py`, since it has the most live checker failures and defines several shared date-range and session helpers.
   - Make date-like inputs explicit, narrow pandas return types, and reshape signatures to match pandas-stubs overloads where possible.
   - Annotation pass has been applied; remaining diagnostics are concentrated in pandas-stubs mismatch hotspots.
   - Exit criterion: `calendar_utils.py` is clean under `ty` and its typed helpers are stable enough for `market_calendar.py` to consume.

3. Type the shared calendar abstractions.
   - Status: In progress.
   - Move next to `market_calendar.py` and `class_registry.py`.
   - Annotate reusable market-time structures, class-level metadata, registry mappings, and metaclass-managed attributes.
   - Use `ClassVar` and narrow mapping aliases where that removes `invalid-assignment` errors without changing behavior.
   - Parameter annotation coverage is complete in `market_calendar.py` and `class_registry.py`; remaining diagnostics are stub-signature mismatches (`weekmask`) and dynamic typing limitations.
   - Resolve the `HolidayCalendar.holidays` override shape and document any unavoidable pandas-stub limitations.
   - Exit criterion: `market_calendar.py` and `class_registry.py` are clean enough that subclass files can inherit stable annotations.

4. Type calendar implementations by family.
   - Status: Completed.
   - Tackle NYSE and mirror-style modules before the broader calendar sweep because they already contribute live diagnostics through `weekmask` and holiday interactions.
   - After that, type CME and Globex modules to validate the shared abstractions across a large family of subclasses.
   - Move to the lighter single-exchange calendars next.
   - Finish with the remaining historically complex calendars after the common patterns are established.
   - In each file, annotate public methods and class attributes first, then add local variable annotations only where inference remains unstable.
   - Current coverage check reports no remaining missing function return or parameter annotations in `pandas_market_calendars/calendars/*.py`.
   - Exit criterion: each calendar family passes focused type validation before moving to the next family.

5. Type holiday modules after the calendar surfaces settle.
   - Status: In progress.
   - Prioritize the holiday files with live import and `weekmask` diagnostics: `holidays/nyse.py`, `holidays/cme.py`, `holidays/cme_globex.py`, `holidays/oz.py`, `holidays/sifma.py`, and `holidays/uk.py`.
   - Annotate holiday factories, exported constants, observance callables, and date computation helpers.
   - Helper function annotation sweep is complete; remaining blockers are known pandas-stub import and `weekmask` signature mismatches.
   - Make optional paths explicit instead of relying on checker inference.
   - Avoid broadening values to `object`; prefer small local aliases and explicit narrowing.
   - Exit criterion: holiday helpers type-check cleanly and align with the calendars that consume them.

6. Revisit overload and generic hotspots only where needed.
   - Status: Pending.
   - Add `TypeVar` only when a type relationship must be preserved.
   - Add `@overload` only where argument shapes or `None` versus non-`None` semantics materially change the return type.
   - Prefer a single readable signature when it is precise enough for Pylance.
   - Exit criterion: no public API is left ambiguous when a precise readable annotation is possible.

7. Validate incrementally and finish with a full sweep.
   - Status: In progress.
   - After each file group, run focused type validation for the touched modules.
   - Run targeted pytest files for touched behavior when annotations require explicit narrowing or expose latent API ambiguity.
   - Incremental checks are being run after each batch; package-wide diagnostics are stable at baseline.
   - Finish with package-wide type analysis, a fast pytest run, and formatting/lint checks for any changed imports.
   - Exit criterion: package-wide typing changes pass the chosen validation commands without runtime regressions.

## Validation Sequence

1. Focused type analysis for the files changed in the current batch.
2. Targeted tests for the touched calendar or utility surface.
3. Package-wide type analysis once a major file group is complete.
4. Package-wide baseline command: `uv run ty check pandas_market_calendars`.
5. `uv run --no-sync pytest -m "not slow"` before finalizing the overall effort.
6. Ruff or formatter checks if import blocks or annotation formatting change.

## Risk Areas

1. Pandas and third-party stubs may be incomplete, especially around timestamp-like operations and schedule DataFrame behavior.
2. Registry code and calendar class factories may need careful typing with `type[...]` and narrow mapping aliases.
3. Calendar class attributes may look mutable or dynamic to the checker and may need explicit `ClassVar` treatment.
4. Date-like inputs may repeat across files; a shared alias should be introduced only if repetition is high enough to reduce noise.
5. Overloads can become harder to maintain than a well-chosen union; use them sparingly.

## Proposed Delivery Shape

1. `calendar_utils.py`
2. `market_calendar.py` and `class_registry.py`
3. NYSE and mirror-related calendar and holiday modules
4. CME and Globex calendars
5. Remaining calendar modules and holidays
6. Final annotation sweep and validation

Each delivery slice should be small enough to review independently and should leave the touched files in a clean type-checking state before the next slice begins.
