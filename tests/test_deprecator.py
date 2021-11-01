# -*- coding: utf-8 -*-
import sys
import warnings

import pytest

import deprecator.classic


class MyDeprecationWarning(DeprecationWarning):
    pass


_PARAMS = [
    None,
    ((), {}),
    (('Good reason',), {}),
    ((), {'reason': 'Good reason'}),
    ((), {'version': '1.2.3'}),
    ((), {'action': 'once'}),
    ((), {'category': MyDeprecationWarning}),
]


@pytest.fixture(scope="module", params=_PARAMS)
def classic_deprecator_function(request):
    if request.param is None:

        @deprecator.classic.deprecator
        def foo1():
            pass

        return foo1
    else:
        args, kwargs = request.param

        @deprecator.classic.deprecator(*args, **kwargs)
        def foo1():
            pass

        return foo1


@pytest.fixture(scope="module", params=_PARAMS)
def classic_deprecator_class(request):
    if request.param is None:

        @deprecator.classic.deprecator
        class Foo2(object):
            pass

        return Foo2
    else:
        args, kwargs = request.param

        @deprecator.classic.deprecator(*args, **kwargs)
        class Foo2(object):
            pass

        return Foo2


@pytest.fixture(scope="module", params=_PARAMS)
def classic_deprecator_method(request):
    if request.param is None:

        class Foo3(object):
            @deprecator.classic.deprecator
            def foo3(self):
                pass

        return Foo3
    else:
        args, kwargs = request.param

        class Foo3(object):
            @deprecator.classic.deprecator(*args, **kwargs)
            def foo3(self):
                pass

        return Foo3


@pytest.fixture(scope="module", params=_PARAMS)
def classic_deprecator_static_method(request):
    if request.param is None:

        class Foo4(object):
            @staticmethod
            @deprecator.classic.deprecator
            def foo4():
                pass

        return Foo4.foo4
    else:
        args, kwargs = request.param

        class Foo4(object):
            @staticmethod
            @deprecator.classic.deprecator(*args, **kwargs)
            def foo4():
                pass

        return Foo4.foo4


@pytest.fixture(scope="module", params=_PARAMS)
def classic_deprecator_class_method(request):
    if request.param is None:

        class Foo5(object):
            @classmethod
            @deprecator.classic.deprecator
            def foo5(cls):
                pass

        return Foo5
    else:
        args, kwargs = request.param

        class Foo5(object):
            @classmethod
            @deprecator.classic.deprecator(*args, **kwargs)
            def foo5(cls):
                pass

        return Foo5


# noinspection PyShadowingNames
def test_classic_deprecator_function__warns(classic_deprecator_function):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        classic_deprecator_function()
    assert len(warns) == 1
    warn = warns[0]
    assert issubclass(warn.category, DeprecationWarning)
    assert "deprecated function (or staticmethod)" in str(warn.message)
    assert warn.filename == __file__, 'Incorrect warning stackLevel'


# noinspection PyShadowingNames
def test_classic_deprecator_class__warns(classic_deprecator_class):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        classic_deprecator_class()
    assert len(warns) == 1
    warn = warns[0]
    assert issubclass(warn.category, DeprecationWarning)
    assert "deprecated class" in str(warn.message)
    assert warn.filename == __file__, 'Incorrect warning stackLevel'


# noinspection PyShadowingNames
def test_classic_deprecator_method__warns(classic_deprecator_method):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        obj = classic_deprecator_method()
        obj.foo3()
    assert len(warns) == 1
    warn = warns[0]
    assert issubclass(warn.category, DeprecationWarning)
    assert "deprecated method" in str(warn.message)
    assert warn.filename == __file__, 'Incorrect warning stackLevel'


# noinspection PyShadowingNames
def test_classic_deprecator_static_method__warns(classic_deprecator_static_method):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        classic_deprecator_static_method()
    assert len(warns) == 1
    warn = warns[0]
    assert issubclass(warn.category, DeprecationWarning)
    assert "deprecated function (or staticmethod)" in str(warn.message)
    assert warn.filename == __file__, 'Incorrect warning stackLevel'


# noinspection PyShadowingNames
def test_classic_deprecator_class_method__warns(classic_deprecator_class_method):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        cls = classic_deprecator_class_method()
        cls.foo5()
    assert len(warns) == 1
    warn = warns[0]
    assert issubclass(warn.category, DeprecationWarning)
    if sys.version_info >= (3, 9):
        assert "deprecated class method" in str(warn.message)
    else:
        assert "deprecated function (or staticmethod)" in str(warn.message)
    assert warn.filename == __file__, 'Incorrect warning stackLevel'


def test_should_raise_type_error():
    try:
        deprecator.classic.deprecator(5)
        assert False, "TypeError not raised"
    except TypeError:
        pass


def test_warning_msg_has_reason():
    reason = "Good reason"

    @deprecator.classic.deprecator(reason=reason)
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        foo()
    warn = warns[0]
    assert reason in str(warn.message)


def test_warning_msg_has_version():
    version = "1.2.3"

    @deprecator.classic.deprecator(version=version)
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        foo()
    warn = warns[0]
    assert version in str(warn.message)


def test_warning_is_ignored():
    @deprecator.classic.deprecator(action='ignore')
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        foo()
    assert len(warns) == 0


def test_specific_warning_cls_is_used():
    @deprecator.classic.deprecator(category=MyDeprecationWarning)
    def foo():
        pass

    with warnings.catch_warnings(record=True) as warns:
        foo()
    warn = warns[0]
    assert issubclass(warn.category, MyDeprecationWarning)


def test_respect_global_filter():
    @deprecator.classic.deprecator(version='1.2.1', reason="deprecated function")
    def fun():
        print("fun")

    warnings.simplefilter("once", category=DeprecationWarning)

    with warnings.catch_warnings(record=True) as warns:
        fun()
        fun()
    assert len(warns) == 1
