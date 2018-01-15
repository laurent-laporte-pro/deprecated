# coding: utf-8
import pytest

from deprecated import sphinx


@pytest.fixture(scope="module",
                params=[
                    ((), {}),
                    ((), {'reason': 'Good reason'}),
                    ((), {'version': '1.2.3'}),
                    ((), {'reason': 'Good reason', 'version': '1.2.3'}),
                ])
def sphinx_deprecated_function(request):
    args, kwargs = request.param

    @sphinx.deprecated(*args, **kwargs)
    def foo():
        pass

    return foo


@pytest.fixture(scope="module",
                params=[
                    ((), {}),
                    ((), {'reason': 'Good reason'}),
                    ((), {'version': '1.2.3'}),
                    ((), {'reason': 'Good reason', 'version': '1.2.3'}),
                ])
def sphinx_deprecated_class(request):
    args, kwargs = request.param

    @sphinx.deprecated(*args, **kwargs)
    class Foo(object):
        pass

    return Foo


@pytest.fixture(scope="module",
                params=[
                    ((), {}),
                    ((), {'reason': 'Good reason'}),
                    ((), {'version': '1.2.3'}),
                    ((), {'reason': 'Good reason', 'version': '1.2.3'}),
                ])
def sphinx_deprecated_method(request):
    args, kwargs = request.param

    class Foo(object):
        @sphinx.deprecated(*args, **kwargs)
        def foo(self):
            pass

    return Foo


@pytest.fixture(scope="module",
                params=[
                    ((), {}),
                    ((), {'reason': 'Good reason'}),
                    ((), {'version': '1.2.3'}),
                    ((), {'reason': 'Good reason', 'version': '1.2.3'}),
                ])
def sphinx_deprecated_static_method(request):
    args, kwargs = request.param

    class Foo(object):
        @staticmethod
        @sphinx.deprecated(*args, **kwargs)
        def foo():
            pass

    return Foo.foo


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
def with_docstring(request):
    def add(x, y):
        return x + y

    add.__doc__ = request.param

    return add
