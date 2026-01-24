"""
Tests for calendar source references.

This module tests the sources functionality that provides reference
information about where calendar data (holidays, trading hours, etc.)
originated from.
"""

import pandas_market_calendars as mcal
from pandas_market_calendars.sources import CALENDAR_SOURCES, Source, get_sources


def test_source_namedtuple_fields():
    # Source should have all expected fields
    source = Source(
        name="Test Source",
        url="https://example.com",
        last_verified="2025-01-24",
        covers="trading hours",
        notes="Test notes",
    )
    assert source.name == "Test Source"
    assert source.url == "https://example.com"
    assert source.last_verified == "2025-01-24"
    assert source.covers == "trading hours"
    assert source.notes == "Test notes"


def test_source_default_values():
    # Source should have sensible defaults
    source = Source(
        name="Test Source",
        url="https://example.com",
        last_verified="2025-01-24",
    )
    assert source.covers == "general"
    assert source.notes == ""


def test_get_sources_native_calendar():
    # Native calendars should return their defined sources
    sources = get_sources("NYSE")
    assert len(sources) > 0
    assert all(isinstance(s, Source) for s in sources)
    # NYSE should have official website source
    urls = [s.url for s in sources]
    assert any("nyse.com" in url for url in urls)


def test_get_sources_mirrored_calendar():
    # Mirrored calendars should return exchange_calendars source
    sources = get_sources("XNYS")
    assert len(sources) > 0
    assert any("exchange_calendars" in s.name for s in sources)


def test_get_sources_unknown_calendar():
    # Unknown calendars should return empty tuple
    sources = get_sources("UNKNOWN_CALENDAR_12345")
    assert sources == ()


def test_calendar_sources_property():
    # Calendar instances should have working sources property
    nyse = mcal.get_calendar("NYSE")
    sources = nyse.sources
    assert isinstance(sources, tuple)
    assert len(sources) > 0
    assert all(isinstance(s, Source) for s in sources)


def test_calendar_sources_property_mirrored():
    # Mirrored calendar instances should have sources
    xlon = mcal.get_calendar("XLON")
    sources = xlon.sources
    assert isinstance(sources, tuple)
    assert len(sources) > 0


def test_all_defined_sources_have_required_fields():
    # All sources in CALENDAR_SOURCES should have valid data
    for cal_name, sources in CALENDAR_SOURCES.items():
        assert isinstance(sources, tuple), f"{cal_name} sources should be a tuple"
        for source in sources:
            assert source.name, f"{cal_name} source missing name"
            assert source.url, f"{cal_name} source missing url"
            assert source.last_verified, f"{cal_name} source missing last_verified"
            # URL should be valid format
            assert source.url.startswith(("http://", "https://")), f"{cal_name} source has invalid URL: {source.url}"


def test_all_defined_sources_have_valid_dates():
    # All last_verified dates should be in YYYY-MM-DD format
    import re

    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    for cal_name, sources in CALENDAR_SOURCES.items():
        for source in sources:
            assert date_pattern.match(source.last_verified), (
                f"{cal_name} source has invalid date format: {source.last_verified}"
            )


def test_major_calendars_have_sources():
    # Major calendars should have sources defined
    major_calendars = [
        "NYSE",
        "NASDAQ",
        "LSE",
        "JPX",
        "HKEX",
        "ASX",
        "TSX",
        "EUREX",
        "CME_Equity",
        "SIFMAUS",
    ]
    for cal_name in major_calendars:
        sources = get_sources(cal_name)
        assert len(sources) > 0, f"{cal_name} should have sources defined"


def test_sources_covers_field_populated():
    # Sources should have meaningful covers field
    sources = get_sources("NYSE")
    assert any(s.covers != "general" for s in sources), "NYSE should have specific covers"


def test_source_notes_optional():
    # Notes field is optional - some sources may not have notes
    # Just verify it doesn't break anything
    for cal_name, sources in CALENDAR_SOURCES.items():
        for source in sources:
            # Should be able to access notes without error
            _ = source.notes
