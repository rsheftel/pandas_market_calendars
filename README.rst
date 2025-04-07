pandas_market_calendars
=======================
Market calendars to use with pandas for trading applications.

.. image:: https://badge.fury.io/py/pandas-market-calendars.svg
    :target: https://badge.fury.io/py/pandas-market-calendars

.. image:: https://readthedocs.org/projects/pandas-market-calendars/badge/?version=latest
   :target: http://pandas-market-calendars.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/rsheftel/pandas_market_calendars/badge.svg?branch=master
    :target: https://coveralls.io/github/rsheftel/pandas_market_calendars?branch=master

Documentation
-------------
http://pandas-market-calendars.readthedocs.io/en/latest/

Overview
--------
The Pandas package is widely used in finance and specifically for time series analysis. It includes excellent
functionality for generating sequences of dates and capabilities for custom holiday calendars, but as an explicit
design choice it does not include the actual holiday calendars for specific exchanges or OTC markets.

The pandas_market_calendars package looks to fill that role with the holiday, late open and early close calendars
for specific exchanges and OTC conventions. pandas_market_calendars also adds several functions to manipulate the
market calendars and includes a date_range function to create a pandas DatetimeIndex including only the datetimes
when the markets are open. Additionally the package contains product specific calendars for future exchanges which
have different market open, closes, breaks and holidays based on product type.

This package provides access to over 50+ unique exchange calendars for global equity and futures markets.

This package is a fork of the Zipline package from Quantopian and extracts just the relevant parts. All credit for
their excellent work to Quantopian.

Major Releases
~~~~~~~~~~~~~~
As of v1.0 this package only works with Python3. This is consistent with Pandas dropping support for Python2.

As of v1.4 this package now has the concept of a break during the trading day. For example this can accommodate Asian
markets that have a lunch break, or futures markets that are open 24 hours with a break in the day for trade processing.

As of v2.0 this package provides a mirror of all the calendars from the `exchange_calendars <https://github.com/gerrymanoim/exchange_calendars>`_
package, which itself is the now maintained fork of the original trading_calendars package. This adds over 50 calendars.

As of v3.0, the function date_range() is more complete and consistent, for more discussion on the topic refer to PR #142 and Issue #138.

As of v4.0, this package provides the framework to add interruptions to calendars. These can also be added to a schedule and viewed using
the new interruptions_df property. A full list of changes can be found in PR #210.

As of v5.0, this package uses the new zoneinfo standard to timezones and depricates and removes pytz. Minimum python version is now 3.9

Source location
~~~~~~~~~~~~~~~
Hosted on GitHub: https://github.com/rsheftel/pandas_market_calendars

Installation
~~~~~~~~~~~~
``pip install pandas_market_calendars``

Arch Linux package available here: https://aur.archlinux.org/packages/python-pandas_market_calendars/

Calendars
---------
The list of `available calendars <https://pandas-market-calendars.readthedocs.io/en/latest/calendars.html>`_

Quick Start
-----------
.. code:: python

    import pandas_market_calendars as mcal
    
    # Create a calendar
    nyse = mcal.get_calendar('NYSE')

    # Show available calendars
    print(mcal.get_calendar_names())

.. code:: python

    early = nyse.schedule(start_date='2012-07-01', end_date='2012-07-10')
    early

    
.. parsed-literal::

                      market_open             market_close
    =========== ========================= =========================
     2012-07-02 2012-07-02 13:30:00+00:00 2012-07-02 20:00:00+00:00
     2012-07-03 2012-07-03 13:30:00+00:00 2012-07-03 17:00:00+00:00
     2012-07-05 2012-07-05 13:30:00+00:00 2012-07-05 20:00:00+00:00
     2012-07-06 2012-07-06 13:30:00+00:00 2012-07-06 20:00:00+00:00
     2012-07-09 2012-07-09 13:30:00+00:00 2012-07-09 20:00:00+00:00
     2012-07-10 2012-07-10 13:30:00+00:00 2012-07-10 20:00:00+00:00

    
