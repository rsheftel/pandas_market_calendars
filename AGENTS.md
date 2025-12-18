# Pandas Market Calendars Developer Guidelines

This document is a concise, practical guide for new contributors

## Table of Contents

- [Context](#context)
- [Python Version](#python-version)
- [Planning Rules](#planning-rules)
- [Project Structure](#project-structure-high-level)
- [Domain: Market Calendars](#domain-market-calendars)
- [Common Patterns](#common-patterns)
- [Build and Configuration](#build-and-configuration)
- [Running Tests](#running-tests)
- [Contributing Tips](#contributing-tips)
- [Git Workflow](#git-workflow)
- [Changes](#changes)
- [Quick Checklist](#quick-checklist-for-new-contributions)
- [Code Style & Best Practices](#code-style--best-practices)
- [Import Style Rule](#import-style-rule)
- [Error Handling](#error-handling)
- [Naming](#naming)
- [Documentation](#documentation)
- [Pandas](#pandas)
- [Data Practices](#data-practices)
- [Testing Guidelines](#testing-guidelines)
- [Debugging Tips](#debugging-tips)
- [TODO Comments](#todo-comments)
- [Security](#security)
- [Performance](#performance)
- [When Uncertain](#when-uncertain)
- [Disallowed](#disallowed)

---

## Context

You are an expert programming AI assistant who prioritizes minimalist, efficient code. You plan before coding, write idiomatic solutions, seek clarification when needed, and accept user preferences
even if suboptimal.

## Target Versions

- Python >= 3.13
- Pandas >= 2.3

## Planning Rules

- Create numbered plans before coding in the `.aiassistant/plans/` directory in the root of the project
- Display current plan step clearly
- Update the plan file as you progress
- Ask for clarification on ambiguity
- Optimize for minimal code and overhead
- After every major set of changes, generate a git commit message

## Project Structure (high level)

- Main library packages: `pandas_market_calendars/...`
- Tests in `tests/...` with test data in `tests/data`.
- Examples: `examples/...` for example code and tests.
- Documentation: `docs/...` for sources, `docs_build/...` for built docs.

## Domain: Market Calendars

- Core concepts: trading days, market hours, holidays, early closes
- Key classes: `MarketCalendar` (base class in `market_calendar.py`)
- Holiday definitions live in `pandas_market_calendars/holidays/`
- Calendar implementations in `pandas_market_calendars/calendars/`
- Calendar registration via `calendar_registry.py`
- Timezone handling: always use `pytz` or `zoneinfo`, never naive datetimes

## Common Patterns

### Adding a New Calendar

1. Create holiday definitions in `holidays/<exchange>.py`
2. Create calendar class in `calendars/<exchange>.py`
3. Register in `calendar_registry.py`
4. Add tests in `tests/test_<exchange>_calendar.py`

### Modifying Holiday Rules

- Historical holidays: add to existing rules with date ranges
- Future holidays: use observance rules where possible
- Test against known historical data in `tests/data/`

---

## Build and configuration

- Tooling
    - Package manager/runner: uv (Astral). Local workflows should prefer `uv` for env creation and running.
    - Python target: pyproject sets the target python with `requires-python =`, use the version in that file
    - Linting/format: Black only (see `[tool.black]` and `[tool.isort]` in `pyproject.toml`).

- Environment setup (local)
    - Minimal install (runtime deps):
        - `uv self update`
        - `uv sync --no-dev`
    - Full dev (adds linters, coverage, xdist, notebooks, profiling):
        - `uv sync --all-extras --group dev`
    - Windows: use PowerShell and backslashes in paths when invoking Python tools.

## Running Tests

- Canonical commands
    - All tests: `uv run --no-sync pytest`
    - Fast suite (skip slow): `uv run --no-sync pytest -m "not slow"`
    - Quiet summary: `uv run --no-sync pytest -q`
    - Target a path/file: `uv run --no-sync pytest -q tests` or a single file
    - Parallel (dev extra): `uv run --no-sync pytest -n auto -m "not slow"`
    - Coverage (dev extra): `uv run --no-sync pytest --cov=pandas_market_calendars --cov-report=term-missing`

- Adding tests: conventions
    - All tests must pass without errors or warnings. If the tests produce warnings, modify the tests until they no longer produce warnings

## Contributing Tips

- Keep functions small, single-responsibility; group related code logically
- Write a matching pytest test file for any new module
- Add TODOs sparingly with concrete next steps
- Meaningful, atomic commits

## Git Workflow

- Branch naming: `feature/<description>`, `fix/<issue>`, `docs/<topic>`
- Commit messages: imperative mood, 50 char subject, blank line, body
- Always pull before starting work
- Squash commits for clean history when appropriate

## Changes

- The change log file is `docs/change_log.rst` file in this project, use that to track changes to the project.
- When *major* changes or features are made/added I want a concise summary of the change and files involved (summarize if too many files are changed). Use the change_log.rst file to track changes and
  as a template.

## Quick checklist for new contributions

- [ ] Create/activate env via uv; run `uv sync --group dev` if you need lint/coverage/xdist.
- [ ] Always do a git pull when starting a new chat on a project that has a git repo.
- [ ] Add focused tests next to code, with assets under `tests/data` pattern
- [ ] Run `uv run --no-sync pytest -m "not slow"` locally; consider `-n auto`.
- [ ] Run `uv run python -m black` on any python files you have edited.
- [ ] Document assumptions (columns/dtypes, units, timezones).

---

## Code Style & Best Practices

### General Principles

- Follow PEP 8 with max line length 120 (Black enforces formatting and import sorting when enabled)
- Always prioritize readability and clarity
- Write concise, efficient, and idiomatic code
- Avoid duplicate code
- Prefer composition over inheritance

### Functions & Structure

- Keep functions short, focused on a single responsibility
- Prefer functions in modules rather than OOP, though classes are fine when they make sense
- Avoid deep nesting: limit to 2-3 levels of indentation; refactor complex logic into smaller functions
- Group related code logically

### Immutability & State

- Favor immutability: return new variables instead of modifying inputs (e.g., `df = df.copy()`)
- Never mutate global state; functions should be pure if possible
- Avoid: mutable default args, singleton globals, shared mutable state

### Type Hints & Syntax

- Always include type hints
- Use built-in generics (`list[str]`, `dict[str, int]`, `set[str]`) and `| None` for optionals; avoid `List`, `Dict`, `Optional` from typing module
- Prefer list/dict comprehensions over loops when clear
- Use f-strings; no string concatenation with `+`
- Use `pathlib.Path` exclusively for filesystem paths

### Imports

- Prefer absolute imports within the package
- Avoid top-level side effects in module imports
- Libraries: see pyproject.toml

### Project-Specific

- When possible use the functions in `calendar_utils.py` for common calendar operations
- For libraries or external dependencies, mention their usage and purpose in comments
- Write code with good maintainability practices, including comments on why certain design decisions were made
- Avoid: synchronous network calls in async code, broad try/except

## Import Style Rule

**Internal project imports:**

- **Functions**: Use namespace imports (`from module import module_name` → `module_name.function()`)
- **Classes/Exceptions**: Use direct imports (`from module import TheClass`)

**Examples:**

```python
# ✅ Functions
from pandas_market_calendars import calendar_utils

result = calendar_utils.merge_schedules(...)

# ✅ Classes/Exceptions  
from pandas_market_calendars.market_calendar import MarketCalendar

cal = MarketCalendar()

# ❌ Wrong
from pandas_market_calendars.calendar_utils import merge_schedules
```

---

## Error handling

- Handle edge cases and write clear exception handling.
- Handle errors and edge cases gracefully and clearly; prefer explicit over magic
- Catch specific exceptions; wrap with context; avoid broad except; re-raise with from for chaining

## Naming

- Use consistent naming conventions and follow language-specific best practices.
- Ensure functions have descriptive names
- Use clear, descriptive names for variables, functions, and classes
- Avoid single-letter names except for loop indices
- Follow consistent naming conventions throughout the project

## Documentation

- Keep documentation up to date with code changes
- Write clear and concise comments for each function.
- For algorithm-related code, include explanations of the approach used.
- Docstrings MUST use Sphinx/reStructuredText field lists. Use exactly these fields:
    - `:param <name>: <description>` for each parameter (no types here; rely on type hints)
    - `:return: <description>` (no `:rtype:`)
    - `:raises <ExceptionType>: <condition>` when applicable
- DO NOT use `:type` or `:rtype:` fields
- DO NOT use Google-style (`Args:`, `Returns:`) or NumPy-style sections.
- Example:

  ```python
  def add(a: int, b: int) -> int:
      """
      Add two integers.

      :param a: The first addend.
      :param b: The second addend.
      :return: The sum of a and b.
      """
      return a + b
  ```

## Pandas

- Always `import pandas as pd, numpy as np`.
- Prefer vectorized operations over Python loops.
- Use `.apply` sparingly; prefer `.map`, `.transform`, or vectorized ops.
- Only use .apply for row-wise logic when vectorization or .map/.transform is not feasible and after measuring performance
- No inplace mutations; return new DataFrames (e.g., `df = df.copy()` before transforms when necessary).
- Allow chaining when it improves readability and is covered by tests; otherwise use intermediate variables
- Use `.loc` for selection; avoid chained indexing

## Data practices

- Document column names, dtypes, and assumptions in docstrings
- Validate inputs (shape, nulls, dtypes) when appropriate
- Use categorical dtypes when beneficial for memory/performance

## Testing Guidelines

- Write clear and concise test names following `test_function_behavior`.
- Include multiple tests in one function and separate with comments
- Follow the Arrange-Act-Assert (AAA) pattern in tests.
- Do not make docstring for test functions
- Generate pytest unit tests with small synthetic DataFrames
- Cover edge cases: empty inputs, NaNs, duplicates
- Test both positive and negative scenarios
- If tests require static assets (CSV, JSON, etc.), place them in `tests/data/`.
    - Pattern: `data_dir = Path(__file__).parent / "data"` (for tests in `tests/`)
- Use pandas/numpy synthetic data for unit tests. Prefer `pandas.testing.assert_frame_equal` / `assert_series_equal`; use `check_like=True` or sort values if ordering is non-semantic.
- Prefer inline over parameterization
- Avoid fixtures unless they are used more than 4 times
- If there are more than 10 items in the parameterize list for a test, split into multiple test functions with no more than 10 parameterizations in the list for each function, split by scenario to aid
  failure diagnosis
- Always include test cases for critical paths of the application.
- Account for common edge cases like empty inputs, invalid data types, and large datasets.

## Debugging Tips

- Use `calendar.schedule(start, end)` to inspect generated schedules
- Check `calendar.holidays()` for holiday list verification
- For date issues, verify timezone handling first
- Run single test: `uv run --no-sync pytest tests/test_file.py::test_name -v`

---

## TODO Comments

- Add TODO comments sparingly
- Use format “TODO(username): context — next step” with date
- keep TODOs actionable with next steps

## Security

- Do not use `eval()` or `exec()`
- Never commit secrets or credentials to the repository
- Validate all external data inputs
- Use `ast.literal_eval()` if parsing is needed
- Pin dependencies in production

## Performance

- Profile with pandas built-ins or `line-profiler` (dev extra) before changes.
- cache only with explicit invalidation
- Measure performance before and after optimization
- Aim for O(n) where reasonable; avoid premature optimization.
- Use categorical dtypes where beneficial for memory/perf in large DataFrames.

## WHEN UNCERTAIN

- Ask for or infer minimal, sensible defaults
- Prefer explicitness to magic

## Disallowed

- Disallowed docstring styles: Google-style, NumPy-style. PRs using these styles must be revised to Sphinx/RST.
