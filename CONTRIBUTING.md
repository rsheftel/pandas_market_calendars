# Contributing

This document outlines the ways to contribute to `pandas_market_calendars`. This is a fairly small, low-traffic project, so most of the contribution norms (coding style, acceptance criteria) have been
developed ad hoc and this document will not be exhaustive. If you are interested in contributing code or documentation, please take a moment to at least review the license section to understand how
your code will be licensed.

## Types of contribution

### Bug reports

Bug reports are an important type of contribution - it's important to get feedback about how the library is failing, and there's no better way to do that than to hear about real-life failure cases. A
good bug report will include:

1. A minimal, reproducible example - a small, self-contained script that can reproduce the behavior is the best way to get your bug fixed. For more information and tips on how to structure these,
   read [Stack Overflow's guide to creating a minimal, complete, verified example](https://stackoverflow.com/help/mcve).

2. The platform and versions of everything involved, at a minimum please include operating system, `python` version and `pandas_market_calendars` version. Instructions on getting your versions:
    - `pandas_market_calendars`: `python -c "import pandas_market_calendars; print(pandas_market_calendars.__version__)"`
    - `Python`: `python --version`

3. A description of the problem - what *is* happening and what *should* happen.

While pull requests fixing bugs are accepted, they are *not* required - the bug report in itself is a great contribution.

### Feature requests

If you would like to see a new feature in `pandas_market_calendars`, it is probably best to start an issue for discussion rather than taking the time to implement a feature which may or may not be
appropriate for `pandas_market_calendars`'s API. For minor features (ones where you don't have to put a lot of effort into the PR), a pull request is fine but still not necessary.

### Pull requests

Please format all code using black.

If you create an editable install with the dev extras you can get a pre-commit hook set-up.

```
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]
pre-commit install
```

If you would like to fix something in `pandas_market_calendars` - improvements to documentation, bug fixes, feature implementations, etc - pull requests are welcome!

All pull requests should be opened against the `dev` branch and should include a clear and concise summary of the changes you made.

The most important thing to include in your pull request are *tests* - please write one or more tests to cover the behavior you intend your patch to improve.
