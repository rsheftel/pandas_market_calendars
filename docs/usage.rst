.. code:: ipython3

    import sys
    sys.path.append("../") 
    from datetime import time
    import pandas as pd
    import pandas_market_calendars as mcal

Calendars
=========

Basic Usage
-----------

Setup new exchange calendar
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    nyse = mcal.get_calendar('NYSE')

Get the time zone

.. code:: ipython3

    nyse.tz.zone




.. parsed-literal::

    'America/New_York'



Get the AbstractHolidayCalendar object

.. code:: ipython3

    holidays = nyse.holidays()
    holidays.holidays[-5:]




.. parsed-literal::

    (numpy.datetime64('2200-06-19'),
     numpy.datetime64('2200-07-04'),
     numpy.datetime64('2200-09-01'),
     numpy.datetime64('2200-11-27'),
     numpy.datetime64('2200-12-25'))



View the available information on regular market times

.. code:: ipython3

    print(nyse.regular_market_times) # more on this under the 'Customizations' heading


.. parsed-literal::

    ProtectedDict(
    {'pre': ((None, datetime.time(4, 0)),),
     'market_open': ((None, datetime.time(10, 0)),
                     ('1985-01-01', datetime.time(9, 30))),
     'market_close': ((None, datetime.time(15, 0)),
                      ('1952-09-29', datetime.time(15, 30)),
                      ('1974-01-01', datetime.time(16, 0))),
     'post': ((None, datetime.time(20, 0)),)}
    )


Exchange open valid business days
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get the valid open exchange business dates between a start and end date.
Note that Dec 26 (Christmas), Jan 2 (New Years) and all weekends are
missing

.. code:: ipython3

    nyse.valid_days(start_date='2016-12-20', end_date='2017-01-10')




.. parsed-literal::

    DatetimeIndex(['2016-12-20 00:00:00+00:00', '2016-12-21 00:00:00+00:00',
                   '2016-12-22 00:00:00+00:00', '2016-12-23 00:00:00+00:00',
                   '2016-12-27 00:00:00+00:00', '2016-12-28 00:00:00+00:00',
                   '2016-12-29 00:00:00+00:00', '2016-12-30 00:00:00+00:00',
                   '2017-01-03 00:00:00+00:00', '2017-01-04 00:00:00+00:00',
                   '2017-01-05 00:00:00+00:00', '2017-01-06 00:00:00+00:00',
                   '2017-01-09 00:00:00+00:00', '2017-01-10 00:00:00+00:00'],
                  dtype='datetime64[ns, UTC]', freq=None)



Schedule
~~~~~~~~

.. code:: ipython3

    schedule = nyse.schedule(start_date='2016-12-30', end_date='2017-01-10')
    schedule




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
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



.. code:: ipython3

    # with early closes
    early = nyse.schedule(start_date='2012-07-01', end_date='2012-07-10')
    early




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
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



.. code:: ipython3

    # including pre and post-market
    extended = nyse.schedule(start_date='2012-07-01', end_date='2012-07-10', start="pre", end="post")
    extended




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>pre</th>
          <th>market_open</th>
          <th>market_close</th>
          <th>post</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2012-07-02</th>
          <td>2012-07-02 08:00:00+00:00</td>
          <td>2012-07-02 13:30:00+00:00</td>
          <td>2012-07-02 20:00:00+00:00</td>
          <td>2012-07-03 00:00:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-03</th>
          <td>2012-07-03 08:00:00+00:00</td>
          <td>2012-07-03 13:30:00+00:00</td>
          <td>2012-07-03 17:00:00+00:00</td>
          <td>2012-07-03 17:00:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-05</th>
          <td>2012-07-05 08:00:00+00:00</td>
          <td>2012-07-05 13:30:00+00:00</td>
          <td>2012-07-05 20:00:00+00:00</td>
          <td>2012-07-06 00:00:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-06</th>
          <td>2012-07-06 08:00:00+00:00</td>
          <td>2012-07-06 13:30:00+00:00</td>
          <td>2012-07-06 20:00:00+00:00</td>
          <td>2012-07-07 00:00:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-09</th>
          <td>2012-07-09 08:00:00+00:00</td>
          <td>2012-07-09 13:30:00+00:00</td>
          <td>2012-07-09 20:00:00+00:00</td>
          <td>2012-07-10 00:00:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-10</th>
          <td>2012-07-10 08:00:00+00:00</td>
          <td>2012-07-10 13:30:00+00:00</td>
          <td>2012-07-10 20:00:00+00:00</td>
          <td>2012-07-11 00:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    # specific market times 
    # CAVEAT: Looking at 2012-07-03, you can see that times will NOT be adjusted to special_opens/sepcial_closes
    # if market_open/market_close are not requested
    specific = nyse.schedule(start_date='2012-07-01', end_date='2012-07-10', market_times= ["post", "market_open"]) # this order will be kept
    specific




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>post</th>
          <th>market_open</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2012-07-02</th>
          <td>2012-07-03 00:00:00+00:00</td>
          <td>2012-07-02 13:30:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-03</th>
          <td>2012-07-04 00:00:00+00:00</td>
          <td>2012-07-03 13:30:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-05</th>
          <td>2012-07-06 00:00:00+00:00</td>
          <td>2012-07-05 13:30:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-06</th>
          <td>2012-07-07 00:00:00+00:00</td>
          <td>2012-07-06 13:30:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-09</th>
          <td>2012-07-10 00:00:00+00:00</td>
          <td>2012-07-09 13:30:00+00:00</td>
        </tr>
        <tr>
          <th>2012-07-10</th>
          <td>2012-07-11 00:00:00+00:00</td>
          <td>2012-07-10 13:30:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



