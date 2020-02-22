import warnings

from deprecated import deprecated


class MyDeprecationWarning(DeprecationWarning):
    """ My DeprecationWarning """


class DeprecatedIn26(MyDeprecationWarning):
    """ deprecated in 2.6 """


class DeprecatedIn30(MyDeprecationWarning):
    """ deprecated in 3.0 """


@deprecated(category=DeprecatedIn26, reason="deprecated function")
def foo():
    print("foo")


@deprecated(category=DeprecatedIn30, reason="deprecated function")
def bar():
    print("bar")


if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=DeprecatedIn30)
    foo()
    bar()
