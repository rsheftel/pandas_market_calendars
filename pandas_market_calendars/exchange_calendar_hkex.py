from datetime import time, timedelta
from functools import partial

from pandas import DateOffset, Timestamp
from pandas.tseries.holiday import AbstractHolidayCalendar, EasterMonday, GoodFriday, Holiday, sunday_to_monday
from pandas.tseries.offsets import LastWeekOfMonth, WeekOfMonth
from pytz import timezone

from pandas_market_calendars.holidays_us import USNewYearsDay
from .holidays_cn import bsd_mapping, dbf_mapping, dnf_mapping, maf_mapping, sf_mapping, tsd_mapping
from .market_calendar import MarketCalendar


def process_date(dt, mapping=None, func=None, delta=None, offset=None):
    if mapping and (dt.year in mapping):
        new_dt = mapping[dt.year]
    else:
        new_dt = dt
    if delta:
        new_dt = new_dt + timedelta(delta)
    dow = new_dt.weekday()
    if dow == 6 and offset:  # sunday
        new_dt = new_dt + timedelta(offset)
    if func:
        return func(new_dt)
    return new_dt


def process_queen_birthday(dt):
    # before 1983
    if dt.year in [1974, 1981]:
        return dt + DateOffset(weekday=6)
    elif dt.year < 1983:
        return sunday_to_monday(dt)
    # after 1983
    wom = WeekOfMonth(week=2, weekday=0)
    if dt.year in [1983, 1988, 1993, 1994]:
        wom = WeekOfMonth(week=1, weekday=0)
    if dt.year in [1985]:
        wom = WeekOfMonth(week=3, weekday=0)
    return dt + wom


HKNewYearsDay = USNewYearsDay

SpringFestivalDayBefore1983 = Holiday(
    name="Spring Festival",
    month=1,
    day=21,
    observance=partial(process_date, mapping=sf_mapping, delta=0, offset=3),
    start_date=Timestamp('1961-01-01'),
    end_date=Timestamp('1983-01-01')
)

SpringFestivalDay2Before1983 = Holiday(
    name="Spring Festival",
    month=1,
    day=21,
    observance=partial(process_date, mapping=sf_mapping, delta=1, offset=2),
    start_date=Timestamp('1961-01-01'),
    end_date=Timestamp('1983-01-01')
)

SpringFestivalDay3Before1983 = Holiday(
    name="Spring Festival",
    month=1,
    day=21,
    observance=partial(process_date, mapping=sf_mapping, delta=2, offset=1),
    start_date=Timestamp('1961-01-01'),
    end_date=Timestamp('1983-01-01')
)

SpringFestivalDayBefore2010 = Holiday(
    name="Spring Festival",
    month=1,
    day=21,
    observance=partial(process_date, mapping=sf_mapping, delta=0, offset=-1),
    start_date=Timestamp('1983-01-01'),
    end_date=Timestamp('2010-07-01')
)

SpringFestivalDay2Before2010 = Holiday(
    name="Spring Festival",
    month=1,
    day=21,
    observance=partial(process_date, mapping=sf_mapping, delta=1, offset=-2),
    start_date=Timestamp('1983-01-01'),
    end_date=Timestamp('2010-07-01')
)

SpringFestivalDay3Before2010 = Holiday(
    name="Spring Festival",
    month=1,
    day=21,
    observance=partial(process_date, mapping=sf_mapping, delta=2, offset=-3),
    start_date=Timestamp('1983-01-01'),
    end_date=Timestamp('2010-07-01')
)

SpringFestivalDay = Holiday(
    name="Spring Festival",
    month=1,
    day=21,
    observance=partial(process_date, mapping=sf_mapping, delta=0, offset=3),
    start_date=Timestamp('2010-07-01')
)

SpringFestivalDay2 = Holiday(
    name="Spring Festival",
    month=1,
    day=21,
    observance=partial(process_date, mapping=sf_mapping, delta=1, offset=2),
    start_date=Timestamp('2010-07-01')
)

SpringFestivalDay3 = Holiday(
    name="Spring Festival",
    month=1,
    day=21,
    observance=partial(process_date, mapping=sf_mapping, delta=2, offset=1),
    start_date=Timestamp('2010-07-01')
)