Get early closes
~~~~~~~~~~~~~~~~

.. code:: ipython3

    nyse.early_closes(schedule=early)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
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



.. code:: ipython3

    nyse.early_closes(schedule=extended)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>pre</th>
          <th>market_open</th>
          <th>market_close</th>
          <th>post</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2012-07-03</th>
          <td>2012-07-03 08:00:00+00:00</td>
          <td>2012-07-03 13:30:00+00:00</td>
          <td>2012-07-03 17:00:00+00:00</td>
          <td>2012-07-03 17:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



Open at time
~~~~~~~~~~~~

Test to see if a given timestamp is during market open hours. (You can
find more on this under the ‘Advanced open_at_time’ header)

.. code:: ipython3

    nyse.open_at_time(early, pd.Timestamp('2012-07-03 12:00', tz='America/New_York'))




.. parsed-literal::

    True



.. code:: ipython3

    nyse.open_at_time(early, pd.Timestamp('2012-07-03 16:00', tz='America/New_York'))




.. parsed-literal::

    False



Other market times will also be considered

.. code:: ipython3

    nyse.open_at_time(extended, pd.Timestamp('2012-07-05 18:00', tz='America/New_York'))




.. parsed-literal::

    True



but can be ignored by setting only_rth = True

.. code:: ipython3

    nyse.open_at_time(extended, pd.Timestamp('2012-07-05 18:00', tz='America/New_York'), only_rth = True)




.. parsed-literal::

    False



Customizations
==============

The simplest way to customize the market times of a calendar is by
passing datetime.time objects to the constructor, which will modify the
open and/or close of *regular trading hours*.

.. code:: ipython3

    cal = mcal.get_calendar('NYSE', open_time=time(10, 0), close_time=time(14, 30))
    print('open, close: %s, %s' % (cal.open_time, cal.close_time))


.. parsed-literal::

    open, close: 10:00:00, 14:30:00


More advanced customizations can be done after initialization or by
inheriting from the closest MarketCalendar class, which requires an
explanation of market times…

Market times
------------

Market times are moments in a trading day that are contained in the
``regular_market_times`` attribute, for example:

.. code:: ipython3

    print("The original NYSE calendar: \n", nyse.regular_market_times)


.. parsed-literal::

    The original NYSE calendar: 
     ProtectedDict(
    {'pre': ((None, datetime.time(4, 0)),),
     'market_open': ((None, datetime.time(10, 0)),
                     ('1985-01-01', datetime.time(9, 30))),
     'market_close': ((None, datetime.time(15, 0)),
                      ('1952-09-29', datetime.time(15, 30)),
                      ('1974-01-01', datetime.time(16, 0))),
     'post': ((None, datetime.time(20, 0)),)}
    )


NYSE’s regular trading hours are referenced by “market_open” and
“market_close”, but NYSE also has extended hours, which are referenced
by “pre” and “post”.

*The attribute ``regular_market_times`` has these requirements:*

-  It needs to be a dictionary

-  Each market_time needs one entry

   -  Regular open must be “market_open”, regular close must be
      “market_close”.
   -  If there is a break, there must be a “break_start” and a
      “break_end”.
   -  only ONE break is currently supported.

-  One tuple for each market_time, containing at least one tuple:

   -  Each nested tuple needs at least two items:
      ``(first_date_used, time[, offset])``.
   -  The first tuple’s date should be None, marking the start. In every
      tuple thereafter this is the date when ``time`` was first used.
   -  Optionally (assumed to be zero, when not present), a positive or
      negative integer, representing an offset in number of days.
   -  Dates need to be in ascending order, None coming first.

E.g.:

.. code:: ipython3

    print(nyse.get_time("market_close", all_times= True)) # all_times = False only returns current


.. parsed-literal::

    ((None, datetime.time(15, 0)), ('1952-09-29', datetime.time(15, 30)), ('1974-01-01', datetime.time(16, 0)))


The first known close was 3pm, which changed on 1952-09-29 to 3:30pm,
which changed on 1974-01-01 to 4pm. The dates are the first dates that
the new time was used.

Customizing after initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are three methods that allow customizing the
``regular_market_times`` of a MarketCalendar instance: \*
``.change_time(market_time, times)`` \*
``.add_time(market_time, times)`` \* ``.remove_time(market_time)``

.. code:: ipython3

    cal = mcal.get_calendar("NYSE")
    cal.change_time("market_open", time(10,30))
    print('open, close: %s, %s' % (cal.open_time, cal.close_time))
    print("\nThe 'market_open' information is entirely replaced:\n", cal.regular_market_times)


.. parsed-literal::

    open, close: 10:30:00, 16:00:00
    
    The 'market_open' information is entirely replaced:
     ProtectedDict(
    {'pre': ((None, datetime.time(4, 0)),),
     'market_open': ((None, datetime.time(10, 30)),),
     'market_close': ((None, datetime.time(15, 0)),
                      ('1952-09-29', datetime.time(15, 30)),
                      ('1974-01-01', datetime.time(16, 0))),
     'post': ((None, datetime.time(20, 0)),)}
    )


