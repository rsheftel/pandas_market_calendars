# Pytest Warning Remediation Plan

Date: 2026-10-31 (revision 7)

**Current step: Follow-up — remove legacy pandas workaround and resolve Ruff findings.**

## 0. Investigation (complete)

- [x] Pull the repository and verify a clean starting worktree.
- [x] Run the full suite, including slow tests, with repeated warnings enabled.
- [x] Preserve the complete pytest output and inspect warning sources.
- [x] Propose fixes, compatibility constraints, and acceptance criteria.
- [x] Review decisions, rounds 1–5 (see "Review decisions").
- [x] Verify:
  - [x] pandas 2.3 APIs;
  - [x] Python 3.15 readiness;
  - [x] that 5.6.0 has not been released.
- [x] Locate every `exchange-calendars` warning trigger.
- [x] Answer open questions (see "Open questions").

Command:

```bash
uv run --no-sync pytest -q -W always -r w
```

Result: **1,577 passed, 1 skipped, 19,555 warning occurrences in 71.96 seconds**.

- All reported warnings are `pandas.errors.Pandas4Warning`.
- `-W always` counts every repeated occurrence.

Environment:

- Python 3.12.3
- pandas 3.1.0
- NumPy 2.5.4
- pytest 9.2.0
- exchange-calendars 4.13.2

Logs are session artifacts and are not committed:

- Full run: `/root/.copilot/session-state/93071cd6f7364ea485ca633bbfb538a7/files/pytest-warnings.log`
- Timezone traceback: `/root/.copilot/session-state/93071cd6f7364ea485ca633bbfb538a7/files/pytest-timezone-warning-trace.log`

### Warning inventory

| Source | Occurrences | Warning / treatment |
|---|---:|---|
| `pandas_market_calendars/calendars/china_futures.py:142` | 42 | `DatetimeIndex.weekday` → `day_of_week` |
| `pandas_market_calendars/calendars/nyse.py:1369` | 441 | `Series.dt.weekday` → `dt.day_of_week` |
| `pandas_market_calendars/calendars/nyse.py:1480` | 141 | `Series.dt.weekday` → `dt.day_of_week` |
| `tests/test_nse_calendar.py:26` | 453 | `Timestamp.dayofweek` → vectorized `day_of_week` |
| `tests/test_nyse_calendar_early_years.py:2009` | 18,436 | `Timestamp.dayofweek` → vectorized `day_of_week` |
| `tests/conftest.py:67` (index wrapper) | 20 | `assert_index_equal` will check `freq` by default |
| pandas `core/series.py:848` | 14 | Timezone-aware `Series.values` drops the timezone (2 local, 12 from `exchange-calendars`) |
| pandas `core/indexes/datetimelike.py:1029` | 2 | Timezone-aware `DatetimeIndex.values` drops the timezone (local) |
| `pandas_market_calendars/market_calendar.py:566` | 6 | DataFrame built from ragged interruption rows |
| **Total** | **19,555** | |

Local timezone warnings: the 4 local occurrences come from `assert_same` in
`tests/test_market_calendar.py:1502-1504`.

Third-party timezone warnings:

- The 12 third-party occurrences are raised inside `exchange_calendars/exchange_calendar.py:403-406` while it builds its
  schedule.
- This repository cannot change that code.
- **Decision: leave these 12 warnings as they are.** Do not suppress them in tests or the library.
- All 12 are triggered by `tests/test_market_calendar.py`:

| Trigger | Occurrences | Phase |
|---|---:|---|
| Line 1440: `ecal_iepa = ecal.get_calendar("IEPA")` | 4 | Module level, during collection |
| `test_ec_property`: `mcaliepa.ec` | 4 | Test run |
| `test_ec_schedule`: `mcaliepa.ec` | 4 | Test run |

Intentional warnings, which are not counted above and must be preserved:

- Warnings asserted with `pytest.warns(...)`:
  - overlapping, insufficient, disappearing, and missing sessions;
  - merge dropping breaks;
  - XKRX discontinued times.
- NYSE weekday warnings hidden by `@pytest.mark.filterwarnings` in `tests/test_schedule_input_dates.py:9,23`. Step 3
  removes these marks.

