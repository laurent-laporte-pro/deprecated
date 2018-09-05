# coding: utf-8
from __future__ import print_function

import re
import sys
import textwrap
import warnings

import pytest

import deprecated.sphinx


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

    # An empty line must separate the original docstring and the directive.
    current = current.replace(expected, '')
    if current:
        assert re.search("\n[ ]*\n$", current, flags=re.DOTALL)


# noinspection PyShadowingNames
@pytest.mark.skipif(sys.version_info < (3, 3),
                    reason="Classes should have mutable docstrings -- resolved in python 3.3")
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
def test_cls_has_sphinx_docstring(docstring, directive, reason, version, expected):
    # The class:
    class Foo(object):
        pass
 
    # with docstring:
    Foo.__doc__ = docstring
 
    # is decorated with:
    decorator_factory = getattr(deprecated.sphinx, directive)
    decorator = decorator_factory(reason=reason, version=version)
    Foo = decorator(Foo)
 
    # The class must contain this Sphinx docstring:
    expected = expected.format(directive=directive, version=version, reason=reason)
 
    current = textwrap.dedent(Foo.__doc__)
    assert current.endswith(expected)
 
    # An empty line must separate the original docstring and the directive.
    current = current.replace(expected, '')
    if current:
        assert re.search("\n[ ]*\n$", current, flags=re.DOTALL)


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
        def foo1():
            pass

        return foo1
    else:
        args, kwargs = request.param

        @deprecated.sphinx.deprecated(*args, **kwargs)
        def foo1():
            pass

        return foo1


@pytest.fixture(scope="module", params=_PARAMS)
def sphinx_deprecated_class(request):
    if request.param is None:
        @deprecated.sphinx.deprecated
        class Foo2(object):
            pass

        return Foo2
    else:
        args, kwargs = request.param

        @deprecated.sphinx.deprecated(*args, **kwargs)
        class Foo2(object):
            pass

        return Foo2


@pytest.fixture(scope="module", params=_PARAMS)
def sphinx_deprecated_method(request):
    if request.param is None:
        class Foo3(object):
            @deprecated.sphinx.deprecated
            def foo3(self):
                pass

        return Foo3
    else:
        args, kwargs = request.param

        class Foo3(object):
            @deprecated.sphinx.deprecated(*args, **kwargs)
            def foo3(self):
                pass

        return Foo3


@pytest.fixture(scope="module", params=_PARAMS)
def sphinx_deprecated_static_method(request):
    if request.param is None:
        class Foo4(object):
            @staticmethod
            @deprecated.sphinx.deprecated
            def foo4():
                pass

        return Foo4.foo4
    else:
        args, kwargs = request.param

        class Foo4(object):
            @staticmethod
            @deprecated.sphinx.deprecated(*args, **kwargs)
            def foo4():
                pass

        return Foo4.foo4


@pytest.fixture(scope="module", params=_PARAMS)
def sphinx_deprecated_class_method(request):
    if request.param is None:
        class Foo5(object):
            @classmethod
            @deprecated.sphinx.deprecated
            def foo5(cls):
                pass

        return Foo5
    else:
        args, kwargs = request.param

        class Foo5(object):
            @classmethod
            @deprecated.sphinx.deprecated(*args, **kwargs)
            def foo5(cls):
                pass

        return Foo5


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
        obj.foo3()
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
        cls.foo5()
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


def test_can_catch_warnings():
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        warnings.warn("A message in a bottle", category=DeprecationWarning, stacklevel=2)
    assert len(warns) == 1