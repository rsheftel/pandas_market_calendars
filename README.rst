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
Raccoon is a lightweight DataFrame implementation inspired by the phenomenal Pandas package for the one use case
where Pandas is known to be sub-optimal: DataFrames that grow in size by rows frequently in the code. Additionally
Raccoon DataFrames can be parametrized to be sorted so that additions to the DataFrame keep the index in sorted order
to speed inserts and retrievals.

Inspiration
-----------
Pandas DataFrames are excellent multi-purpose data structures for data management and analysis. One of the use cases
I had was to use DataFrames as a type of in-memory database table. The issue was that this required lots of growing
the rows of the DataFrame, something that is known to be slow in Pandas. The reason it is slow in Pandas is that the
underlying data structure is numpy which does a complete copy of the data when the size of the array grows.

Limited Functionality
---------------------
Raccoon implements what is needed to use the DataFrame as an in memory store of index and column data structure
supporting simple and tuple indexes to mimic the hierarchical indexes of Pandas. The methods included are primarily
about setting values of the data frame, growing and appending the data frame and getting values from the data frame.
The raccoon DataFrame is not intended for math operations like pandas and only limited basic math methods are included.

Why Raccoon?
------------
According to wikipedia some scientists believe the panda is related to the raccoon

Future
------
This package serves the needs it was originally created for. Any future additions by myself will be driven by my own
needs, but it is completely open source to I encourage anyone to add on and expand.

My hope is that one day Pandas solves the speed problem with growing DataFrames and this package becomes obsolete.
