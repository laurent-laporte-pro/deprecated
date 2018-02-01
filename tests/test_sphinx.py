# coding: utf-8
from __future__ import print_function

import sys
import textwrap
import warnings

import deprecated.sphinx
import pytest


@pytest.fixture(scope="module",
                params=[None,
                        """This function adds *x* and *y*.""",
                        """
                        This function adds *x* and *y*.

                        :param x: number *x*
                        :param y: number *y*
                        :return: sum = *x* + *y*
                        """])
def docstring(request):
    return request.param


@pytest.fixture(scope="module",
                params=['versionadded', 'versionchanged', 'deprecated'])
def directive(request):
    return request.param


# noinspection PyShadowingNames
@pytest.mark.parametrize("reason, version, expected", [
    ('A good reason',
     '1.2.0',
     textwrap.dedent("""\
                     .. {directive}:: {version}
                        {reason}
                     """)),
    (None,
     '1.2.0',
     textwrap.dedent("""\
                     .. {directive}:: {version}
                     """)),
    ('A good reason',
     None,
     textwrap.dedent("""\
                 .. {directive}::
                    {reason}
                 """)),
])
def test_has_sphinx_docstring(docstring, directive, reason, version, expected):
    # The function:
    def foo(x, y):
        return x + y

    # with docstring:
    foo.__doc__ = docstring

    # is decorated with:
    decorator_factory = getattr(deprecated.sphinx, directive)
    decorator = decorator_factory(reason=reason, version=version)
    foo = decorator(foo)

    # The function must contains this Sphinx docstring:
    expected = expected.format(directive=directive, version=version, reason=reason)

    current = textwrap.dedent(foo.__doc__)
    assert current.endswith(expected)


class MyDeprecationWarning(DeprecationWarning):
    pass


_PARAMS = [None,
           ((), {}),
           (('Good reason',), {}),
           ((), {'reason': 'Good reason'}),
           ((), {'version': '1.2.3'}),
           ((), {'action': 'once'}),
           ((), {'category': MyDeprecationWarning}),
           ]


@pytest.fixture(scope="module", params=_PARAMS)
def sphinx_deprecated_function(request):
    if request.param is None:
        @deprecated.sphinx.deprecated
        def foo():
            pass

        return foo
    else:
        args, kwargs = request.param

        @deprecated.sphinx.deprecated(*args, **kwargs)
        def foo():
            pass

        return foo


@pytest.fixture(scope="module", params=_PARAMS)
def sphinx_deprecated_class(request):
    if request.param is None:
        @deprecated.sphinx.deprecated
        class Foo(object):
            pass

        return Foo
    else:
        args, kwargs = request.param

        @deprecated.sphinx.deprecated(*args, **kwargs)
        class Foo(object):
            pass

        return Foo


@pytest.fixture(scope="module", params=_PARAMS)
def sphinx_deprecated_method(request):
    if request.param is None:
        class Foo(object):
            @deprecated.sphinx.deprecated
            def foo(self):
                pass

        return Foo
    else:
        args, kwargs = request.param

        class Foo(object):
            @deprecated.sphinx.deprecated(*args, **kwargs)
            def foo(self):
                pass

        return Foo


@pytest.fixture(scope="module", params=_PARAMS)
def sphinx_deprecated_static_method(request):
    if request.param is None:
        class Foo(object):
            @staticmethod
            @deprecated.sphinx.deprecated
            def foo():
                pass

        return Foo.foo
    else:
        args, kwargs = request.param

        class Foo(object):
            @staticmethod
            @deprecated.sphinx.deprecated(*args, **kwargs)
            def foo():
                pass

        return Foo.foo


@pytest.fixture(scope="module", params=_PARAMS)
def sphinx_deprecated_class_method(request):
    if request.param is None:
        class Foo(object):
            @classmethod
            @deprecated.sphinx.deprecated
            def foo(cls):
                pass

        return Foo
    else:
        args, kwargs = request.param

        class Foo(object):
            @classmethod
            @deprecated.sphinx.deprecated(*args, **kwargs)
            def foo(cls):
                pass

        return Foo


# noinspection PyShadowingNames
def test_sphinx_deprecated_function__warns(sphinx_deprecated_function):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        sphinx_deprecated_function()
    assert len(warns) == 1
    warn = warns[0]
    assert issubclass(warn.category, DeprecationWarning)
    assert "deprecated function (or staticmethod)" in str(warn.message)


# noinspection PyShadowingNames
@pytest.mark.skipif(sys.version_info < (3, 3),
                    reason="Classes should have mutable docstrings -- resolved in python 3.3")
def test_sphinx_deprecated_class__warns(sphinx_deprecated_class):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        sphinx_deprecated_class()
    assert len(warns) == 1
    warn = warns[0]
    assert issubclass(warn.category, DeprecationWarning)
    assert "deprecated class" in str(warn.message)


# noinspection PyShadowingNames
def test_sphinx_deprecated_method__warns(sphinx_deprecated_method):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        obj = sphinx_deprecated_method()
        obj.foo()
    assert len(warns) == 1
    warn = warns[0]
    assert issubclass(warn.category, DeprecationWarning)
    assert "deprecated method" in str(warn.message)


# noinspection PyShadowingNames
def test_sphinx_deprecated_static_method__warns(sphinx_deprecated_static_method):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        sphinx_deprecated_static_method()
    assert len(warns) == 1
    warn = warns[0]
    assert issubclass(warn.category, DeprecationWarning)
    assert "deprecated function (or staticmethod)" in str(warn.message)


# noinspection PyShadowingNames
def test_sphinx_deprecated_class_method__warns(sphinx_deprecated_class_method):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        cls = sphinx_deprecated_class_method()
        cls.foo()
    assert len(warns) == 1
    warn = warns[0]
    assert issubclass(warn.category, DeprecationWarning)
    assert "deprecated function (or staticmethod)" in str(warn.message)


def test_should_raise_type_error():
    try:
        deprecated.sphinx.deprecated(5)
        assert False, "TypeError not raised"
    except TypeError:
        pass


def test_warning_msg_has_reason():
    reason = "Good reason"

    @deprecated.sphinx.deprecated(reason=reason)
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        foo()
    warn = warns[0]
    assert reason in str(warn.message)


def test_warning_msg_has_version():
    version = "1.2.3"

    @deprecated.sphinx.deprecated(version=version)
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        foo()
    warn = warns[0]
    assert version in str(warn.message)


def test_warning_is_ignored():
    @deprecated.sphinx.deprecated(action='ignore')
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        foo()
    assert len(warns) == 0


def test_specific_warning_cls_is_used():
    @deprecated.sphinx.deprecated(category=MyDeprecationWarning)
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        foo()
    warn = warns[0]
    assert issubclass(warn.category, MyDeprecationWarning)