.. code:: ipython3

    cal.remove_time("post")
    cal.add_time("new_post", time(19))
    print(cal.regular_market_times)


.. parsed-literal::

    ProtectedDict(
    {'pre': ((None, datetime.time(4, 0)),),
     'market_open': ((None, datetime.time(10, 30)),),
     'market_close': ((None, datetime.time(15, 0)),
                      ('1952-09-29', datetime.time(15, 30)),
                      ('1974-01-01', datetime.time(16, 0))),
     'new_post': ((None, datetime.time(19, 0)),)}
    )


.. code:: ipython3

    cal.remove_time("pre")
    cal.remove_time("new_post")

The methods ``.add_time`` and ``.change_time`` also accept the time
information in these formats:

.. code:: ipython3

    cal.add_time("just_time", time(10))
    cal.add_time("with_offset", (time(10), -1))
    cal.add_time("changes_and_offset", ((None, time(17)), ("2009-12-28", time(11), -2)))
    print(cal.regular_market_times)


.. parsed-literal::

    ProtectedDict(
    {'market_open': ((None, datetime.time(10, 30)),),
     'market_close': ((None, datetime.time(15, 0)),
                      ('1952-09-29', datetime.time(15, 30)),
                      ('1974-01-01', datetime.time(16, 0))),
     'just_time': ((None, datetime.time(10, 0)),),
     'with_offset': ((None, datetime.time(10, 0), -1),),
     'changes_and_offset': ((None, datetime.time(17, 0)),
                            ('2009-12-28', datetime.time(11, 0), -2))}
    )


CAVEATS:
~~~~~~~~

FIRST
^^^^^

| *Internally, an order of market_times is detected based on their
  current time*.
| Because of the offsets in “with_offset” and “changes_and_offset”, the
  columns in a schedule are in the following order:

.. code:: ipython3

    cal.schedule("2009-12-23", "2009-12-29", market_times= "all")




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>changes_and_offset</th>
          <th>with_offset</th>
          <th>just_time</th>
          <th>market_open</th>
          <th>market_close</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2009-12-23</th>
          <td>2009-12-23 22:00:00+00:00</td>
          <td>2009-12-22 15:00:00+00:00</td>
          <td>2009-12-23 15:00:00+00:00</td>
          <td>2009-12-23 15:30:00+00:00</td>
          <td>2009-12-23 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2009-12-24</th>
          <td>2009-12-24 18:00:00+00:00</td>
          <td>2009-12-23 15:00:00+00:00</td>
          <td>2009-12-24 15:00:00+00:00</td>
          <td>2009-12-24 15:30:00+00:00</td>
          <td>2009-12-24 18:00:00+00:00</td>
        </tr>
        <tr>
          <th>2009-12-28</th>
          <td>2009-12-26 16:00:00+00:00</td>
          <td>2009-12-27 15:00:00+00:00</td>
          <td>2009-12-28 15:00:00+00:00</td>
          <td>2009-12-28 15:30:00+00:00</td>
          <td>2009-12-28 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2009-12-29</th>
          <td>2009-12-27 16:00:00+00:00</td>
          <td>2009-12-28 15:00:00+00:00</td>
          <td>2009-12-29 15:00:00+00:00</td>
          <td>2009-12-29 15:30:00+00:00</td>
          <td>2009-12-29 21:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



On 2009-12-23 changes_and_offset doesn’t seem to be in the right order,
but as of 2009-12-28 it is.

Passing a list to ``market_times``, allows you to keep a custom order:

.. code:: ipython3

    cal.schedule("2009-12-23", "2009-12-29", market_times= ["with_offset", "market_open", "market_close", "changes_and_offset"])




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>with_offset</th>
          <th>market_open</th>
          <th>market_close</th>
          <th>changes_and_offset</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2009-12-23</th>
          <td>2009-12-22 15:00:00+00:00</td>
          <td>2009-12-23 15:30:00+00:00</td>
          <td>2009-12-23 21:00:00+00:00</td>
          <td>2009-12-23 22:00:00+00:00</td>
        </tr>
        <tr>
          <th>2009-12-24</th>
          <td>2009-12-23 15:00:00+00:00</td>
          <td>2009-12-24 15:30:00+00:00</td>
          <td>2009-12-24 18:00:00+00:00</td>
          <td>2009-12-24 18:00:00+00:00</td>
        </tr>
        <tr>
          <th>2009-12-28</th>
          <td>2009-12-27 15:00:00+00:00</td>
          <td>2009-12-28 15:30:00+00:00</td>
          <td>2009-12-28 21:00:00+00:00</td>
          <td>2009-12-26 16:00:00+00:00</td>
        </tr>
        <tr>
          <th>2009-12-29</th>
          <td>2009-12-28 15:00:00+00:00</td>
          <td>2009-12-29 15:30:00+00:00</td>
          <td>2009-12-29 21:00:00+00:00</td>
          <td>2009-12-27 16:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



SECOND
^^^^^^

| *Special closes of market_closes will override all later times,
  special opens of market_opens will override all earlier times*.
| In the prior schedule, 2009-12-24 is a special market_close, which was
  enforced in the changes_and_offset column.

Providing ``False`` or ``None`` to the ``force_special_times`` keyword
argument, changes this behaviour:

