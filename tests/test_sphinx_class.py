# coding: utf-8
from __future__ import print_function

import inspect
import io
import sys
import warnings

import pytest

import deprecated.sphinx


def test_class_deprecation_using_a_simple_decorator():
    # stream is used to store the deprecation message for testing
    stream = io.StringIO()

    # To deprecated the class, we use a simple decorator
    # which patches the original ``__new__`` method.

    def simple_decorator(wrapped_cls):
        old_new = wrapped_cls.__new__

        def wrapped_new(unused, *args, **kwargs):
            print(u"I am deprecated!", file=stream)
            return old_new(*args, **kwargs)

        wrapped_cls.__new__ = classmethod(wrapped_new)
        return wrapped_cls

    @simple_decorator
    class MyBaseClass(object):
        pass

    class MySubClass(MyBaseClass):
        pass

    obj = MySubClass()
    assert isinstance(obj, MyBaseClass)
    assert inspect.isclass(MyBaseClass)
    assert stream.getvalue().strip() == u"I am deprecated!"


@pytest.mark.skipif(sys.version_info < (3, 3),
                    reason="Classes should have mutable docstrings -- resolved in python 3.3")
def test_class_deprecation_using_deprecated_decorator():
    @deprecated.sphinx.deprecated
    class MyBaseClass(object):
        pass

    class MySubClass(MyBaseClass):
        pass

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        obj = MySubClass()

    assert len(warns) == 1
    assert isinstance(obj, MyBaseClass)
    assert inspect.isclass(MyBaseClass)
    assert issubclass(MySubClass, MyBaseClass)


@pytest.mark.skipif(sys.version_info < (3, 3),
                    reason="Classes should have mutable docstrings -- resolved in python 3.3")
def test_subclass_deprecation_using_deprecated_decorator():
    @deprecated.sphinx.deprecated
    class MyBaseClass(object):
        pass

    @deprecated.sphinx.deprecated
    class MySubClass(MyBaseClass):
        pass

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        obj = MySubClass()

    assert len(warns) == 2
    assert isinstance(obj, MyBaseClass)
    assert inspect.isclass(MyBaseClass)
    assert issubclass(MySubClass, MyBaseClass)
