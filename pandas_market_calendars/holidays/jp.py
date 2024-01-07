from dateutil.relativedelta import MO
from pandas import DateOffset, Timestamp
from pandas.tseries.holiday import Holiday, sunday_to_monday

from pandas_market_calendars.holidays.jpx_equinox import (
    autumnal_citizen_dates,
    autumnal_equinox,
    vernal_equinox,
)

AscensionDays = [
    Timestamp("2019-04-30", tz="UTC"),  # National Holiday
    Timestamp("2019-05-01", tz="UTC"),  # Ascension Day
    Timestamp("2019-05-02", tz="UTC"),  # National Holiday
]

MarriageDays = [
    Timestamp("1959-04-10", tz="UTC"),  # Akihito
    Timestamp("1993-06-09", tz="UTC"),  # Naruhito
]

FuneralShowa = [
    Timestamp("1989-02-24", tz="UTC"),
]

EnthronementDays = [
    Timestamp("1990-11-12", tz="UTC"),  # Akihito
    Timestamp("2019-10-22", tz="UTC"),  # Naruhito
]

AutumnalCitizenDates = autumnal_citizen_dates()

NoN225IndexPrices = [
    # source:  https://indexes.nikkei.co.jp/en/nkave/archives/data
    # TODO: determine if these dates were also national holidays
    Timestamp("1951-02-15", tz="UTC"),
    Timestamp("1953-02-09", tz="UTC"),
    Timestamp("1954-10-26", tz="UTC"),
    Timestamp("1959-04-10", tz="UTC"),
]

EquityTradingSystemFailure = [
    # The Failure of Equity Trading System on October 1, 2020
    # source: https://www.jpx.co.jp/english/corporate/news/news-releases/0060/20201019-01.html
    Timestamp("2020-10-01", tz="UTC"),
]

JapanNewYearsDay2 = Holiday(
    name="New Year's Day",
    month=1,
    day=2,
    observance=sunday_to_monday,
)

JapanNewYearsDay3 = Holiday(
    name="New Year's Day",
    month=1,
    day=3,
)

JapanComingOfAgeDay1951To1973 = Holiday(
    name="Coming of Age Day",
    month=1,
    day=15,
    start_date=Timestamp(1951, 1, 1),
    end_date=Timestamp(1973, 12, 31),
)

JapanComingOfAgeDay1974To1999 = Holiday(
    name="Coming of Age Day",
    month=1,
    day=15,
    start_date=Timestamp(1974, 1, 1),
    end_date=Timestamp(1999, 12, 31),
    observance=sunday_to_monday,
)

JapanComingOfAgeDay = Holiday(  # second monday of january
    name="Coming of Age Day",
    month=1,
    day=1,
    start_date=Timestamp(2000, 1, 1),
    offset=DateOffset(weekday=MO(2)),
)

JapanNationalFoundationDay1969To1973 = Holiday(
    name="National Foundation Day",
    month=2,
    day=11,
    start_date=Timestamp(1969, 1, 1),  # also held 1872 to 1948 as Kigen-setsu
    end_date=Timestamp(1973, 12, 31),
)

JapanNationalFoundationDay = Holiday(
    name="National Foundation Day",
    month=2,
    day=11,
    start_date=Timestamp(1974, 1, 1),
    observance=sunday_to_monday,
)

JapanEmperorsBirthday = Holiday(
    name="The Emperor's Birthday",
    month=2,
    day=23,
    start_date=Timestamp(2020, 1, 1),
    observance=sunday_to_monday,
)

JapanVernalEquinox = Holiday(
    name="Vernal Equinox", month=3, day=20, observance=vernal_equinox
)

JapanShowaDayUntil1972 = Holiday(
    name="Showa Day",
    month=4,
    day=29,
    end_date=Timestamp(1972, 12, 31),  # 1965
)

JapanShowaDay = Holiday(
    name="Showa Day",
    month=4,
    day=29,
    start_date=Timestamp(1973, 1, 1),
    observance=sunday_to_monday,
)

