import sys
import textwrap
import warnings

import pytest

import deprecated.google
from deprecated.google import GoogleAdapter
from deprecated.google import add_section_item


class MyDeprecationWarning(DeprecationWarning):
    pass


@pytest.fixture(
    scope="module",
    params=[
        None,
        """This function adds *x* and *y*.""",
        """
        This function adds *x* and *y*.

        Args:
            x: number *x*
            y: number *y*

        Returns:
            sum = *x* + *y*
        """,
        """This function adds *x* and *y*.

        Args:
            x: number *x*
            y: number *y*

        Returns:
            sum = *x* + *y*
        """,
    ],
    ids=["no_docstring", "short_docstring", "D213_long_docstring", "D212_long_docstring"],
)
def docstring(request):
    return request.param


@pytest.fixture(scope="module", params=["versionadded", "versionchanged", "deprecated"])
def section(request):
    return request.param


HEADERS = {
    "versionadded": "Version added",
    "versionchanged": "Version changed",
    "deprecated": "Deprecated",
}


# noinspection PyShadowingNames
@pytest.mark.parametrize(
    ("reason", "version", "expected"),
    [
        ("A good reason", "1.2.0", "{header}:\n    {version}: {reason}\n"),
        (None, "1.2.0", "{header}:\n    {version}\n"),
    ],
    ids=["reason&version", "version"],
)
def test_has_google_docstring(docstring, section, reason, version, expected):
    def foo(x, y):
        return x + y

    foo.__doc__ = docstring

    decorator_factory = getattr(deprecated.google, section)
    foo = decorator_factory(reason=reason, version=version)(foo)

    expected = expected.format(header=HEADERS[section], version=version, reason=reason)
    assert foo.__doc__ is not None
    current = textwrap.dedent(foo.__doc__)
    assert current.endswith(expected)

    current = current[: -len(expected)]
    if docstring:
        # An empty line must separate the original docstring and the section.
        assert current.endswith("\n\n")
        assert not current.endswith("\n\n\n")
    else:
        assert current == ""

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        foo(1, 2)

    if section in {"versionadded", "versionchanged"}:
        assert len(warns) == 0
    else:
        assert len(warns) == 1
        assert issubclass(warns[0].category, DeprecationWarning)


# noinspection PyShadowingNames
def test_cls_has_google_docstring(docstring, section):
    class Foo:
        pass

    Foo.__doc__ = docstring

    decorator_factory = getattr(deprecated.google, section)
    decorated_cls = decorator_factory(reason="A good reason", version="1.2.0")(Foo)

    expected = f"{HEADERS[section]}:\n    1.2.0: A good reason\n"
    assert decorated_cls.__doc__ is not None
    assert textwrap.dedent(decorated_cls.__doc__).endswith(expected)

    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        decorated_cls()

    if section in {"versionadded", "versionchanged"}:
        assert len(warns) == 0
    else:
        assert len(warns) == 1
        assert str(warns[0].message) == (
            "Call to deprecated class Foo. (A good reason) -- Deprecated since version 1.2.0."
        )


@pytest.mark.parametrize(
    ("line_length", "expected"),
    [
        (
            50,
            textwrap.dedent(
                """
                Description of foo

                Returns:
                    nothing

                {header}:
                    1.2.3: foo has changed in this version

                        bar bar bar bar bar bar bar bar bar bar
                        bar bar bar bar bar bar bar bar bar bar
                        bar bar bar
                """
            ),
        ),
        (
            0,
            textwrap.dedent(
                """
                Description of foo

                Returns:
                    nothing

                {header}:
                    1.2.3: foo has changed in this version

                        bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar
                """  # noqa: E501
            ),
        ),
    ],
    ids=["wrapped", "long"],
)
def test_google_adapter(section, line_length, expected):
    reason = "\n".join(["foo has changed in this version", "", "bar " * 23, ""])
    adapter = GoogleAdapter(section, reason=reason, version="1.2.3", line_length=line_length)

    def foo():
        """
        Description of foo

        Returns:
            nothing
        """

    wrapped = adapter(foo)
    assert wrapped.__doc__ == expected.format(header=HEADERS[section])


def test_stacked_decorators():
    @deprecated.google.deprecated(reason="Use bar() instead.", version="0.3.0")
    @deprecated.google.versionchanged(reason="Add the *y* parameter.", version="0.2.0")
    @deprecated.google.versionchanged(version="0.1.5")
    @deprecated.google.versionadded(reason="Here is my new function.", version="0.1.0")
    def foo(x, y=0):
        """Add *x* and *y*.

        Args:
            x: number *x*
            y: number *y*
        """
        return x + y

    assert foo.__doc__ == textwrap.dedent(
        """\
        Add *x* and *y*.

        Args:
            x: number *x*
            y: number *y*

        Version added:
            0.1.0: Here is my new function.

        Version changed:
            0.1.5
            0.2.0: Add the *y* parameter.

        Deprecated:
            0.3.0: Use bar() instead.
        """
    )


def test_add_item_to_existing_section():
    docstring = """Summary.

    Version changed:
        1.0.0: First change.


    Returns:
        nothing
    """
    assert add_section_item(docstring, "Version changed", ["    1.1.0: Second change."]) == (
        textwrap.dedent(
            """\
            Summary.

            Version changed:
                1.0.0: First change.
                1.1.0: Second change.


            Returns:
                nothing
            """
        )
    )


def test_method_and_classmethod():
    class Foo:
        @deprecated.google.deprecated(reason="Use bar()", version="1.0.0")
        def foo(self):
            """Do foo."""

        @classmethod
        @deprecated.google.deprecated(version="1.0.0")
        def baz(cls):
            """Do baz."""

    assert Foo.foo.__doc__ == "Do foo.\n\nDeprecated:\n    1.0.0: Use bar()\n"
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")
        Foo().foo()
        Foo.baz()
    if sys.version_info < (3, 13):
        baz_kind = "class method"
    else:
        # Since Python 3.13, ``classmethod`` no longer wraps the descriptor of the function.
        baz_kind = "function (or staticmethod)"
    assert [str(w.message) for w in warns] == [
        "Call to deprecated method foo. (Use bar()) -- Deprecated since version 1.0.0.",
        f"Call to deprecated {baz_kind} baz. -- Deprecated since version 1.0.0.",
    ]


def test_deprecated_keyword_arguments():
    @deprecated.google.deprecated(
        version="1.0.0", action="error", category=MyDeprecationWarning, line_length=0
    )
    def foo():
        pass

    with pytest.raises(MyDeprecationWarning):
        foo()


@pytest.mark.parametrize("version", [None, ""])
def test_version_is_required(section, version):
    def foo():
        pass

    decorator_factory = getattr(deprecated.google, section)
    with pytest.raises(ValueError, match="'version' argument is required"):
        decorator_factory(reason="A good reason", version=version)(foo)


def test_invalid_section():
    with pytest.raises(ValueError, match="invalid Google docstring section"):
        GoogleAdapter("todo", version="1.0.0")  # type: ignore[arg-type]
