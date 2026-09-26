"""
Classic deprecation warning
===========================

Classic ``@deprecated`` decorator to deprecate old python classes, functions or methods.

.. _The Warnings Filter: https://docs.python.org/3/library/warnings.html#the-warnings-filter
"""

import functools
import importlib
import inspect
import os
import pickle
import warnings
from collections.abc import Callable
from typing import Any
from typing import Literal
from typing import SupportsIndex
from typing import cast
from typing import overload

import wrapt

#: Frames of these packages are skipped when computing the location of a warning,
#: so the warning always refers to the user code, whatever the wrapt implementation
#: (C extension or pure Python) and the number of nested deprecated wrappers.
SKIP_FILE_PREFIXES: tuple[str, ...] = tuple(
    os.path.dirname(module_file) + os.sep for module_file in (__file__, wrapt.__file__)
)

#: Warning filter action, see: `The Warnings Filter`_ in the Python documentation.
type WarningAction = Literal["default", "error", "ignore", "always", "module", "once"]

#: Object which can be decorated: a class, a function or a method.
type Deprecatable = Callable[..., Any]


def _resolve_wrapper(module_name: str, qualname: str) -> object:
    """
    Find a deprecated routine by its qualified name in its module (used to unpickle it).

    The attributes are read with :func:`inspect.getattr_static`, so that the wrapper
    stored in a class is returned as is, instead of a new wrapper bound at each access.

    :param module_name: Name of the module which defines the routine.
    :param qualname: Qualified name of the routine in its module.
    :return: The wrapper of the deprecated routine.
    """
    obj: object = importlib.import_module(module_name)
    for name in qualname.split("."):
        obj = inspect.getattr_static(obj, name)
        if isinstance(obj, (staticmethod, classmethod)):
            obj = obj.__func__
    return obj


# The wrapt classes are only generic in the type stubs (they can't be subscripted at runtime).
class _DeprecatedBoundFunctionWrapper(wrapt.BoundFunctionWrapper):  # type: ignore[type-arg]
    """
    Bound wrapper of a deprecated method, which can be pickled like a bound method.

    wrapt proxies refuse to be pickled: a deprecated method bound to an instance
    (or a class method bound to its class) is pickled by reference,
    as ``getattr(instance, name)``, like a regular bound method.
    A method accessed from its class (not bound) is pickled as its parent wrapper.
    """

    def __reduce_ex__(self, protocol: SupportsIndex) -> tuple[Any, ...]:
        instance = self._self_instance
        if instance is None:
            return cast(tuple[Any, ...], self._self_parent.__reduce_ex__(protocol))
        return getattr, (instance, self.__name__)

    def __reduce__(self) -> tuple[Any, ...]:
        return self.__reduce_ex__(pickle.DEFAULT_PROTOCOL)


class _DeprecatedFunctionWrapper(wrapt.FunctionWrapper):  # type: ignore[type-arg]
    """
    Wrapper of a deprecated routine, which can be pickled like the routine itself.

    wrapt proxies refuse to be pickled, so a deprecated function could not be sent to a
    child process by :mod:`multiprocessing` (the default *spawn* start method on Windows
    and macOS). The wrapper is pickled by reference, like a regular function:
    it is found again by its qualified name in its module when it is unpickled.
    """

    __bound_function_wrapper__ = _DeprecatedBoundFunctionWrapper

    def __reduce_ex__(self, protocol: SupportsIndex) -> tuple[Any, ...]:
        module_name = str(self.__module__)
        qualname = str(self.__qualname__)
        # Like a regular function, fail early if the routine can't be found by its name
        # (a local function, or a wrapper which is not stored under its own name).
        try:
            found = _resolve_wrapper(module_name, qualname)
        except (ImportError, AttributeError) as exc:
            msg = f"Can't pickle {self!r}: it's not found as {module_name}.{qualname}"
            raise pickle.PicklingError(msg) from exc
        if found is not self:
            msg = f"Can't pickle {self!r}: it's not the same object as {module_name}.{qualname}"
            raise pickle.PicklingError(msg)
        return _resolve_wrapper, (module_name, qualname)

    def __reduce__(self) -> tuple[Any, ...]:
        return self.__reduce_ex__(pickle.DEFAULT_PROTOCOL)


