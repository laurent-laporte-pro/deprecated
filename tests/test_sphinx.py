# coding: utf-8
from __future__ import print_function

import warnings

import pytest

from deprecated.sphinx import deprecated
from deprecated.sphinx import versionadded
from deprecated.sphinx import versionchanged


@pytest.fixture(scope="module",
                params=[None,
                        """This function adds *x* and *y*.""",
                        """
                        This function adds *x* and *y*.

                        :param x: number *x*
                        :param y: number *y*
                        :return: sum = *x* + *y*
                        """
                        ])
def a_function(request):
    def add(x, y):
        return x + y

    add.__doc__ = request.param

    return add


# noinspection PyShadowingNames
def test_versionadded(a_function):
    reason = "This is a new feature"
    version = "1.2.0"
    f = versionadded(reason=reason, version=version)(a_function)
    assert ".. versionadded:: {0}".format(version) in f.__doc__
    assert reason in f.__doc__
    assert f(3, 4) == 7


# noinspection PyShadowingNames
def test_versionchanged(a_function):
    reason = "The feature has changed"
    version = "1.3.0"
    f = versionchanged(reason=reason, version=version)(a_function)
    assert ".. versionchanged:: {0}".format(version) in f.__doc__
    assert reason in f.__doc__
    assert f(3, 4) == 7


# noinspection PyShadowingNames
def test_deprecated(a_function):
    reason = "You should not use it anymore"
    version = "1.4.0"
    f = deprecated(reason=reason, version=version)(a_function)
    assert ".. deprecated:: {0}".format(version) in f.__doc__
    assert reason in f.__doc__
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        assert f(3, 4) == 7
        assert len(warns) == 1
        warn = warns[0]
        assert issubclass(warn.category, DeprecationWarning)
        assert "deprecated" in str(warn.message)
