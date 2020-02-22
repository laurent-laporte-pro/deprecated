import warnings
from deprecated import deprecated


@deprecated(version='1.2.1', reason="deprecated function")
def fun():
    print("fun")


if __name__ == '__main__':
    warnings.simplefilter("ignore", category=DeprecationWarning)
    fun()