### Verified facts

- **pandas 2.3.3**
  - `day_of_week` exists on `Timestamp`, `DatetimeIndex`, and `Series.dt`.
  - `pandas.testing.assert_index_equal` has **no** `check_freq` parameter.
  - `pandas.errors.Pandas4Warning` does not exist, so code and warning filters must not reference it by name.
- **Lockfile and local environment**
  - `uv.lock` resolves pandas 2.3.3 on Python 3.10, because pandas 3.x requires Python >= 3.11.
  - It resolves pandas 3.1.0 on Python >= 3.11.
  - Python 3.10.21 with pandas 2.3.3 runs locally through uv.
- **Python 3.15**
  - `actions/setup-python` provides 3.15.0–3.15.2.
  - pandas 3.1.0 and NumPy 2.5.4 publish cp315 wheels.
  - exchange-calendars is pure Python.
- **Test matrices**
  - `.github/workflows/test_runner.yml:19` lists Python 3.10–3.14.
  - `.github/workflows/release.yml:17` also lists Python 3.10–3.14.
  - In `release.yml`, build and publish run only on Python 3.14 with `ubuntu-latest`.
- **Release status**
  - 5.6.0 is untagged and not on PyPI; PyPI's latest release is 5.5.0.
  - `pyproject.toml` already says `version = "5.6.0"`.
  - Adding entries to the existing 5.6.0 changelog section is therefore correct.

## Review decisions

1. **Minimum pandas:** Change `pyproject.toml` from `pandas>=1.1` to `pandas>=2.3`. All fixes must work on pandas 2.3 and
   3.x.
2. **Frequency checks:** Implement the frequency policy in the `tests/conftest.py` index wrapper.
3. **`exchange-calendars` warnings:**
   - Do not file or draft an upstream issue.
   - Leave the 12 warnings visible in the test suite; do not add suppressions.
   - Leave the warning visible to library users who access `.ec`; do not suppress it in library code.
4. **Warnings policy:** Do not make warnings errors in `pyproject.toml` or CI.
5. **cloudpickle:** No change; the one skipped test stays skipped.
6. **Workflow:** Use branch `fix/pandas-deprecation-warnings`, created from `origin/dev`, and submit one PR against `dev`.
7. **Version:** Do not bump `pyproject.toml` `version`.
8. **Python 3.15:**
   - Add the Python 3.15 classifier.
   - Add Python 3.15 to **every** test matrix: `test_runner.yml` and `release.yml`.
9. **Testing:** Test on both pandas 2.3 and 3.1. Require **zero warnings on pandas 3.1**, except the 12 from
   `exchange-calendars`. Warnings on pandas 2.3 do not block the PR.
10. **Changelog:** Add the new items under the existing 5.6.0 section, including the pandas >= 2.3 minimum.
11. **Accepted suggestions:**
    - Remove pre-2.3 pandas workarounds in a separate follow-up PR.
    - Fix `AGENTS.md`.
    - Add `-r w` to CI pytest.
    - Set the Ruff target to `py310`.
    - Do **not** add a free-threaded `3.15t` CI job.
12. **PR number in the changelog:** Open the PR as a draft first, then write the changelog lines with the real PR number.
    This avoids placeholder text and an extra fix-up commit.
13. **Merge strategy:** Squash merge into `dev`.
    - Commits on the branch stay small, which keeps review easy.
    - `dev` receives one commit.
    - The PR title is the squash commit subject.
14. **Review and merge:** You review the PR and perform the squash merge. I will not merge it.
15. **Plan file:** This plan is committed on the branch and reaches `dev` through the squash merge, like the other plans
    in `.github/plans/`.

## 1. Create the work branch

- [x] Run `git fetch origin`. Local `dev` was 3 commits behind `origin/dev` at the last check.
- [x] Create the branch from `origin/dev`: `git switch -c fix/pandas-deprecation-warnings origin/dev`.
  - Removed the automatic `origin/dev` upstream so a plain `git push` cannot target `dev`.
