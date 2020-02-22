import warnings
from deprecated import deprecated


@deprecated(reason="do not call it", action="error")
def foo():
    print("foo")


if __name__ == '__main__':
    warnings.simplefilter("ignore")
    foo()
