import pandas as pd
from pandas.testing import assert_index_equal
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.bursa_malaysia import (
    BursaMalaysiaFCPOExchangeCalendar, BursaMalaysiaFKLIExchangeCalendar
)


def test_time_zone():
    assert BursaMalaysiaFCPOExchangeCalendar().tz == ZoneInfo("Asia/Kuala_Lumpur")
    assert BursaMalaysiaFKLIExchangeCalendar().tz == ZoneInfo("Asia/Kuala_Lumpur")



def test_june_hols():
    cal = BursaMalaysiaFCPOExchangeCalendar()
    sched_2026 = cal.schedule("2026-05-20", "2026-06-10")
    assert pd.Timestamp("2026-06-01") not in sched_2026.index.get_level_values(0)

    
