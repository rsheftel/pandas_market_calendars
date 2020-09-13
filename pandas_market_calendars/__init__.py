# Fork of Zipline by Quantopian released under MIT license. Original Zipline license below.
#
# Copyright 2016 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pkg_resources

from .calendar_registry import get_calendar, get_calendar_names
from .calendar_utils import convert_freq, date_range, merge_schedules
# TODO: is the below needed? Can I replace all the imports on the calendars with ".market_calendar"
from .market_calendar import MarketCalendar

# if running in development there may not be a package
try:
    __version__ = pkg_resources.get_distribution('pandas_market_calendars').version
except pkg_resources.DistributionNotFound:
    __version__ = 'development'

__all__ = [
    'MarketCalendar',
    'get_calendar',
    'get_calendar_names',
    'merge_schedules',
    'date_range',
    'convert_freq'
]
