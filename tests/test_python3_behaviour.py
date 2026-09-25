"""
Non-regression tests for behaviours which differ between Python 2 and Python 3.

These tests secure the migration to Python 3.12+: text/bytes handling, dictionary
ordering (formerly ``collections.OrderedDict``), keyword-only/variadic parameters
and the static typing of the public decorators.
"""

import warnings
from collections.abc import Callable
from typing import assert_type

import pytest

import deprecated.classic
import deprecated.sphinx
from deprecated.params import deprecated_params


def _record_messages(func: Callable[..., object], *args: object, **kwargs: object) -> list[str]:
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        func(*args, **kwargs)
    return [str(warn.message) for warn in warns]


class TestTextAndBytes:
    def test_warning_message_is_str(self):
        @deprecated.classic.deprecated("Good reason", version="1.2.3")
        def foo():
            pass

        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter("always")
            foo()
        message = warns[0].message
        assert isinstance(message, DeprecationWarning)
        assert isinstance(message.args[0], str)

    def test_non_ascii_reason_is_preserved(self):
        reason = "Utilisez « bar() » à la place — 使用 bar"

        @deprecated.classic.deprecated(reason=reason)
        def foo():
            pass

        assert _record_messages(foo) == [
            f"Call to deprecated function (or staticmethod) foo. ({reason})"
        ]

    def test_non_ascii_reason_in_sphinx_docstring(self):
        reason = "Utilisez « bar() » à la place"

        @deprecated.sphinx.deprecated(reason=reason, version="1.0")
        def foo():
            """Fonction dépréciée."""

        assert foo.__doc__ == f"Fonction dépréciée.\n\n.. deprecated:: 1.0\n   {reason}\n"

    def test_bytes_positional_reason_is_still_accepted(self):
        # With Python 2, ``str`` was ``bytes``: a byte string reason was accepted.
        # This (undocumented) behaviour is kept: the reason is formatted with ``str.format``.
        decorator = deprecated.classic.deprecated(b"old reason")  # type: ignore[call-overload]

        @decorator
        def foo():
            pass

        assert _record_messages(foo) == [
            "Call to deprecated function (or staticmethod) foo. (b'old reason')"
        ]


class TestDeprecatedParams:
    def test_messages_follow_the_parameters_order(self):
        # ``collections.OrderedDict`` was replaced by a plain ``dict`` (ordered since Python 3.7).
        @deprecated_params({"b": "b is deprecated", "a": "a is deprecated"})
        def foo(a=None, b=None):
            pass

        assert _record_messages(foo, a=1, b=2) == ["a is deprecated", "b is deprecated"]
        assert _record_messages(foo, b=2, a=1) == ["a is deprecated", "b is deprecated"]

    def test_variadic_keyword_parameters_are_checked(self):
        @deprecated_params("old")
        def foo(**kwargs):
            return kwargs

        assert _record_messages(foo, old=1, new=2) == ["'old' parameter is deprecated"]

    def test_keyword_only_parameter(self):
        @deprecated_params("old", reason="use 'new'")
        def foo(*, old=None, new=None):
            return old or new

        assert _record_messages(foo, new=1) == []
        assert _record_messages(foo, old=1) == ["use 'new'"]

    def test_wrapper_preserves_metadata_and_result(self):
        @deprecated_params("z")
        def add(x: int, y: int, z: int = 0) -> int:
            """Add two numbers."""
            return x + y + z

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert add(1, 2, z=3) == 6
        assert add.__name__ == "add"
        assert add.__doc__ == "Add two numbers."

    @pytest.mark.parametrize("param", [b"z", 5, ["z"]])
    def test_invalid_param_type_raises_type_error(self, param):
        with pytest.raises(TypeError):
            deprecated_params(param)


class TestStaticTyping:
    """These assertions are checked by mypy (``hatch check types``) and at runtime."""

    def test_classic_decorator_preserves_the_signature(self):
        @deprecated.classic.deprecated
        def foo(x: int) -> str:
            return str(x)

        @deprecated.classic.deprecated(reason="use bar", version="1.0")
        def bar(x: int) -> str:
            return str(x)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # `assert_type` fails if the decorator leaks `Any`.
            assert assert_type(foo(1), str) == "1"
            assert assert_type(bar(1), str) == "1"

    def test_class_decorator_preserves_the_class(self):
        @deprecated.classic.deprecated(reason="use Bar")
        class Foo:
            pass

        assert_type(Foo, type[Foo])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert isinstance(assert_type(Foo(), Foo), Foo)

    def test_deprecated_params_preserves_the_signature(self):
        @deprecated_params("y")
        def foo(x: int, y: int = 0) -> int:
            return x + y

        assert assert_type(foo(1), int) == 1
