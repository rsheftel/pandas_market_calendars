# GitHub Copilot Instructions for pandas_market_calendars

This repository provides market and exchange trading calendars for pandas. These instructions help GitHub Copilot understand the project structure, conventions, and best practices.

## Project Overview

- **Purpose**: Market and exchange trading calendars for pandas with support for holidays, early closes, and market hours
- **Language**: Python (>=3.8)
- **Key Dependencies**: pandas (>=1.1), exchange-calendars (>=3.3)
- **Build Tool**: uv (Astral package manager)
- **Testing**: pytest
- **Formatting**: Black

## Quick Start Commands

### Environment Setup
```bash
# Update uv
uv self update

# Minimal install (runtime dependencies only)
uv sync --no-dev

# Full development environment (linters, coverage, xdist, notebooks, profiling)
uv sync --all-extras --group dev
```

### Testing
```bash
# Run all tests
uv run --no-sync pytest

# Run fast tests only (skip slow tests)
uv run --no-sync pytest -m "not slow"

# Run specific test file
uv run --no-sync pytest tests/test_file.py

# Run with coverage
uv run --no-sync pytest --cov=pandas_market_calendars --cov-report=term-missing

# Run tests in parallel
uv run --no-sync pytest -n auto -m "not slow"
```

### Code Formatting
```bash
# Format Python files with Black
uv run python -m black <file_or_directory>
```

## Project Structure

- `pandas_market_calendars/` - Main library package
  - `calendars/` - Calendar implementations for specific exchanges
  - `holidays/` - Holiday definitions for exchanges
  - `market_calendar.py` - Base `MarketCalendar` class
  - `calendar_registry.py` - Calendar registration system
  - `calendar_utils.py` - Common calendar utility functions
- `tests/` - Test suite
  - `data/` - Test data and fixtures
- `docs/` - Documentation sources
- `examples/` - Example code and usage

## Domain Concepts

- **Trading days**: Days when the market is open for trading
- **Market hours**: Opening and closing times for trading
- **Holidays**: Days when the market is closed
- **Early closes**: Days when the market closes earlier than usual
- **Timezone handling**: Always use `pytz` or `zoneinfo`, never naive datetimes

## Coding Standards

### Python Style
- Follow PEP 8 with max line length 120
- Use Black for code formatting (enforced)
- Always include type hints
- Use built-in generics (`list[str]`, `dict[str, int]`) and `| None` for optionals
- Prefer f-strings over string concatenation
- Use `pathlib.Path` for filesystem paths

### Import Style
**Internal project imports:**
- **Functions**: Use namespace imports (`from pandas_market_calendars import calendar_utils` → `calendar_utils.function()`)
- **Classes/Exceptions**: Use direct imports (`from pandas_market_calendars.market_calendar import MarketCalendar`)

**Standard imports:**
```python
import pandas as pd
import numpy as np
```

### Documentation
- Use Sphinx/reStructuredText docstrings
- Required fields: `:param <name>:`, `:return:`, `:raises <ExceptionType>:`
- DO NOT use `:type:` or `:rtype:` fields (rely on type hints)
- DO NOT use Google-style or NumPy-style docstrings

Example:
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

## Testing Guidelines

- Write tests using pytest
- Test file naming: `test_<module>_calendar.py` or `test_<feature>.py`
- Follow Arrange-Act-Assert (AAA) pattern
- Do not add docstrings to test functions
- All tests must pass without errors or warnings
- Place test data in `tests/data/` directory
- Use `pandas.testing.assert_frame_equal` and `assert_series_equal` for DataFrame/Series comparisons
- Cover edge cases: empty inputs, NaNs, duplicates
- Prefer inline test cases over parameterization for clarity
- Avoid fixtures unless used more than 4 times

## Pandas Best Practices

- Prefer vectorized operations over Python loops
- Use `.apply` sparingly; prefer `.map`, `.transform`, or vectorized operations
- No inplace mutations; return new DataFrames
- Use `.loc` for selection; avoid chained indexing
- Document column names, dtypes, and assumptions in docstrings

## Common Patterns

### Adding a New Calendar
1. Create holiday definitions in `holidays/<exchange>.py`
2. Create calendar class in `calendars/<exchange>.py` extending `MarketCalendar`
3. Register in `calendar_registry.py`
4. Add tests in `tests/test_<exchange>_calendar.py`

### Modifying Holiday Rules
- Historical holidays: add to existing rules with date ranges
- Future holidays: use observance rules where possible
- Test against known historical data in `tests/data/`

### Debugging
- Use `calendar.schedule(start, end)` to inspect generated schedules
- Check `calendar.holidays()` for holiday list verification
- For date issues, verify timezone handling first
- Run single test: `uv run --no-sync pytest tests/test_file.py::test_name -v`

## Security

- Do not use `eval()` or `exec()`
- Never commit secrets or credentials
- Validate all external data inputs
- Use `ast.literal_eval()` if parsing is needed

## Git Workflow

- Branch naming: `feature/<description>`, `fix/<issue>`, `docs/<topic>`
- Commit messages: imperative mood, 50 char subject, blank line, body
- All PRs should target the `dev` branch
- Squash commits for clean history when appropriate

## Additional Documentation

For more detailed guidelines, see:
- [AGENTS.md](../AGENTS.md) - Comprehensive developer guidelines
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [README.rst](../README.rst) - Project overview and usage
