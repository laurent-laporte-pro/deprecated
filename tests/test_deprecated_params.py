# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import warnings

import pytest

from deprecated import deprecated_params

PY3 = sys.version_info[0] == 3
PY38 = sys.version_info[0:2] >= (3, 8)


# This example shows a function with an unused optional parameter. A warning
# message should be emitted if `z` is used (as a positional or keyword parameter).

if PY38:
    # Positional-Only Arguments are only available for Python >= 3
    # On other version, this code raises a SyntaxError exception.
    exec (
        """
@deprecated_params("z")
def pow2(x, y, z=None, /):
    return x ** y
        """
    )

else:

    @deprecated_params("z")
    def pow2(x, y, z=None):
        return x ** y


@pytest.mark.parametrize(
    "args, kwargs, expected",
    [
        pytest.param((5, 6), {}, [], id="'z' not used: no warnings"),
        pytest.param(
            (5, 6, 8),
            {},
            ["'z' parameter is deprecated"],
            id="'z' used in positional params",
        ),
        pytest.param(
            (5, 6),
            {"z": 8},
            ["'z' parameter is deprecated"],
            id="'z' used in keyword params",
            marks=pytest.mark.skipif(PY38, reason="'z' parameter is positional only"),
        ),
    ],
)
def test_pow2(args, kwargs, expected):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        pow2(*args, **kwargs)
    actual = [str(warn.message) for warn in warns]
    assert actual == expected


# This example shows a function with a keyword-only parameter. A warning
# message should be emitted if `key` is used (as a positional or keyword parameter).

if PY3:
    # Keyword-Only Arguments are only available for Python >= 3
    # On Python 2.7, this code raises a SyntaxError exception.
    exec (
        """
@deprecated_params({"key": "Parameter 'key' should be avoided for security reasons"})
def compare(a, b, *, key=None):
    if key is None:
        return a < b
    return key(a) < key(b)
        """
    )

else:

    @deprecated_params({"key": "Parameter 'key' should be avoided for security reasons"})
    def compare(a, b, key=None):
        if key is None:
            return a < b
        return key(a) < key(b)


@pytest.mark.parametrize(
    "args, kwargs, expected",
    [
        pytest.param(("a", "B"), {}, [], id="'key' not used: no warnings"),
        pytest.param(
            (
                [2, 1],
                [1, 2],
            ),
            {"key": lambda i: i.pop()},
            ["Parameter 'key' should be avoided for security reasons"],
            id="'key' used in keyword-argument",
        ),
    ],
)
def test_compare(args, kwargs, expected):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        compare(*args, **kwargs)
    actual = [str(warn.message) for warn in warns]
    assert actual == expected


# This example shows how to implement a function that accepts two positional
# arguments or two keyword arguments. A warning message should be emitted
# if `x` and `y` are used instead of `width` and `height`.


@deprecated_params(
    {
        "x": "use `width` instead or `x`",
        "y": "use `height` instead or `y`",
    },
)
def area(*args, **kwargs):
    def _area_impl(width, height):
        return width * height

    if args:
        # positional arguments (no checking)
        return _area_impl(*args)
    elif set(kwargs) == {"width", "height"}:
        # nominal case: no warning
        return _area_impl(kwargs["width"], kwargs["height"])
    elif set(kwargs) == {"x", "y"}:
        # old case: deprecation warning
        return _area_impl(kwargs["x"], kwargs["y"])
    else:
        raise TypeError("invalid arguments")


@pytest.mark.parametrize(
    "args, kwargs, expected",
    [
        pytest.param((4, 6), {}, [], id="positional arguments: no warning"),
        pytest.param((), {"width": 3, "height": 6}, [], id="correct keyword arguments"),
        pytest.param(
            (),
            {"x": 2, "y": 7},
            ['use `width` instead or `x`', 'use `height` instead or `y`'],
            id="wrong keyword arguments",
        ),
        pytest.param(
            (),
            {"x": 2, "height": 7},
            [],
            id="invalid arguments is raised",
            marks=pytest.mark.xfail(raises=TypeError, strict=True),
        ),
    ],
)
def test_area(args, kwargs, expected):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        area(*args, **kwargs)
    actual = [str(warn.message) for warn in warns]
    assert actual == expected
