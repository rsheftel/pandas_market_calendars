Calendar Status
===============

pandas_market_calendars now imports and provides access to all the calendars in `trading_calendars <https://github.com/quantopian/trading_calendars>`

Use the ISO code on the trading_calendars page for those calendars. Many of the calendars are duplicated between
the pandas_market_calendars and trading_calendars projects, there is a program in place to merge these. For now use
whichever one you prefer.

========= ====== ===================== ============ ==========
 Type      Name         Class           Unit Tests   Creator
========= ====== ===================== ============ ==========
Exchange  NYSE   NYSEExchangeCalendar    Yes        Quantopian
Exchange  LSE    LSEExchangeCalendar     Yes        Quantopian
Exchange  CME    CMEExchangeCalendar     Yes        Quantopian
Exchange  ICE    ICEExchangeCalendar     Yes        Quantopian
Exchange  CFE    CFEExchangeCalendar     Yes        Quantopian
Exchange  BMF    BMFExchangeCalendar                Quantopian
Exchange  TSX    TSXExchangeCalendar     Yes        Quantopian
Exchange  EUREX  EUREXExchangeCalendar   Yes        kewlfft
Exchange  JPX    JPXExchangeCalendar     Yes        gabalese
Exchange  SIX    SIXExchangeCalendar     Yes        oliverfu89
Exchange  OSE    OSEExchangeCalendar     Yes        busteren
Exchange  SSE    SSEExchangeCalendar     Yes        keli
Exchange  TASE   TASEExchangeCalendar               gabglus
Exchange  HKEX   HKEXExchangeCalendar    Yes        1dot75cm
Exchange  ASX    ASXExchangeCalendar                pulledlamb
Exchange  XBOM   XBOMExchangeCalendar               rakesh1988
========= ====== ===================== ============ ==========

Futures Calendars
#################
========== ================ =================================== ============ ============
 Exchange        Name             Class                          Unit Tests    Creator
========== ================ =================================== ============ ============
CME        CME_Equity         CMEEquityExchangeCalendar           Yes         rsheftel
CME        CME_Bond           CMEBondExchangeCalendar             Yes         rsheftel
CME        CME_Agricultural   CMEAgriculturalExchangeCalendar     Yes        lionelyoung
========== ================ =================================== ============ ============
