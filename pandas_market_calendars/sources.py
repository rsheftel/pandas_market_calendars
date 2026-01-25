"""
Calendar source references for pandas_market_calendars.

This module provides structured source information for all calendars,
allowing users to verify where calendar data (holidays, market hours, etc.)
originated from and when it was last verified.

Usage:
    from pandas_market_calendars import get_calendar
    cal = get_calendar("NYSE")
    for source in cal.sources:
        print(f"{source.name}: {source.url}")
        print(f"  Covers: {source.covers}, Verified: {source.last_verified}")
        if source.notes:
            print(f"  Notes: {source.notes}")
"""

from typing import NamedTuple


class Source(NamedTuple):
    """
    Represents a source reference for calendar information.

    :param name: Human-readable name of the source (e.g., "NYSE Official Website")
    :param url: URL to the source documentation
    :param last_verified: Date when this source was last verified (YYYY-MM-DD format)
    :param covers: What aspects this source covers (e.g., "holidays", "trading hours", "special closes")
    :param notes: Optional notes about this source or its data
    """

    name: str
    url: str
    last_verified: str
    covers: str = "general"  # e.g., "holidays", "trading hours", "special closes", "early closes", "general"
    notes: str = ""


# Sources for calendars implemented directly in pandas_market_calendars
CALENDAR_SOURCES: dict[str, tuple[Source, ...]] = {
    # region ---- Australian Securities Exchange ----
    "ASX": (
        Source(
            name="ASX Trading Calendar",
            url="https://www.asx.com.au/markets/market-resources/trading-hours-calendar/cash-market-trading-hours/trading-calendar",
            last_verified="2025-01-24",
            covers="trading hours, holidays, early closes",
        ),
    ),
    # endregion
    # region ---- B3 (Brasil Bolsa Balcao) / BMF ----
    "BMF": (
        Source(
            name="B3 Trading Hours",
            url="https://www.b3.com.br/en_us/solutions/platforms/puma-trading-system/for-members-702702702702702702702702702702702702702/trading-702702702702702702702702702702702702702/schedules-702702702702702702702702702702702702702/",
            last_verified="2025-01-24",
            covers="trading hours",
        ),
        Source(
            name="B3 Holiday Calendar",
            url="https://www.b3.com.br/en_us/solutions/platforms/puma-trading-system/for-members-702702702702702702702702702702702702702/trading-702702702702702702702702702702702702702/holiday-702702702702702702702702702702702702702/",
            last_verified="2025-01-24",
            covers="holidays",
        ),
    ),
    "B3": (
        Source(
            name="B3 Trading Hours",
            url="https://www.b3.com.br/en_us/solutions/platforms/puma-trading-system/for-members-702702702702702702702702702702702702702/trading-702702702702702702702702702702702702702/schedules-702702702702702702702702702702702702702/",
            last_verified="2025-01-24",
            covers="trading hours",
        ),
    ),
    # endregion
    # region ---- Bombay Stock Exchange / NSE India ----
    "BSE": (
        Source(
            name="BSE India Trading Calendar",
            url="https://www.bseindia.com/static/markets/equity/EQReports/tra_cal.aspx",
            last_verified="2025-01-24",
            covers="trading hours, holidays",
        ),
        Source(
            name="NSE India Holiday Calendar",
            url="https://www.nseindia.com/resources/exchange-communication-holidays",
            last_verified="2025-01-24",
            covers="holidays",
            notes="BSE and NSE India share the same holiday schedule",
        ),
    ),
    "NSE": (
        Source(
            name="NSE India Holiday Calendar",
            url="https://www.nseindia.com/resources/exchange-communication-holidays",
            last_verified="2025-01-24",
            covers="holidays",
        ),
    ),
    # endregion
    # region ---- CBOE (Chicago Board Options Exchange) ----
    "CFE": (
        Source(
            name="CBOE Futures Exchange Expiration Calendar",
            url="https://www.cboe.com/us/futures/market_statistics/expiration_calendar/",
            last_verified="2025-01-24",
            covers="expiration dates",
        ),
        Source(
            name="CBOE US Futures Trading Hours",
            url="https://www.cboe.com/about/hours/us-futures/",
            last_verified="2025-01-24",
            covers="trading hours",
        ),
    ),
    "CBOE_Futures": (
        Source(
            name="CBOE Futures Exchange",
            url="https://www.cboe.com/us/futures/market_statistics/expiration_calendar/",
            last_verified="2025-01-24",
            covers="expiration dates, holidays",
        ),
    ),
    "CBOE_Equity_Options": (
        Source(
            name="CBOE Equity Options Hours",
            url="https://www.cboe.com/about/hours/equity-options/",
            last_verified="2025-01-24",
            covers="trading hours",
        ),
    ),
    "CBOE_Index_Options": (
        Source(
            name="CBOE Index Options Hours",
            url="https://www.cboe.com/about/hours/index-options/",
            last_verified="2025-01-24",
            covers="trading hours",
        ),
    ),
    # endregion
    # region ---- CME Group ----
    "CME_Equity": (
        Source(
            name="CME Group Holiday Calendar",
            url="https://www.cmegroup.com/tools-information/holiday-calendar.html",
            last_verified="2025-01-24",
            covers="holidays, early closes",
        ),
        Source(
            name="CME Group Equity Index Products",
            url="https://www.cmegroup.com/markets/equities.html",
            last_verified="2025-01-24",
            covers="trading hours",
        ),
    ),
    "CME_Agriculture": (
        Source(
            name="CME Group Agriculture Markets",
            url="https://www.cmegroup.com/markets/agriculture.html",
            last_verified="2025-01-24",
            covers="trading hours, product specs",
        ),
        Source(
            name="CME Group Holiday Calendar",
            url="https://www.cmegroup.com/tools-information/holiday-calendar.html",
            last_verified="2025-01-24",
            covers="holidays",
        ),
    ),
    "CME_Rate": (
        Source(
            name="CME Group Interest Rate Products",
            url="https://www.cmegroup.com/markets/interest-rates.html",
            last_verified="2025-01-24",
            covers="trading hours, product specs",
        ),
    ),
    "CME_Bond": (
        Source(
            name="CME Group Interest Rate Products",
            url="https://www.cmegroup.com/markets/interest-rates.html",
            last_verified="2025-01-24",
            covers="trading hours, product specs",
        ),
    ),
    # endregion
    # region ---- CME Globex ----
    "CME Globex Equity": (
        Source(
            name="CME Globex Equity Index Futures",
            url="https://www.cmegroup.com/markets/equities.html",
            last_verified="2025-01-24",
            covers="trading hours, product specs",
        ),
        Source(
            name="CME Group Holiday Calendar - Globex",
            url="https://www.cmegroup.com/tools-information/holiday-calendar.html#cmeGlobex",
            last_verified="2025-01-24",
            covers="holidays, early closes",
        ),
    ),
    "CME Globex Fixed Income": (
        Source(
            name="CME Globex Interest Rate Products",
            url="https://www.cmegroup.com/markets/interest-rates.html",
            last_verified="2025-01-24",
            covers="trading hours, product specs",
        ),
    ),
    "CME Globex Cryptocurrencies": (
        Source(
            name="CME Bitcoin Futures Contract Specs",
            url="https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/bitcoin.contractSpecs.html",
            last_verified="2025-01-24",
            covers="trading hours, product specs",
        ),
        Source(
            name="CME Group Holiday Calendar",
            url="https://www.cmegroup.com/tools-information/holiday-calendar.html",
            last_verified="2025-01-24",
            covers="holidays",
        ),
    ),
    "CMEGlobex_EnergyAndMetals": (
        Source(
            name="CME Group Energy Products",
            url="https://www.cmegroup.com/markets/energy.html",
            last_verified="2025-01-24",
            covers="energy trading hours",
        ),
        Source(
            name="CME Group Metals Products",
            url="https://www.cmegroup.com/markets/metals.html",
            last_verified="2025-01-24",
            covers="metals trading hours",
        ),
        Source(
            name="CME Crude Oil Contract Specs",
            url="https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.contractSpecs.html",
            last_verified="2025-01-24",
            covers="CL contract specs",
        ),
        Source(
            name="CME Group Holiday Calendar",
            url="https://www.cmegroup.com/tools-information/holiday-calendar.html",
            last_verified="2025-01-24",
            covers="holidays",
        ),
    ),
    "CMEGlobex_FX": (
        Source(
            name="CME Group FX Products",
            url="https://www.cmegroup.com/markets/fx.html",
            last_verified="2025-01-24",
            covers="trading hours, product specs",
        ),
        Source(
            name="CME FX Product Guide (PDF)",
            url="https://www.cmegroup.com/trading/fx/files/fx-product-guide-2021-us.pdf",
            last_verified="2025-01-24",
            covers="detailed product specifications",
            notes="PDF may be outdated; check main FX page for current info",
        ),
    ),
    "CMEGlobex_Grains": (
        Source(
            name="CME Group Grain and Oilseed Products",
            url="https://www.cmegroup.com/trading/agricultural/grain-and-oilseed.html",
            last_verified="2025-01-24",
            covers="trading hours, product specs",
        ),
    ),
    "CMEGlobex_Livestock": (
        Source(
            name="CME Group Livestock Products",
            url="https://www.cmegroup.com/trading/agricultural/livestock.html",
            last_verified="2025-01-24",
            covers="trading hours, product specs",
        ),
    ),
    # endregion
    # region ---- EUREX ----
    "EUREX": (
        Source(
            name="EUREX Trading Calendar",
            url="https://www.eurex.com/ex-en/trade/trading-calendar",
            last_verified="2025-01-24",
            covers="trading hours, holidays",
        ),
    ),
    "EUREX_Bond": (
        Source(
            name="EUREX Fixed Income Trading Calendar",
            url="https://www.eurex.com/ex-en/trade/trading-calendar",
            last_verified="2025-01-24",
            covers="trading hours, holidays",
        ),
    ),
    # endregion
    # region ---- Hong Kong Stock Exchange ----
    "HKEX": (
        Source(
            name="HKEX Trading Hours",
            url="https://www.hkex.com.hk/Services/Trading/Securities/Overview/Trading-Hours?sc_lang=en",
            last_verified="2025-01-24",
            covers="trading hours, lunch break",
        ),
        Source(
            name="HKEX Holiday Calendar",
            url="https://www.hkex.com.hk/News/HKEX-Calendar?sc_lang=en",
            last_verified="2025-01-24",
            covers="holidays",
        ),
    ),
    # endregion
    # region ---- ICE Futures ----
    "ICE": (
        Source(
            name="ICE Futures US Trading Hours (PDF)",
            url="https://www.theice.com/publicdocs/futures_us/ICE_Futures_US_Regular_Trading_Hours.pdf",
            last_verified="2025-01-24",
            covers="trading hours",
        ),
    ),
    "ICEUS": (
        Source(
            name="ICE Futures US Trading Hours (PDF)",
            url="https://www.theice.com/publicdocs/futures_us/ICE_Futures_US_Regular_Trading_Hours.pdf",
            last_verified="2025-01-24",
            covers="trading hours",
        ),
    ),
    # endregion
    # region ---- IEX (Investors Exchange) ----
    "IEX": (
        Source(
            name="IEX Exchange",
            url="https://exchange.iex.io/",
            last_verified="2025-01-24",
            covers="general",
        ),
        Source(
            name="IEX Trading Hours and Holidays",
            url="https://exchange.iex.io/resources/trading/trading-hours-holidays/",
            last_verified="2025-01-24",
            covers="trading hours, holidays",
            notes="IEX follows NYSE holiday schedule",
        ),
    ),
    # endregion
    # region ---- Japan Exchange Group ----
    "JPX": (
        Source(
            name="JPX Trading Hours",
            url="https://www.jpx.co.jp/english/equities/trading/domestic/index.html",
            last_verified="2025-01-24",
            covers="trading hours, lunch break",
        ),
        Source(
            name="JPX Non-Trading Days",
            url="https://www.jpx.co.jp/english/corporate/about-jpx/calendar/index.html",
            last_verified="2025-01-24",
            covers="holidays",
        ),
    ),
    # endregion
    # region ---- London Stock Exchange ----
    "LSE": (
        Source(
            name="LSE Business Days",
            url="https://www.londonstockexchange.com/securities-trading/trading-access/business-days",
            last_verified="2025-01-24",
            covers="trading hours, holidays",
        ),
    ),
    # endregion
    # region ---- New York Stock Exchange ----
    "NYSE": (
        Source(
            name="NYSE Holidays and Trading Hours",
            url="https://www.nyse.com/markets/hours-calendars",
            last_verified="2025-01-24",
            covers="trading hours, holidays, early closes",
        ),
        Source(
            name="NYSE Historical Trading Hours (Archive)",
            url="https://web.archive.org/web/20141224054812/http://www.nyse.com/about/history/timeline_trading.html",
            last_verified="2025-01-24",
            covers="historical trading hours",
            notes="Archive.org snapshot of historical NYSE trading hour changes",
        ),
        Source(
            name="Historical NYSE Closings Reference (PDF)",
            url="https://github.com/rsheftel/pandas_market_calendars/files/6827110/Stocks.NYSE-Closings.pdf",
            last_verified="2025-01-24",
            covers="historical ad-hoc closings",
            notes="Comprehensive list of NYSE closings from 1885-2011",
        ),
        Source(
            name="Brief History of Trading Hours",
            url="https://www.marketwatch.com/story/a-brief-history-of-trading-hours-on-wall-street-2015-05-29",
            last_verified="2025-01-24",
            covers="historical context",
        ),
    ),
    "NASDAQ": (
        Source(
            name="NASDAQ Stock Market Hours",
            url="https://www.nasdaq.com/stock-market-trading-hours-for-nasdaq",
            last_verified="2025-01-24",
            covers="trading hours, holidays",
            notes="NASDAQ follows NYSE holiday schedule",
        ),
    ),
    "BATS": (
        Source(
            name="CBOE BZX Exchange (formerly BATS)",
            url="https://www.cboe.com/us/equities/trading/",
            last_verified="2025-01-24",
            covers="trading hours",
            notes="BATS was acquired by CBOE in 2017",
        ),
    ),
    # endregion
    # region ---- Oslo Stock Exchange ----
    "OSE": (
        Source(
            name="Oslo Bors Trading Calendar",
            url="https://www.euronext.com/en/trade/trading-hours-holidays",
            last_verified="2025-01-24",
            covers="trading hours, holidays",
            notes="Oslo Bors is now part of Euronext",
        ),
    ),
    # endregion
    # region ---- SIFMA (Securities Industry and Financial Markets Association) ----
    "SIFMAUS": (
        Source(
            name="SIFMA US Holiday Schedule",
            url="https://www.sifma.org/resources/general/holiday-schedule/",
            last_verified="2025-01-24",
            covers="US bond market holidays, early closes",
            notes="SIFMA recommends early closes for US bond markets",
        ),
    ),
    "SIFMA_US": (
        Source(
            name="SIFMA US Holiday Schedule",
            url="https://www.sifma.org/resources/general/holiday-schedule/",
            last_verified="2025-01-24",
            covers="US bond market holidays, early closes",
        ),
    ),
    "SIFMAUK": (
        Source(
            name="SIFMA UK Holiday Schedule",
            url="https://www.sifma.org/resources/general/holiday-schedule/",
            last_verified="2025-01-24",
            covers="UK bond market holidays, early closes",
        ),
    ),
    "SIFMA_UK": (
        Source(
            name="SIFMA UK Holiday Schedule",
            url="https://www.sifma.org/resources/general/holiday-schedule/",
            last_verified="2025-01-24",
            covers="UK bond market holidays, early closes",
        ),
    ),
    "SIFMAJP": (
        Source(
            name="SIFMA JP Holiday Schedule",
            url="https://www.sifma.org/resources/general/holiday-schedule/",
            last_verified="2025-01-24",
            covers="Japan bond market holidays",
        ),
    ),
    "SIFMA_JP": (
        Source(
            name="SIFMA JP Holiday Schedule",
            url="https://www.sifma.org/resources/general/holiday-schedule/",
            last_verified="2025-01-24",
            covers="Japan bond market holidays",
        ),
    ),
    # endregion
    # region ---- SIX Swiss Exchange ----
    "SIX": (
        Source(
            name="SIX Swiss Exchange Trading Hours",
            url="https://www.six-group.com/en/products-services/the-swiss-stock-exchange/trading/trading-hours.html",
            last_verified="2025-01-24",
            covers="trading hours, holidays",
        ),
    ),
    # endregion
    # region ---- Shanghai Stock Exchange ----
    "SSE": (
        Source(
            name="SSE Trading Hours",
            url="http://english.sse.com.cn/tradingservice/trading/overview/",
            last_verified="2025-01-24",
            covers="trading hours, lunch break",
        ),
    ),
    # endregion
    # region ---- Tel Aviv Stock Exchange ----
    "TASE": (
        Source(
            name="TASE Trading Schedule",
            url="https://info.tase.co.il/eng/about_tase/corp/pages/trading_schedule.aspx",
            last_verified="2025-01-24",
            covers="trading hours, holidays",
        ),
        Source(
            name="TASE Transition to Mon-Fri (2026)",
            url="https://github.com/gerrymanoim/exchange_calendars/issues/518",
            last_verified="2025-01-24",
            covers="weekmask transition",
            notes="TASE changed from Sun-Thu to Mon-Fri on January 5, 2026",
        ),
    ),
    "XTAE": (
        Source(
            name="TASE Trading Schedule",
            url="https://info.tase.co.il/eng/about_tase/corp/pages/trading_schedule.aspx",
            last_verified="2025-01-24",
            covers="trading hours, holidays",
        ),
        Source(
            name="exchange_calendars XTAE Implementation",
            url="https://github.com/gerrymanoim/exchange_calendars",
            last_verified="2025-01-24",
            covers="implementation reference",
        ),
    ),
    # endregion
    # region ---- Toronto Stock Exchange ----
    "TSX": (
        Source(
            name="TSX Trading Hours",
            url="https://www.tsx.com/trading/toronto-stock-exchange/trading-hours",
            last_verified="2025-01-24",
            covers="trading hours",
        ),
        Source(
            name="TSX Holiday Schedule",
            url="https://www.tsx.com/trading/toronto-stock-exchange/trading-hours#holidays",
            last_verified="2025-01-24",
            covers="holidays",
        ),
    ),
    "TSXV": (
        Source(
            name="TSX Venture Exchange Trading Hours",
            url="https://www.tsx.com/trading/tsx-venture-exchange/trading-hours",
            last_verified="2025-01-24",
            covers="trading hours, holidays",
        ),
    ),
    # endregion
}

# Default source for calendars mirrored from exchange_calendars
_EXCHANGE_CALENDARS_SOURCE = (
    Source(
        name="exchange_calendars (GitHub)",
        url="https://github.com/gerrymanoim/exchange_calendars",
        last_verified="2025-01-24",
        covers="implementation reference",
        notes="Calendar data mirrored from the exchange_calendars package",
    ),
)


def get_sources(calendar_name: str) -> tuple[Source, ...]:
    """
    Get source references for a calendar by name.

    :param calendar_name: The calendar name (e.g., 'NYSE', 'XNYS', 'LSE')
    :return: Tuple of Source objects for the calendar
    """
    if calendar_name in CALENDAR_SOURCES:
        return CALENDAR_SOURCES[calendar_name]

    # For mirrored calendars from exchange_calendars (MIC codes starting with X)
    if calendar_name.startswith("X") or calendar_name in (
        "24/5",
        "24/7",
        "AIXK",
        "ASEX",
        "BVMF",
        "CMES",
        "IEPA",
        "us_futures",
    ):
        return _EXCHANGE_CALENDARS_SOURCE

    # Return empty tuple if no sources found
    return ()
