 Change Log
==========

Updates
-------
4.1.3 (12/26/2022)
~~~~~~~~~~~~~~
- Added Chinese 2023 holidays

4.1.2 (12/08/2022)
~~~~~~~~~~~~~~
- Added 2023 holidays to BSE calendar

4.1.1 (10/31/2022)
~~~~~~~~~~~~~~
- Fix for bug in NYSEExchangeCalendar.valid_days

4.1.0 (10/08/2022)
~~~~~~~~~~~~~~
- Added UK and Australia holidays for Queen Elizabeth II's State Funeral

4.0.3 (10/08/2022)
~~~~~~~~~~~~~~
- Enabled tests that failed before PR #215

4.0.2 (10/08/2022)
~~~~~~~~~~~~~~
- Implemented new release management  

4.0.1 (09/03/22)
~~~~~~~~~~~~~~
- Fix duplicates bug in special_dates
- Fix tz=None bug in NYSEExchangeCalendar.valid_days

4.0 (08/02/22)
~~~~~~~~~~~~~~
- Added interruptions support
- Updated MarketCalendar.open_at_time to respect interruptions
- Special times can be set with offsets
- MarketCalendar.days_at_time returns a pandas.Series
- calendar_utils.date_range supports schedules of any timezone

3.5 (06/25/22)
~~~~~~~~~~~~~~
- Updated BMF
- New CME calendar setup
- New CME calendars for equities, fixed income, ags, energies, metals, and FX

3.4 (03/05/22)
~~~~~~~~~~~~~~
- Update to work with pandas 1.4.0
- Fix boxing day for Australia
- Add SIFMA US, UK and JP calendars
- Add IEX calendar
- Add NSE calendar

3.3 (01/30/22)
~~~~~~~~~~~~~~
- `PR #166 <https://github.com/rsheftel/pandas_market_calendars/pull/166>`_ to solve the issue raised in
  `#164 <https://github.com/rsheftel/pandas_market_calendars/issues/164>`_
- Add Juneteenth to NYSE calendar
- Fixed CN holidays
- Make MarketCalendars pickleable

3.2 (10/10/21)
~~~~~~~~~~~~~~
- Major refactoring of the underlying code from `PR #150 <https://github.com/rsheftel/pandas_market_calendars/pull/150>`_
  thanks to https://github.com/Stryder-Git
- Fixed 12/24/1999 early close on NYSE

3.1 (08/29/21)
~~~~~~~~~~~~~~
- Added September 11 holidays to TSX calendar
- Made the minimum version for exchange_calendars >= 3.3 to resolve problem with newer versions of pandas

3.0 (8/17/21)
~~~~~~~~~~~~~
- Major update to the date_range() functionality. This new behavior is more complete and consistent, but changes
  behavior in some cases, so a new major version is warranted. For more discussion on the topic refer to
  `PR #142 <https://github.com/rsheftel/pandas_market_calendars/pull/142>`_ and
  `Issue #138 <https://github.com/rsheftel/pandas_market_calendars/issues/138>`_

2.1 (8/16/21)
~~~~~~~~~~~~~
- Updated to work with pandas 1.3
- Raise minimum python to 3.7
- NYSE calendar valid from 1885 to present. Includes all full day closes, early closes, and late opens. PR #141

2.0.1 (5/20/21)
~~~~~~~~~~~~~~~
- Fixed the TSE calendar for Christmas falling on a Saturday

2.0 (5/8/21)
~~~~~~~~~~~~
This version replaces the trading_calendars integration with exchange_calendars, closing out #120. `exchange_calendars <https://github.com/gerrymanoim/exchange_calendars>`_
if the fork of trading_calendars that is currently actively maintained. trading_calendars is now abandoned because
it's corporate sponsor is out of business and gone.

1.7 (5/6/21)
~~~~~~~~~~~~
This version eliminated the generic CMEExchangeCalendar. This calendar did not represent a specific market and thus
was not appropriate for any use. With the addition of the specific calendars for product types this is no longer
needed and is removed. To see the product specific calendars here: https://pandas-market-calendars.readthedocs.io/en/latest/calendars.html#futures-calendars

For the CMEEquityExchangeCalendar, this no longer is a mirror of the NYSE calendar as some of the holidays for the NYSE
are an open day with early close for CME. This calendar now has its own set of holiday assumptions. This may cause
some holidays missing until this calendar is fully tested and vetted.

1.6.2 (5/6/21)
~~~~~~~~~~~~~~
- Fix UK Holidays for #130
- Fix CME Bond calendar for Good Friday #132

1.6.1 (11/3/20)
~~~~~~~~~~~~~~~
- Add trading breaks to the trading_calendars import mirror
- Fix the CFE calendar for Good Friday #116
- Renamed XBOM to BSE to avoid conflict with trading_calendars

1.6 (9/14/20)
~~~~~~~~~~~~~
This is the first version of the merge of this project with the quantopian trading-calendars.

