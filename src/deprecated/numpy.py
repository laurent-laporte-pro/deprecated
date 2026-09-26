"""
NumPy docstring integration
===========================

We usually need to document the life-cycle of functions and classes:
when they are created, modified or deprecated.

The `numpydoc docstring guide`_ organizes a docstring in sections: a section starts with a
header underlined with hyphens (like ``Parameters`` or ``Returns``).

The purpose of this module is to define decorators which add the following sections
to the docstring of your functions and classes:

- ``Version added``: to document the version of the project which added the described feature
  to the library,
- ``Version changed``: to document changes of a feature,
- ``Deprecated``: to document a deprecated feature.

Each item of these sections is made of the version, followed by the indented reason message,
like the items of the ``Raises`` section. If the section already exists in the docstring
(for instance when the ``@versionchanged`` decorator is used several times),
the item is appended to it.

Of course, the ``@deprecated`` decorator will emit a deprecation warning
when the function/method is called or the class is constructed.

.. note::

   The ``Deprecated`` section is understood by `Griffe`_ (used by *mkdocstrings*).
   `Napoleon`_ doesn't know these sections: to render them with Sphinx, declare them with
   ``napoleon_custom_sections = ["Version added", "Version changed", "Deprecated"]``
   in your :file:`conf.py`.

.. _numpydoc docstring guide: https://numpydoc.readthedocs.io/en/latest/format.html
.. _Griffe: https://mkdocstrings.github.io/griffe/
.. _Napoleon: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

.. versionadded:: 3.0.0
"""

import re
import textwrap
from collections.abc import Callable
from typing import Any
from typing import Literal

from deprecated.classic import ClassicAdapter
from deprecated.classic import Deprecatable
from deprecated.classic import WarningAction
from deprecated.classic import deprecated as _classic_deprecated

#: Life-cycle section inserted in the docstring.
type NumpySection = Literal["versionadded", "versionchanged", "deprecated"]

#: Header of each life-cycle section.
SECTION_HEADERS: dict[NumpySection, str] = {
    "versionadded": "Version added",
    "versionchanged": "Version changed",
    "deprecated": "Deprecated",
}

#: Indentation of the reason message in a section item.
_INDENT = " " * 4

#: Underline of a section header.
_UNDERLINE_REGEX = re.compile(r"^-{3,}\s*$")


