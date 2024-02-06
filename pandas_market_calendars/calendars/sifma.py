from datetime import time

from pandas.tseries.holiday import AbstractHolidayCalendar
from pytz import timezone
from itertools import chain

########################################################################################################################
# SIFMA Financial Markets Calendar for US, UK, JP
#
# https://www.sifma.com/
#
# US: SIFMAUSExchangeCalendar() ['SIFMAUS', 'SIFMA_US', "Capital_Markets_US", "Financial_Markets_US", "Bond_Markets_US"]
# UK: SIFMAUKExchangeCalendar() ['SIFMAUK', 'SIFMA_UK', "Capital_Markets_UK", "Financial_Markets_UK", "Bond_Markets_UK"]
# JP: SIFMAJPExchangeCalendar() ['SIFMAJP', 'SIFMA_JP', "Capital_Markets_JP", "Financial_Markets_JP", "Bond_Markets_JP"]
#
# Trading Hours:
# US: 7:00 to 17:30
# UK: 8:00 to 17:00
# JP: 8:30 to 18:30
########################################################################################################################


from pandas_market_calendars.holidays.sifma import (
    # US Holidays
    USNewYearsDay,  # Not observed if a Saturday
    USNewYearsEve2pmEarlyClose,
    MartinLutherKingJr,
    USPresidentsDay,
    GoodFridayThru2020,
    DayBeforeGoodFriday2pmEarlyCloseThru2020,
    GoodFridayAdHoc,
    GoodFriday2pmEarlyCloseAdHoc,
    DayBeforeGoodFriday2pmEarlyCloseAdHoc,
    DayBeforeUSMemorialDay2pmEarlyClose,
    USMemorialDay,
    USJuneteenthAfter2022,
    USIndependenceDay,
    DayBeforeUSIndependenceDay2pmEarlyClose,
    ThursdayBeforeUSIndependenceDay2pmEarlyClose,
    USLaborDay,
    USColumbusDay,
    USVeteransDay2022,
    USVeteransDay,
    USThanksgivingDay,
    DayAfterThanksgiving2pmEarlyClose,
    Christmas,
    ChristmasEve2pmEarlyClose,
    ChristmasEveThursday2pmEarlyClose,
    # UK Specific Holidays
    UKNewYearsDay,  # Saturdays observed on Monday
    UKGoodFriday,
    UKEasterMonday,
    UKMayDay,
    UKSpringBankAdHoc,  # Usually follows US Memorial Day but not always
    UKSummerBank,
    UKChristmas,
    UKChristmaEve,
    UKWeekendChristmas,  # Observed Tuesday when Boxing Day is on Monday
    UKBoxingDay,
    UKWeekendBoxingDay,
    UKPlatinumJubilee2022,
)
from pandas_market_calendars.market_calendar import MarketCalendar


########################################################################################################################
# SIFMA Financial Markets Calendar for US, UK, JP
#
# https://www.sifma.com/
#
# US: SIFMAUSExchangeCalendar() ['SIFMAUS', 'SIFMA_US', "Capital_Markets_US", "Financial_Markets_US", "Bond_Markets_US"]
# UK: SIFMAUKExchangeCalendar() ['SIFMAUK', 'SIFMA_UK', "Capital_Markets_UK", "Financial_Markets_UK", "Bond_Markets_UK"]
# JP: SIFMAJPExchangeCalendar() ['SIFMAJP', 'SIFMA_JP', "Capital_Markets_JP", "Financial_Markets_JP", "Bond_Markets_JP"]
#
# Trading Hours:
# US: 7:00 to 17:30
# UK: 8:00 to 17:00
# JP: 8:30 to 18:30
########################################################################################################################

# AbstractHolidayCalendar.start_date = '1998-01-01'

############################################################
# US
############################################################


class SIFMAUSExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for SIFMA United States

    https://www.sifma.org/resources/general/holiday-schedule/#US

    """

    aliases = [
        "SIFMAUS",
        "SIFMA_US",
        "Capital_Markets_US",
        "Financial_Markets_US",
        "Bond_Markets_US",
    ]

    regular_market_times = {
        "market_open": ((None, time(7)),),
        "market_close": ((None, time(17, 30)),),
    }

    @property
    def name(self):
        return "SIFMA_US"

    @property
    def tz(self):
        return timezone("America/New_York")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                MartinLutherKingJr,
                USPresidentsDay,
                GoodFridayThru2020,
                USMemorialDay,
                USJuneteenthAfter2022,
                USIndependenceDay,
                USLaborDay,
                USColumbusDay,
                USVeteransDay2022,
                USVeteransDay,
                USThanksgivingDay,
                Christmas,
            ]
        )

    @property
    def adhoc_holidays(self):
        return list(
            chain(
                GoodFridayAdHoc,
            )
        )

    @property
    def special_closes(self):
        return [
            (
                time(14),
                AbstractHolidayCalendar(
                    rules=[
                        DayBeforeGoodFriday2pmEarlyCloseThru2020,
                        DayBeforeUSMemorialDay2pmEarlyClose,
                        DayBeforeUSIndependenceDay2pmEarlyClose,
                        ThursdayBeforeUSIndependenceDay2pmEarlyClose,
                        DayAfterThanksgiving2pmEarlyClose,
                        ChristmasEve2pmEarlyClose,
                        ChristmasEveThursday2pmEarlyClose,
                        USNewYearsEve2pmEarlyClose,
                    ]
                ),
            )
        ]

    @property
    def special_closes_adhoc(self):
        return [
            (
                time(14, tzinfo=timezone("America/New_York")),
                GoodFriday2pmEarlyCloseAdHoc  # list
                + DayBeforeGoodFriday2pmEarlyCloseAdHoc,
            ),
        ]


############################################################
# UK
############################################################


class SIFMAUKExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for SIFMA United Kingdom

    https://www.sifma.org/resources/general/holiday-schedule/#UK

    """

    aliases = [
        "SIFMAUK",
        "SIFMA_UK",
        "Capital_Markets_UK",
        "Financial_Markets_UK",
        "Bond_Markets_UK",
    ]

    regular_market_times = {
        "market_open": ((None, time(8)),),
        "market_close": ((None, time(17)),),
    }

    @property
    def name(self):
        return "SIFMA_UK"

    @property
    def tz(self):
        return timezone("Europe/London")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                UKNewYearsDay,
                MartinLutherKingJr,
                USPresidentsDay,
                UKGoodFriday,
                UKEasterMonday,
                UKMayDay,
                USMemorialDay,
                USJuneteenthAfter2022,
                USIndependenceDay,
                UKSummerBank,
                USLaborDay,
                USColumbusDay,
                USVeteransDay2022,
                USVeteransDay,
                USThanksgivingDay,
                UKChristmas,
                UKChristmaEve,
                UKWeekendChristmas,
                UKBoxingDay,
                UKWeekendBoxingDay,
            ]
        )

    @property
    def adhoc_holidays(self):
        return list(
            chain(
                UKSpringBankAdHoc,
                UKPlatinumJubilee2022,
            )
        )


############################################################
# Japan
############################################################
from pandas_market_calendars.holidays.jp import (
    JapanComingOfAgeDay,
    JapanNationalFoundationDay,
    JapanEmperorsBirthday,
    JapanVernalEquinox,
    JapanShowaDay,
    JapanConstitutionMemorialDay,
    JapanGreeneryDay,
    JapanChildrensDay,
    JapanMarineDay,
    JapanMountainDay,
    JapanRespectForTheAgedDay,
    JapanAutumnalEquinox,
    JapanHealthAndSportsDay2000To2019,
    JapanSportsDay2020,
    JapanSportsDay,
    JapanCultureDay,
    JapanLaborThanksgivingDay,
)


class SIFMAJPExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for SIFMA Japan

    https://www.sifma.org/resources/general/holiday-schedule/#JP

    """

    aliases = [
        "SIFMAJP",
        "SIFMA_JP",
        "Capital_Markets_JP",
        "Financial_Markets_JP",
        "Bond_Markets_JP",
    ]

    regular_market_times = {
        "market_open": ((None, time(8, 30)),),
        "market_close": ((None, time(18, 30)),),
    }

    @property
    def name(self):
        return "SIFMA_JP"

    @property
    def tz(self):
        return timezone("Asia/Tokyo")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                UKNewYearsDay,
                JapanComingOfAgeDay,
                MartinLutherKingJr,
                JapanNationalFoundationDay,
                USPresidentsDay,
                JapanEmperorsBirthday,
                JapanVernalEquinox,
                UKGoodFriday,
                UKEasterMonday,
                JapanShowaDay,
                JapanConstitutionMemorialDay,
                JapanGreeneryDay,
                JapanChildrensDay,
                USMemorialDay,
                USJuneteenthAfter2022,
                USIndependenceDay,
                JapanMarineDay,
                JapanMountainDay,
                UKSummerBank,
                USLaborDay,
                JapanRespectForTheAgedDay,
                JapanAutumnalEquinox,
                JapanSportsDay,
                JapanSportsDay2020,
                JapanHealthAndSportsDay2000To2019,
                JapanCultureDay,
                USVeteransDay2022,
                USVeteransDay,
                JapanLaborThanksgivingDay,
                USThanksgivingDay,
                UKChristmas,
                UKChristmaEve,
                UKBoxingDay,
                UKWeekendBoxingDay,
            ]
        )

    @property
    def adhoc_holidays(self):
        return list(
            chain(
                UKSpringBankAdHoc,
                UKPlatinumJubilee2022,
            )
        )

    @property
    def special_closes(self):
        return [
            (time(15), AbstractHolidayCalendar(rules=[UKMayDay, UKWeekendChristmas]))
        ]