- Added the trading_calendars.py module that brings in all current and future calendars from the quantopian project
- All calendars from trading-calendars are now available in pandas_market_calendars

1.5 (8/30/20)
~~~~~~~~~~~~~
- Add the is_open_now() function
- Add TASE calendar from #114
- Holiday calendar is now cached to improve performance #117

1.4.2 (8/11/20)
~~~~~~~~~~~~~~~
- Fixed for changes to pandas 1.1.0

1.4.1 (7/22/20)
~~~~~~~~~~~~~~~
- Added CME_Bond calendar for bond and interest rate futures
- Added futures specific items to the documentations along with examples with breaks

1.4 (7/11/20)
~~~~~~~~~~~~~
- Add the concept of a break during the trading day. For example this can accommodate Asian markets that have a lunch
  break, or futures markets that are open 24 hours with a break in the day for trade processing.
- Added product specific contract calendars for CME futures exchange. First calendars are the CME Agricultural and
  CME Equity calendars
- Add ability to set time zone on schedule() function #42
- Add the Bombay exchange (XBOM) from #96
- Fixed Christmas holidays in SIX #100

1.3 (4/23/20)
~~~~~~~~~~~~~
- Fixes to support Pandas v1.0
- Remove support for Python 3.4 based on underlying packages removing support for v3.4
- Added ASXExchangeCalendar from PR #85
- Fixes to UK holidays in #84

1.2 (10/22/19)
~~~~~~~~~~~~~~
- Support calendars with valid business days on the weekend (PR #75)
- Fixed SSE 2019 labour's day holidays (PR #74)
- Better JPX calendar support for the time period 1949-2099 (PR #72)
- Reformat Japan's Ascension days, removed duplicate days (PR #68)
- Added German national holidays (PR #77)

1.1 (5/3/19)
~~~~~~~~~~~~
- add JPX Ascension Day holidays for 2019 from PR #64

1.0 (3/26/19)
~~~~~~~~~~~~~
- Official move to Python3 only support
- Version moved to 1.0 as the package has been around and stable long enough to warrant a 1.0

0.22 (3/25/19)
~~~~~~~~~~~~~~
- Added Shanghai Stock Exchange (SSE) calendar from PR #58
- Added HKEX calendar from PR #61
- Fixed tests for pandas v0.24 and higher

0.21 (12/2/18)
~~~~~~~~~~~~~~
- Added Oslo Stock Exchange (OSE) calendar
- Added GW Bush Holiday to NYSE calendar from PR #53 and #54

0.20 (7/2/18)
~~~~~~~~~~~~~~
- Improvements in the internals for how calendars are registered and aliased thanks for PR #45

0.19 (7/2/18)
~~~~~~~~~~~~~~
- schedule() method no longer raises exception if there are no valid trading days between start_date and end_date,
  will now return an empty DataFrame

0.18 (6/8/18)
~~~~~~~~~~~~~~
- Changed NYSE holiday calendar to start 1/1/1900 (was previously 1/1/1970).
- Fixed an error that schedule() method would fail if the end date was prior to 1993

0.17 (5/24/18)
~~~~~~~~~~~~~~
- Added SIX (Swiss Exchange) calendar, Pull Request #36

0.16 (5/12/18)
~~~~~~~~~~~~~~
- Fixed the equinox for Japanese calendar, Pull Request #33
- Fixed Victoria Day for TSX, issue #34

0.15 (2/23/18)
~~~~~~~~~~~~~~
- Removed toolz as a required package and removed from the one test that required it
- Added daily closes on NYSE back to 1928 from PR #30 thanks to @pldrouin

0.14 (1/7/18)
~~~~~~~~~~~~~
- Made default open and close times time-zone aware

0.13 (1/5/18)
~~~~~~~~~~~~~
- Corrected JPX calendar for issue #22

0.12 (12/10/17)
~~~~~~~~~~~~~~~
- Added new JPX calendar thanks to gabalese from PR #21

0.11 (10/30/17)
~~~~~~~~~~~~~~~
- Corrected the NYSE calendar for Independence Day on Thursday post 2013 to fix #20
- Added new convert_freq() function to convert a date_range to a lower frequency to fix #19

0.10 (9/12/17)
~~~~~~~~~~~~~~
- Added open_time_default and close_time_default as abstract property methods to fix #17

0.9 (9/12/17)
~~~~~~~~~~~~~
- Fix #12 to Eurex calendar

0.8 (8/24/17)
~~~~~~~~~~~~~
- Fix #10 to make merge_schedules work properly for more than 2 markets

0.7 (5/30/17)
~~~~~~~~~~~~~
- Fix a couple deprecated imports

0.6 (3/31/17)
~~~~~~~~~~~~~
- Added coveralls.io test coverage

0.5 (3/27/17)
~~~~~~~~~~~~~
- Added Python2.7 support

0.4
~~~
- Fixed bug #5

0.3
~~~
- Added Eurex calendar

0.2
~~~
- Fix to allow start_date and end_date to be the same in schedule()

0.1
~~~
- Initial version