TombSweepingDay = Holiday(
    name="Tomb-sweeping Day",  # 清明节4月5日
    month=4,
    day=4,
    observance=partial(process_date, mapping=tsd_mapping, func=sunday_to_monday),
    start_date=Timestamp('1961-01-01')
)

LabourDay = Holiday(
    name="Labour Day",  # 劳动节
    month=5,
    day=1,
    observance=sunday_to_monday,
    start_date=Timestamp('1999-05-01')
)

BuddhaShakyamuniDay = Holiday(
    name="Buddha Shakyamuni Day",  # 浴佛节 98年农历4月8日定为法定假日
    month=4,
    day=28,
    observance=partial(process_date, mapping=bsd_mapping, func=sunday_to_monday),
    start_date=Timestamp('1999-04-28')
)

DragonBoatFestivalDay = Holiday(
    name="Dragon Boat Festival",  # 端午节
    month=5,
    day=27,
    observance=partial(process_date, mapping=dbf_mapping, func=sunday_to_monday),
    start_date=Timestamp('1961-01-01')
)

HKRegionEstablishmentDay = Holiday(
    name="Hong Kong Special Region Establishment Day",
    month=7,
    day=1,
    observance=sunday_to_monday,
    start_date=Timestamp('1997-07-01')
)

MidAutumnFestivalDayBefore1983 = Holiday(
    name="Mid-autumn Festival",  # 中秋节翌日
    month=9,
    day=7,
    observance=partial(process_date, mapping=maf_mapping, delta=1, func=sunday_to_monday),
    start_date=Timestamp('1961-01-01'),
    end_date=Timestamp('1983-01-01')
)

MidAutumnFestivalDayBefore2010 = Holiday(
    name="Mid-autumn Festival",  # 中秋节翌日
    month=9,
    day=7,
    observance=partial(process_date, mapping=maf_mapping, delta=1, offset=-1),
    start_date=Timestamp('1983-01-01'),
    end_date=Timestamp('2010-12-31')
)

MidAutumnFestivalDay = Holiday(
    name="Mid-autumn Festival",  # 中秋节翌日
    month=9,
    day=7,
    observance=partial(process_date, mapping=maf_mapping, delta=1, func=sunday_to_monday),
    start_date=Timestamp('2011-01-01')
)

DoubleNinthFestivalDay = Holiday(
    name="Double Ninth Festival",  # 重阳节
    month=10,
    day=2,
    observance=partial(process_date, mapping=dnf_mapping, func=sunday_to_monday),
    start_date=Timestamp('1961-01-01')
)

NationalDay = Holiday(
    name="National Day",
    month=10,
    day=1,
    observance=sunday_to_monday,
    start_date=Timestamp('1997-07-01')
)

Christmas = Holiday(
    name='Christmas',
    month=12,
    day=25,
    observance=partial(process_date, offset=2),
    start_date=Timestamp('1954-01-01')
)

BoxingDay = Holiday(
    name='Boxing day',  # 圣诞节后第一个平日
    month=12,
    day=26,
    observance=sunday_to_monday,
    start_date=Timestamp('1954-01-01')
)

QueenBirthday = Holiday(
    name="Queen's Birthday",  # 英女王生日 6月
    month=6,
    day=10,
    observance=process_queen_birthday,
    start_date=Timestamp('1983-01-01'),
    end_date=Timestamp('1997-06-01')
)

QueenBirthday2 = Holiday(
    name="Queen's Birthday",  # 英女王生日 4月
    month=4,
    day=21,
    observance=process_queen_birthday,
    start_date=Timestamp('1926-04-21'),
    end_date=Timestamp('1983-01-01')
)

CommemoratingAlliedVictory = Holiday(
    name="Commemorating the allied victory",  # 重光纪念日 8月最后一个星期一
    month=8,
    day=20,
    offset=LastWeekOfMonth(weekday=0),
    start_date=Timestamp('1945-08-30'),
    end_date=Timestamp('1997-07-01')
)

IDontKnow = Holiday(
    name="I dont know these days, please tell me",  # 8月第一个星期一
    month=7,
    day=31,
    offset=WeekOfMonth(week=0, weekday=0),
    start_date=Timestamp('1960-08-01'),
    end_date=Timestamp('1983-01-01')
)

