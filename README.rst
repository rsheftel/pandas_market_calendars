pandas_exchange_calendars
=========================
Exchange calendars to use with pandas for trading applications.

.. image:: https://travis-ci.org/rsheftel/pandas_exchange_calendars.svg?branch=master
    :target: https://travis-ci.org/rsheftel/pandas_exchange_calendars
    
Documentation
-------------
http://pandas_exchange_calendars.readthedocs.io/en/latest/

Overview
--------
The Pandas package is widely used in finance and specifically for time series analysis. It includes excellent
functionality for generating sequences of dates and capabilities for custom holiday calendars, but as an explicit
design choice it does not include the actual holiday calendars for specific exchanges.

The pandas_exchange_calendars package looks to fill that role with the holiday, late open and early close calendars
for specific exchanges and OTC conventions. pandas_exchange_calendars also adds several functions to manipulate the
exchange calendars and includes a date_range function to create a pandas DatetimeIndex including only the datetimes
when the markets are open.

This package is a fork of the Zipline package from Quantopian and extracts just the relevant parts. All credit for
their excellent work to Quantopian.

Installation
------------
``pip install pandas_exchange_calendars``

Quick Start
-----------
.. code:: python

    import pandas_exchange_calendars as pec
    nyse = pec.get_calendar('NYSE')


.. code:: python

    early = nyse.schedule(start_date='2012-07-01', end_date='2012-07-10')
    early

.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>market_open</th>
          <th>market_close</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2012-07-02</th>
          <td>2012-07-02 13:30:00+00:00</td>
          <td>2012-07-02 20:00:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-03</th>
          <td>2012-07-03 13:30:00+00:00</td>
          <td>2012-07-03 17:00:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-05</th>
          <td>2012-07-05 13:30:00+00:00</td>
          <td>2012-07-05 20:00:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-06</th>
          <td>2012-07-06 13:30:00+00:00</td>
          <td>2012-07-06 20:00:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-09</th>
          <td>2012-07-09 13:30:00+00:00</td>
          <td>2012-07-09 20:00:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-10</th>
          <td>2012-07-10 13:30:00+00:00</td>
          <td>2012-07-10 20:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>

.. code:: python

    pec.date_range(early, frequency='1D')




.. parsed-literal::

    DatetimeIndex(['2012-07-02 20:00:00+00:00', '2012-07-03 17:00:00+00:00',
                   '2012-07-05 20:00:00+00:00', '2012-07-06 20:00:00+00:00',
                   '2012-07-09 20:00:00+00:00', '2012-07-10 20:00:00+00:00'],
                  dtype='datetime64[ns, UTC]', freq=None)



.. code:: python

    pec.date_range(early, frequency='1H')




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

Future
------
This package is open sourced under the MIT license. Everyone is welcome to add more exchanges or OTC markets, confirm
or correct the existing calendars, and generally do whatever they desire with this code.
