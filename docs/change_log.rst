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
