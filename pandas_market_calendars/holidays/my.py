import pandas as pd
from pandas.tseries.holiday import (
    Holiday,
    AbstractHolidayCalendar,
    sunday_to_monday,
)
from pandas.tseries.offsets import WeekOfMonth


# ---------------------------------------------------------------------------
# Fixed-date holidays
# ---------------------------------------------------------------------------

NewYearsDay = Holiday(
    "New Year's Day",
    month=1,
    day=1,
    observance=sunday_to_monday,
)

LabourDay = Holiday(
    "Labour Day",
    month=5,
    day=1,
    observance=sunday_to_monday,
)

YangDiPertuanAgongBirthday = Holiday(
    # First Monday of June
    "Birthday of Yang Di-Pertuan Agong",
    month=6,
    day=1,
    offset=pd.offsets.WeekOfMonth(week=0, weekday=0),
)

NationalDay = Holiday(
    "National Day",
    month=8,
    day=31,
    observance=sunday_to_monday,
)

MalaysiaDay = Holiday(
    "Malaysia Day",
    month=9,
    day=16,
    observance=sunday_to_monday,
)

ChristmasDay = Holiday(
    "Christmas Day",
    month=12,
    day=25,
    observance=sunday_to_monday,
)

# ---------------------------------------------------------------------------
#
# Lunar / Islamic holidays — dates shift each year and must be listed
# explicitly as ad-hoc dates.  The list below covers 2020-2026 based on
# official Bursa Malaysia announcements.  Extend as new years are published.
#
# Key:
#   CNY1 / CNY2  – Chinese New Year day 1 & day 2
#   Thaipusam    – Tamil harvest moon festival (KL/Selangor)
#   Wesak        – Vesak / Buddha's Birthday
#   EidFitri1/2  – Hari Raya Aidilfitri (Eid al-Fitr) days 1 & 2
#   EidAdha      – Hari Raya Aidiladha (Eid al-Adha)
#   NuzulQuran   – Nuzul Al-Quran (revelation of Quran, Ramadan)
#   MaalHijrah   – Awal Muharram / Islamic New Year
#   MaulidNabi   – Birthday of Prophet Muhammad (saw)
#   Deepavali    – Diwali / Hindu festival
#
# NB: When a holiday falls on Sunday the Monday substitute is listed.
#     Federal Territory Day (1 Feb) is a Labuan/KL holiday only — Bursa
#     does NOT close for it so it is omitted here.
# ---------------------------------------------------------------------------

ChineseNewYear1 = AbstractHolidayCalendar(
    rules=[
        Holiday("Chinese New Year Day 1", year=2020, month=1, day=25),
        Holiday("Chinese New Year Day 1", year=2021, month=2, day=12),
        Holiday("Chinese New Year Day 1", year=2022, month=2, day=1),
        Holiday("Chinese New Year Day 1", year=2023, month=1, day=23),
        Holiday("Chinese New Year Day 1", year=2024, month=2, day=10),
        Holiday("Chinese New Year Day 1", year=2025, month=1, day=29),  # 28 is Sun → Mon sub
        Holiday("Chinese New Year Day 1", year=2026, month=2, day=17),
    ]
)

ChineseNewYear2 = AbstractHolidayCalendar(
    rules=[
        Holiday("Chinese New Year Day 2", year=2020, month=1, day=27),  # 26 Sun → Mon
        Holiday("Chinese New Year Day 2", year=2021, month=2, day=13),
        Holiday("Chinese New Year Day 2", year=2022, month=2, day=2),
        Holiday("Chinese New Year Day 2", year=2023, month=1, day=24),
        Holiday("Chinese New Year Day 2", year=2024, month=2, day=12),  # 11 Sun → Mon
        Holiday("Chinese New Year Day 2", year=2025, month=1, day=30),
        Holiday("Chinese New Year Day 2", year=2026, month=2, day=18),
    ]
)

Thaipusam = AbstractHolidayCalendar(
    rules=[
        Holiday("Thaipusam", year=2020, month=2, day=8),
        Holiday("Thaipusam", year=2021, month=1, day=28),
        Holiday("Thaipusam", year=2022, month=1, day=18),
        Holiday("Thaipusam", year=2023, month=2, day=4),  # 5 Feb
        Holiday("Thaipusam", year=2024, month=1, day=25),
        Holiday("Thaipusam", year=2025, month=2, day=11),
        Holiday("Thaipusam", year=2026, month=2, day=2),  # 1 Feb is Sun → Mon
    ]
)

WesakDay = AbstractHolidayCalendar(
    rules=[
        Holiday("Wesak Day", year=2020, month=5, day=7),
        Holiday("Wesak Day", year=2021, month=5, day=26),
        Holiday("Wesak Day", year=2022, month=5, day=15),  # 15 May
        Holiday("Wesak Day", year=2023, month=5, day=4),
        Holiday("Wesak Day", year=2024, month=5, day=22),
        Holiday("Wesak Day", year=2025, month=5, day=12),
        Holiday("Wesak Day", year=2026, month=6, day=1),  # 31 May is Sun → Mon 1 Jun
    ]
)

