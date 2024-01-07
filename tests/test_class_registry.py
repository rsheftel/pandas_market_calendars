from abc import ABCMeta, abstractmethod
from datetime import time
from pprint import pformat

import pytest

from pandas_market_calendars.class_registry import RegisteryMeta, ProtectedDict


def test_inheritance():
    class Base(object):
        regular_market_times = {
            "market_open": {None: time(0)},
            "market_close": {None: time(23)},
        }
        open_close_map = {}

        @classmethod
        def _prepare_regular_market_times(cls):
            return

        def __init__(self, arg0, kw0=None):
            self.arg0 = arg0
            self.kw0 = kw0
            super(Base, self).__init__()

        def special_opens(self):
            return []

        special_closes = special_closes_adhoc = special_opens_adhoc = special_opens

    class Class1(Base, metaclass=RegisteryMeta):
        def __init__(self, arg0, arg1, kw1=None, **kwargs):
            self.arg1 = arg1
            self.kw1 = kw1
            super(Class1, self).__init__(arg0, **kwargs)

    factory1 = Class1.factory

    class Class2(Base, metaclass=RegisteryMeta):
        aliases = ["class 2"]

        def __init__(self, arg0, arg2, kw2=None, **kwargs):
            self.arg2 = arg2
            self.kw2 = kw2
            super(Class2, self).__init__(arg0, **kwargs)

    factory2 = Class2.factory

    class Class1a(Class1):
        aliases = ["class 1a"]

        def __init__(self, arg0, arg1, arg1a, kw1a=None, **kwargs):
            self.arg1a = arg1a
            self.kw1a = kw1a
            super(Class1a, self).__init__(arg0, arg1, **kwargs)

    class Class1b(Class1):
        def __init__(self, arg0, arg1, arg1b, kw1b=None, **kwargs):
            self.arg1b = arg1b
            self.kw1b = kw1b
            super(Class1b, self).__init__(arg0, arg1, **kwargs)

    class Class12a(Class1, Class2):
        aliases = ["class 12a"]

        def __init__(self, arg0, arg1, arg2, arg12a, kw12a=None, **kwargs):
            self.arg12a = arg12a
            self.kw12a = kw12a
            super(Class12a, self).__init__(arg0=arg0, arg1=arg1, arg2=arg2, **kwargs)

    assert set(Class1._regmeta_class_registry.keys()) == {
        "Class1",
        "class 1a",
        "Class1b",
        "class 12a",
    }
    assert set(Class2._regmeta_class_registry.keys()) == {"class 2", "class 12a"}

    o = factory1("Class1", "0", "1", kw0="k0", kw1="k1")
    assert (o.arg0, o.arg1, o.kw0, o.kw1) == ("0", "1", "k0", "k1")
    assert Class1 == o.__class__

    o = factory1("class 1a", "0", "1", "a", kw0="k0", kw1="k1", kw1a="k1a")
    assert (o.arg0, o.arg1, o.arg1a, o.kw0, o.kw1, o.kw1a) == (
        "0",
        "1",
        "a",
        "k0",
        "k1",
        "k1a",
    )
    assert Class1a == o.__class__

    o = factory1("Class1b", "0", "1", "b", kw0="k0", kw1="k1", kw1b="k1b")
    assert (o.arg0, o.arg1, o.arg1b, o.kw0, o.kw1, o.kw1b) == (
        "0",
        "1",
        "b",
        "k0",
        "k1",
        "k1b",
    )
    assert Class1b == o.__class__

    o = factory1(
        "class 12a", "0", "1", "2", "a", kw0="k0", kw1="k1", kw2="k2", kw12a="k12a"
    )
    assert (o.arg0, o.arg1, o.arg2, o.arg12a, o.kw0, o.kw1, o.kw2, o.kw12a) == (
        "0",
        "1",
        "2",
        "a",
        "k0",
        "k1",
        "k2",
        "k12a",
    )
    assert Class12a == o.__class__

    o = factory2("class 2", "0", "2", kw0="k0", kw2="k2")
    assert (o.arg0, o.arg2, o.kw0, o.kw2) == ("0", "2", "k0", "k2")
    assert Class2 == o.__class__


def test_metamixing():
    BaseMeta = type("BaseMeta", (ABCMeta, RegisteryMeta), {})

    class Base(metaclass=BaseMeta):
        regular_market_times = {
            "market_open": {None: time(0)},
            "market_close": {None: time(23)},
        }
        open_close_map = {}

        @classmethod
        def _prepare_regular_market_times(cls):
            return

        def special_opens(self):
            return []

        special_closes = special_closes_adhoc = special_opens_adhoc = special_opens

        @abstractmethod
        def test(self):
            pass

    class Class1(Base):
        aliases = ["c1", "c 1"]

        def test(self):
            return 123

    try:
        Base()
    except TypeError:
        pass
    else:
        raise RuntimeError("Abstract class is instantiated")

    o1 = Base.factory("c1")
    o2 = Base.factory("c 1")
    assert o1.test() == o2.test()

    with pytest.raises(RuntimeError):
        Base.factory("error")  # doesn't exist

    class Class2(Base):  # no aliases
        def test(self):
            return "test"

    assert Base.factory("Class2").test() == "test"


def test_protected_dict():
    dct = ProtectedDict(dict(a=1, b=2))

    with pytest.raises(TypeError):
        dct["a"] = 2

    with pytest.raises(TypeError):
        del dct["b"]

    del dct._INIT_RAN_NORMALLY
    del dct["b"]

    dct = ProtectedDict(dict(a=1, b=2))

    s = "ProtectedDict(\n" + pformat(dict(dct), sort_dicts=False) + "\n)"
    assert str(dct) == s


# if __name__ == '__main__':
#
#     for ref, obj in locals().copy().items():
#         if ref.startswith("test_"):
#             print("running: ", ref)
#             obj()