JapanConstitutionMemorialDayUntil1972 = Holiday(
    name="Constitution Memorial Day",
    month=5,
    day=3,
    start_date=Timestamp(1948, 1, 1),
    end_date=Timestamp(1972, 12, 31),
)

JapanConstitutionMemorialDay = Holiday(
    name="Constitution Memorial Day",
    month=5,
    day=3,
    start_date=Timestamp(1973, 1, 1),
    observance=sunday_to_monday,
)

JapanGreeneryDay = Holiday(
    name="Greenery Day",  # prior to 1985 was a Citizen's Day
    month=5,
    day=4,
    start_date=Timestamp(1985, 1, 1),
    observance=sunday_to_monday,
)

JapanChildrensDayUntil1972 = Holiday(
    name="Children's Day",
    month=5,
    day=5,
    start_date=Timestamp(1948, 1, 1),
    end_date=Timestamp(1972, 12, 31),
)

JapanChildrensDay = Holiday(
    name="Children's Day",
    month=5,
    day=5,
    start_date=Timestamp(1973, 1, 1),
    observance=sunday_to_monday,
)

# starting in 2007, there can be a holiday on May 6 if May 3 or 4 falls on a Sunday
JapanGoldenWeekBonusDay = Holiday(
    name="Golden Week Bonus Day",
    month=5,
    day=6,
    start_date=Timestamp(2007, 1, 1),
    days_of_week=(1, 2),
)

JapanMarineDay1996To2002 = Holiday(
    name="Marine Day",
    month=7,
    day=20,
    start_date=Timestamp(1996, 1, 1),
    end_date=Timestamp(2002, 12, 31),
    observance=sunday_to_monday,
)

JapanMarineDay2003To2019 = Holiday(
    name="Marine Day",
    month=7,
    day=1,
    start_date=Timestamp(2003, 1, 1),
    end_date=Timestamp(2019, 12, 31),
    offset=DateOffset(weekday=MO(3)),
)

JapanMarineDay2020 = Holiday(
    name="Marine Day",  # shift for Olympics
    year=2020,
    month=7,
    day=23,
)

JapanMarineDay2021 = Holiday(
    name="Marine Day",
    # shift for Olympics (Olympics and Paralympics postponed until 2021 due to the COVID-19 pandemic)
    year=2021,
    month=7,
    day=22,
)

JapanMarineDay = Holiday(
    name="Marine Day",
    month=7,
    day=1,
    start_date=Timestamp(2022, 1, 1),
    offset=DateOffset(weekday=MO(3)),
)

JapanMountainDay2016to2019 = Holiday(
    name="Mountain Day",
    month=8,
    day=11,
    start_date=Timestamp(2016, 1, 1),
    end_date=Timestamp(2019, 12, 31),
    observance=sunday_to_monday,
)

JapanMountainDay2020 = Holiday(
    name="Mountain Day",  # shift for Olympics
    year=2020,
    month=8,
    day=10,
)

JapanMountainDay2021 = Holiday(
    name="Mountain Day",
    # shift for Olympics (Olympics and Paralympics postponed until 2021 due to the COVID-19 pandemic)
    year=2021,
    month=8,
    day=8,
)

JapanMountainDay2021NextDay = Holiday(
    name="Mountain Day",
    # shift for Olympics (Olympics and Paralympics postponed until 2021 due to the COVID-19 pandemic)
    year=2021,
    month=8,
    day=9,
)

JapanMountainDay = Holiday(
    name="Mountain Day",
    month=8,
    day=11,
    start_date=Timestamp(2022, 1, 1),
    observance=sunday_to_monday,
)

JapanRespectForTheAgedDay1966To1972 = Holiday(
    name="Respect for the Aged Day",
    month=9,
    day=15,
    start_date=Timestamp(1966, 1, 1),
    end_date=Timestamp(1972, 12, 31),
)

