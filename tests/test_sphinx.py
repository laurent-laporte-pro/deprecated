# coding: utf-8
from __future__ import print_function

import warnings

from deprecated.sphinx import deprecated
from deprecated.sphinx import versionadded
from deprecated.sphinx import versionchanged


def test_versionadded_has_docstring(with_docstring):
    reason = "This is a new feature"
    version = "1.2.0"
    f = versionadded(reason=reason, version=version)(with_docstring)
    assert ".. versionadded:: {0}".format(version) in f.__doc__
    assert reason in f.__doc__


def test_versionchanged_has_docstring(with_docstring):
    reason = "The feature has changed"
    version = "1.3.0"
    f = versionchanged(reason=reason, version=version)(with_docstring)
    assert ".. versionchanged:: {0}".format(version) in f.__doc__
    assert reason in f.__doc__


def test_deprecated_has_docstring(with_docstring):
    reason = "You should not use it anymore"
    version = "1.4.0"
    f = deprecated(reason=reason, version=version)(with_docstring)
    assert ".. deprecated:: {0}".format(version) in f.__doc__
    assert reason in f.__doc__


def test_sphinx_deprecated_function__warns(sphinx_deprecated_function):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        sphinx_deprecated_function()
        assert len(warns) == 1
        warn = warns[0]
        assert issubclass(warn.category, DeprecationWarning)
        assert "deprecated function (or staticmethod)" in str(warn.message)


def test_sphinx_deprecated_class__warns(sphinx_deprecated_class):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        sphinx_deprecated_class()
        assert len(warns) == 1
        warn = warns[0]
        assert issubclass(warn.category, DeprecationWarning)
        assert "deprecated class" in str(warn.message)


def test_sphinx_deprecated_method__warns(sphinx_deprecated_method):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        obj = sphinx_deprecated_method()
        obj.foo()
        assert len(warns) == 1
        warn = warns[0]
        assert issubclass(warn.category, DeprecationWarning)
        assert "deprecated method" in str(warn.message)


def test_sphinx_deprecated_static_method__warns(sphinx_deprecated_static_method):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        sphinx_deprecated_static_method()
        assert len(warns) == 1
        warn = warns[0]
        assert issubclass(warn.category, DeprecationWarning)
        assert "deprecated function (or staticmethod)" in str(warn.message)
