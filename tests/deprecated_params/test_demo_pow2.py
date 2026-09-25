"""
This example shows a function with an unused optional parameter. A warning
message should be emitted if `z` is used (as a positional or keyword parameter).
"""

import warnings

import pytest

from deprecated.params import deprecated_params


@deprecated_params("z")
def pow2(x, y, z=None, /):
    return x**y


@pytest.mark.parametrize(
    ("args", "kwargs", "expected"),
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
            [],
            id="'z' is positional only: keyword usage is rejected",
            marks=pytest.mark.xfail(raises=TypeError, strict=True),
        ),
    ],
)
def test_pow2(args, kwargs, expected):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        pow2(*args, **kwargs)
    actual = [str(warn.message) for warn in warns]
    assert actual == expected
