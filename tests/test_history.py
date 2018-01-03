# coding: utf-8
from __future__ import print_function

import pytest

from deprecated.history import versionadded, versionchanged, deprecated


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
    assert f(3, 4) == 7
