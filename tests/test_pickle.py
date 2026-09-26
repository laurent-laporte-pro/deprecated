"""
Pickling of deprecated routines, and use with :mod:`multiprocessing` (issue #16).

The deprecated routines must be defined at module level, so that they can be pickled
by reference and found again when they are unpickled (in the same or in a child process).
"""

import multiprocessing
import pickle
import warnings

import pytest

import deprecated.classic
import deprecated.google
import deprecated.numpy
import deprecated.sphinx
from deprecated.params import deprecated_params


@deprecated.classic.deprecated(reason="use new_function")
def old_function(x):
    return x * 2


@deprecated.sphinx.deprecated(version="1.2.3", reason="use new_function")
def old_sphinx_function(x):
    return x * 3


@deprecated.google.deprecated(version="1.2.3", reason="use new_function")
def old_google_function(x):
    return x * 4


@deprecated.numpy.deprecated(version="1.2.3", reason="use new_function")
def old_numpy_function(x):
    return x * 5


@deprecated_params("y", reason="y is ignored")
def function_with_deprecated_params(x, y=None):
    return x


class Foo:
    def __init__(self, value=1):
        self.value = value

    @deprecated.classic.deprecated
    def old_method(self, x):
        return self.value + x

    @classmethod
    @deprecated.classic.deprecated
    def old_class_method(cls, x):
        return x + 10

    @staticmethod
    @deprecated.classic.deprecated
    def old_static_method(x):
        return x + 30


def _round_trip(obj):
    for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
        clone = pickle.loads(pickle.dumps(obj, protocol=protocol))
    return clone


@pytest.mark.parametrize(
    ("func", "expected"),
    [
        (old_function, 2),
        (old_sphinx_function, 3),
        (old_google_function, 4),
        (old_numpy_function, 5),
    ],
    ids=["classic", "sphinx", "google", "numpy"],
)
def test_pickle_deprecated_function(func, expected):
    clone = _round_trip(func)
    # Pickled by reference, like a regular function.
    assert clone is func
    with pytest.warns(DeprecationWarning, match="deprecated"):
        assert clone(1) == expected


def test_pickle_function_with_deprecated_params():
    clone = _round_trip(function_with_deprecated_params)
    assert clone is function_with_deprecated_params
    with pytest.warns(DeprecationWarning, match="y is ignored"):
        assert clone(1, y=2) == 1


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("old_class_method", 11),
        ("old_static_method", 31),
    ],
)
def test_pickle_deprecated_class_level_method(name, expected):
    for owner in (Foo, Foo(5)):
        clone = _round_trip(getattr(owner, name))
        with pytest.warns(DeprecationWarning, match="deprecated"):
            assert clone(1) == expected


def test_pickle_deprecated_unbound_method():
    clone = _round_trip(Foo.old_method)
    # wrapt creates a new (unbound) wrapper at each access: compare the wrapped functions.
    assert clone.__wrapped__ is Foo.old_method.__wrapped__  # type: ignore[attr-defined]
    with pytest.warns(DeprecationWarning, match="deprecated"):
        assert clone(Foo(5), 1) == 6


def test_pickle_deprecated_bound_method():
    clone = _round_trip(Foo(5).old_method)
    # The instance is pickled with the bound method.
    assert clone.__self__.value == 5
    with pytest.warns(DeprecationWarning, match="deprecated"):
        assert clone(1) == 6


def test_pickle_local_deprecated_function():
    # Like a regular local function, a local deprecated function can't be pickled by reference.
    @deprecated.classic.deprecated
    def local_function():
        pass

    with pytest.raises(pickle.PicklingError):
        pickle.dumps(local_function)


def _call_old_function(x):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = old_function(x)
    return result, [str(w.message) for w in caught]


def test_deprecated_function_with_spawn_pool():
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(1) as pool:
        # The deprecated function itself is sent to the child process...
        assert pool.map(old_function, [1, 2]) == [2, 4]
        # ... and it still emits the deprecation warning there.
        result, messages = pool.apply(_call_old_function, (21,))
    assert result == 42
    assert messages == [
        "Call to deprecated function (or staticmethod) old_function. (use new_function)"
    ]


def test_deprecated_function_as_spawn_process_target():
    ctx = multiprocessing.get_context("spawn")
    process = ctx.Process(target=old_function, args=(1,))
    process.start()
    process.join(timeout=60)
    assert process.exitcode == 0
