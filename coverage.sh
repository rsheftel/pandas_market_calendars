#!/bin/bash

# This only works in Cygwin on Windows

py3 -m pytest --color=yes --cov=pandas_exchange_calendars --cov-report html
cygstart $TEMP/pec_coverage_report/index.html
