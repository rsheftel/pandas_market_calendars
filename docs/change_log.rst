Change Log
==========

Updates
-------
0.1
~~~
- Initial version

0.2
~~~
- Fix to allow start_date and end_date to be the same in schedule()

0.3
~~~
- Added Eurex calendar

0.4
~~~
- Fixed bug #5

0.5 (3/27/17)
~~~~~~~~~~~~~
- Added Python2.7 support

0.6 (3/31/17)
~~~~~~~~~~~~~
- Added coveralls.io test coverage

0.7 (5/30/17)
~~~~~~~~~~~~~
- Fix a couple deprecated imports

0.8 (8/24/17)
~~~~~~~~~~~~~
- Fix #10 to make merge_schedules work properly for more than 2 markets

0.9 (9/12/17)
~~~~~~~~~~~~~
- Fix #12 to Eurex calendar

0.10 (9/12/17)
~~~~~~~~~~~~~~
- Added open_time_default and close_time_default as abstract property methods to fix #17

0.11 (10/30/17)
~~~~~~~~~~~~~~~
- Corrected the NYSE calendar for Independence Day on Thursday post 2013 to fix #20
- Added new convert_freq() function to convert a date_range to a lower frequency to fix #19

0.12 (12/10/17)
~~~~~~~~~~~~~~~
- Added new JPX calendar thanks to gabalese from PR #21

0.13 (1/5/18)
~~~~~~~~~~~~~
- Corrected JPX calendar for issue #22

0.14 (1/7/18)
~~~~~~~~~~~~~
- Made default open and close times time-zone aware

0.15 (2/23/18)
~~~~~~~~~~~~~~
- Removed toolz as a required package and removed from the one test that required it
- Added daily closes on NYSE back to 1928 from PR #30 thanks to @pldrouin

0.16 (5/12/18)
~~~~~~~~~~~~~~
- Fixed the equinox for Japanese calendar, Pull Request #33
- Fixed Victoria Day for TSX, issue #34

0.17 (5/24/18)
~~~~~~~~~~~~~~
- Added SIX (Swiss Exchange) calendar, Pull Request #36

0.18 (6/8/18)
~~~~~~~~~~~~~~
- Changed NYSE holiday calendar to start 1/1/1900 (was previously 1/1/1970).
- Fixed an error that schedule() method would fail if the end date was prior to 1993

0.19 (7/2/18)
~~~~~~~~~~~~~~
- schedule() method no longer raises exception if there are no valid trading days between start_date and end_date,
  will now return an empty DataFrame

0.20 (7/2/18)
~~~~~~~~~~~~~~
- Improvements in the internals for how calendars are registered and aliased thanks for PR #45
