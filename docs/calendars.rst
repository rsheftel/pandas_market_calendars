Calendar Status
===============

Equity Market Calendars
#######################
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
Exchange  BSE    BSEExchangeCalendar     Yes        rakesh1988
Exchange  NSE    NSEExchangeCalendar     Yes        rakesh1988
Exchange  IEX    IEXExchangeCalendar     Yes        carterjfulcher
========= ====== ===================== ============ ==========

Futures Calendars
#################
=========  ====================  ================================  ===========  ==========================
Exchange   Name                  Class                             Unit Tests   Creator
=========  ====================  ================================  ===========  ==========================
CME        CME_Equity            CMEEquityExchangeCalendar         Yes          rsheftel
CME        CME_Bond              CMEBondExchangeCalendar           Yes          rsheftel
CME        CME_Agriculture       CMEAgriculturalExchangeCalendar   Yes          lionelyoung
CME        CME Globex Crypto     CMEGlobexCryptoExchangeCalendar   Yes          Coinbase Asset Management
CME        CMEGlobex_Grains      CMEGlobexGrainsExchangeCalendar   Yes          rundef
EUREX      EUREX_Bond            EUREXFixedIncomeCalendar          Yes          rundef
EUREX      EUREX_PrePost         EUREXPrePostExchangeCalendar      Yes          rsheftel
SHFE       SHFE                  SHFEExchangeCalendar              Yes          yangodds
SHFE       SHFE_BaseMetals       SHFEBaseMetalsCalendar            Yes          yangodds
SHFE       SHFE_PreciousMetals   SHFEPreciousMetalsCalendar        Yes          yangodds
SHFE       SHFE_Industrials      SHFEIndustrialsCalendar           Yes          yangodds
INE        INE                   INEExchangeCalendar               Yes          yangodds
INE        INE_Crude             INECrudeCalendar                  Yes          yangodds
INE        INE_Copper            INECopperCalendar                 Yes          yangodds
INE        INE_Industrials       INEIndustrialsCalendar            Yes          yangodds
DCE        DCE                   DCEExchangeCalendar               Yes          yangodds
DCE        DCE_Night             DCENightCalendar                  Yes          yangodds
CZCE       CZCE                  CZCEExchangeCalendar              Yes          yangodds
CZCE       CZCE_Night            CZCENightCalendar                 Yes          yangodds
GFEX       GFEX                  GFEXExchangeCalendar              Yes          yangodds
CFFEX      CFFEX                 CFFEXExchangeCalendar             Yes          yangodds
CFFEX      CFFEX_Bond            CFFEXBondExchangeCalendar         Yes          yangodds
=========  ====================  ================================  ===========  ==========================

Forex/OTC Market Calendars
##########################
========== ================= =================================== ============ ============
 Type            Name             Class                          Unit Tests    Creator
========== ================= =================================== ============ ============
OTC        FOREX             ForexExchangeCalendar                Yes         wiktorkisielewski
========== ================= =================================== ============ ============

Bond Market Calendars
#####################
========== ================ =================================== ============ ============
 Country        Name             Class                          Unit Tests    Creator
========== ================ =================================== ============ ============
   US          SIFMAUS        SIFMAUSExchangeCalendar             Yes
   UK          SIFMAUK        SIFMAUKExchangeCalendar             Yes
   JP          SIFMAJP        SIFMAJPExchangeCalendar             Yes
========== ================ =================================== ============ ============

Exchange Calendars Package
##########################
pandas_market_calendars now imports and provides access to all the calendars in `exchange_calendars <https://github.com/gerrymanoim/exchange_calendars>`_

Use the ISO code on the trading_calendars page for those calendars. Many of the calendars are duplicated between
the pandas_market_calendars and trading_calendars projects. Use whichever one you prefer.
