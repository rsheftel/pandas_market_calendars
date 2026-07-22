from datetime import time


GRAINS_AND_OILSEEDS_MARKET_TIMES = {
    # Pre 2012
    # https://www.agweb.com/news/crops/corn/cme-announces-expanded-grain-oilseed-trading-hours?utm_source=chatgpt.com
    # 2012 Change - Can only have discontinued break as last session, so am setting it to just be at open.
    # https://www.cmegroup.com/media-room/press-releases/2012/5/17/cme_group_introducesrevisedcbotgrainandoilseedtradinghoursinsupp.html
    # https://investor.cmegroup.com/news-releases/news-release-details/cme-group-announces-reduced-grain-and-oilseed-trading-hours
    "market_open": ((None, time(18,0), -1), ("2012-05-14", time(17,0), -1),("2013-04-08", time(19), -1),),  
    "market_close": ((None, time(13,15)), ("2012-05-14", time(14,0)), ("2013-04-08", time(13, 20)),),
    "break_start": ((None, time(7, 15)),("2012-05-14", time(17, 0), -1), ("2013-04-08", time(7,45))),
    "break_end": ((None, time(9, 30)), ("2012-05-14", time(17,0), -1), ("2013-04-08", time(8, 30)),),
}