- [x] Re-run the Step 0 capture on the new branch. Refresh counts if new `dev` commits changed them.
  - Result: 1,579 passed, 1 skipped, 19,555 warnings. The warning count is unchanged.
- [x] Commit this plan as the first commit: `Add pytest warning remediation plan`.

## 2. Update package metadata, tooling, and CI

- [x] In `pyproject.toml`, change `"pandas>=1.1"` to `"pandas>=2.3"`.
- [x] In `pyproject.toml`, add `'Programming Language :: Python :: 3.15',` after the 3.14 classifier.
- [x] In `pyproject.toml`, change `[tool.ruff] target-version` from `"py38"` to `"py310"`.
  - Change configuration only.
  - Leave any new `UP` lint findings for the follow-up PR.
  - Confirm `ruff check` on files touched by this PR does not newly fail (checked in Step 8).
  - Finding: `py310` adds 256 repo-wide findings (UP006/UP007/UP035/UP045/UP036, I001 because `zoneinfo`
    becomes stdlib, B905, RUF100). CI does not run Ruff. These belong to the follow-up PR. Changed files are
    therefore checked with `--target-version py38` to prove the edits themselves add no findings.
- [x] Regenerate the lockfile with `uv lock`, then confirm:
  - [x] Python 3.10 still resolves pandas 2.3.3.
  - [x] Python >= 3.11 resolves pandas 3.x.
  - `uv.lock` is gitignored (`.gitignore:111`), so it is regenerated locally but not committed.
- [x] Update `.github/workflows/test_runner.yml`:
  - [x] Add `'3.15'` to the `python-version` matrix.
  - [x] Change the test command to `coverage run --source=pandas_market_calendars -m pytest tests -r w`.
- [x] Add `"3.15"` to the `python-version` matrix in `.github/workflows/release.yml`.
  - Leave every `matrix.python-version == '3.14'` build/publish condition unchanged.
  - Python 3.15 is tested, but artifacts are still built on Python 3.14.
- [x] Keep pre-2.3 compatibility code in this PR; its removal belongs to the follow-up PR.
- [x] Commit: `Require pandas 2.3 and add Python 3.15 support`.

## 3. Replace deprecated weekday accessors

- [x] In `china_futures.py:142`, change `hol.weekday` to `hol.day_of_week`.
- [x] In `nyse.py:1369` and `nyse.py:1480`, change `.dt.weekday` to `.dt.day_of_week`.
- [x] In `test_nse_calendar.py:26`, replace the per-date loop with
  `assert (pd.DatetimeIndex(NSEClosedDay).day_of_week < 5).all()`.
- [x] In `test_nyse_calendar_early_years.py:2009`, replace the loop with
  `assert not (valid_days.day_of_week == 5).any()`.
- [x] Remove both `filterwarnings` marks and their comment from `tests/test_schedule_input_dates.py`.
  - Also removed the now-unused `pytest` import.
- [x] Leave Python `datetime.weekday()` calls unchanged; they are not deprecated.
- [x] Run the targeted China futures, NYSE, NSE, and schedule-input tests.
  - 260 passed with weekday/dayofweek warnings as errors; only the 11 Step 5 `freq` warnings remained.
- [x] Commit: `Use day_of_week instead of deprecated weekday`.

This step removes 19,513 of the 19,555 warning occurrences, about 99.8%.

## 4. Make timezone-aware comparisons explicit

- [x] Rewrite `assert_same` in `tests/test_market_calendar.py` to compare UTC instants without `.values`.
  - Convert both inputs to UTC and the same datetime unit.
  - Compare the converted values with `.to_numpy()`.
  - Handle `Series` and `DatetimeIndex` inputs separately.
- [x] Keep the existing length check and comparison strictness.
- [x] Leave unrelated `.values` uses on timedelta and integer data unchanged; they do not warn.
- [x] Run `test_closes_opens`.
  - Implemented as `pd.DatetimeIndex(x).tz_convert("UTC")` equality, which accepts both input types.
  - Verified that equal instants in different timezones, units, and containers pass.
  - Verified that a shifted instant and `NaT` still fail.
  - Only the 4 expected collection-time `exchange-calendars` warnings remain.
- [x] Commit: `Compare timezone-aware datetimes explicitly in tests`.

