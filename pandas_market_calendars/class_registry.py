import inspect
from pprint import pformat

def _regmeta_instance_factory(cls, name, *args, **kwargs):
    """
    :param cls(RegisteryMeta): registration meta class
    :param name(str): name of class that needs to be instantiated
    :param args(Optional(tuple)): instance positional arguments
    :param kwargs(Optional(dict)): instance named arguments
    :return: class instance
    """
    try:
        class_ = cls._regmeta_class_registry[name]
    except KeyError:
        raise RuntimeError(
            'Class {} is not one of the registered classes: {}'.format(name, cls._regmeta_class_registry.keys()))
    return class_(*args, **kwargs)

def _regmeta_register_class(cls, regcls, name):
    """
    :param cls(RegisteryMeta): registration base class
    :param regcls(class): class to be registered
    :param name(str): name of the class to be registered
    """
    if hasattr(regcls, 'aliases'):
        if regcls.aliases:
            for alias in regcls.aliases:
                cls._regmeta_class_registry[alias] = regcls
        else:
            cls._regmeta_class_registry[name] = regcls
    else:
        cls._regmeta_class_registry[name] = regcls


class RegisteryMeta(type):
    """
    Metaclass used to register all classes inheriting from RegisteryMeta
    """

    def __new__(mcs, name, bases, attr):
        cls = super(RegisteryMeta, mcs).__new__(mcs, name, bases, attr)
        if not hasattr(cls, '_regmeta_class_registry'):
            cls._regmeta_class_registry = {}
            cls.factory = classmethod(_regmeta_instance_factory)

        return cls

    def __init__(cls, name, bases, attr):
        if not inspect.isabstract(cls):
            _regmeta_register_class(cls, cls, name)
            for b in bases:
                if hasattr(b, '_regmeta_class_registry'):
                    _regmeta_register_class(b, cls, name)

        super(RegisteryMeta, cls).__init__(name, bases, attr)

        cls.regular_market_times = _ProtectedDict(cls.regular_market_times)

        cls.special_market_open = cls.special_opens
        cls.special_market_open_adhoc = cls.special_opens_adhoc

        cls.special_market_close = cls.special_closes
        cls.special_market_close_adhoc = cls.special_closes_adhoc


class _ProtectedDict(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # __init__ is bypassed when unpickling, which causes __setitem__ to fail
        # without the _INIT_RAN_NORMALLY flag
        self._INIT_RAN_NORMALLY = True
        self._ALLOW_SETTING_TIMES = False

    def __setitem__(self, key, value):
        if not hasattr(self, "_INIT_RAN_NORMALLY") or self._ALLOW_SETTING_TIMES:
            self._ALLOW_SETTING_TIMES = False
            return super().__setitem__(key, value)

        raise TypeError("You cannot set a value directly, "
                        "please use the instance methods MarketCalendar.change_time or "
                        "MarketCalendar.add_time to alter the regular_market_times information, "
                        "or inherit from MarketCalendar to create a new Class with custom times.")

    def __delitem__(self, key):
        if not hasattr(self, "_INIT_RAN_NORMALLY") or self._ALLOW_SETTING_TIMES:
            self._ALLOW_SETTING_TIMES = False
            return super().__delitem__(key)

        raise TypeError("You are not allowed to delete an item directly."
                        "Pleas use the instance method MarketCalendar.remove_time.")

    def __repr__(self):
        return self.__class__.__name__+ "(" + super().__repr__() + ")"

    def __str__(self):
        try:
            formatted = pformat(self, sort_dicts= False) # sort_dicts apparently not available < python3.8
        except TypeError:
            formatted = pformat(self)

        return self.__class__.__name__+ "(\n" + formatted + "\n)"

    def copy(self):
        return self.__class__(super().copy())