class NumpyAdapter(ClassicAdapter):
    """
    NumPy docstring adapter -- *for advanced usage only*

    This adapter overrides the :class:`~deprecated.classic.ClassicAdapter`
    in order to add a life-cycle section to the function/class docstring,
    using the `numpydoc docstring guide`_ format.

    - The section can be one of "versionadded", "versionchanged" or "deprecated".
    - The section item starts with the version number, followed by the indented reason message
      if not empty.
    - The item is appended to the section if it already exists,
      otherwise the section is added at the end of the docstring.
    """

    def __init__(
        self,
        section: NumpySection,
        reason: str | None = "",
        version: str | None = "",
        action: WarningAction | Literal[""] | None = None,
        category: type[Warning] = DeprecationWarning,
        extra_stacklevel: int = 0,
        line_length: int = 70,
    ) -> None:
        """
        Construct a wrapper adapter.

        :type  section: str
        :param section:
            Life-cycle section: can be one of "versionadded", "versionchanged" or "deprecated".

        :type  reason: str | None
        :param reason:
            Reason message which documents the deprecation in your library (can be omitted).

        :type  version: str
        :param version:
            Version of your project which deprecates this feature.
            If you follow the `Semantic Versioning <https://semver.org/>`_,
            the version number has the format "MAJOR.MINOR.PATCH".

        :type  action: Literal["default", "error", "ignore", "always", "module", "once"]
        :param action:
            A warning filter used to activate or not the deprecation warning.
            Can be one of "error", "ignore", "always", "default", "module", or "once".
            If ``None`` or empty, the global filtering mechanism is used.
            See: `The Warnings Filter`_ in the Python documentation.

        :type  category: Type[Warning]
        :param category:
            The warning category to use for the deprecation warning.
            By default, the category class is :class:`~DeprecationWarning`,
            you can inherit this class to define your own deprecation warning category.

        :type  extra_stacklevel: int
        :param extra_stacklevel:
            Number of additional stack levels to consider instrumentation rather than user code.
            With the default value of 0, the warning refers to where the class was instantiated
            or the function was called.

        :type  line_length: int
        :param line_length:
            Max line length of the reason message (including its indentation).
            If non-zero, a long text is wrapped in several lines.
        """
        if not version:
            raise ValueError("'version' argument is required in NumPy docstring sections")
        if section not in SECTION_HEADERS:
            raise ValueError(f"invalid NumPy docstring section: {section!r}")
        self.section = section
        self.line_length = line_length
        super().__init__(
            reason=reason,
            version=version,
            action=action,
            category=category,
            extra_stacklevel=extra_stacklevel,
        )

    def get_section_item(self) -> list[str]:
        """
        Build the lines of the section item: the version, followed by the indented reason message.

        :return: the lines of the section item, without line ending.
        """
        item_lines = [self.version]
        width = self.line_length if self.line_length > len(_INDENT) else 2**16
        reason = textwrap.dedent(self.reason).strip()
        for paragraph in reason.splitlines():
            if paragraph:
                item_lines.extend(
                    textwrap.fill(
                        paragraph,
                        width=width,
                        initial_indent=_INDENT,
                        subsequent_indent=_INDENT,
                    ).splitlines()
                )
            else:
                item_lines.append("")
        return item_lines

    def __call__[T: Deprecatable](self, wrapped: T) -> T:
        """
        Add the NumPy docstring section to your class or function.

        :param wrapped: Wrapped class or function.

        :return: the decorated class or function.
        """
        wrapped.__doc__ = add_section_item(
            wrapped.__doc__,
            SECTION_HEADERS[self.section],
            self.get_section_item(),
        )
        if self.section in {"versionadded", "versionchanged"}:
            return wrapped
        return super().__call__(wrapped)


def _is_section_header(doc_lines: list[str], index: int) -> bool:
    """Check if the line at *index* is a section header: a text underlined with hyphens."""
    return (
        index + 1 < len(doc_lines)
        and bool(doc_lines[index].strip())
        and not doc_lines[index][0].isspace()
        and _UNDERLINE_REGEX.match(doc_lines[index + 1]) is not None
    )


def add_section_item(docstring: str | None, header: str, item_lines: list[str]) -> str:
    """
    Add an item to a section of a NumPy docstring.

    The docstring is normalized first: the lines following the summary line are dedented,
    so that the section headers are not indented.

    - If the section already exists, the item is appended to the end of the section.
    - Otherwise, the section is added to the end of the docstring,
      separated from the previous text by an empty line.

    :param docstring: The docstring to update (can be ``None`` or empty).

    :param header: The section header.

    :param item_lines: The lines of the section item, without line ending.

    :return: the updated docstring.
    """
    # -- get the docstring, normalize the trailing newlines
    # keep a consistent behaviour if the docstring starts with newline
    # or directly on the first one
    lines = (docstring or "").splitlines(True) or [""]
    docstring = lines[0] + (textwrap.dedent("".join(lines[1:])) if len(lines) > 1 else "")
    doc_lines = docstring.rstrip().splitlines()

    # -- search the section, at the first level (not indented)
    start = next(
        (
            i
            for i, line in enumerate(doc_lines)
            if line.rstrip() == header and _is_section_header(doc_lines, i)
        ),
        None,
    )
    if start is None:
        # An empty line must separate the original docstring and the new section.
        if any(line.strip() for line in doc_lines):
            doc_lines.append("")
        doc_lines.append(header)
        doc_lines.append("-" * len(header))
        doc_lines.extend(item_lines)
    else:
        # The section ends before the next section header (or at the end).
        end = next(
            (i for i in range(start + 2, len(doc_lines)) if _is_section_header(doc_lines, i)),
            len(doc_lines),
        )
        while end > start + 2 and not doc_lines[end - 1].strip():
            end -= 1
        doc_lines[end:end] = item_lines
    return "".join(f"{line}\n" for line in doc_lines)