## 5. Implement the frequency policy in the index wrapper

- [x] Default `check_freq` to `False` in `_patched_assert_index_equal`, matching the Series and DataFrame wrappers.
- [x] At import, detect support for `check_freq` with `inspect.signature`, not a version string.
  - Pass `check_freq` through only when pandas supports it.
- [x] On pandas 2.3, handle explicit `check_freq=True` inside the wrapper.
  - Assert `left.freq == right.freq`.
  - Never drop the flag silently.
- [x] Add focused tests in new `tests/test_conftest_wrappers.py` that verify:
  - [x] equal values with different `freq` pass by default;
  - [x] different `freq` fails when `check_freq=True`;
  - [x] different values still fail;
  - [x] datetime resolution normalization still works.
- [x] Update the module docstring.
- [x] Verified with `-W error` on pandas 3.1.0 and on Python 3.10 with pandas 2.3.3: 5 passed on each.
  The 20 `freq` warnings are gone from the affected suites.
- [x] Commit: `Default index freq checks off in test wrapper`.

## 6. Pad ragged interruption rows explicitly

- [x] In `MarketCalendar.interruptions_df`:
  - [x] Read `self.interruptions` once.
  - [x] Pad each row with `None` to the longest row length before building the DataFrame.
- [x] Preserve:
  - [x] column naming;
  - [x] `NaT` for missing slots;
  - [x] day offsets;
  - [x] UTC conversion;
  - [x] sort order.
- [x] Continue accepting variable-length rows, as documented; callers do not need to pad.
- [x] Reuse `test_interruptions_df` and `test_schedule_w_interruptions`.
- [x] Add missing coverage for equal-length rows and single-row input.
  - Added `test_interruptions_df_rows_of_equal_and_single_length`.
- [x] Verified `interruptions_df` output is identical, including dtypes, before and after for NSE, XNSE,
  `FakeCalendar`, and `FakeBreakCalendar`.
- [x] Commit: `Pad interruption rows before building DataFrame`.

## 7. Update contributor guidance in `AGENTS.md`

- [x] At line 45, change `Python >= 3.8` to `Python >= 3.10`, matching `requires-python`.
- [x] Keep `Pandas >= 2.3`.
- [x] At line 95, replace "Black only (see `[tool.black]` and `[tool.isort]`)" with
  "Ruff (see `[tool.ruff]` in `pyproject.toml`)".
- [x] At line 156, replace the Black command with:
  - `uv run ruff format <files>`;
  - `uv run ruff check <files>`.
- [x] At line 165, replace "Black enforces formatting and import sorting" with
  "Ruff enforces formatting and import sorting".
- [x] Commit: `Align AGENTS.md with Python 3.10 and Ruff`.

## 8. Validate

- [x] Format each changed file with `uv run ruff format <changed files>`.
  `tests/test_nse_calendar.py` was already unformatted on `dev`. It was left as is to avoid unrelated churn.
- [x] Check each changed file with `uv run ruff check <changed files>`.
  All checks pass with `--target-version py38`, so these edits add no new findings.
- [x] Verify the warning requirement on pandas 3.1:

  ```bash
  uv run --no-sync pytest -q -W always -r w
  ```

  Required result:
  - All tests pass.
  - The warnings summary contains **exactly 12** occurrences.
  - All 12 come from `exchange_calendars` through `pandas/core/series.py`, with the `Series.values ... drops timezone`
    message.
  - No warning comes from `pandas_market_calendars/` or `tests/`.
  - Result: 1,585 passed, 1 skipped, exactly 12 `exchange-calendars` warnings.
- [x] Run the same full suite on Python 3.10 with pandas 2.3.3:

  ```bash
  uv run --python 3.10 --isolated --with-editable . --with pytest pytest -q -r w
  ```

  - All tests must pass.
  - Warnings are reported, but they do not block the PR.
  - Result: 1,585 passed, 1 skipped, 54 warnings. All 54 are a pandas 2.3 `FutureWarning` about empty-entry concatenation from
    `market_calendar.py:657`, raised during the CME Globex tests. `origin/dev` produces the same 54 warnings.