.. code:: ipython3

    # False - will only adjust the columns itself (changes_and_offset left alone, market_close adjusted)
    cal.schedule("2009-12-23", "2009-12-28", market_times= ["changes_and_offset", "market_close"], force_special_times= False)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>changes_and_offset</th>
          <th>market_close</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2009-12-23</th>
          <td>2009-12-23 22:00:00+00:00</td>
          <td>2009-12-23 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2009-12-24</th>
          <td>2009-12-24 22:00:00+00:00</td>
          <td>2009-12-24 18:00:00+00:00</td>
        </tr>
        <tr>
          <th>2009-12-28</th>
          <td>2009-12-26 16:00:00+00:00</td>
          <td>2009-12-28 21:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    # None - will not adjust any column (both are left alone)
    cal.schedule("2009-12-23", "2009-12-28", market_times= ["changes_and_offset", "market_close"], force_special_times= None) 




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>changes_and_offset</th>
          <th>market_close</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2009-12-23</th>
          <td>2009-12-23 22:00:00+00:00</td>
          <td>2009-12-23 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2009-12-24</th>
          <td>2009-12-24 22:00:00+00:00</td>
          <td>2009-12-24 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2009-12-28</th>
          <td>2009-12-26 16:00:00+00:00</td>
          <td>2009-12-28 21:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



Inheriting from a MarketCalendar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You get even more control over a calendar (or help this package by
contributing a calendar) by inheriting from a MarketCalendar class. The
following three sections cover:

::

   * Setting special times for market_times
   * Setting interruptions
   * How to make sure open_at_time works

Special Times
^^^^^^^^^^^^^

Any market_time in regular_market_times can have special times, which
are looked for in two properties:

::

   special_{market_time}_adhoc
       same format as special_opens_adhoc, which is the same as special_market_open_adhoc
   special_{market_time}
       same format as special_opens, which is the same as special_market_open

.. code:: ipython3

    # For example, CFEExchangeCalendar only has the regular trading hours for the futures exchange (8:30 - 15:15).
    # If you want to use the equity options exchange (8:30 - 15:00), including the order acceptance time at 7:30, and
    # some special cases when the order acceptance time was different, do this:
    
    from pandas_market_calendars.exchange_calendar_cboe import CFEExchangeCalendar 
    
    class DemoOptionsCalendar(CFEExchangeCalendar):  # Inherit what doesn't need to change
        name = "Demo_Options"
        aliases = [name]
        regular_market_times = {**CFEExchangeCalendar.regular_market_times, # unpack the parent's regular_market_times
                                "order_acceptance": ((None, time(7,30)),),  # add your market time of interest
                                "market_close": ((None, time(15)),)} # overwrite the market time you want to change  
        
        @property
        def special_order_acceptance_adhoc(self):  # include special cases
            return [(time(8,30), ["2000-12-27", "2001-12-27"])]


.. code:: ipython3

    options = mcal.get_calendar("Demo_Options")
    
    print(options.regular_market_times)


.. parsed-literal::

    ProtectedDict(
    {'market_open': ((None, datetime.time(8, 30)),),
     'market_close': ((None, datetime.time(15, 0)),),
     'order_acceptance': ((None, datetime.time(7, 30)),)}
    )


.. code:: ipython3

    schedule = options.schedule("2000-12-22", "2000-12-28", start= "order_acceptance") 
    schedule




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>order_acceptance</th>
          <th>market_open</th>
          <th>market_close</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2000-12-22</th>
          <td>2000-12-22 13:30:00+00:00</td>
          <td>2000-12-22 14:30:00+00:00</td>
          <td>2000-12-22 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2000-12-26</th>
          <td>2000-12-26 13:30:00+00:00</td>
          <td>2000-12-26 14:30:00+00:00</td>
          <td>2000-12-26 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2000-12-27</th>
          <td>2000-12-27 14:30:00+00:00</td>
          <td>2000-12-27 14:30:00+00:00</td>
          <td>2000-12-27 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2000-12-28</th>
          <td>2000-12-28 13:30:00+00:00</td>
          <td>2000-12-28 14:30:00+00:00</td>
          <td>2000-12-28 21:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



Dec 25th is filtered out already because it is inherited from the
CFEExchangeCalendar, and the special case on 2000-12-27 is also
integrated

Interruptions
^^^^^^^^^^^^^

MarketCalendar subclasses also support interruptions, which can be
defined in the ``interruptions`` property. To view interruptions, you
can use the ``interruptions_df`` property or set ``interruptions= True``
when calling ``schedule``.

.. code:: ipython3

    class InterruptionsDemo(DemoOptionsCalendar):
        @property
        def interruptions(self):
            return [
                ("2002-02-03", (time(11), -1), time(11, 2)),
                ("2010-01-11", time(11), (time(11, 1), 1)),
                ("2010-01-13", time(9, 59), time(10), time(10, 29), time(10, 30)),
                ("2011-01-10", time(11), time(11, 1))]
        

.. code:: ipython3

    cal = InterruptionsDemo()