HKClosedDay = [
    # I dont know these days
    Timestamp('1970-07-01', tz='UTC'),
    Timestamp('1971-07-01', tz='UTC'),
    Timestamp('1973-07-02', tz='UTC'),
    Timestamp('1974-07-01', tz='UTC'),
    Timestamp('1975-07-01', tz='UTC'),
    Timestamp('1976-07-01', tz='UTC'),
    Timestamp('1977-07-01', tz='UTC'),
    Timestamp('1979-07-02', tz='UTC'),
    Timestamp('1980-07-01', tz='UTC'),
    Timestamp('1981-07-01', tz='UTC'),
    Timestamp('1982-07-01', tz='UTC'),
    Timestamp('1971-03-22', tz='UTC'),
    Timestamp('1971-12-06', tz='UTC'),
    Timestamp('1971-12-20', tz='UTC'),
    Timestamp('1975-07-28', tz='UTC'),
    Timestamp('1985-07-29', tz='UTC'),

    Timestamp('1970-07-16', tz='UTC'),  # 台风Ruby7003
    Timestamp('1970-09-14', tz='UTC'),  # 台风Georgia7011
    Timestamp('1971-07-22', tz='UTC'),  # 台风Lucy7114
    Timestamp('1971-08-31', tz='UTC'),  # 重光纪念日?
    Timestamp('1973-04-16', tz='UTC'),  # 股灾休市?
    Timestamp('1973-07-17', tz='UTC'),  # 台风Dot7304
    Timestamp('1974-04-25', tz='UTC'),  # 英国女王生日
    Timestamp('1975-10-14', tz='UTC'),  # 台风Elsie7514
    Timestamp('1978-07-26', tz='UTC'),  # 台风Agnes7807
    Timestamp('1978-07-27', tz='UTC'),
    Timestamp('1979-01-26', tz='UTC'),  # 春节补假
    Timestamp('1979-08-02', tz='UTC'),  # 台风Hope7908
    Timestamp('1980-05-21', tz='UTC'),  # 台风Georgia8004
    Timestamp('1980-07-22', tz='UTC'),  # 台风Joy8007
    Timestamp('1981-04-27', tz='UTC'),  # 英国女王生日
    Timestamp('1981-07-06', tz='UTC'),  # 台风Lynn8106
    Timestamp('1981-07-07', tz='UTC'),
    Timestamp('1981-07-29', tz='UTC'),  # 查理斯王子与戴安娜婚礼
    Timestamp('1983-09-09', tz='UTC'),  # 台风Ellen8309
    Timestamp('1985-06-24', tz='UTC'),  # 台风Hal8504
    Timestamp('1986-04-01', tz='UTC'),  # 复活节星期一翌日
    Timestamp('1986-10-22', tz='UTC'),  # 英女王伊丽莎白二世访港
    Timestamp('1987-10-20', tz='UTC'),  # 黑色星期一后,休市4天
    Timestamp('1987-10-21', tz='UTC'),
    Timestamp('1987-10-22', tz='UTC'),
    Timestamp('1987-10-23', tz='UTC'),
    Timestamp('1988-04-05', tz='UTC'),  # 清明节翌日
    # Timestamp('1988-06-13', tz='UTC'),  # 英国女王生日
    Timestamp('1991-06-18', tz='UTC'),  # 英国女王生日翌日
    Timestamp('1992-07-22', tz='UTC'),  # 台风Cary9207
    # Timestamp('1993-06-14', tz='UTC'),  # 英国女王生日
    Timestamp('1993-09-17', tz='UTC'),  # 台风Becky9316
    Timestamp('1994-06-14', tz='UTC'),  # 英国女王生日翌日,端午节翌日
    Timestamp('1997-06-30', tz='UTC'),  # 英国女王生日
    Timestamp('1997-07-02', tz='UTC'),  # 香港回归纪念日翌日
    Timestamp('1997-08-18', tz='UTC'),  # 抗战胜利纪念日
    Timestamp('1997-10-02', tz='UTC'),  # 国庆节翌日
    Timestamp('1998-08-17', tz='UTC'),  # 抗战胜利纪念日
    Timestamp('1998-10-02', tz='UTC'),  # 国庆节翌日
    Timestamp('1999-04-06', tz='UTC'),  # 清明节翌日
    Timestamp('1999-09-16', tz='UTC'),  # 台风约克
    Timestamp('1999-12-31', tz='UTC'),  # 千年虫
    Timestamp('2001-07-06', tz='UTC'),  # 台风尤特0104
    Timestamp('2001-07-25', tz='UTC'),  # 台风玉兔0107
    # Timestamp(2008-06-25', tz='UTC'),  # 台风风神0806,上午休市
    Timestamp('2008-08-06', tz='UTC'),  # 台风北冕0809
    Timestamp('2008-08-22', tz='UTC'),  # 台风鹦鹉0810
    # Timestamp(2009-09-15', tz='UTC'),  # 台风巨爵0915,上午休市
    Timestamp('2010-04-06', tz='UTC'),  # 清明节翌日
    Timestamp('2011-09-29', tz='UTC'),  # 台风纳沙1117
    # Timestamp(2012-07-24', tz='UTC'),  # 台风韦森特1208,上午休市
    Timestamp('2012-10-02', tz='UTC'),  # 中秋节补假
    # Timestamp(2013-05-22', tz='UTC'),  # 暴雨,上午休市
    Timestamp('2013-08-14', tz='UTC'),  # 台风尤特1311
    # Timestamp(2013-09-23', tz='UTC'),  # 台风天兔1319,上午休市
    # Timestamp(2014-09-16', tz='UTC'),  # 台风海鸥1415,上午休市
    Timestamp('2015-04-07', tz='UTC'),  # 复活节+清明节补假
    # Timestamp(2015-07-09', tz='UTC'),  # 台风莲花1520,期货夜盘休市
    Timestamp('2015-09-03', tz='UTC'),  # 抗战70周年纪念
    # Timestamp(2016-08-01', tz='UTC'),  # 台风妮妲1604,期货夜盘20:55收市
    Timestamp('2016-08-02', tz='UTC'),  # 台风妮妲1604
    Timestamp('2016-10-21', tz='UTC'),  # 台风海马1622
    # Timestamp(2017-06-12', tz='UTC'),  # 台风苗柏1702,期货夜盘17:35休市
    Timestamp('2017-08-23', tz='UTC'),  # 台风天鸽1713
]


class HKEXExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for Hong Kong Stock Exchange

    Open Time: 9:30 AM, Asia/Shanghai
    LUNCH BREAK :facepalm: : 12:00 AM - 1:00 PM Asia/Shanghai
    Close Time: 4:00 PM, Asia/Shanghai
    """
    aliases = ['HKEX']
    regular_market_times = {
        "market_open": ((None, time(9, 30)),),
        "market_close": ((None, time(16)),),
        "break_start": ((None, time(12)),),
        "break_end": ((None, time(13)),)
    }

    @property
    def name(self):
        return "HKEX"

    @property
    def tz(self):
        return timezone('Asia/Shanghai')


    @property
    def regular_holidays(self):
        """
        Rules are guesses based on observations of recent year.
        Rectify accordingly once the next year's holidays arrangement is published by the government.
        """
        return AbstractHolidayCalendar(rules=[
            HKNewYearsDay,
            SpringFestivalDayBefore1983,
            SpringFestivalDay2Before1983,
            SpringFestivalDay3Before1983,
            SpringFestivalDayBefore2010,
            SpringFestivalDay2Before2010,
            SpringFestivalDay3Before2010,
            SpringFestivalDay,
            SpringFestivalDay2,
            SpringFestivalDay3,
            GoodFriday,
            EasterMonday,
            TombSweepingDay,
            LabourDay,
            BuddhaShakyamuniDay,
            DragonBoatFestivalDay,
            HKRegionEstablishmentDay,
            MidAutumnFestivalDayBefore1983,
            MidAutumnFestivalDayBefore2010,
            MidAutumnFestivalDay,
            NationalDay,
            DoubleNinthFestivalDay,
            Christmas,
            BoxingDay,
            CommemoratingAlliedVictory,
            QueenBirthday,
            QueenBirthday2,
            IDontKnow
        ])

    @property
    def adhoc_holidays(self):
        return HKClosedDay