HariRayaPuasa1 = AbstractHolidayCalendar(
    rules=[
        Holiday("Hari Raya Puasa Day 1", year=2020, month=5, day=25),
        Holiday("Hari Raya Puasa Day 1", year=2021, month=5, day=13),
        Holiday("Hari Raya Puasa Day 1", year=2022, month=5, day=3),
        Holiday("Hari Raya Puasa Day 1", year=2023, month=4, day=22),
        Holiday("Hari Raya Puasa Day 1", year=2024, month=4, day=10),
        Holiday("Hari Raya Puasa Day 1", year=2025, month=3, day=31),
        Holiday("Hari Raya Puasa Day 1", year=2026, month=3, day=21),
    ]
)

HariRayaPuasa2 = AbstractHolidayCalendar(
    rules=[
        Holiday("Hari Raya Puasa Day 2", year=2020, month=5, day=26),
        Holiday("Hari Raya Puasa Day 2", year=2021, month=5, day=14),
        Holiday("Hari Raya Puasa Day 2", year=2022, month=5, day=4),
        Holiday("Hari Raya Puasa Day 2", year=2023, month=4, day=24),  # 23 Sun → Mon
        Holiday("Hari Raya Puasa Day 2", year=2024, month=4, day=11),
        Holiday("Hari Raya Puasa Day 2", year=2025, month=4, day=1),
        Holiday("Hari Raya Puasa Day 2", year=2026, month=3, day=23),  # 22 Sun -> Mon
    ]
)

NuzulAlQuran = AbstractHolidayCalendar(
    rules=[
        Holiday("Nuzul Al-Quran", year=2020, month=5, day=10),
        Holiday("Nuzul Al-Quran", year=2021, month=4, day=29),
        Holiday("Nuzul Al-Quran", year=2022, month=4, day=19),
        Holiday("Nuzul Al-Quran", year=2023, month=4, day=7),  # 8 Apr
        Holiday("Nuzul Al-Quran", year=2024, month=3, day=27),
        Holiday("Nuzul Al-Quran", year=2025, month=3, day=17),
        Holiday("Nuzul Al-Quran", year=2026, month=3, day=7),  # Sat — not a trading day; no closure expected
    ]
)

HariRayaHaji = AbstractHolidayCalendar(
    rules=[
        Holiday("Hari Raya Haji", year=2020, month=7, day=31),
        Holiday("Hari Raya Haji", year=2021, month=7, day=20),
        Holiday("Hari Raya Haji", year=2022, month=7, day=10),
        Holiday("Hari Raya Haji", year=2023, month=6, day=29),
        Holiday("Hari Raya Haji", year=2024, month=6, day=17),
        Holiday("Hari Raya Haji", year=2025, month=6, day=7),
        Holiday("Hari Raya Haji", year=2026, month=5, day=27),  # Sat — if Mon sub: 29 May; confirm with Bursa
    ]
)

MaalHijrah = AbstractHolidayCalendar(
    rules=[
        Holiday("Awal Muharram (Islamic New Year)", year=2020, month=8, day=20),
        Holiday("Awal Muharram (Islamic New Year)", year=2021, month=8, day=10),
        Holiday("Awal Muharram (Islamic New Year)", year=2022, month=7, day=30),
        Holiday("Awal Muharram (Islamic New Year)", year=2023, month=7, day=19),
        Holiday("Awal Muharram (Islamic New Year)", year=2024, month=7, day=7),
        Holiday("Awal Muharram (Islamic New Year)", year=2025, month=6, day=26),
        Holiday("Awal Muharram (Islamic New Year)", year=2026, month=6, day=17),
    ]
)

MaulidNabi = AbstractHolidayCalendar(
    rules=[
        Holiday("Birthday of Prophet Muhammad", year=2020, month=10, day=29),
        Holiday("Birthday of Prophet Muhammad", year=2021, month=10, day=19),
        Holiday("Birthday of Prophet Muhammad", year=2022, month=10, day=10),
        Holiday("Birthday of Prophet Muhammad", year=2023, month=9, day=28),
        Holiday("Birthday of Prophet Muhammad", year=2024, month=9, day=16),
        Holiday("Birthday of Prophet Muhammad", year=2025, month=9, day=5),
        Holiday("Birthday of Prophet Muhammad", year=2026, month=8, day=25),
    ]
)

Deepavali = AbstractHolidayCalendar(
    rules=[
        Holiday("Deepavali", year=2020, month=11, day=14),
        Holiday("Deepavali", year=2021, month=11, day=4),
        Holiday("Deepavali", year=2022, month=10, day=24),
        Holiday("Deepavali", year=2023, month=11, day=13),
        Holiday("Deepavali", year=2024, month=10, day=31),
        Holiday("Deepavali", year=2025, month=10, day=20),
        Holiday("Deepavali", year=2026, month=11, day=9),  # 8 Nov is Sun → Mon 9 Nov
    ]
)
