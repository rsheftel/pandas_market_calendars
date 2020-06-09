New Market or Exchange
======================
To create a new exchange (or OTC market):

#. Create a new class that inherits from MarketCalendar
#. In the new class create the following class attributes (variables):

   #. aliases = [...]
   #. open_time_default = datetime.time(...)
   #. close_time_default = datetime.time(...)
   #. regular_early_close = datetime.time(...)

#. Define the following property methods:

   #. name
   #. tz (time zone)

#. Now optionally define any of the following property methods:

   #. Days where the market is fully closed:

      #. regular_holidays - returns an pandas AbstractHolidayCalendar object
      #. adhoc_holidays - returns a list of pandas Timestamp of a DatetimeIndex

   #. Days where the market closes early:

      #. special_closes - returns a list of tuples. The tuple is (datetime.time of close, AbstractHolidayCalendar)
      #. special_closes_adhoc - returns a list of tuples. The tuple is (datetime.time of close, list of date strings)

   #. Days where the market opens late:

      #. special_opens - returns a list of tuples. The tuple is (datetime.time of open, AbstractHolidayCalendar)
      #. special_opens_adhoc - returns a list of tuples. The tuple is (datetime.time of open, list of date strings)

#. Import your new calendar class in `calendar_registry.py`:

.. code:: python

   from .exchange_calendar_xxx import XXXExchangeCalendar
