Change Log
==========

Updates
-------
1.4 (7/11/20)
~~~~~~~~~~~~
- Add the concept of a break during the trading day. For example this can accommodate Asian markets that have a lunch
  break, or futures markets that are open 24 hours with a break in the day for trade processing.
- Added product specific contract calendars for CME futures exchange
-- First calendars are the CME Agricultural and CME Equity calendars
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