.. code:: ipython3

    cal.interruptions_df




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>interruption_start_1</th>
          <th>interruption_end_1</th>
          <th>interruption_start_2</th>
          <th>interruption_end_2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2002-02-03</th>
          <td>2002-02-02 17:00:00+00:00</td>
          <td>2002-02-03 17:02:00+00:00</td>
          <td>NaT</td>
          <td>NaT</td>
        </tr>
        <tr>
          <th>2010-01-11</th>
          <td>2010-01-11 17:00:00+00:00</td>
          <td>2010-01-12 17:01:00+00:00</td>
          <td>NaT</td>
          <td>NaT</td>
        </tr>
        <tr>
          <th>2010-01-13</th>
          <td>2010-01-13 15:59:00+00:00</td>
          <td>2010-01-13 16:00:00+00:00</td>
          <td>2010-01-13 16:29:00+00:00</td>
          <td>2010-01-13 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2011-01-10</th>
          <td>2011-01-10 17:00:00+00:00</td>
          <td>2011-01-10 17:01:00+00:00</td>
          <td>NaT</td>
          <td>NaT</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    sched = cal.schedule("2010-01-09", "2010-01-15", interruptions= True)
    sched




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>market_open</th>
          <th>market_close</th>
          <th>interruption_start_1</th>
          <th>interruption_end_1</th>
          <th>interruption_start_2</th>
          <th>interruption_end_2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2010-01-11</th>
          <td>2010-01-11 14:30:00+00:00</td>
          <td>2010-01-11 21:00:00+00:00</td>
          <td>2010-01-11 17:00:00+00:00</td>
          <td>2010-01-12 17:01:00+00:00</td>
          <td>NaT</td>
          <td>NaT</td>
        </tr>
        <tr>
          <th>2010-01-12</th>
          <td>2010-01-12 14:30:00+00:00</td>
          <td>2010-01-12 21:00:00+00:00</td>
          <td>NaT</td>
          <td>NaT</td>
          <td>NaT</td>
          <td>NaT</td>
        </tr>
        <tr>
          <th>2010-01-13</th>
          <td>2010-01-13 14:30:00+00:00</td>
          <td>2010-01-13 21:00:00+00:00</td>
          <td>2010-01-13 15:59:00+00:00</td>
          <td>2010-01-13 16:00:00+00:00</td>
          <td>2010-01-13 16:29:00+00:00</td>
          <td>2010-01-13 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2010-01-14</th>
          <td>2010-01-14 14:30:00+00:00</td>
          <td>2010-01-14 21:00:00+00:00</td>
          <td>NaT</td>
          <td>NaT</td>
          <td>NaT</td>
          <td>NaT</td>
        </tr>
        <tr>
          <th>2010-01-15</th>
          <td>2010-01-15 14:30:00+00:00</td>
          <td>2010-01-15 21:00:00+00:00</td>
          <td>NaT</td>
          <td>NaT</td>
          <td>NaT</td>
          <td>NaT</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    def is_open(c, s, *dates):
        for t in dates:
            print("open on", t, ":", c.open_at_time(s, t))

Advanced open_at_time
^^^^^^^^^^^^^^^^^^^^^

``MarketCalendar.open_at_time`` uses the class attribute
``open_close_map`` to determine if a market_time opens or closes the
market. It will also look for the ‘interruption\_’ prefix in the columns
to respect interruptions.

Here you can see that MarketCalendar.open_at_time respects interruptions
(the last two timestamps):

.. code:: ipython3

    is_open(cal, sched, "2010-01-12 14:00:00", "2010-01-12 14:35:00","2010-01-13 15:59:00","2010-01-13 16:30:00")


.. parsed-literal::

    open on 2010-01-12 14:00:00 : False
    open on 2010-01-12 14:35:00 : True
    open on 2010-01-13 15:59:00 : False
    open on 2010-01-13 16:30:00 : True


In the ``DemoOptionsCalendar``, we did not specify what order_acceptance
means for the market, which will not allow open_at_time to work.

.. code:: ipython3

    sched = cal.schedule("2010-01-09", "2010-01-15", start= "order_acceptance", interruptions= True)
    try: 
        cal.open_at_time(sched, "2010-01-12")
    except ValueError as e: 
        print(e)


.. parsed-literal::

    You seem to be using a schedule that isn't based on the market_times, or includes market_times that are not represented in the open_close_map.


.. code:: ipython3

    # These are the defaults that every MarketCalendar has, which is still missing order_accpetance.
    print(cal.open_close_map)


.. parsed-literal::

    ProtectedDict(
    {'market_open': True,
     'market_close': False,
     'break_start': False,
     'break_end': True,
     'pre': True,
     'post': False}
    )


To correct the calendar we should include the following:

