from datetime import time
import functools

import pandas as pd
from pandas.tseries.holiday import AbstractHolidayCalendar
from zoneinfo import ZoneInfo
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
    # --- Good Friday Rules --- #
    is_first_friday,
    GoodFridayThru2020,
    DayBeforeGoodFriday2pmEarlyCloseThru2020,
    GoodFridayPotentialPost2020,  # Potential dates, filtered later
    DayBeforeGoodFridayPotentialPost2020,  # Potential dates, filtered later
    # --- End Good Friday Rules --- #
    DayBeforeUSMemorialDay2pmEarlyClose,
    USMemorialDay,
    USJuneteenthAfter2022,
    USIndependenceDay,
    DayBeforeUSIndependenceDay2pmEarlyClose,
    ThursdayBeforeUSIndependenceDay2pmEarlyClose,
    USLaborDay,
    USColumbusDay,
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
    def full_name(self):
        return "Securities Industry and Financial Markets Association"

    @property
    def tz(self):
        return ZoneInfo("America/New_York")

    # Helper method to calculate and cache dynamic dates
    @functools.lru_cache()
    def _get_dynamic_gf_rules(self):
        # Calculate rules for a wide fixed range to avoid arbitrary cutoffs
        # while preventing infinite generation. 1970-2100 is a reasonable range.
        calc_start = pd.Timestamp("1970-01-01")
        calc_end = pd.Timestamp("2100-12-31")

        # Filter potential dates based on the start_date of the underlying Holiday rules
        gf_rule_start = GoodFridayPotentialPost2020.start_date
        thurs_rule_start = DayBeforeGoodFridayPotentialPost2020.start_date

        # Ensure calculation range respects the rule start dates
        effective_gf_start = max(calc_start, gf_rule_start) if gf_rule_start else calc_start
        effective_thurs_start = max(calc_start, thurs_rule_start) if thurs_rule_start else calc_start

        potential_gf_dates = GoodFridayPotentialPost2020.dates(effective_gf_start, calc_end)
        gf_full_holidays = [d for d in potential_gf_dates if not is_first_friday(d)]
        gf_12pm_early_closes = [d for d in potential_gf_dates if is_first_friday(d)]

        potential_thurs_dates = DayBeforeGoodFridayPotentialPost2020.dates(effective_thurs_start, calc_end)
        thurs_before_gf_2pm_early_closes = [
            thurs for thurs in potential_thurs_dates if not is_first_friday(thurs + pd.Timedelta(days=1))
        ]
        return gf_full_holidays, gf_12pm_early_closes, thurs_before_gf_2pm_early_closes

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
                USVeteransDay,
                USThanksgivingDay,
                Christmas,
            ]
        )

    @property
    def adhoc_holidays(self):
        gf_full_holidays, _, _ = self._get_dynamic_gf_rules()
        return gf_full_holidays

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
        _, gf_12pm_early_closes, thurs_before_gf_2pm_early_closes = self._get_dynamic_gf_rules()
        return [
            (
                time(12), # SIFMA rule specifies 12:00 PM ET
                gf_12pm_early_closes,
            ),
            (
                time(14), # SIFMA rule specifies 2:00 PM ET
                thurs_before_gf_2pm_early_closes,
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
        return ZoneInfo("Europe/London")

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
        return ZoneInfo("Asia/Tokyo")

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
        return [(time(15), AbstractHolidayCalendar(rules=[UKMayDay, UKWeekendChristmas]))]
