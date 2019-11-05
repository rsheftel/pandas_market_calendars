def _regmeta_class_factory(cls, name):
    """
    :param cls(RegisteryMeta): registration meta class
    :param name(str): name of class
    :return: class
    """
    if name in cls._regmeta_class_registry:
        return cls._regmeta_class_registry[name]
    else:
        raise RuntimeError(
            'Class {} is not one of the registered classes: {}'.format(name, cls._regmeta_class_registry.keys()))


def _regmeta_instance_factory(cls, name, *args, **kwargs):
    """
    :param cls(RegisteryMeta): registration meta class
    :param name(str): name of class that needs to be instantiated
    :param args(Optional(tuple)): instance positional arguments
    :param kwargs(Optional(dict)): instance named arguments
    :return: class instance
    """
    return cls._regmeta_class_factory(name)(*args, **kwargs)


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


def _regmeta_classes(cls):
    return list(cls._regmeta_class_registry.keys())


class RegisteryMeta(type):
    """
    Metaclass used to register all classes inheriting from RegisteryMeta
    """

    def __new__(mcs, name, bases, attr):
        cls = super(RegisteryMeta, mcs).__new__(mcs, name, bases, attr)

        if not hasattr(cls, '_regmeta_class_registry'):
            cls._regmeta_class_registry = {}
            cls._regmeta_class_factory = classmethod(_regmeta_class_factory)
            cls._regmeta_instance_factory = classmethod(_regmeta_instance_factory)
            cls._regmeta_classes = classmethod(_regmeta_classes)

        return cls

    def __init__(cls, name, bases, attr):
        _regmeta_register_class(cls, cls, name)
        for b in bases:
            if hasattr(b, '_regmeta_class_registry'):
                _regmeta_register_class(b, cls, name)
        super(RegisteryMeta, cls).__init__(name, bases, attr)
