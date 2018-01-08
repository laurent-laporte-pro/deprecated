# -*- coding: utf-8 -*-
"""
Classic deprecation warning
===========================

Classic ``@deprecated`` decorator to deprecate old python classes, functions or methods.

"""
import functools
import inspect
import warnings

import wrapt

string_types = (type(b''), type(u''))


class Annotation(object):
    def __init__(self, reason=None, version=None):
        self.reason = reason
        self.version = version

    def get_deprecated_msg(self, wrapped, instance):
        if instance is None:
            if inspect.isclass(wrapped):
                fmt = "Call to deprecated class {name}."
            else:
                fmt = "Call to deprecated function (or staticmethod) {name}."
        else:
            if inspect.isclass(instance):
                fmt = "Call to deprecated class method {name}."
            else:
                fmt = "Call to deprecated method {name}."
        if self.reason:
            fmt += " ({reason})"
        if self.version:
            fmt += " -- Deprecated since version {version}."
        return fmt.format(name=wrapped.__name__,
                          reason=self.reason or "",
                          version=self.version or "")


class Deprecate(Annotation):
    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        msg = self.get_deprecated_msg(wrapped, instance)
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)
        return wrapped(*args, **kwargs)


def deprecated(*args, **kwargs):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.

    **Classic usage:**

    To use this, decorate your deprecated function with **@deprecated** decorator:

    .. code-block:: python

       from deprecated import deprecated


       @deprecated
       def some_old_function(x, y):
           return x + y

    You can also decorate a class or a method:

    .. code-block:: python

       from deprecated import deprecated


       class SomeClass(object):
           @deprecated
           def some_old_method(self, x, y):
               return x + y


       @deprecated
       class SomeOldClass(object):
           pass

    You can give a "reason" message to help the developer to choose another function/class:

    .. code-block:: python

       from deprecated import deprecated


       @deprecated(reason="use another function")
       def some_old_function(x, y):
           return x + y

    """
    if args and isinstance(args[0], string_types):
        kwargs['reason'] = args[0]
        args = args[1:]

    if args and not inspect.isfunction(args[0]) and not inspect.isclass(args[0]):
        raise TypeError(repr(type(args[0])))

    if args:
        return Deprecate(**kwargs)(args[0])

    return functools.partial(deprecated, **kwargs)
