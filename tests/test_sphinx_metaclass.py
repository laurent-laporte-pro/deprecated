import warnings
from typing import ClassVar

import deprecated.sphinx


def test_with_init():
    @deprecated.sphinx.deprecated(version="1.2.3")
    class MyClass:
        def __init__(self, a, b=5):
            self.a = a
            self.b = b

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        obj = MyClass("five")

    assert len(warns) == 1

    assert obj.a == "five"
    assert obj.b == 5


def test_with_new():
    @deprecated.sphinx.deprecated(version="1.2.3")
    class MyClass:
        c: float

        def __new__(cls, a, b=5):
            obj = super().__new__(cls)
            obj.c = 3.14
            return obj

        def __init__(self, a, b=5):
            self.a = a
            self.b = b

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        obj = MyClass("five")

    assert len(warns) == 1

    assert obj.a == "five"
    assert obj.b == 5
    assert obj.c == 3.14


def test_with_metaclass():
    class Meta(type):
        def __call__(cls, *args, **kwargs):
            obj = super().__call__(*args, **kwargs)
            obj.c = 3.14
            return obj

    @deprecated.sphinx.deprecated(version="1.2.3")
    class MyClass(metaclass=Meta):
        c: float

        def __init__(self, a, b=5):
            self.a = a
            self.b = b

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        obj = MyClass("five")

    assert len(warns) == 1

    assert obj.a == "five"
    assert obj.b == 5
    assert obj.c == 3.14


def test_with_singleton_metaclass():
    class Singleton(type):
        _instances: ClassVar[dict[type, object]] = {}

        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
            return cls._instances[cls]

    @deprecated.sphinx.deprecated(version="1.2.3")
    class MyClass(metaclass=Singleton):
        def __init__(self, a, b=5):
            self.a = a
            self.b = b

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        obj1 = MyClass("five")
        obj2 = MyClass("six", b=6)

    # __new__ is called only once:
    # the instance is constructed only once,
    # so we have only one warning.
    assert len(warns) == 1

    assert obj1.a == "five"
    assert obj1.b == 5
    assert obj2 is obj1


def test_docstring_with_metaclass():
    class Meta(type):
        pass

    @deprecated.sphinx.deprecated(version="1.2.3", reason="use another class")
    class MyClass(metaclass=Meta):
        """My class."""

    assert MyClass.__doc__ == "My class.\n\n.. deprecated:: 1.2.3\n   use another class\n"
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        MyClass()
    assert [str(w.message) for w in warns] == [
        "Call to deprecated class MyClass. (use another class) -- Deprecated since version 1.2.3."
    ]
