
from .market_calendar import MarketCalendar


def get_calendar(name, open_time=None, close_time=None):
    """
    Retrieves an instance of an MarketCalendar whose name is given.

    :param name: The name of the MarketCalendar to be retrieved.
    :param open_time: Market open time override as datetime.time object. If None then default is used.
    :param close_time: Market close time override as datetime.time object. If None then default is used.
    :return: MarketCalendar of the desired calendar.
    """
    return MarketCalendar.factory(name, open_time=open_time, close_time=close_time)


def get_calendar_names():
    """All Market Calendar names and aliases that can be used in "factory"
    :return: list(str)
    """
    return MarketCalendar.calendar_names()
