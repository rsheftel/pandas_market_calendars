
Examples
========

.. code:: python

    import sys
    sys.path.append("../") 
    from datetime import time
    import pandas as pd
    import pandas_exchange_calendars as pec

Setup new exchange calendar
---------------------------

.. code:: python

    nyse = pec.get_calendar('NYSE')

Get the time zone

.. code:: python

    nyse.tz.zone




.. parsed-literal::

    'America/New_York'



Get the AbstractHolidayCalendar object

.. code:: python

    holidays = nyse.holidays()
    holidays.holidays[-5:]




.. parsed-literal::

    (numpy.datetime64('2030-05-27'),
     numpy.datetime64('2030-07-04'),
     numpy.datetime64('2030-09-02'),
     numpy.datetime64('2030-11-28'),
     numpy.datetime64('2030-12-25'))



Exchange open valid business days
---------------------------------

Get the valid open exchange business dates between a start and end date.
Note that Dec 26 (Christmas), Jan 2 (New Years) and all weekends are
missing

.. code:: python

    nyse.valid_days(start_date='2016-12-20', end_date='2017-01-10')




.. parsed-literal::

    DatetimeIndex(['2016-12-20', '2016-12-21', '2016-12-22', '2016-12-23',
                   '2016-12-27', '2016-12-28', '2016-12-29', '2016-12-30',
                   '2017-01-03', '2017-01-04', '2017-01-05', '2017-01-06',
                   '2017-01-09', '2017-01-10'],
                  dtype='datetime64[ns, UTC]', freq='C')



Schedule
--------

.. code:: python

    schedule = nyse.schedule(start_date='2016-12-30', end_date='2017-01-10')
    schedule




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
          <th>2016-12-30</th>
          <td>2016-12-30 14:30:00+00:00</td>
          <td>2016-12-30 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2017-01-03</th>
          <td>2017-01-03 14:30:00+00:00</td>
          <td>2017-01-03 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2017-01-04</th>
          <td>2017-01-04 14:30:00+00:00</td>
          <td>2017-01-04 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2017-01-05</th>
          <td>2017-01-05 14:30:00+00:00</td>
          <td>2017-01-05 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2017-01-06</th>
          <td>2017-01-06 14:30:00+00:00</td>
          <td>2017-01-06 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2017-01-09</th>
          <td>2017-01-09 14:30:00+00:00</td>
          <td>2017-01-09 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2017-01-10</th>
          <td>2017-01-10 14:30:00+00:00</td>
          <td>2017-01-10 21:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # with early closes
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



Get early closes
----------------

.. code:: python

    nyse.early_closes(schedule=early)




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
          <th>2012-07-03</th>
          <td>2012-07-03 13:30:00+00:00</td>
          <td>2012-07-03 17:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



Open at time
------------

Test to see if a given timestamp is during market open hours

.. code:: python

    nyse.open_at_time(early, pd.Timestamp('2012-07-03 12:00', tz='America/New_York'))




.. parsed-literal::

    True



.. code:: python

    nyse.open_at_time(early, pd.Timestamp('2012-07-03 16:00', tz='America/New_York'))




.. parsed-literal::

    False



Date Range
----------

This function will take a schedule DataFrame and return a DatetimeIndex
with all timestamps at the frequency given for all of the exchange open
dates and times.

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



Custom open and close times
---------------------------

If you want to override the market open and close times enter these at
construction

.. code:: python

    cal = pec.get_calendar('NYSE', open_time=time(10, 0), close_time=time(14, 30))
    print('open, close: %s, %s' % (cal.open_time, cal.close_time))


.. parsed-literal::

    open, close: 10:00:00, 14:30:00
    

Merge schedules
---------------