class ClassicAdapter(wrapt.AdapterFactory):
    """
    Classic adapter -- *for advanced usage only*

    This adapter is used to get the deprecation message according to the wrapped object type:
    class, function, standard method, static method, or class method.

    This is the base class of the :class:`~deprecated.sphinx.SphinxAdapter` class
    which is used to update the wrapped object docstring.

    You can also inherit this class to change the deprecation message.

    In the following example, we change the message into "The ... is deprecated.":

    .. code-block:: python

       import inspect

       from deprecated.classic import ClassicAdapter
       from deprecated.classic import deprecated


       class MyClassicAdapter(ClassicAdapter):
           def get_deprecated_msg(self, wrapped: Deprecatable, instance: object | None) -> str:
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
               return fmt.format(
                   name=wrapped.__name__, reason=self.reason or "", version=self.version or ""
               )

    Then, you can use your ``MyClassicAdapter`` class like this in your source code:

    .. code-block:: python

       @deprecated(reason="use another function", adapter_cls=MyClassicAdapter)
       def some_old_function(x, y):
           return x + y
    """

    def __init__(
        self,
        reason: str | None = "",
        version: str | None = "",
        action: WarningAction | Literal[""] | None = None,
        category: type[Warning] = DeprecationWarning,
        extra_stacklevel: int = 0,
    ) -> None:
        """
        Construct a wrapper adapter.

        :type  reason: str | None
        :param reason:
            Reason message which documents the deprecation in your library (can be omitted).

        :type  version: str
        :param version:
            Version of your project which deprecates this feature.
            If you follow the `Semantic Versioning <https://semver.org/>`_,
            the version number has the format "MAJOR.MINOR.PATCH".

        :type  action: Literal["default", "error", "ignore", "always", "module", "once"]
        :param action:
            A warning filter used to activate or not the deprecation warning.
            Can be one of "error", "ignore", "always", "default", "module", or "once".
            If ``None`` or empty, the global filtering mechanism is used.
            See: `The Warnings Filter`_ in the Python documentation.

        :type  category: Type[Warning]
        :param category:
            The warning category to use for the deprecation warning.
            By default, the category class is :class:`~DeprecationWarning`,
            you can inherit this class to define your own deprecation warning category.

        :type  extra_stacklevel: int
        :param extra_stacklevel:
            Number of additional stack levels to consider instrumentation rather than user code.
            With the default value of 0, the warning refers to where the class was instantiated
            or the function was called.

        .. versionchanged:: 1.2.15
            Add the *extra_stacklevel* parameter.
        """
        self.reason = reason or ""
        self.version = version or ""
        self.action = action
        self.category = category
        self.extra_stacklevel = extra_stacklevel
        super().__init__()

    def get_deprecated_msg(self, wrapped: Deprecatable, instance: object | None) -> str:
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
        if self.reason:
            fmt += " ({reason})"
        if self.version:
            fmt += " -- Deprecated since version {version}."
        # Only classes and routines are decorated: they always have a `__name__`.
        name = wrapped.__name__  # ty: ignore[unresolved-attribute]
        return fmt.format(name=name, reason=self.reason or "", version=self.version or "")

    def warn(self, msg: str) -> None:
        """
        Emit the deprecation warning, using the *action* filter if any.

        The warning refers to the first frame outside of this library
        (see :data:`SKIP_FILE_PREFIXES`), plus *extra_stacklevel* frames.

        :param msg: The warning message.

        .. versionadded:: 3.0.0
        """
        stacklevel = 2 + self.extra_stacklevel
        if self.action:
            with warnings.catch_warnings():
                warnings.simplefilter(self.action, self.category)
                warnings.warn(
                    msg,
                    category=self.category,
                    stacklevel=stacklevel,
                    skip_file_prefixes=SKIP_FILE_PREFIXES,
                )
        else:
            warnings.warn(
                msg,
                category=self.category,
                stacklevel=stacklevel,
                skip_file_prefixes=SKIP_FILE_PREFIXES,
            )

    def __call__[T: Deprecatable](self, wrapped: T) -> T:
        """
        Decorate your class or function.

        :param wrapped: Wrapped class or function.

        :return: the decorated class or function.

        .. versionchanged:: 1.2.4
           Don't pass arguments to :meth:`object.__new__` (other than *cls*).

        .. versionchanged:: 1.2.8
           The warning filter is not set if the *action* parameter is ``None`` or empty.

        .. versionchanged:: 3.0.0
           A deprecated function or method can be pickled (by reference, like a regular
           function), so it can be used with :mod:`multiprocessing`.
        """
        if inspect.isclass(wrapped):
            old_new1 = wrapped.__new__

            def wrapped_cls(cls: type, *args: Any, **kwargs: Any) -> object:
                self.warn(self.get_deprecated_msg(wrapped, None))
                if old_new1 is object.__new__:
                    return old_new1(cls)
                # actually, we don't know the real signature of *old_new1*
                return old_new1(cls, *args, **kwargs)

            # `__new__` is patched on purpose: `setattr` avoids a type checker error.
            setattr(wrapped, "__new__", staticmethod(wrapped_cls))  # noqa: B010

        elif inspect.isroutine(wrapped):

            @wrapt.decorator(proxy=_DeprecatedFunctionWrapper)
            def wrapper_function(
                wrapped_: Callable[..., Any],
                instance_: object | None,
                args_: tuple[Any, ...],
                kwargs_: dict[str, Any],
            ) -> object:
                self.warn(self.get_deprecated_msg(wrapped_, instance_))
                return wrapped_(*args_, **kwargs_)

            # The function wrapper is a transparent proxy of the wrapped routine.
            return cast(T, wrapper_function(wrapped))

        else:  # pragma: no cover
            raise TypeError(repr(type(wrapped)))

        return wrapped


