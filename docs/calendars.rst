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
================  ================= ====================================== ============ ============
Exchange          Name              Class                                  Unit Tests   Creator
================  ================= ====================================== ============ ============
ASX               ASX24_Index       ASX24IndexFuturesCalendar              Yes          lusewell
ASX               ASX24_Rates       ASX24IRFuturesCalendar                 Yes          lusewell
Bursa Malyasia    BURSAMY_FCPO      BursaMalaysiaFCPOCalendar              Yes          lusewell
Bursa Malyasia    BURSAMY_FKLI      BursaMalaysiaFKLICalendar              Yes          lusewell
CBOE              CFE               CFEExchangeCalendar                 
CME               CME_Equity        CMEEquityExchangeCalendar              Yes          rsheftel
CME               CME_Bond          CMEBondExchangeCalendar                Yes          rsheftel
CME               CME_Agriculture   CMEAgriculturalExchangeCalendar        Yes          lionelyoung
CME               CME Globex Crypto CMEGlobexCryptoExchangeCalendar        Yes          Coinbase Asset Management
CME               CMEGlobex_Grains  CMEGlobexGrainsExchangeCalendar        Yes          rundef
EUREX             EUREX_Bond        EUREXFixedIncomeCalendar               Yes          rundef
EUREX             EUREX_PrePost     EUREXPrePostExchangeCalendar           Yes          rsheftel
Euronext          ENX_AMS_INDEX     EuronextAmsterdamIndexDerivsCalendar   Yes          lusewell
Euronext          ENX_BRU_INDEX     EuronextBrusselsIndexDerivsCalendar    Yes          lusewell
Euronext          ENX_LIS_INDEX     EuronextLisbonIndexDerivsCalendar      Yes          lusewell
Euronext          ENX_MIL_INDEX     EuronextMilanIndexDerivsCalendar       Yes          lusewell
Euronext          ENX_OSL_INDEX     EuronextOsloIndexDerivsCalendar        Yes          lusewell
Euronext          ENX_PAR_INDEX     EuronextParisIndexDerivsCalendar       Yes          lusewell
Euronext          ENX_PAR_COMM      EuronextParisCommodityDerivsCalendar   Yes          lusewell
HKEX              HKFE              HKFEDomesticExchangeCalendar           Yes          lusewell
HKEX              HKFE_A50          HKFEA50ExchangeCalendar                             lusewell
HKEX              HKFE_TW           HKFETaiwanExchangeCalendar                          lusewell
HKEX              HKFE_CNH          HKFECNHExchangeCalendar                             lusewell
ICE               ICEUS_COFFEE      ICEUSCoffeeCalendar                    Yes          lusewell
ICE               ICEUS_COTTON      ICEUSCottonCalendar                    Yes          lusewell
ICE               ICEUS_COCOA       ICEUSCocoaCalendar                     Yes          lusewell
ICE               ICEUS_SUGAR11     ICEUSSugar11Calendar                   Yes          lusewell
ICE               ICEUS_SUGAR16     ICEUSSugar16Calendar                                lusewell
ICE               ICEUS_CANOLA      ICEUSCanolaCalendar                    Yes          lusewell
ICE               ICEUS_ENERGIES    ICEUSEnergiesCalendar                  Yes          lusewell
ICE               ICEUS_FX          ICEUSFxCalendar                        Yes          lusewell
ICE               ICEUS_FINANCIALS  ICEUSFinancialsCalendar                             lusewell
ICE               ICE_DAILY_PR      ICEUSDailyGoldSilverCalendar           Yes          lusewell

================= ================= ====================================== ============ ============

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
