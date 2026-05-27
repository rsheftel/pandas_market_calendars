from datetime import time


GRAINS_AND_OILSEEDS_MARKET_TIMES = {
    "market_open": ((None, time(19), -1),),  # offset by -1 day
    "market_close": ((None, time(13, 20)),),
    "break_start": ((None, time(7, 45)),),
    "break_end": ((None, time(8, 30)),),
}