.. code:: python

    # NYSE Calendar
    nyse = pec.get_calendar('NYSE')
    schedule_nyse = nyse.schedule('2015-12-20', '2016-01-06')
    schedule_nyse




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
          <th>2015-12-21</th>
          <td>2015-12-21 14:30:00+00:00</td>
          <td>2015-12-21 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-22</th>
          <td>2015-12-22 14:30:00+00:00</td>
          <td>2015-12-22 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-23</th>
          <td>2015-12-23 14:30:00+00:00</td>
          <td>2015-12-23 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-24</th>
          <td>2015-12-24 14:30:00+00:00</td>
          <td>2015-12-24 18:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-28</th>
          <td>2015-12-28 14:30:00+00:00</td>
          <td>2015-12-28 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-29</th>
          <td>2015-12-29 14:30:00+00:00</td>
          <td>2015-12-29 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-30</th>
          <td>2015-12-30 14:30:00+00:00</td>
          <td>2015-12-30 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-31</th>
          <td>2015-12-31 14:30:00+00:00</td>
          <td>2015-12-31 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2016-01-04</th>
          <td>2016-01-04 14:30:00+00:00</td>
          <td>2016-01-04 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2016-01-05</th>
          <td>2016-01-05 14:30:00+00:00</td>
          <td>2016-01-05 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2016-01-06</th>
          <td>2016-01-06 14:30:00+00:00</td>
          <td>2016-01-06 21:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # LSE Calendar
    lse = pec.get_calendar('LSE')
    schedule_lse = lse.schedule('2015-12-20', '2016-01-06')
    schedule_lse




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
          <th>2015-12-21</th>
          <td>2015-12-21 08:00:00+00:00</td>
          <td>2015-12-21 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-22</th>
          <td>2015-12-22 08:00:00+00:00</td>
          <td>2015-12-22 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-23</th>
          <td>2015-12-23 08:00:00+00:00</td>
          <td>2015-12-23 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-24</th>
          <td>2015-12-24 08:00:00+00:00</td>
          <td>2015-12-24 12:30:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-29</th>
          <td>2015-12-29 08:00:00+00:00</td>
          <td>2015-12-29 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-30</th>
          <td>2015-12-30 08:00:00+00:00</td>
          <td>2015-12-30 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-31</th>
          <td>2015-12-31 08:00:00+00:00</td>
          <td>2015-12-31 12:30:00+00:00</td>
        </tr>
        <tr>
          <th>2016-01-04</th>
          <td>2016-01-04 08:00:00+00:00</td>
          <td>2016-01-04 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2016-01-05</th>
          <td>2016-01-05 08:00:00+00:00</td>
          <td>2016-01-05 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2016-01-06</th>
          <td>2016-01-06 08:00:00+00:00</td>
          <td>2016-01-06 16:30:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



Inner merge
~~~~~~~~~~~

This will find the dates where both the NYSE and LSE are open. Notice
that Dec 28th is open for NYSE but not LSE. Also note that some days
have a close prior to the open. This function does not currently check
for that.

.. code:: python

    pec.merge_schedules(schedules=[schedule_nyse, schedule_lse], how='inner')




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
          <th>2015-12-21</th>
          <td>2015-12-21 14:30:00+00:00</td>
          <td>2015-12-21 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-22</th>
          <td>2015-12-22 14:30:00+00:00</td>
          <td>2015-12-22 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-23</th>
          <td>2015-12-23 14:30:00+00:00</td>
          <td>2015-12-23 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-24</th>
          <td>2015-12-24 14:30:00+00:00</td>
          <td>2015-12-24 12:30:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-29</th>
          <td>2015-12-29 14:30:00+00:00</td>
          <td>2015-12-29 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-30</th>
          <td>2015-12-30 14:30:00+00:00</td>
          <td>2015-12-30 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-31</th>
          <td>2015-12-31 14:30:00+00:00</td>
          <td>2015-12-31 12:30:00+00:00</td>
        </tr>
        <tr>
          <th>2016-01-04</th>
          <td>2016-01-04 14:30:00+00:00</td>
          <td>2016-01-04 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2016-01-05</th>
          <td>2016-01-05 14:30:00+00:00</td>
          <td>2016-01-05 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2016-01-06</th>
          <td>2016-01-06 14:30:00+00:00</td>
          <td>2016-01-06 16:30:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



Outer merge
~~~~~~~~~~~

This will return the dates and times where either the NYSE or the LSE
are open

.. code:: python

    pec.merge_schedules(schedules=[schedule_nyse, schedule_lse], how='outer')




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
          <th>2015-12-21</th>
          <td>2015-12-21 08:00:00+00:00</td>
          <td>2015-12-21 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-22</th>
          <td>2015-12-22 08:00:00+00:00</td>
          <td>2015-12-22 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-23</th>
          <td>2015-12-23 08:00:00+00:00</td>
          <td>2015-12-23 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-24</th>
          <td>2015-12-24 08:00:00+00:00</td>
          <td>2015-12-24 18:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-28</th>
          <td>2015-12-28 14:30:00+00:00</td>
          <td>2015-12-28 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-29</th>
          <td>2015-12-29 08:00:00+00:00</td>
          <td>2015-12-29 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-30</th>
          <td>2015-12-30 08:00:00+00:00</td>
          <td>2015-12-30 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2015-12-31</th>
          <td>2015-12-31 08:00:00+00:00</td>
          <td>2015-12-31 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2016-01-04</th>
          <td>2016-01-04 08:00:00+00:00</td>
          <td>2016-01-04 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2016-01-05</th>
          <td>2016-01-05 08:00:00+00:00</td>
          <td>2016-01-05 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2016-01-06</th>
          <td>2016-01-06 08:00:00+00:00</td>
          <td>2016-01-06 21:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



