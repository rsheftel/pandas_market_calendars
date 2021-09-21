from datetime import time

from pandas.tseries.holiday import AbstractHolidayCalendar, EasterMonday, GoodFriday, Holiday
from pandas.tseries.offsets import Day, Easter
from pytz import timezone

from .market_calendar import MarketCalendar

OSENewYearsDay = Holiday(
    "New Year's Day",
    month=1,
    day=1
)

OSEWednesdayBeforeEaster = Holiday(
    "Wednesday before Easter",
    month=1,
    day=1,
    offset=[Easter(), Day(-4)]

)

OSEMaundyThursday = Holiday(
    "Maundy Thursday",
    month=1,
    day=1,
    offset=[Easter(), Day(-3)]
)

OSEGoodFriday = GoodFriday

OSEEasterMonday = EasterMonday

OSELabourDay = Holiday(
    "Labour Day",
    month=5,
    day=1
)

OSEConstitutionDay = Holiday(
    "Constitution Day",
    month=5,
    day=17
)

OSEWhitMonday = Holiday(
    "Whit Monday",
    month=1,
    day=1,
    offset=[Easter(), Day(50)]
)

OSEAscensionDay = Holiday(
    "Ascension Day",
    month=1,
    day=1,
    offset=[Easter(), Day(39)]
)

OSEChristmasEve = Holiday(
    "Christmas Eve",
    month=12,
    day=24,
)

OSEChristmasDay = Holiday(
    "Christmas Day",
    month=12,
    day=25
)

OSEBoxingDay = Holiday(
    "Boxing Day",
    month=12,
    day=26
)

OSENewYearsEve = Holiday(
    "New Year's Eve",
    month=12,
    day=31
)


class OSEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for Oslo Stock Exchange

    Note these dates are only checked against 2017, 2018 and 2019
    https://www.oslobors.no/ob_eng/Oslo-Boers/About-Oslo-Boers/Opening-hours

    Opening times for the regular trading of equities (not including closing auction call)
    Open Time: 9:00 AM, CEST/EST
    Close Time: 4:20 PM, CEST/EST

    Regularly-Observed Holidays (not necessarily in order):
    - New Years Day
    - Wednesday before Easter (Half trading day)
    - Maundy Thursday
    - Good Friday
    - Easter Monday
    - Labour Day
    - Ascension Day
    - Constitution Day
    - Whit Monday
    - Christmas Eve
    - Christmas Day
    - Boxing Day
    - New Year's Eve
    """

    aliases = ['OSE']
    regular_market_times = {
        "market_open": ((None, time(9)),),
        "market_close": ((None, time(16,20)),)
    }

    @property
    def name(self):
        return "OSE"

    @property
    def tz(self):
        return timezone("Europe/Oslo")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            OSENewYearsDay,
            OSEMaundyThursday,
            OSEGoodFriday,
            OSEEasterMonday,
            OSELabourDay,
            OSEConstitutionDay,
            OSEWhitMonday,
            OSEAscensionDay,
            OSEChristmasEve,
            OSEChristmasDay,
            OSEBoxingDay,
            OSENewYearsEve
        ])

    @property
    def special_closes(self):
        return [(
            time(13, 0, tzinfo=self.tz),
            AbstractHolidayCalendar(rules=[
                OSEWednesdayBeforeEaster
            ])
        )]
