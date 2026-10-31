from pandas.tseries.holiday import GoodFriday

import pandas_market_calendars as mcal
from pandas_market_calendars.calendars.cme import goodFridayOpen


# CME Globex trades on Good Friday only when the US jobs report falls on it. CME_Bond's goodFridayOpen list
# records those days, so every Globex calendar with a Good Friday session must agree with it.
def test_good_friday_matches_the_bond_calendar_from_2022():
    calendars = [
        mcal.get_calendar("CME Globex Fixed Income"),
        mcal.get_calendar("CME Globex Equity"),
        mcal.get_calendar("CMEGlobex_FX"),
        mcal.get_calendar("CME Globex Crypto"),
        mcal.get_calendar("CME_Equity"),
    ]
    good_fridays = GoodFriday.dates("2022-01-01", "2099-12-31")

    for calendar in calendars:
        sessions = calendar.schedule("2022-01-01", "2099-12-31").index
        for day in good_fridays:
            trades = day.strftime("%Y-%m-%d") in goodFridayOpen
            assert (day in sessions) == trades, f"{calendar.name} {day.date()}"