.. code:: ipython3

    class OpenCloseDemo(InterruptionsDemo):
        
        open_close_map = {**CFEExchangeCalendar.open_close_map, 
                         "order_acceptance": True}  
    
    cal = OpenCloseDemo()
    
    sched = cal.schedule("2010-01-09", "2010-01-15", start= "order_acceptance", interruptions= True)
    sched




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>order_acceptance</th>
          <th>market_open</th>
          <th>market_close</th>
          <th>interruption_start_1</th>
          <th>interruption_end_1</th>
          <th>interruption_start_2</th>
          <th>interruption_end_2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2010-01-11</th>
          <td>2010-01-11 13:30:00+00:00</td>
          <td>2010-01-11 14:30:00+00:00</td>
          <td>2010-01-11 21:00:00+00:00</td>
          <td>2010-01-11 17:00:00+00:00</td>
          <td>2010-01-12 17:01:00+00:00</td>
          <td>NaT</td>
          <td>NaT</td>
        </tr>
        <tr>
          <th>2010-01-12</th>
          <td>2010-01-12 13:30:00+00:00</td>
          <td>2010-01-12 14:30:00+00:00</td>
          <td>2010-01-12 21:00:00+00:00</td>
          <td>NaT</td>
          <td>NaT</td>
          <td>NaT</td>
          <td>NaT</td>
        </tr>
        <tr>
          <th>2010-01-13</th>
          <td>2010-01-13 13:30:00+00:00</td>
          <td>2010-01-13 14:30:00+00:00</td>
          <td>2010-01-13 21:00:00+00:00</td>
          <td>2010-01-13 15:59:00+00:00</td>
          <td>2010-01-13 16:00:00+00:00</td>
          <td>2010-01-13 16:29:00+00:00</td>
          <td>2010-01-13 16:30:00+00:00</td>
        </tr>
        <tr>
          <th>2010-01-14</th>
          <td>2010-01-14 13:30:00+00:00</td>
          <td>2010-01-14 14:30:00+00:00</td>
          <td>2010-01-14 21:00:00+00:00</td>
          <td>NaT</td>
          <td>NaT</td>
          <td>NaT</td>
          <td>NaT</td>
        </tr>
        <tr>
          <th>2010-01-15</th>
          <td>2010-01-15 13:30:00+00:00</td>
          <td>2010-01-15 14:30:00+00:00</td>
          <td>2010-01-15 21:00:00+00:00</td>
          <td>NaT</td>
          <td>NaT</td>
          <td>NaT</td>
          <td>NaT</td>
        </tr>
      </tbody>
    </table>
    </div>



Now we can see that not only interruptions (last two) but also
order_acceptance (first) is respected

.. code:: ipython3

    is_open(cal, sched, "2010-01-11 13:35:00", "2010-01-12 14:35:00", "2010-01-13 15:59:00", "2010-01-13 16:30:00")


.. parsed-literal::

    open on 2010-01-11 13:35:00 : True
    open on 2010-01-12 14:35:00 : True
    open on 2010-01-13 15:59:00 : False
    open on 2010-01-13 16:30:00 : True


You can even change this dynamically, using the ``opens`` keyword in
``.change_time`` and ``.add_time``

.. code:: ipython3

    cal.change_time("order_acceptance", cal["order_acceptance"], opens= False)
    
    is_open(cal, sched, "2010-01-11 13:35:00", "2010-01-12 14:35:00", "2010-01-13 15:59:00", "2010-01-13 16:30:00")


.. parsed-literal::

    open on 2010-01-11 13:35:00 : False
    open on 2010-01-12 14:35:00 : True
    open on 2010-01-13 15:59:00 : False
    open on 2010-01-13 16:30:00 : True


.. code:: ipython3

    cal.change_time("order_acceptance", cal["order_acceptance"], opens= True)
    
    cal.add_time("order_closed", time(8), opens= False)
    
    sched = cal.schedule("2010-01-09", "2010-01-15", start= "order_acceptance")
    sched




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>order_acceptance</th>
          <th>order_closed</th>
          <th>market_open</th>
          <th>market_close</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2010-01-11</th>
          <td>2010-01-11 13:30:00+00:00</td>
          <td>2010-01-11 14:00:00+00:00</td>
          <td>2010-01-11 14:30:00+00:00</td>
          <td>2010-01-11 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2010-01-12</th>
          <td>2010-01-12 13:30:00+00:00</td>
          <td>2010-01-12 14:00:00+00:00</td>
          <td>2010-01-12 14:30:00+00:00</td>
          <td>2010-01-12 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2010-01-13</th>
          <td>2010-01-13 13:30:00+00:00</td>
          <td>2010-01-13 14:00:00+00:00</td>
          <td>2010-01-13 14:30:00+00:00</td>
          <td>2010-01-13 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2010-01-14</th>
          <td>2010-01-14 13:30:00+00:00</td>
          <td>2010-01-14 14:00:00+00:00</td>
          <td>2010-01-14 14:30:00+00:00</td>
          <td>2010-01-14 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2010-01-15</th>
          <td>2010-01-15 13:30:00+00:00</td>
          <td>2010-01-15 14:00:00+00:00</td>
          <td>2010-01-15 14:30:00+00:00</td>
          <td>2010-01-15 21:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    is_open(cal, sched, "2010-01-11 13:35:00", "2010-01-11 14:15:00", "2010-01-11 14:35:00")


.. parsed-literal::

    open on 2010-01-11 13:35:00 : True
    open on 2010-01-11 14:15:00 : False
    open on 2010-01-11 14:35:00 : True


Extra Usage
===========

Checking for special times
--------------------------

*The following functions respect varying times in regular_market_times*

These will only check market_close/market_open columns for early/late
times

.. code:: ipython3

    options.early_closes(schedule), options.late_opens(schedule)




.. parsed-literal::

    (Empty DataFrame
     Columns: [order_acceptance, market_open, market_close]
     Index: [],
     Empty DataFrame
     Columns: [order_acceptance, market_open, market_close]
     Index: [])



The ``is_different`` method uses the name of the series passed to it, to
determine which rows are not equal to the regular market times, and
return a boolean Series

.. code:: ipython3

    schedule[options.is_different(schedule["order_acceptance"])]




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>order_acceptance</th>
          <th>market_open</th>
          <th>market_close</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2000-12-27</th>
          <td>2000-12-27 14:30:00+00:00</td>
          <td>2000-12-27 14:30:00+00:00</td>
          <td>2000-12-27 21:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



