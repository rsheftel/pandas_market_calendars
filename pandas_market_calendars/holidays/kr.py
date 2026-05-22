


def _jp_observed(dt):
    """Japan substitute holiday: if holiday falls on Sunday, next Monday off.
    If Monday is also a holiday, Tuesday is off (sandwiched day rule — not
    fully implemented here; most cases are covered by the Sunday->Monday shift).
    """
    if dt.weekday() == 6:  # Sunday
        return dt + Day(1)
    return dt

# ---------------------------------------------------------------------------
# Korean public holidays (for KU — Korean Won futures)
# Fixed + lunar s-hoc
# ---------------------------------------------------------------------------

_KRFixedHolidays = [
    # Samil (Independence Movement) Day — Mar 1
    # Children's Day — May 5
    # Memorial Day — Jun 6
    # Liberation Day — Aug 15
    # National Foundation Day — Oct 3
    # Hangeul Day — Oct 9
    # Christmas — Dec 25
]

_KRSamil = Holiday("Samil Day", month=3, day=1, observance=_jp_observed)
_KRChildrensDay = Holiday("Children's Day", month=5, day=5, observance=_jp_observed)
_KRMemorialDay = Holiday("Memorial Day", month=6, day=6, observance=_jp_observed)
_KRLiberationDay = Holiday("Liberation Day", month=8, day=15, observance=_jp_observed)
_KRNationalFoundationDay = Holiday(
    "National Foundation Day", month=10, day=3, observance=_jp_observed
)
_KRHangeulDay = Holiday("Hangeul Day", month=10, day=9, observance=_jp_observed)
_KRChristmas = Holiday("Christmas", month=12, day=25, observance=_jp_observed)

# Lunar holidays: Seollal (LNY) 3 days, Chuseok (Harvest) 3 days,
# Buddha's Birthday — all ad-hoc
_KRLunarHolidays = [
    # 2020: Seollal Jan 24-27, Chuseok Sep 30-Oct 2, Buddha May 30
    Timestamp("2020-01-24"), Timestamp("2020-01-27"),
    Timestamp("2020-04-30"),  # substitute
    Timestamp("2020-09-30"), Timestamp("2020-10-01"), Timestamp("2020-10-02"),
    # 2021: Seollal Feb 11-13, Chuseok Sep 20-22, Buddha May 19
    Timestamp("2021-02-11"), Timestamp("2021-02-12"), Timestamp("2021-02-13"),
    Timestamp("2021-05-19"),
    Timestamp("2021-09-20"), Timestamp("2021-09-21"), Timestamp("2021-09-22"),
    # 2022: Seollal Feb 1-3, Chuseok Sep 9-12, Buddha May 8
    Timestamp("2022-02-01"), Timestamp("2022-02-02"), Timestamp("2022-02-03"),
    Timestamp("2022-05-08"), Timestamp("2022-05-10"),  # substitute
    Timestamp("2022-09-09"), Timestamp("2022-09-12"),
    # 2023: Seollal Jan 21-24, Chuseok Sep 28-Oct 3, Buddha May 29
    Timestamp("2023-01-21"), Timestamp("2023-01-23"), Timestamp("2023-01-24"),
    Timestamp("2023-05-29"),
    Timestamp("2023-09-28"), Timestamp("2023-09-29"), Timestamp("2023-10-02"),
    # 2024: Seollal Feb 9-12, Chuseok Sep 16-18, Buddha May 15
    Timestamp("2024-02-09"), Timestamp("2024-02-12"),
    Timestamp("2024-05-15"),
    Timestamp("2024-09-16"), Timestamp("2024-09-17"), Timestamp("2024-09-18"),
    # 2025: Seollal Jan 28-30, Chuseok Oct 5-7, Buddha May 5
    Timestamp("2025-01-28"), Timestamp("2025-01-29"), Timestamp("2025-01-30"),
    Timestamp("2025-10-05"), Timestamp("2025-10-06"), Timestamp("2025-10-07"),
    # 2026: Seollal Feb 16-18, Chuseok Sep 24-26, Buddha May 24
    Timestamp("2026-02-16"),Timestamp("2026-02-17"), Timestamp("2026-02-18"), 
    Timestamp("2026-05-25"),  # May 24 Sun -> Mon
    Timestamp("2026-09-24"), Timestamp("2026-09-25"), Timestamp("2026-09-28"),
    # 2027: Seollal Feb 6-8, Chuseok Sep 14-16, Buddha May 13
    Timestamp("2027-02-06"), Timestamp("2027-02-07"), Timestamp("2027-02-08"),
    Timestamp("2027-05-13"),
    Timestamp("2027-09-14"), Timestamp("2027-09-15"), Timestamp("2027-09-16"),
]
# Korea year-end: KRX closed Dec 31 most years
_KRYearEnd = [
    Timestamp("2020-12-31"), Timestamp("2021-12-31"),
    Timestamp("2022-12-30"),  # Dec 31 Sat
    Timestamp("2023-12-29"),  # Dec 31 Sun -> but KRX closes the last trading day
    Timestamp("2024-12-31"), Timestamp("2025-12-31"),
    Timestamp("2026-12-31"), Timestamp("2027-12-31"),
]