def versionadded(
    reason: str | None = "", version: str | None = "", line_length: int = 70
) -> NumpyAdapter:
    """
    This decorator can be used to insert a "Version added" section
    in your function/class docstring in order to document the
    version of the project which adds this new functionality in your library.

    :param str reason:
        Reason message which documents the addition in your library (can be omitted).

    :param str version:
        Version of your project which adds this feature.
        If you follow the `Semantic Versioning <https://semver.org/>`_,
        the version number has the format "MAJOR.MINOR.PATCH", and,
        in the case of a new functionality, the "PATCH" component should be "0".

    :type  line_length: int
    :param line_length:
        Max line length of the reason message. If non-zero, a long text is wrapped in several lines.

    :return: the decorated function.
    """
    return NumpyAdapter(
        "versionadded",
        reason=reason,
        version=version,
        line_length=line_length,
    )


def versionchanged(
    reason: str | None = "", version: str | None = "", line_length: int = 70
) -> NumpyAdapter:
    """
    This decorator can be used to insert a "Version changed" section
    in your function/class docstring in order to document the
    version of the project which modifies this functionality in your library.

    :param str reason:
        Reason message which documents the modification in your library (can be omitted).

    :param str version:
        Version of your project which modifies this feature.
        If you follow the `Semantic Versioning <https://semver.org/>`_,
        the version number has the format "MAJOR.MINOR.PATCH".

    :type  line_length: int
    :param line_length:
        Max line length of the reason message. If non-zero, a long text is wrapped in several lines.

    :return: the decorated function.
    """
    return NumpyAdapter(
        "versionchanged",
        reason=reason,
        version=version,
        line_length=line_length,
    )


def deprecated[T: Deprecatable](
    reason: str | None = "",
    version: str | None = "",
    line_length: int = 70,
    **kwargs: Any,
) -> Callable[[T], T]:
    """
    This decorator can be used to insert a "Deprecated" section
    in your function/class docstring in order to document the
    version of the project which deprecates this functionality in your library.

    :param str reason:
        Reason message which documents the deprecation in your library (can be omitted).

    :param str version:
        Version of your project which deprecates this feature.
        If you follow the `Semantic Versioning <https://semver.org/>`_,
        the version number has the format "MAJOR.MINOR.PATCH".

    :type  line_length: int
    :param line_length:
        Max line length of the reason message. If non-zero, a long text is wrapped in several lines.

    Keyword arguments can be:

    -   "action":
        A warning filter used to activate or not the deprecation warning.
        Can be one of "error", "ignore", "always", "default", "module", or "once".
        If ``None``, empty or missing, the global filtering mechanism is used.

    -   "category":
        The warning category to use for the deprecation warning.
        By default, the category class is :class:`~DeprecationWarning`,
        you can inherit this class to define your own deprecation warning category.

    -   "extra_stacklevel":
        Number of additional stack levels to consider instrumentation rather than user code.
        With the default value of 0, the warning refers to where the class was instantiated
        or the function was called.

    :return: a decorator used to deprecate a function.
    """
    section = kwargs.pop("section", "deprecated")
    adapter_cls = kwargs.pop("adapter_cls", NumpyAdapter)
    kwargs["reason"] = reason
    kwargs["version"] = version
    kwargs["line_length"] = line_length
    return _classic_deprecated(section=section, adapter_cls=adapter_cls, **kwargs)
