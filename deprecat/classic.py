# -*- coding: utf-8 -*-
"""
Classic deprecation warning
===========================

Classic ``@deprecat`` decorator to deprecate old python classes, functions or methods.

.. _The Warnings Filter: https://docs.python.org/3/library/warnings.html#the-warnings-filter
"""
import functools
import inspect
import platform
import warnings

import wrapt

try:
    # If the C extension for wrapt was compiled and wrapt/_wrappers.pyd exists, then the
    # stack level that should be passed to warnings.warn should be 2. However, if using
    # a pure python wrapt, a extra stacklevel is required.
    import wrapt._wrappers

    _routine_stacklevel = 2
    _class_stacklevel = 2
except ImportError:
    _routine_stacklevel = 3
    if platform.python_implementation() == "PyPy":
        _class_stacklevel = 2
    else:
        _class_stacklevel = 3

string_types = (type(b''), type(u''))


class ClassicAdapter(wrapt.AdapterFactory):
    """
    Classic adapter -- *for advanced usage only*

    This adapter is used to get the deprecation message according to the wrapped object type:
    class, function, standard method, static method, or class method.

    This is the base class of the :class:`~deprecat.sphinx.SphinxAdapter` class
    which is used to update the wrapped object docstring.

    You can also inherit this class to change the deprecation message.

    In the following example, we change the message into "The ... is deprecated.":

    .. code-block:: python

       import inspect

       from deprecat.classic import ClassicAdapter
       from deprecat.classic import deprecat


       class MyClassicAdapter(ClassicAdapter):
           def get_deprecat_msg(self, wrapped, instance):
               if instance is None:
                   if inspect.isclass(wrapped):
                       fmt = "The class {name} is deprecated."
                   else:
                       fmt = "The function {name} is deprecated."
               else:
                   if inspect.isclass(instance):
                       fmt = "The class method {name} is deprecated."
                   else:
                       fmt = "The method {name} is deprecated."
               if self.reason:
                   fmt += " ({reason})"
               if self.version:
                   fmt += " -- Deprecated since version {version}."
               return fmt.format(name=wrapped.__name__,
                                 reason=self.reason or "",
                                 version=self.version or "")

    Then, you can use your ``MyClassicAdapter`` class like this in your source code:

    .. code-block:: python

       @deprecat(reason="use another function", adapter_cls=MyClassicAdapter)
       def some_old_function(x, y):
           return x + y
    """

    def __init__(self, reason="", version="", action=None, deprecated_args=None, category=DeprecationWarning):
        """
        Construct a wrapper adapter.

        :type  reason: str
        :param reason:
            Reason message which documents the deprecation in your library (can be omitted).

        :type  version: str
        :param version:
            Version of your project which deprecates this feature.
            If you follow the `Semantic Versioning <https://semver.org/>`_,
            the version number has the format "MAJOR.MINOR.PATCH".

        :type  action: str
        :param action:
            A warning filter used to activate or not the deprecation warning.
            Can be one of "error", "ignore", "always", "default", "module", or "once".
            If ``None`` or empty, the the global filtering mechanism is used.
            See: `The Warnings Filter`_ in the Python documentation.

        :type deprecated_args: str
        :param deprecated_args:
            String of kwargs to be deprecated, e.g. "x y" to deprecate `x` and `y`.

        :type  category: type
        :param category:
            The warning category to use for the deprecation warning.
            By default, the category class is :class:`~DeprecationWarning`,
            you can inherit this class to define your own deprecation warning category.
        """
        self.reason = reason or ""
        self.version = version or ""
        self.action = action
        self.category = category
        self.deprecated_args=deprecated_args
        super(ClassicAdapter, self).__init__()

    def get_deprecated_msg(self, wrapped, instance, kwargs):
        """
        Get the deprecation warning message for the user.

        :param wrapped: Wrapped class or function.

        :param instance: The object to which the wrapped function was bound when it was called.

        :return: The warning message.
        """
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
        if self.deprecated_args is None:
            name = wrapped.__name__
        if self.deprecated_args is not None:
            fmt = "Call to deprecated Parameter(s) {name}."
            deprecated_args = set(self.deprecated_args.split())
            argstodeprecate = deprecated_args.intersection(kwargs)
            if len(argstodeprecate)!=0:
                name = ", ".join(repr(arg) for arg in argstodeprecate)
            else:
                name=""
        if name=="":
            return None
        if self.reason:
            fmt += " ({reason})"
        if self.version:
            fmt += " -- Deprecated since version {version}."
        return fmt.format(name=name, reason=self.reason or "", version=self.version or "")


    def __call__(self, wrapped):
        """
        Decorate your class or function.

        :param wrapped: Wrapped class or function.

        :return: the decorated class or function.

        .. versionchanged:: 1.2.4
           Don't pass arguments to :meth:`object.__new__` (other than *cls*).

        .. versionchanged:: 1.2.8
           The warning filter is not set if the *action* parameter is ``None`` or empty.
        """
        if inspect.isclass(wrapped):
            old_new1 = wrapped.__new__

            def wrapped_cls(cls, *args, **kwargs):
                msg = self.get_deprecated_msg(wrapped=wrapped, instance=None, kwargs=kwargs)
                if self.action:
                    with warnings.catch_warnings():
                        warnings.simplefilter(self.action, self.category)
                        warnings.warn(msg, category=self.category, stacklevel=_class_stacklevel)
                else:
                    warnings.warn(msg, category=self.category, stacklevel=_class_stacklevel)
                if old_new1 is object.__new__:
                    return old_new1(cls)
                # actually, we don't know the real signature of *old_new1*
                return old_new1(cls, *args, **kwargs)

            wrapped.__new__ = staticmethod(wrapped_cls)

        return wrapped


