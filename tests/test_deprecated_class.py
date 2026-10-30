import inspect
import io
import warnings

import pytest

import deprecated.classic
import deprecated.google
import deprecated.numpy
import deprecated.sphinx


@pytest.mark.parametrize(
    "decorator",
    [
        deprecated.classic.deprecated,
        deprecated.sphinx.deprecated,
        deprecated.google.deprecated,
        deprecated.numpy.deprecated,
    ],
)
@pytest.mark.parametrize("custom_new", [False, True])
def test_deprecated_class_preserves_signature(decorator, custom_new):
    class WithInit:
        def __init__(self, value: int = 1, *, label: str = "default"):
            self.value = value
            self.label = label

    class WithNew:
        value: int
        label: str

        def __new__(cls, value: int = 1, *, label: str = "default"):
            obj = super().__new__(cls)
            obj.value = value
            obj.label = label
            return obj

    original = WithNew if custom_new else WithInit
    signature = inspect.signature(original)
    decorated = decorator(reason="Use a replacement", version="1.0")(original)

    assert decorated is original
    assert inspect.signature(decorated) == signature
    with pytest.warns(DeprecationWarning, match="Use a replacement"):
        instance = decorated(2, label="custom")
    assert (instance.value, instance.label) == (2, "custom")


@pytest.mark.parametrize("builtin", [False, True])
def test_deprecated_class_preserves_empty_and_builtin_signatures(builtin):
    class Empty:
        pass

    class List(list[int]):
        pass

    original = List if builtin else Empty
    signature = inspect.signature(original)
    decorated = deprecated.classic.deprecated(original)

    assert inspect.signature(decorated) == signature
    with pytest.warns(DeprecationWarning, match="Call to deprecated class"):
        assert isinstance(decorated(), original)


def test_deprecated_class_preserves_constructor_parameter_named_cls():
    class Target:
        def __init__(self, cls: int = 1):
            self.value = cls

    signature = inspect.signature(Target)
    decorated = deprecated.classic.deprecated(Target)

    assert inspect.signature(decorated) == signature
    with pytest.warns(DeprecationWarning, match="Call to deprecated class Target"):
        assert decorated(2).value == 2


def test_deprecated_class_with_unavailable_signature():
    class Target(dict[str, int]):
        pass

    with pytest.raises(ValueError, match="signature"):
        inspect.signature(Target)
    decorated = deprecated.classic.deprecated(Target)

    with pytest.warns(DeprecationWarning, match="Call to deprecated class Target"):
        assert decorated(value=2) == {"value": 2}


def test_deprecated_class_preserves_subclass_signature():
    @deprecated.classic.deprecated
    class Base:
        def __init__(self, base_value: int = 1):
            self.base_value = base_value

    class Subclass(Base):
        def __init__(self, text: str, *, flag: bool = False):
            self.text = text
            self.flag = flag

    assert str(inspect.signature(Subclass)) == "(text: str, *, flag: bool = False)"
    with pytest.warns(DeprecationWarning, match="Call to deprecated class Base"):
        instance = Subclass("value", flag=True)
    assert (instance.text, instance.flag) == ("value", True)


def test_simple_class_deprecation():
    # stream is used to store the deprecation message for testing
    stream = io.StringIO()

    # To deprecate a class, it is better to emit a message when ``__new__`` is called.
    # The simplest way is to override the ``__new__``method.
    class MyBaseClass:
        def __new__(cls, *args, **kwargs):
            print("I am deprecated!", file=stream)
            return super().__new__(cls, *args, **kwargs)

    # Of course, the subclass will be deprecated too
    class MySubClass(MyBaseClass):
        pass

    obj = MySubClass()
    assert isinstance(obj, MyBaseClass)
    assert inspect.isclass(MyBaseClass)
    assert stream.getvalue().strip() == "I am deprecated!"


def test_class_deprecation_using_wrapper():
    # stream is used to store the deprecation message for testing
    stream = io.StringIO()

    class MyBaseClass:
        pass

    # To deprecated the class, we use a wrapper function which emits
    # the deprecation message and calls ``__new__```.

    original_new = MyBaseClass.__new__

    def wrapped_new(unused, *args, **kwargs):
        print("I am deprecated!", file=stream)
        return original_new(*args, **kwargs)

    # Like ``__new__``, this wrapper is a class method.
    # It is used to patch the original ``__new__``method.
    setattr(MyBaseClass, "__new__", classmethod(wrapped_new))  # noqa: B010

    class MySubClass(MyBaseClass):
        pass

    obj = MySubClass()
    assert isinstance(obj, MyBaseClass)
    assert inspect.isclass(MyBaseClass)
    assert stream.getvalue().strip() == "I am deprecated!"


def test_class_deprecation_using_a_simple_decorator():
    # stream is used to store the deprecation message for testing
    stream = io.StringIO()

    # To deprecated the class, we use a simple decorator
    # which patches the original ``__new__`` method.

    def simple_decorator(wrapped_cls):
        old_new = wrapped_cls.__new__

        def wrapped_new(unused, *args, **kwargs):
            print("I am deprecated!", file=stream)
            return old_new(*args, **kwargs)

        wrapped_cls.__new__ = classmethod(wrapped_new)
        return wrapped_cls

    @simple_decorator
    class MyBaseClass:
        pass

    class MySubClass(MyBaseClass):
        pass

    obj = MySubClass()
    assert isinstance(obj, MyBaseClass)
    assert inspect.isclass(MyBaseClass)
    assert stream.getvalue().strip() == "I am deprecated!"


def test_class_deprecation_using_deprecated_decorator():
    @deprecated.classic.deprecated
    class MyBaseClass:
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


def test_class_respect_global_filter():
    @deprecated.classic.deprecated
    class MyBaseClass:
        pass

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("once")
        MyBaseClass()
        MyBaseClass()

    assert len(warns) == 1


def test_subclass_deprecation_using_deprecated_decorator():
    @deprecated.classic.deprecated
    class MyBaseClass:
        pass

    @deprecated.classic.deprecated
    class MySubClass(MyBaseClass):
        pass

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        obj = MySubClass()

    assert len(warns) == 2
    assert isinstance(obj, MyBaseClass)
    assert inspect.isclass(MyBaseClass)
    assert issubclass(MySubClass, MyBaseClass)


def test_simple_class_deprecation_with_args():
    @deprecated.classic.deprecated("kwargs class")
    class MyClass:
        def __init__(self, arg):
            super().__init__()
            self.args = arg

    with pytest.warns(DeprecationWarning, match="kwargs class"):
        MyClass(5)
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        obj = MyClass(5)

    assert len(warns) == 1
    assert isinstance(obj, MyClass)
    assert inspect.isclass(MyClass)
