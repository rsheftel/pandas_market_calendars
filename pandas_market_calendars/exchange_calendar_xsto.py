from datetime import time

from pandas.tseries.holiday import AbstractHolidayCalendar, EasterMonday, GoodFriday, Holiday
from dateutil.relativedelta import FR

from .market_calendar import MarketCalendar

XSTONewYearsDay = Holiday(
    "New Year's Day",
    month = 1,
    day = 1
)

XSTOEpiphanyEve = Holiday(
    "Epiphany Eve",
    month = 1,
    day = 5
)

XSTOEpiphanyDay = Holiday(
    "Epiphany Day",
    month = 1,
    day = 6
)

XSTOMaundyThursday = Holiday(
    "Maundy Thursday",
    month = 1,
    day = 1,
    offset = [Easter(), Day(-3)]
)

XSTOGoodFriday = GoodFriday

XSTOEasterMonday = EasterMonday

XSTOWalpurgisNight = Holiday(
    "Walpurgis Night",
    month = 4,
    day = 30
)

XSTOWorkersDay = Holiday(
    "International Workers' Day",
    month = 5,
    day = 1
)

XSTOAscensionEve = Holiday(
    "Ascension Eve",
    month = 1,
    day = 1,
    offset = [Easter(), Day(38)]
)

XSTOAscensionDay = Holiday(
    "Ascension Day",
    month = 1,
    day = 1,
    offset = [Easter(), Day(39)]
)

XSTONationalDay = Holiday(
    "National Day",
    month = 6,
    day = 6
)

XSTOMidsummerEve = Holiday(
    "Midsummer Eve",
    month = 6,
    day = 25,
    offset = pd.DateOffset(weekday=FR(-1))
)

XSTOAllSaintsEve = Holiday(
    "All Saints' Eve",
    month = 11
    day = 5,
    offset = pd.DateOffset(weekday=FR(-1))
)

XSTOChristmasEve = Holiday(
    "Christmas Eve",
    month = 12,
    day = 24
)

XSTOChristmasDay = Holiday(
    "Christmas Day",
    month = 12,
    day = 25
)

XSTOBoxingDay = Holiday(
    "Boxing Day",
    month = 12,
    day = 26
)

XSTONewYearsEve = Holiday(
    "New Year's Eve"
    month = 12,
    day = 31
)

class XSTOExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for Stockholm Stock Exchange

    Opening times for the regular trading of equities
    Open Time: 9:00 AM, Europe/Stockholm
    Close Time: 5:30 PM, Europe/Stockholm
    """

    aliases = ['XSTO']
    regular_market_times = {
        "market_open": ((None, time(9)),),
        "market_close": ((None, time(17, 30)),)
    }

    @property
    def name(self):
        return "XSTO"

    @property
    def tz(self):
        return timezone("Europe/Stockholm")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            XSTONewYearsDay,
            XSTOEpiphanyDay,
            XSTOGoodFriday,
            XSTOEasterMonday,
            XSTOWorkersDay,
            XSTOAscensionDay,
            XSTONationalDay,
            XSTOMidsummerEve,
            XSTOChristmasEve,
            XSTOChristmasDay,
            XSTOBoxingDay,
            XSTONewYearsEve
        ])

    @property
    def special_closes(self):
        return [(
            time(13, 0, tzinfo=self.tz),
            AbstractHolidayCalendar(rules=[
                XSTOEpiphanyEve,
                XSTOMaundyThursday,
                XSTOWalpurgisNight,
                XSTOAscensionEve,
                XSTOAllSaintsEve
            ])
        )]
