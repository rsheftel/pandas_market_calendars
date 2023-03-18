"""
Bombay Stock Exchnage
"""

from pandas import Timestamp
from pytz import timezone
from datetime import time
from .market_calendar import MarketCalendar


BSEClosedDay = [
    Timestamp('1997-01-23', tz='UTC'),
    Timestamp('1997-03-07', tz='UTC'),
    Timestamp('1997-03-24', tz='UTC'),
    Timestamp('1997-04-08', tz='UTC'),
    Timestamp('1997-04-14', tz='UTC'),
    Timestamp('1997-04-16', tz='UTC'),
    Timestamp('1997-04-18', tz='UTC'),
    Timestamp('1997-05-01', tz='UTC'),
    Timestamp('1997-05-08', tz='UTC'),
    Timestamp('1997-08-15', tz='UTC'),
    Timestamp('1997-08-18', tz='UTC'),
    Timestamp('1997-08-25', tz='UTC'),
    Timestamp('1997-10-02', tz='UTC'),
    Timestamp('1997-10-28', tz='UTC'),
    Timestamp('1997-10-29', tz='UTC'),
    Timestamp('1997-10-31', tz='UTC'),
    Timestamp('1997-12-25', tz='UTC'),
    Timestamp('1998-04-09', tz='UTC'),
    Timestamp('1998-04-14', tz='UTC'),
    Timestamp('1998-04-28', tz='UTC'),
    Timestamp('1998-12-25', tz='UTC'),
    Timestamp('1999-01-01', tz='UTC'),
    Timestamp('1999-01-20', tz='UTC'),
    Timestamp('1999-01-26', tz='UTC'),
    Timestamp('1999-03-02', tz='UTC'),
    Timestamp('1999-03-18', tz='UTC'),
    Timestamp('1999-03-25', tz='UTC'),
    Timestamp('1999-03-29', tz='UTC'),
    Timestamp('1999-04-02', tz='UTC'),
    Timestamp('1999-04-14', tz='UTC'),
    Timestamp('1999-04-27', tz='UTC'),
    Timestamp('1999-04-30', tz='UTC'),
    Timestamp('1999-09-13', tz='UTC'),
    Timestamp('1999-10-19', tz='UTC'),
    Timestamp('1999-11-08', tz='UTC'),
    Timestamp('1999-11-10', tz='UTC'),
    Timestamp('1999-11-23', tz='UTC'),
    Timestamp('1999-12-31', tz='UTC'),
    Timestamp('2000-01-26', tz='UTC'),
    Timestamp('2000-03-17', tz='UTC'),
    Timestamp('2000-03-20', tz='UTC'),
    Timestamp('2000-04-14', tz='UTC'),
    Timestamp('2000-04-21', tz='UTC'),
    Timestamp('2000-05-01', tz='UTC'),
    Timestamp('2000-08-15', tz='UTC'),
    Timestamp('2000-09-01', tz='UTC'),
    Timestamp('2000-10-02', tz='UTC'),
    Timestamp('2000-12-25', tz='UTC'),
    Timestamp('2001-01-01', tz='UTC'),
    Timestamp('2001-01-26', tz='UTC'),
    Timestamp('2001-03-06', tz='UTC'),
    Timestamp('2001-04-05', tz='UTC'),
    Timestamp('2001-04-13', tz='UTC'),
    Timestamp('2001-05-01', tz='UTC'),
    Timestamp('2001-08-15', tz='UTC'),
    Timestamp('2001-08-22', tz='UTC'),
    Timestamp('2001-10-02', tz='UTC'),
    Timestamp('2001-10-26', tz='UTC'),
    Timestamp('2001-11-16', tz='UTC'),
    Timestamp('2001-11-30', tz='UTC'),
    Timestamp('2001-12-17', tz='UTC'),
    Timestamp('2001-12-25', tz='UTC'),
    Timestamp('2002-03-25', tz='UTC'),
    Timestamp('2002-03-29', tz='UTC'),
    Timestamp('2002-05-01', tz='UTC'),
    Timestamp('2002-08-15', tz='UTC'),
    Timestamp('2002-09-10', tz='UTC'),
    Timestamp('2002-10-02', tz='UTC'),
    Timestamp('2002-10-15', tz='UTC'),
    Timestamp('2002-11-06', tz='UTC'),
    Timestamp('2002-11-19', tz='UTC'),
    Timestamp('2002-12-25', tz='UTC'),
    Timestamp('2003-02-13', tz='UTC'),
    Timestamp('2003-03-14', tz='UTC'),
    Timestamp('2003-03-18', tz='UTC'),
    Timestamp('2003-04-14', tz='UTC'),
    Timestamp('2003-04-18', tz='UTC'),
    Timestamp('2003-05-01', tz='UTC'),
    Timestamp('2003-08-15', tz='UTC'),
    Timestamp('2003-10-02', tz='UTC'),
    Timestamp('2003-11-26', tz='UTC'),
    Timestamp('2003-12-25', tz='UTC'),
    Timestamp('2004-01-01', tz='UTC'),
    Timestamp('2004-01-26', tz='UTC'),
    Timestamp('2004-02-02', tz='UTC'),
    Timestamp('2004-03-02', tz='UTC'),
    Timestamp('2004-04-09', tz='UTC'),
    Timestamp('2004-04-14', tz='UTC'),
    Timestamp('2004-04-26', tz='UTC'),
    Timestamp('2004-10-13', tz='UTC'),
    Timestamp('2004-10-22', tz='UTC'),
    Timestamp('2004-11-15', tz='UTC'),
    Timestamp('2004-11-26', tz='UTC'),
    Timestamp('2005-01-21', tz='UTC'),
    Timestamp('2005-01-26', tz='UTC'),
    Timestamp('2005-03-25', tz='UTC'),
    Timestamp('2005-04-14', tz='UTC'),
    Timestamp('2005-07-28', tz='UTC'),
    Timestamp('2005-08-15', tz='UTC'),
    Timestamp('2005-09-07', tz='UTC'),
    Timestamp('2005-10-12', tz='UTC'),
    Timestamp('2005-11-03', tz='UTC'),
    Timestamp('2005-11-04', tz='UTC'),
    Timestamp('2005-11-15', tz='UTC'),
    Timestamp('2006-01-11', tz='UTC'),
    Timestamp('2006-01-26', tz='UTC'),
    Timestamp('2006-02-09', tz='UTC'),
    Timestamp('2006-03-15', tz='UTC'),
    Timestamp('2006-04-06', tz='UTC'),
    Timestamp('2006-04-11', tz='UTC'),
    Timestamp('2006-04-14', tz='UTC'),
    Timestamp('2006-05-01', tz='UTC'),
    Timestamp('2006-08-15', tz='UTC'),
    Timestamp('2006-10-02', tz='UTC'),
    Timestamp('2006-10-24', tz='UTC'),
    Timestamp('2006-10-25', tz='UTC'),
    Timestamp('2006-12-25', tz='UTC'),
    Timestamp('2007-01-01', tz='UTC'),
    Timestamp('2007-01-26', tz='UTC'),
    Timestamp('2007-01-30', tz='UTC'),
    Timestamp('2007-02-16', tz='UTC'),
    Timestamp('2007-03-27', tz='UTC'),
    Timestamp('2007-04-06', tz='UTC'),
    Timestamp('2007-05-01', tz='UTC'),
    Timestamp('2007-05-02', tz='UTC'),
    Timestamp('2007-08-15', tz='UTC'),
    Timestamp('2007-10-02', tz='UTC'),
    Timestamp('2007-12-21', tz='UTC'),
    Timestamp('2007-12-25', tz='UTC'),
    Timestamp('2008-03-06', tz='UTC'),
    Timestamp('2008-03-20', tz='UTC'),
    Timestamp('2008-03-21', tz='UTC'),
    Timestamp('2008-04-14', tz='UTC'),
    Timestamp('2008-04-18', tz='UTC'),
    Timestamp('2008-05-01', tz='UTC'),
    Timestamp('2008-05-19', tz='UTC'),
    Timestamp('2008-08-15', tz='UTC'),
    Timestamp('2008-09-03', tz='UTC'),
    Timestamp('2008-10-02', tz='UTC'),
    Timestamp('2008-10-09', tz='UTC'),
    Timestamp('2008-10-30', tz='UTC'),
    Timestamp('2008-11-13', tz='UTC'),
    Timestamp('2008-11-27', tz='UTC'),
    Timestamp('2008-12-09', tz='UTC'),
    Timestamp('2008-12-25', tz='UTC'),
    Timestamp('2009-01-08', tz='UTC'),
    Timestamp('2009-01-26', tz='UTC'),
    Timestamp('2009-02-23', tz='UTC'),
    Timestamp('2009-03-10', tz='UTC'),
    Timestamp('2009-03-11', tz='UTC'),
    Timestamp('2009-04-03', tz='UTC'),
    Timestamp('2009-04-07', tz='UTC'),
    Timestamp('2009-04-10', tz='UTC'),
    Timestamp('2009-04-14', tz='UTC'),
    Timestamp('2009-04-30', tz='UTC'),
    Timestamp('2009-05-01', tz='UTC'),
    Timestamp('2009-09-21', tz='UTC'),
    Timestamp('2009-09-28', tz='UTC'),
    Timestamp('2009-10-02', tz='UTC'),
    Timestamp('2009-10-13', tz='UTC'),
    Timestamp('2009-10-19', tz='UTC'),
    Timestamp('2009-11-02', tz='UTC'),
    Timestamp('2009-12-25', tz='UTC'),
    Timestamp('2009-12-28', tz='UTC'),
    Timestamp('2010-01-01', tz='UTC'),
    Timestamp('2010-01-26', tz='UTC'),
    Timestamp('2010-02-12', tz='UTC'),
    Timestamp('2010-03-01', tz='UTC'),
    Timestamp('2010-03-24', tz='UTC'),
    Timestamp('2010-04-02', tz='UTC'),
    Timestamp('2010-04-14', tz='UTC'),
    Timestamp('2010-09-10', tz='UTC'),
    Timestamp('2010-11-17', tz='UTC'),
    Timestamp('2010-12-17', tz='UTC'),
    Timestamp('2011-01-26', tz='UTC'),
    Timestamp('2011-03-02', tz='UTC'),
    Timestamp('2011-04-12', tz='UTC'),
    Timestamp('2011-04-14', tz='UTC'),
    Timestamp('2011-04-22', tz='UTC'),
    Timestamp('2011-08-15', tz='UTC'),
    Timestamp('2011-08-31', tz='UTC'),
    Timestamp('2011-09-01', tz='UTC'),
    Timestamp('2011-10-06', tz='UTC'),
    Timestamp('2011-10-27', tz='UTC'),
    Timestamp('2011-11-07', tz='UTC'),
    Timestamp('2011-11-10', tz='UTC'),
    Timestamp('2011-12-06', tz='UTC'),
    Timestamp('2012-01-26', tz='UTC'),
    Timestamp('2012-02-20', tz='UTC'),
    Timestamp('2012-03-08', tz='UTC'),
    Timestamp('2012-04-05', tz='UTC'),
    Timestamp('2012-04-06', tz='UTC'),
    Timestamp('2012-05-01', tz='UTC'),
    Timestamp('2012-08-15', tz='UTC'),
    Timestamp('2012-08-20', tz='UTC'),
    Timestamp('2012-09-19', tz='UTC'),
    Timestamp('2012-10-02', tz='UTC'),
    Timestamp('2012-10-24', tz='UTC'),
    Timestamp('2012-11-14', tz='UTC'),
    Timestamp('2012-11-28', tz='UTC'),
    Timestamp('2012-12-25', tz='UTC'),
    Timestamp('2013-03-27', tz='UTC'),
    Timestamp('2013-03-29', tz='UTC'),
    Timestamp('2013-04-19', tz='UTC'),
    Timestamp('2013-04-24', tz='UTC'),
    Timestamp('2013-05-01', tz='UTC'),
    Timestamp('2013-08-09', tz='UTC'),
    Timestamp('2013-08-15', tz='UTC'),
    Timestamp('2013-09-09', tz='UTC'),
    Timestamp('2013-10-02', tz='UTC'),
    Timestamp('2013-10-16', tz='UTC'),
    Timestamp('2013-11-04', tz='UTC'),
    Timestamp('2013-11-15', tz='UTC'),
    Timestamp('2013-12-25', tz='UTC'),
    Timestamp('2014-02-27', tz='UTC'),
    Timestamp('2014-03-17', tz='UTC'),
    Timestamp('2014-04-08', tz='UTC'),
    Timestamp('2014-04-14', tz='UTC'),
    Timestamp('2014-04-18', tz='UTC'),
    Timestamp('2014-04-24', tz='UTC'),
    Timestamp('2014-05-01', tz='UTC'),
    Timestamp('2014-07-29', tz='UTC'),
    Timestamp('2014-08-15', tz='UTC'),
    Timestamp('2014-08-29', tz='UTC'),
    Timestamp('2014-10-02', tz='UTC'),
    Timestamp('2014-10-03', tz='UTC'),
    Timestamp('2014-10-06', tz='UTC'),
    Timestamp('2014-10-15', tz='UTC'),
    Timestamp('2014-10-24', tz='UTC'),
    Timestamp('2014-11-04', tz='UTC'),
    Timestamp('2014-11-06', tz='UTC'),
    Timestamp('2014-12-25', tz='UTC'),
    Timestamp('2015-01-26', tz='UTC'),
    Timestamp('2015-02-17', tz='UTC'),
    Timestamp('2015-03-06', tz='UTC'),
    Timestamp('2015-04-02', tz='UTC'),
    Timestamp('2015-04-03', tz='UTC'),
    Timestamp('2015-04-14', tz='UTC'),
    Timestamp('2015-05-01', tz='UTC'),
    Timestamp('2015-09-17', tz='UTC'),
    Timestamp('2015-09-25', tz='UTC'),
    Timestamp('2015-10-02', tz='UTC'),
    Timestamp('2015-10-22', tz='UTC'),
    Timestamp('2015-11-12', tz='UTC'),
    Timestamp('2015-11-25', tz='UTC'),
    Timestamp('2015-12-25', tz='UTC'),
    Timestamp('2016-01-26', tz='UTC'),
    Timestamp('2016-03-07', tz='UTC'),
    Timestamp('2016-03-24', tz='UTC'),
    Timestamp('2016-03-25', tz='UTC'),
    Timestamp('2016-04-14', tz='UTC'),
    Timestamp('2016-04-15', tz='UTC'),
    Timestamp('2016-04-19', tz='UTC'),
    Timestamp('2016-07-06', tz='UTC'),
    Timestamp('2016-08-15', tz='UTC'),
    Timestamp('2016-09-05', tz='UTC'),
    Timestamp('2016-09-13', tz='UTC'),
    Timestamp('2016-10-11', tz='UTC'),
    Timestamp('2016-10-12', tz='UTC'),
    Timestamp('2016-10-31', tz='UTC'),
    Timestamp('2016-11-14', tz='UTC'),
    Timestamp('2017-01-26', tz='UTC'),
    Timestamp('2017-02-24', tz='UTC'),
    Timestamp('2017-03-13', tz='UTC'),
    Timestamp('2017-04-04', tz='UTC'),
    Timestamp('2017-04-14', tz='UTC'),
    Timestamp('2017-05-01', tz='UTC'),
    Timestamp('2017-06-26', tz='UTC'),
    Timestamp('2017-08-15', tz='UTC'),
    Timestamp('2017-08-25', tz='UTC'),
    Timestamp('2017-10-02', tz='UTC'),
    Timestamp('2017-10-20', tz='UTC'),
    Timestamp('2017-12-25', tz='UTC'),
    Timestamp('2018-01-26', tz='UTC'),
    Timestamp('2018-02-13', tz='UTC'),
    Timestamp('2018-03-02', tz='UTC'),
    Timestamp('2018-03-29', tz='UTC'),
    Timestamp('2018-03-30', tz='UTC'),
    Timestamp('2018-05-01', tz='UTC'),
    Timestamp('2018-08-15', tz='UTC'),
    Timestamp('2018-08-22', tz='UTC'),
    Timestamp('2018-09-13', tz='UTC'),
    Timestamp('2018-09-20', tz='UTC'),
    Timestamp('2018-10-02', tz='UTC'),
    Timestamp('2018-10-18', tz='UTC'),
    Timestamp('2018-11-08', tz='UTC'),
    Timestamp('2018-11-23', tz='UTC'),
    Timestamp('2018-12-25', tz='UTC'),
    Timestamp('2019-01-26', tz='UTC'),
    Timestamp('2019-03-02', tz='UTC'),
    Timestamp('2019-03-04', tz='UTC'),
    Timestamp('2019-03-21', tz='UTC'),
    Timestamp('2019-04-17', tz='UTC'),
    Timestamp('2019-04-19', tz='UTC'),
    Timestamp('2019-04-29', tz='UTC'),
    Timestamp('2019-05-01', tz='UTC'),
    Timestamp('2019-06-05', tz='UTC'),
    Timestamp('2019-08-12', tz='UTC'),
    Timestamp('2019-08-15', tz='UTC'),
    Timestamp('2019-09-02', tz='UTC'),
    Timestamp('2019-09-10', tz='UTC'),
    Timestamp('2019-10-02', tz='UTC'),
    Timestamp('2019-10-08', tz='UTC'),
    Timestamp('2019-10-21', tz='UTC'),
    Timestamp('2019-10-28', tz='UTC'),
    Timestamp('2019-11-12', tz='UTC'),
    Timestamp('2019-12-25', tz='UTC'),
    Timestamp('2020-02-21', tz='UTC'),
    Timestamp('2020-03-10', tz='UTC'),
    Timestamp('2020-04-02', tz='UTC'),
    Timestamp('2020-04-06', tz='UTC'),
    Timestamp('2020-04-10', tz='UTC'),
    Timestamp('2020-04-14', tz='UTC'),
    Timestamp('2020-05-01', tz='UTC'),
    Timestamp('2020-07-31', tz='UTC'),
    Timestamp('2020-10-02', tz='UTC'),
    Timestamp('2020-11-16', tz='UTC'),
    Timestamp('2020-11-30', tz='UTC'),
    Timestamp('2020-12-25', tz='UTC'),
    Timestamp('2021-01-26', tz='UTC'),  # Republic Day
    Timestamp('2021-03-11', tz='UTC'),  # Maha Shivaratri
    Timestamp('2021-03-29', tz='UTC'),  # Holi
    Timestamp('2021-04-02', tz='UTC'),  # Good Friday
    Timestamp('2021-04-14', tz='UTC'),  # Dr.Baba Saheb Ambedkar Jayanti
    Timestamp('2021-04-21', tz='UTC'),  # Ram Navami
    Timestamp('2021-05-13', tz='UTC'),  # Id-ul-Fitr
    Timestamp('2021-07-21', tz='UTC'),  # Id-al-Adha
    Timestamp('2021-08-19', tz='UTC'),  # Ashura
    Timestamp('2021-09-10', tz='UTC'),  # Ganesh Chaturthi
    Timestamp('2021-10-15', tz='UTC'),  # Vijaya Dashami
    Timestamp('2021-11-04', tz='UTC'),  # Diwali/Laxmi Puja. muhurat trading day
    Timestamp('2021-11-05', tz='UTC'),  # Diwali/Laxmi Puja
    Timestamp('2021-11-19', tz='UTC'),  # Guru Nanak Jayanti
    Timestamp('2022-01-26', tz='UTC'),  # Republic Day
    Timestamp('2022-03-01', tz='UTC'),  # Maha Shivaratri
    Timestamp('2022-03-18', tz='UTC'),  # Holi
    Timestamp('2022-04-14', tz='UTC'),  # Dr.Baba Saheb Ambedkar Jayanti
    Timestamp('2022-04-15', tz='UTC'),  # Good Friday
    Timestamp('2022-05-03', tz='UTC'),  # Id-ul-Fitr
    Timestamp('2022-08-09', tz='UTC'),  # Moharram
    Timestamp('2022-08-15', tz='UTC'),  # Independence Day
    Timestamp('2022-08-31', tz='UTC'),  # Ganesh Chaturthi
    Timestamp('2022-10-05', tz='UTC'),  # Vijaya Dashami
    Timestamp('2022-10-24', tz='UTC'),  # Diwali/Laxmi Puja. muhurat trading day
    Timestamp('2022-10-26', tz='UTC'),  # Diwali-Balipratipada
    Timestamp('2022-11-08', tz='UTC'),  # Guru Nanak Jayanti
    Timestamp('2023-01-26', tz='UTC'), # Thu, Republic Day
    Timestamp('2023-03-07', tz='UTC'), # Wed, Holi
    Timestamp('2023-03-18', tz='UTC'), # Sat, Maha Shivaratri
    Timestamp('2023-03-30', tz='UTC'), # Thu, Ramanavami
    Timestamp('2023-04-04', tz='UTC'), # Tue, Mahavir Jayanthi
    Timestamp('2023-04-07', tz='UTC'), # Fri, Good Friday
    Timestamp('2023-04-14', tz='UTC'), # Fri, Ambedkar Jayanti
    Timestamp('2023-04-22', tz='UTC'), # Sat, EID AL FITR
    Timestamp('2023-05-01', tz='UTC'), # Mon, Maharashtra Din
    Timestamp('2023-06-28', tz='UTC'), # Wed, Bakri Id / Eid ul-Adha
    Timestamp('2023-08-15', tz='UTC'), # Tue, Independence Day
    Timestamp('2023-08-29', tz='UTC'), # Tue, Muharram
    Timestamp('2023-09-19', tz='UTC'), # Tue, Ganesh Chaturthi
    Timestamp('2023-10-02', tz='UTC'), # Mon, Gandhi Jayanti
    Timestamp('2023-10-24', tz='UTC'), # Tue, Dussehra
    Timestamp('2023-11-12', tz='UTC'), # Sun, Diwali
    Timestamp('2023-11-14', tz='UTC'), # Tue, Diwali
    Timestamp('2023-11-27', tz='UTC'), # Mon, Guru Nanak's Birthday
    Timestamp('2023-12-25', tz='UTC'), # Mon, Christmas

    
    
]


class BSEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for the Bombay Stock Exchange (BSE, XBOM).
    Open Time: 9:15 AM, Asia/Calcutta
    Close Time: 3:30 PM, Asia/Calcutta

    Due to the complexity around the BSE holidays, we are hardcoding a list
    of holidays back to 1997, and forward through 2020.  There are no known
    early closes or late opens.
    """
    aliases = ['BSE', 'NSE']
    regular_market_times = {
        "market_open": ((None, time(9, 15)),),
        "market_close": ((None, time(15, 30)),)
    }

    @property
    def name(self):
        return "BSE"

    @property
    def tz(self):
        return timezone('Asia/Calcutta')

    @property
    def adhoc_holidays(self):
        return BSEClosedDay
