New Market or Exchange
======================
*See examples/usage.ipynb for demonstrations*

To create a new exchange (or OTC market):

#. Create a new class that inherits from MarketCalendar

#. Set the class attribute `aliases: [...]` for accessing the calendar through `mcal.get_calendar`

#. Create the `regular_market_times` class attribute, meeting these requirements:

   #. It needs to be a dictionary

   #. Each market_time needs one entry

      #. Regular open must be "market_open", regular close must be "market_close".
      #. If there is a break, there must be a "break_start" and a "break_end".
      #. only ONE break is currently supported.

   #. One list/tuple for each market_time, containing at least one list/tuple:

      #. Each nested iterable needs at least two items: `(first_date_used, time[, offset])`.
      #. The first iterable's date should be None, marking the start. In every iterable thereafter this is the date when `time` was first used.
      #. Optionally (assumed to be zero, when not present), a positive or negative integer, representing an offset in number of days.
      #. Dates need to be in ascending order, None coming first.


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

   #. Set special times for any market_time in regular_market_times, by setting a property in this format:

      #. special_{market_time}_adhoc
            same format as special_opens_adhoc, which is the same as special_market_open_adhoc
      #. special_{market_time}
           same format as special_opens, which is the same as special_market_open



#. Import your new calendar class in `calendar_registry.py`:

.. code:: python

   from .exchange_calendar_xxx import XXXExchangeCalendar
