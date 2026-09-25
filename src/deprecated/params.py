"""
Parameters deprecation
======================

.. _Tantale's Blog: https://tantale.github.io/
.. _Deprecated Parameters: https://tantale.github.io/articles/deprecated_params/

This module introduces a :class:`deprecated_params` decorator to specify that one (or more)
parameter(s) are deprecated: when the user executes a function with a deprecated parameter,
he will see a warning message in the console.

The decorator is customizable, the user can specify the deprecated parameter names
and associate to each of them a message providing the reason of the deprecation.
As with the :func:`~deprecated.classic.deprecated` decorator, the user can specify
a version number (using the *version* parameter) and also define the warning message category
(a subclass of :class:`Warning`) and when to display the messages (using the *action* parameter).

The complete study concerning the implementation of this decorator is available
on the `Tantale's blog`_, on the `Deprecated Parameters`_ page.
"""

import dataclasses
import functools
import inspect
import warnings
from collections.abc import Callable
from typing import Any

from deprecated.classic import SKIP_FILE_PREFIXES

#: Attribute used to mark the wrappers created by :class:`DeprecatedParams`.
_STACK_ATTR = "__deprecated_params__"


@dataclasses.dataclass(frozen=True)
class _DecoratorStack:
    """Stacked :class:`DeprecatedParams` decorators (outermost first) of a function."""

    wrapper: Callable[..., Any]
    decorators: tuple["DeprecatedParams", ...]
    target: Callable[..., Any]


def _get_stack(func: Callable[..., Any]) -> _DecoratorStack | None:
    # The attribute may have been copied by another decorator (with `functools.wraps`):
    # only the wrapper created by `DeprecatedParams` can be merged.
    stack = getattr(func, _STACK_ATTR, None)
    if isinstance(stack, _DecoratorStack) and stack.wrapper is func:
        return stack
    return None


class DeprecatedParams:
    """
    Decorator used to decorate a function which at least one
    of the parameters is deprecated.

    .. versionchanged:: 3.0.0
       When several ``@deprecated_params`` decorators are stacked, only one warning
       is emitted for each deprecated parameter: the one of the outermost decorator.
    """

    def __init__(
        self,
        param: str | dict[str, str],
        reason: str | None = "",
        category: type[Warning] = DeprecationWarning,
    ) -> None:
        self.messages: dict[str, str] = {}
        self.category = category
        self.populate_messages(param, reason=reason)

    def populate_messages(self, param: str | dict[str, str], reason: str | None = "") -> None:
        if isinstance(param, dict):
            self.messages.update(param)
        elif isinstance(param, str):
            self.messages[param] = reason or f"'{param}' parameter is deprecated"
        else:
            raise TypeError(param)

    def check_params(
        self,
        signature: inspect.Signature,
        *args: object,
        **kwargs: object,
    ) -> list[str]:
        binding = signature.bind(*args, **kwargs)
        bound = {**binding.arguments, **binding.kwargs}
        return [param for param in bound if param in self.messages]

    def warn_messages(self, messages: list[str]) -> None:
        # The warnings refer to the first frame outside of this library.
        for message in messages:
            warnings.warn(
                message,
                category=self.category,
                stacklevel=2,
                skip_file_prefixes=SKIP_FILE_PREFIXES,
            )

    def __call__[**P, R](self, f: Callable[P, R]) -> Callable[P, R]:
        # Merge with an inner `@deprecated_params` decorator, if any,
        # to emit a single warning for each deprecated parameter.
        inner = _get_stack(f)
        decorators = (self, *inner.decorators) if inner else (self,)
        target: Callable[P, R] = inner.target if inner else f
        signature = inspect.signature(target)

        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            warned: set[str] = set()
            for decorator in decorators:
                params = [
                    param
                    for param in decorator.check_params(signature, *args, **kwargs)
                    if param not in warned
                ]
                warned.update(params)
                decorator.warn_messages([decorator.messages[param] for param in params])
            return target(*args, **kwargs)

        setattr(wrapper, _STACK_ATTR, _DecoratorStack(wrapper, decorators, target))
        return wrapper


#: Decorator used to decorate a function which at least one
#: of the parameters is deprecated.
deprecated_params = DeprecatedParams
