"""
This example shows a function with an unused optional parameter. A warning
message should be emitted if `z` is used (as a positional or keyword parameter).
"""

import functools
import warnings

from deprecated.params import deprecated_params


class V2DeprecationWarning(DeprecationWarning):
    pass


# noinspection PyUnusedLocal
@deprecated_params(
    {
        "epsilon": "epsilon is deprecated in version v2",
        "start": "start is removed in version v2",
    },
    category=V2DeprecationWarning,
)
@deprecated_params("epsilon", reason="epsilon is deprecated in version v1.1")
def integrate(f, a, b, n=0, epsilon=0.0, start=None):
    epsilon = epsilon or (b - a) / n
    n = n or int((b - a) / epsilon)
    return sum(
        (f(a + (i * epsilon)) + f(a + (i * epsilon) + epsilon)) * epsilon / 2 for i in range(n)
    )


def test_only_one_warning_for_each_parameter():
    """
    This unit test checks that only one warning message is emitted for each deprecated parameter:
    the message of the outermost decorator wins (here, the `epsilon` message of version v2).
    """
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        integrate(lambda x: x**2, 0, 2, epsilon=0.0012, start=123)
    actual = [{"message": str(w.message), "category": w.category} for w in warns]
    assert actual == [
        {"category": V2DeprecationWarning, "message": "epsilon is deprecated in version v2"},
        {"category": V2DeprecationWarning, "message": "start is removed in version v2"},
    ]
    # The warnings refer to the caller, not to the library.
    assert {w.filename for w in warns} == {__file__}


def test_inner_decorator_messages_are_kept():
    # A parameter only deprecated by the inner decorator is still reported.
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        integrate(lambda x: x**2, 0, 2, n=10)
    assert warns == []


@deprecated_params("b", reason="outer b", category=V2DeprecationWarning)
@deprecated_params({"a": "inner a", "b": "inner b"})
def combine(a=None, b=None, c=None):
    return a, b, c


def test_stacked_decorators_are_merged():
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        assert combine(a=1, b=2, c=3) == (1, 2, 3)
    assert [(str(w.message), w.category) for w in warns] == [
        ("outer b", V2DeprecationWarning),
        ("inner a", DeprecationWarning),
    ]
    assert combine.__name__ == "combine"


def test_other_decorator_between_deprecated_params_is_called():
    calls = []

    def spy(func):
        @functools.wraps(func)  # copies the marker attribute of the inner wrapper
        def spy_wrapper(*args, **kwargs):
            calls.append(kwargs)
            return func(*args, **kwargs)

        return spy_wrapper

    @deprecated_params("b", reason="outer b")
    @spy
    @deprecated_params("a", reason="inner a")
    def foo(a=None, b=None):
        return a, b

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        assert foo(a=1, b=2) == (1, 2)
    assert calls == [{"a": 1, "b": 2}]
    assert [str(w.message) for w in warns] == ["outer b", "inner a"]