JapanRespectForTheAgedDay1973To2002 = Holiday(
    name="Respect for the Aged Day",
    month=9,
    day=15,
    start_date=Timestamp(1973, 1, 1),
    end_date=Timestamp(2002, 12, 31),
    observance=sunday_to_monday,
)

JapanRespectForTheAgedDay = Holiday(
    name="Respect for the Aged Day",
    month=9,
    day=1,
    start_date=Timestamp(2003, 1, 1),
    offset=DateOffset(weekday=MO(3)),
)

# Citizen's Day added in some years between Respect for Aged and Autumnal Equinox

JapanAutumnalEquinox = Holiday(
    name="Autumnal Equinox",
    month=9,
    day=22,
    observance=autumnal_equinox,
)

JapanHealthAndSportsDay1966To1972 = Holiday(
    name="Health and Sports Day",
    month=10,
    day=10,
    start_date=Timestamp(1966, 1, 1),
    end_date=Timestamp(1972, 12, 31),
)

JapanHealthAndSportsDay1973To1999 = Holiday(
    name="Health and Sports Day",
    month=10,
    day=10,
    start_date=Timestamp(1973, 1, 1),
    end_date=Timestamp(1999, 12, 31),
    observance=sunday_to_monday,
)

JapanHealthAndSportsDay2000To2019 = Holiday(
    name="Health and Sports Day",
    month=10,
    day=1,
    start_date=Timestamp(2000, 1, 1),
    end_date=Timestamp(2019, 12, 31),
    offset=DateOffset(weekday=MO(2)),
)

JapanSportsDay2020 = Holiday(
    name="Sports Day",  # shift for Olympics
    year=2020,
    month=7,
    day=24,
)

JapanSportsDay2021 = Holiday(
    name="Sports Day",
    # shift for Olympics (Olympics and Paralympics postponed until 2021 due to the COVID-19 pandemic)
    year=2021,
    month=7,
    day=23,
)

JapanSportsDay = Holiday(
    name="Sports Day",
    month=10,
    day=1,
    start_date=Timestamp(2022, 1, 1),
    offset=DateOffset(weekday=MO(2)),
)

JapanCultureDayUntil1972 = Holiday(
    name="Culture Day",  # prior to 1948 Emperor Meiji's Birthday
    month=11,
    day=3,
    start_date=Timestamp(1948, 1, 1),
    end_date=Timestamp(1972, 12, 31),
)

JapanCultureDay = Holiday(
    name="Culture Day",
    month=11,
    day=3,
    start_date=Timestamp(1973, 1, 1),
    observance=sunday_to_monday,
)

JapanLaborThanksgivingDayUntil1972 = Holiday(
    name="Labor Thanksgiving Day",  # prior to 1948 harvest festival Niiname-sai
    month=11,
    day=23,
    end_date=Timestamp(1972, 12, 31),
)

JapanLaborThanksgivingDay = Holiday(
    name="Labor Thanksgiving Day",
    month=11,
    day=23,
    start_date=Timestamp(1973, 1, 1),
    observance=sunday_to_monday,
)

JapanEmperorAkahitosBirthday = Holiday(
    name="Emperor Akahito's Birthday",
    month=12,
    day=23,
    start_date=Timestamp(1990, 1, 1),
    end_date=Timestamp(2018, 12, 31),
    observance=sunday_to_monday,
)

JapanDecember29Until1988 = Holiday(
    name="Closed Decenber 29",
    month=12,
    day=29,
    end_date=Timestamp(1988, 12, 31),
)

JapanDecember30Until1988 = Holiday(
    name="Closed December 30",
    month=12,
    day=30,
    end_date=Timestamp(1988, 12, 31),
)

JapanBeforeNewYearsDay = Holiday(
    name="Before New Year's Day",  # prior to 1948 harvest festival Niname-sai
    month=12,
    day=31,
    observance=sunday_to_monday,
)
