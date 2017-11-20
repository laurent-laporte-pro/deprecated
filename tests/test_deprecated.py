# -*- coding: utf-8 -*-

import unittest
import warnings

import deprecated


def some_function():
    pass


@deprecated.deprecated
def some_old_function1(x, y):
    return x + y


@deprecated.deprecated("use another function")
def some_old_function2(x, y):
    return x + y


@deprecated.deprecated(reason="use another function")
def some_old_function3(x, y):
    return x + y


class SomeClass(object):
    @deprecated.deprecated
    def some_old_method1(self, x, y):
        return x + y

    @deprecated.deprecated("use another method")
    def some_old_method2(self, x, y):
        return x + y

    @deprecated.deprecated(reason="use another method")
    def some_old_method3(self, x, y):
        return x + y


@deprecated.deprecated
class SomeOldClass1(object):
    pass


@deprecated.deprecated("use another class")
class SomeOldClass2(object):
    pass


@deprecated.deprecated(reason="use another class")
class SomeOldClass3(object):
    pass


@deprecated.deprecated(reason="Use something else!")
def old_function_with_docstring(x, y):
    """
    This is an old function.

    :param x: a number
    :param y: a number
    :return: the sum of two numbers.
    """
    return x + y


class DeprecatedTest(unittest.TestCase):
    def test_should_warn_deprecated_function(self):
        for old_function in [some_old_function1,
                             some_old_function2,
                             some_old_function3]:
            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter("always")
                old_function(4, 5)
                self.assertEqual(len(warns), 1)
                warn = warns[0]
                self.assertTrue(issubclass(warn.category, DeprecationWarning))
                self.assertTrue("deprecated" in str(warn.message))

    def test_should_warn_deprecated_method(self):
        obj = SomeClass()
        for old_method in [obj.some_old_method1,
                           obj.some_old_method2,
                           obj.some_old_method3]:
            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter("always")
                old_method(4, 5)
                self.assertEqual(len(warns), 1)
                warn = warns[0]
                self.assertTrue(issubclass(warn.category, DeprecationWarning))
                self.assertTrue("deprecated" in str(warn.message))

    def test_should_warn_deprecated_class(self):
        for old_cls in [SomeOldClass1,
                        SomeOldClass2,
                        SomeOldClass3]:
            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter("always")
                old_cls()
                self.assertEqual(len(warns), 1)
                warn = warns[0]
                self.assertTrue(issubclass(warn.category, DeprecationWarning))
                self.assertTrue("deprecated" in str(warn.message))

    def test_should_not_warn_non_deprecated_function(self):
        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter("always")
            some_function()
            self.assertEqual(len(warns), 0)

    def test_should_raise_TypeError(self):
        try:
            deprecated.deprecated(5)
            self.fail("TypeError not called")
        except TypeError:
            pass

    def test_should_have_a_docstring(self):
        docstring = old_function_with_docstring.__doc__
        self.assertTrue(docstring is not None)
        self.assertTrue("This is an old function." in docstring)

    def test_deprecated_has_docstring(self):
        self.assertTrue(deprecated.__doc__ is not None)

    def test_deprecated_has_version(self):
        self.assertTrue(deprecated.__version__ is not None)


if __name__ == '__main__':
    unittest.main(module='tests.test_deprecated')