You can also pass ``pd.Series.lt/ -.gt / -.ge / etc.`` for more control
over the comparison

.. code:: ipython3

    schedule[options.is_different(schedule["order_acceptance"], pd.Series.lt)]




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>order_acceptance</th>
          <th>market_open</th>
          <th>market_close</th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    schedule[options.is_different(schedule["order_acceptance"], pd.Series.ge)]




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>order_acceptance</th>
          <th>market_open</th>
          <th>market_close</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2000-12-22</th>
          <td>2000-12-22 13:30:00+00:00</td>
          <td>2000-12-22 14:30:00+00:00</td>
          <td>2000-12-22 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2000-12-26</th>
          <td>2000-12-26 13:30:00+00:00</td>
          <td>2000-12-26 14:30:00+00:00</td>
          <td>2000-12-26 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2000-12-27</th>
          <td>2000-12-27 14:30:00+00:00</td>
          <td>2000-12-27 14:30:00+00:00</td>
          <td>2000-12-27 21:00:00+00:00</td>
        </tr>
        <tr>
          <th>2000-12-28</th>
          <td>2000-12-28 13:30:00+00:00</td>
          <td>2000-12-28 14:30:00+00:00</td>
          <td>2000-12-28 21:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



Checking custom times
~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    options.has_custom # order_acceptance is not considered custom because it is hardcoded into the class




.. parsed-literal::

    False



.. code:: ipython3

    options.add_time("post", time(17))

.. code:: ipython3

    options.has_custom, options.is_custom("market_open"), options.is_custom("post")




.. parsed-literal::

    (True, False, True)



Get the regular time on a certain date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    nyse.open_time, nyse.close_time  # these always refer to the current time of market_open/market_close




.. parsed-literal::

    (datetime.time(9, 30, tzinfo=<DstTzInfo 'America/New_York' LMT-1 day, 19:04:00 STD>),
     datetime.time(16, 0, tzinfo=<DstTzInfo 'America/New_York' LMT-1 day, 19:04:00 STD>))



.. code:: ipython3

    nyse.get_time("post"), nyse.get_time("pre")  # these also refer to the current time 




.. parsed-literal::

    (datetime.time(20, 0, tzinfo=<DstTzInfo 'America/New_York' LMT-1 day, 19:04:00 STD>),
     datetime.time(4, 0, tzinfo=<DstTzInfo 'America/New_York' LMT-1 day, 19:04:00 STD>))



.. code:: ipython3

    # open_time_on looks for market_open, close_time_on looks for market_close and get_time_on looks for the provided market time
    nyse.open_time_on("1950-01-01"), nyse.get_time_on("market_close", "1960-01-01") 




.. parsed-literal::

    (datetime.time(10, 0, tzinfo=<DstTzInfo 'America/New_York' LMT-1 day, 19:04:00 STD>),
     datetime.time(15, 30, tzinfo=<DstTzInfo 'America/New_York' LMT-1 day, 19:04:00 STD>))



Special Methods
~~~~~~~~~~~~~~~

.. code:: ipython3

    nyse["market_open"] # gets the current time




.. parsed-literal::

    datetime.time(9, 30, tzinfo=<DstTzInfo 'America/New_York' LMT-1 day, 19:04:00 STD>)



.. code:: ipython3

    nyse["market_open", "all"] # gets all times




.. parsed-literal::

    ((None, datetime.time(10, 0)), ('1985-01-01', datetime.time(9, 30)))



.. code:: ipython3

    nyse["market_open", "1950-01-01"] # gets the time on a certain date




.. parsed-literal::

    datetime.time(10, 0, tzinfo=<DstTzInfo 'America/New_York' LMT-1 day, 19:04:00 STD>)



This tries to *add* a time, which will fail if it already exists. In
that case ``.change_time`` is the explicit alternative.

.. code:: ipython3

    nyse["new_post"] = time(20)  
    nyse["new_post"]




.. parsed-literal::

    datetime.time(20, 0, tzinfo=<DstTzInfo 'America/New_York' LMT-1 day, 19:04:00 STD>)



.. code:: ipython3

    try: nyse["post"] = time(19)
    except AssertionError as e: print(e)


.. parsed-literal::

    post is already in regular_market_times:
    ['pre', 'market_open', 'market_close', 'post', 'new_post']


Array of special times
~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    options.special_dates("order_acceptance", "2000-12-22", "2001-12-28")




.. parsed-literal::

    2000-12-27   2000-12-27 14:30:00+00:00
    2001-12-27   2001-12-27 14:30:00+00:00
    dtype: datetime64[ns, UTC]



Handling discontinued times
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    xkrx = mcal.get_calendar("XKRX")