@overload
def deprecated[T: Deprecatable](wrapped: T, /) -> T: ...


@overload
def deprecated[T: Deprecatable](
    reason: str | None = "",
    /,
    *,
    version: str | None = "",
    action: WarningAction | Literal[""] | None = None,
    category: type[Warning] = DeprecationWarning,
    extra_stacklevel: int = 0,
    adapter_cls: type[ClassicAdapter] = ...,
    **kwargs: Any,
) -> Callable[[T], T]: ...


def deprecated(*args: Any, **kwargs: Any) -> Any:
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


       class SomeClass:
           @deprecated
           def some_old_method(self, x, y):
               return x + y


       @deprecated
       class SomeOldClass:
           pass

    You can give a *reason* message to help the developer to choose another function/class,
    and a *version* number to specify the starting version number of the deprecation.

    .. code-block:: python

       from deprecated import deprecated


       @deprecated(reason="use another function", version="1.2.0")
       def some_old_function(x, y):
           return x + y

    The *category* keyword argument allow you to specify the deprecation warning class
    of your choice. By default, :exc:`DeprecationWarning` is used, but you can choose
    :exc:`FutureWarning`, :exc:`PendingDeprecationWarning` or a custom subclass.

    .. code-block:: python

       from deprecated import deprecated


       @deprecated(category=PendingDeprecationWarning)
       def some_old_function(x, y):
           return x + y

    The *action* keyword argument allow you to locally change the warning filtering.
    *action* can be one of "error", "ignore", "always", "default", "module", or "once".
    If ``None``, empty or missing, the global filtering mechanism is used.
    See: `The Warnings Filter`_ in the Python documentation.

    .. code-block:: python

       from deprecated import deprecated


       @deprecated(action="error")
       def some_old_function(x, y):
           return x + y

    The *extra_stacklevel* keyword argument allows you to specify additional stack levels
    to consider instrumentation rather than user code. With the default value of 0, the
    warning refers to where the class was instantiated or the function was called.
    """
    # Note: a `bytes` reason is still accepted for backward compatibility with Python 2
    # (where `str` was `bytes`), but only `str` is documented and typed.
    if args and isinstance(args[0], (str, bytes)):
        kwargs["reason"] = args[0]
        args = args[1:]

    if args and not callable(args[0]):
        raise TypeError(repr(type(args[0])))

    if args:
        adapter_cls = kwargs.pop("adapter_cls", ClassicAdapter)
        adapter = adapter_cls(**kwargs)
        wrapped = args[0]
        return adapter(wrapped)

    return functools.partial(deprecated, **kwargs)