.. code:: python

    mcal.date_range(early, frequency='1D')




.. parsed-literal::

    DatetimeIndex(['2012-07-02 20:00:00+00:00', '2012-07-03 17:00:00+00:00',
                   '2012-07-05 20:00:00+00:00', '2012-07-06 20:00:00+00:00',
                   '2012-07-09 20:00:00+00:00', '2012-07-10 20:00:00+00:00'],
                  dtype='datetime64[ns, UTC]', freq=None)



.. code:: python

    mcal.date_range(early, frequency='1H')




.. parsed-literal::

    DatetimeIndex(['2012-07-02 14:30:00+00:00', '2012-07-02 15:30:00+00:00',
                   '2012-07-02 16:30:00+00:00', '2012-07-02 17:30:00+00:00',
                   '2012-07-02 18:30:00+00:00', '2012-07-02 19:30:00+00:00',
                   '2012-07-02 20:00:00+00:00', '2012-07-03 14:30:00+00:00',
                   '2012-07-03 15:30:00+00:00', '2012-07-03 16:30:00+00:00',
                   '2012-07-03 17:00:00+00:00', '2012-07-05 14:30:00+00:00',
                   '2012-07-05 15:30:00+00:00', '2012-07-05 16:30:00+00:00',
                   '2012-07-05 17:30:00+00:00', '2012-07-05 18:30:00+00:00',
                   '2012-07-05 19:30:00+00:00', '2012-07-05 20:00:00+00:00',
                   '2012-07-06 14:30:00+00:00', '2012-07-06 15:30:00+00:00',
                   '2012-07-06 16:30:00+00:00', '2012-07-06 17:30:00+00:00',
                   '2012-07-06 18:30:00+00:00', '2012-07-06 19:30:00+00:00',
                   '2012-07-06 20:00:00+00:00', '2012-07-09 14:30:00+00:00',
                   '2012-07-09 15:30:00+00:00', '2012-07-09 16:30:00+00:00',
                   '2012-07-09 17:30:00+00:00', '2012-07-09 18:30:00+00:00',
                   '2012-07-09 19:30:00+00:00', '2012-07-09 20:00:00+00:00',
                   '2012-07-10 14:30:00+00:00', '2012-07-10 15:30:00+00:00',
                   '2012-07-10 16:30:00+00:00', '2012-07-10 17:30:00+00:00',
                   '2012-07-10 18:30:00+00:00', '2012-07-10 19:30:00+00:00',
                   '2012-07-10 20:00:00+00:00'],
                  dtype='datetime64[ns, UTC]', freq=None)

Contributing
------------
All improvements and additional (and corrections) in the form of pull requests are welcome. This package will grow in
value and correctness the more eyes are on it.

To add new functionality please include tests which are in standard pytest format. 

Use pytest to run the test suite.

For complete information on contributing see CONTRIBUTING.md_

.. _CONTRIBUTING.md: https://github.com/rsheftel/pandas_market_calendars/blob/master/CONTRIBUTING.md

Future
------
This package is open sourced under the MIT license. Everyone is welcome to add more exchanges or OTC markets, confirm
or correct the existing calendars, and generally do whatever they desire with this code.

Sponsor
-------
.. image:: https://www.tradinghours.com/img/logo-with-words.png
    :target: https://www.tradinghours.com/data
    :alt: TradingHours.com

`TradingHours.com <https://www.tradinghours.com?utm_source=github&utm_medium=sponsor&utm_campaign=panda>`_ provides the most accurate and comprehensive coverage of market holidays and trading hours data available. They cover over 1,100 markets worldwide, with extensive historical data and full coverage of all global trading venues, including the CME, ICE, Eurex, and more.

Their data is continuously monitored for changes and updated daily. If there's a market you need that they don't currently cover, they'll add it. For when accurate, reliable data matters most, choose TradingHours.com. `Learn more <https://www.tradinghours.com/data?utm_source=github&utm_medium=sponsor&utm_campaign=panda>`_