.. parsed-literal::

    /opt/hostedtoolcache/Python/3.10.9/x64/lib/python3.10/site-packages/pandas_market_calendars/market_calendar.py:144: UserWarning: ['break_start', 'break_end'] are discontinued, the dictionary `.discontinued_market_times` has the dates on which these were discontinued. The times as of those dates are incorrect, use .remove_time(market_time) to ignore a market_time.
      warnings.warn(f"{list(discontinued.keys())} are discontinued, the dictionary"


.. code:: ipython3

    xkrx.schedule("2020-01-01", "2020-01-05")




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>market_open</th>
          <th>break_start</th>
          <th>break_end</th>
          <th>market_close</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2020-01-02</th>
          <td>2020-01-02 00:00:00+00:00</td>
          <td>2020-01-02 03:00:00+00:00</td>
          <td>2020-01-02 04:00:00+00:00</td>
          <td>2020-01-02 06:30:00+00:00</td>
        </tr>
        <tr>
          <th>2020-01-03</th>
          <td>2020-01-03 00:00:00+00:00</td>
          <td>2020-01-03 03:00:00+00:00</td>
          <td>2020-01-03 04:00:00+00:00</td>
          <td>2020-01-03 06:30:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    xkrx.discontinued_market_times # these are the dates as of which the market time didn't exist anymore




.. parsed-literal::

    ProtectedDict({'break_start': Timestamp('2000-05-22 00:00:00'), 'break_end': Timestamp('2000-05-22 00:00:00')})



.. code:: ipython3

    print(xkrx.has_discontinued)
    xkrx.remove_time("break_start")
    xkrx.remove_time("break_end")
    print(xkrx.has_discontinued)


.. parsed-literal::

    True
    False


.. code:: ipython3

    xkrx.schedule("2020-01-01", "2020-01-05")




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
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
          <th>2020-01-02</th>
          <td>2020-01-02 00:00:00+00:00</td>
          <td>2020-01-02 06:30:00+00:00</td>
        </tr>
        <tr>
          <th>2020-01-03</th>
          <td>2020-01-03 00:00:00+00:00</td>
          <td>2020-01-03 06:30:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



Helpers
=======

*schedules with columns other than market_open, break_start, break_end
or market_close are not yet supported by the following functions*

Date Range
----------

This function will take a schedule DataFrame and return a DatetimeIndex
with all timestamps at the frequency given for all of the exchange open
dates and times.

.. code:: ipython3

    mcal.date_range(early, frequency='1D')




.. parsed-literal::

    DatetimeIndex(['2012-07-02 20:00:00+00:00', '2012-07-03 17:00:00+00:00',
                   '2012-07-05 20:00:00+00:00', '2012-07-06 20:00:00+00:00',
                   '2012-07-09 20:00:00+00:00', '2012-07-10 20:00:00+00:00'],
                  dtype='datetime64[ns, UTC]', freq=None)



.. code:: ipython3

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



Merge schedules
---------------

.. code:: ipython3

    # NYSE Calendar
    nyse = mcal.get_calendar('NYSE')
    schedule_nyse = nyse.schedule('2015-12-20', '2016-01-06')
    schedule_nyse




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
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



.. code:: ipython3

    # LSE Calendar
    lse = mcal.get_calendar('LSE')
    schedule_lse = lse.schedule('2015-12-20', '2016-01-06')
    schedule_lse




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
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

.. code:: ipython3

    mcal.merge_schedules(schedules=[schedule_nyse, schedule_lse], how='inner')




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
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

.. code:: ipython3

    mcal.merge_schedules(schedules=[schedule_nyse, schedule_lse], how='outer')




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
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



Use holidays in numpy
---------------------

This will use your exchange calendar in numpy to add business days

.. code:: ipython3

    import numpy as np
    cme = mcal.get_calendar("CME_Agriculture")
    np.busday_offset(dates="2020-05-22", holidays=cme.holidays().holidays, offsets=1)




.. parsed-literal::

    numpy.datetime64('2020-05-26')



Trading Breaks
--------------

Some markets have breaks in the day, like the CME Equity Futures markets
which are closed from 4:15 - 4:35 (NY) daily. These calendars will have
additional columns in the schedule() DataFrame

.. code:: ipython3

    cme = mcal.get_calendar('CME_Equity')
    schedule = cme.schedule('2020-01-01', '2020-01-04')
    schedule




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>market_open</th>
          <th>break_start</th>
          <th>break_end</th>
          <th>market_close</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2020-01-02</th>
          <td>2020-01-01 23:00:00+00:00</td>
          <td>2020-01-02 21:15:00+00:00</td>
          <td>2020-01-02 21:30:00+00:00</td>
          <td>2020-01-02 22:00:00+00:00</td>
        </tr>
        <tr>
          <th>2020-01-03</th>
          <td>2020-01-02 23:00:00+00:00</td>
          <td>2020-01-03 21:15:00+00:00</td>
          <td>2020-01-03 21:30:00+00:00</td>
          <td>2020-01-03 22:00:00+00:00</td>
        </tr>
      </tbody>
    </table>
    </div>



The date_range() properly accounts for the breaks

.. code:: ipython3

    mcal.date_range(schedule, '5H')




.. parsed-literal::

    DatetimeIndex(['2020-01-02 04:00:00+00:00', '2020-01-02 09:00:00+00:00',
                   '2020-01-02 14:00:00+00:00', '2020-01-02 19:00:00+00:00',
                   '2020-01-02 21:15:00+00:00', '2020-01-02 22:00:00+00:00',
                   '2020-01-03 04:00:00+00:00', '2020-01-03 09:00:00+00:00',
                   '2020-01-03 14:00:00+00:00', '2020-01-03 19:00:00+00:00',
                   '2020-01-03 21:15:00+00:00', '2020-01-03 22:00:00+00:00'],
                  dtype='datetime64[ns, UTC]', freq=None)