- [x] Confirm that existing expected-data tests pass without changing their expected data.
- [x] After pushing, confirm all CI jobs pass (all 18 `run_tests` jobs passed):
  - [x] Python 3.10, which tests pandas 2.3: pandas 2.3.3, 54 pre-existing warnings;
  - [x] Python 3.14, which tests pandas 3.1: pandas 3.1.0, 12 warnings;
  - [x] new Python 3.15 jobs: pandas 3.1.0, 12 warnings.

## 9. Draft PR, changelog, and handoff

- [x] Push the branch.
- [x] Open a **draft** PR against `dev` with `gh pr create --draft --base dev`. Opened as #515.
  - Title: `Remove pandas 3.1 deprecation warnings`. This becomes the squash commit subject.
  - The repository has no PR template.
- [x] In the PR description, include:
  - [x] Warning counts: 19,555 before and 12 after on pandas 3.1.
  - [x] The 12 remaining warnings come from `exchange-calendars` and are intentionally left alone.
  - [x] The minimum pandas version is now 2.3.
  - [x] Python 3.15 support.
  - [x] Python 3.15 in both test matrices.
  - [x] The Ruff target is now `py310`.
  - [x] `AGENTS.md` was updated.
  - [x] A note that the PR should be **squash merged**.
- [x] Append these lines to the **existing 5.6.0 section** of `docs/change_log.rst`, using the real PR number and the
  section's style:
  - [x] `- Raised the minimum pandas version to 2.3 (PR #515)`
  - [x] `- Added Python 3.15 support (PR #515)`
  - [x] `- Removed pandas 3.1 deprecation warnings from the library and tests (PR #515)`
- [x] Commit `Update change log for pandas warning cleanup` and push.
- [x] Mark every completed checklist item in this plan, then commit and push the final plan.
- [x] Confirm all CI jobs pass, then mark the PR ready for review with `gh pr ready`.
- [x] Hand off to you for review and squash merge into `dev`. My work ends here.
- [ ] Address review feedback with new commits on the same branch.
- [x] Update this checklist as each step completes, not only at the end.

## Follow-up (separate PR, after this merges)

- [x] Confirm PR #515 merged into `dev` and create `fix/pandas-deprecation-warnings-follow-up` from updated `origin/dev`.
- [x] Capture the Ruff baseline with `uv run --no-sync ruff check --target-version py310 --statistics .`: 256 findings (218 auto-fixable).
- [ ] Remove the pandas <2.3 workaround in `MarketCalendar._convert`; verify missing interruption values remain `NaT`.
- [ ] Resolve all Ruff findings now exposed by the `py310` target, including `UP`, import sorting, `B905`, `RUF100`, and `UP036`.
- [ ] Add or update focused tests for any behavior changes required by Ruff fixes.
- [ ] Run Ruff checks and formatting on changed Python files.
- [ ] Run the complete test suite on pandas 3.1 and Python 3.10/pandas 2.3.3; allow only the previously documented warning sets.
- [ ] Confirm Python 3.14 and 3.15 CI coverage remains intact.
- [ ] Add a follow-up entry to the existing 5.6.0 change-log section using the new PR number.
- [ ] Commit and push the branch; open a draft PR against `dev` and include the Ruff/pandas validation details.
- [ ] Confirm CI passes, mark the PR ready, and hand off for review and squash merge.

## Acceptance criteria

- With pandas 3.1, the full suite passes with **only** the 12 `exchange-calendars` warnings.
- Ruff reports no findings using the repository's configured Python 3.10 target.
- No warnings come from `pandas_market_calendars/` or `tests/`.
- With pandas 2.3 on Python 3.10, the full suite passes; warnings are allowed.
- CI passes on Python 3.10–3.15 across all operating systems in both workflow matrices.
- Calendar outputs are unchanged.
- Intentional `pytest.warns` assertions still pass.
- The PR does not add warning filters or suppressions, pandas upper bounds, a version bump, or new skips.
- The work is submitted as one PR against `dev` from `fix/pandas-deprecation-warnings` and squash merged.

## Open questions

None.

## Suggestions

None. The plan is ready to implement.