def deprecat(*args, **kwargs):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.

    **Classic usage:**

    To use this, decorate your deprecated function with **@deprecat** decorator:

    .. code-block:: python

       from deprecat import deprecat


       @deprecat
       def some_old_function(x, y):
           return x + y

    You can also decorate a class or a method:

    .. code-block:: python

       from deprecat import deprecat


       class SomeClass(object):
           @deprecat
           def some_old_method(self, x, y):
               return x + y


       @deprecat
       class SomeOldClass(object):
           pass

    You can give a *reason* message to help the developer to choose another function/class,
    and a *version* number to specify the starting version number of the deprecation.

    .. code-block:: python

       from deprecat import deprecat


       @deprecat(reason="use another function", version='1.2.0')
       def some_old_function(x, y):
           return x + y

    The *category* keyword argument allow you to specify the deprecation warning class of your choice.
    By default, :exc:`DeprecationWarning` is used but you can choose :exc:`FutureWarning`,
    :exc:`PendingDeprecationWarning` or a custom subclass.

    .. code-block:: python

       from deprecat import deprecat


       @deprecat(category=PendingDeprecationWarning)
       def some_old_function(x, y):
           return x + y

    The *action* keyword argument allow you to locally change the warning filtering.
    *action* can be one of "error", "ignore", "always", "default", "module", or "once".
    If ``None``, empty or missing, the the global filtering mechanism is used.
    See: `The Warnings Filter`_ in the Python documentation.

    .. code-block:: python

       from deprecat import deprecat


       @deprecat(action="error")
       def some_old_function(x, y):
           return x + y

    """
    if args and isinstance(args[0], string_types):
        kwargs['reason'] = args[0]
        args = args[1:]

    if args and not callable(args[0]):
        raise TypeError(repr(type(args[0])))

    if args:
        action = kwargs.get('action')
        category = kwargs.get('category', DeprecationWarning)
        adapter_cls = kwargs.pop('adapter_cls', ClassicAdapter)
        adapter = adapter_cls(**kwargs)

        wrapped = args[0]
        if inspect.isclass(wrapped):
            wrapped = adapter(wrapped)
            return wrapped

        elif inspect.isroutine(wrapped):

            @wrapt.decorator(adapter=adapter)
            def wrapper_function(wrapped_, instance_, args_, kwargs_):
                msg = adapter.get_deprecated_msg(wrapped_, instance_, kwargs_)
                if msg:
                    if action:
                        with warnings.catch_warnings():
                            warnings.simplefilter(action, category)
                            warnings.warn(msg, category=category, stacklevel=_routine_stacklevel)
                    else:
                        warnings.warn(msg, category=category, stacklevel=_routine_stacklevel)
                return wrapped_(*args_, **kwargs_)

            return wrapper_function(wrapped)

        else:
            raise TypeError(repr(type(wrapped)))

    return functools.partial(deprecat, **kwargs)
