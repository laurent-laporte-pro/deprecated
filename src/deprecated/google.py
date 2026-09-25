"""
Google docstring integration
============================

We usually need to document the life-cycle of functions and classes:
when they are created, modified or deprecated.

The `Google Python Style Guide`_ organizes a docstring in sections: a section starts with a
header line ending with a colon (like ``Args:`` or ``Returns:``) followed by an indented block.

The purpose of this module is to define decorators which add the following sections
to the docstring of your functions and classes:

- ``Version added:``: to document the version of the project which added the described feature
  to the library,
- ``Version changed:``: to document changes of a feature,
- ``Deprecated:``: to document a deprecated feature.

Each item of these sections has the format ``version: reason``, like the items of the
``Raises:`` section. If the section already exists in the docstring (for instance when the
``@versionchanged`` decorator is used several times), the item is appended to it.

Of course, the ``@deprecated`` decorator will emit a deprecation warning
when the function/method is called or the class is constructed.

.. note::

   `Napoleon`_ doesn't know these sections: to render them with Sphinx, declare them with
   ``napoleon_custom_sections = ["Version added", "Version changed", "Deprecated"]``
   in your :file:`conf.py`.

.. _Google Python Style Guide: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
.. _Napoleon: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

.. versionadded:: 3.0.0
"""

import textwrap
from collections.abc import Callable
from typing import Any
from typing import Literal

from deprecated.classic import ClassicAdapter
from deprecated.classic import Deprecatable
from deprecated.classic import WarningAction
from deprecated.classic import deprecated as _classic_deprecated

#: Life-cycle section inserted in the docstring.
type GoogleSection = Literal["versionadded", "versionchanged", "deprecated"]

#: Header of each life-cycle section (without the trailing colon).
SECTION_HEADERS: dict[GoogleSection, str] = {
    "versionadded": "Version added",
    "versionchanged": "Version changed",
    "deprecated": "Deprecated",
}

#: Indentation of the section items, and of the continuation lines of an item.
_INDENT = " " * 4


class GoogleAdapter(ClassicAdapter):
    """
    Google docstring adapter -- *for advanced usage only*

    This adapter override the :class:`~deprecated.classic.ClassicAdapter`
    in order to add a life-cycle section to the function/class docstring,
    using the `Google Python Style Guide`_ format.

    - The section can be one of "versionadded", "versionchanged" or "deprecated".
    - The section item starts with the version number, followed by the reason message if not empty.
    - The item is appended to the section if it already exists,
      otherwise the section is added at the end of the docstring.
    """

    def __init__(
        self,
        section: GoogleSection,
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
            Max line length of the section item (including its indentation).
            If non nul, a long text is wrapped in several lines.
        """
        if not version:
            raise ValueError("'version' argument is required in Google docstring sections")
        if section not in SECTION_HEADERS:
            raise ValueError(f"invalid Google docstring section: {section!r}")
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
        Build the lines of the section item: ``version: reason``.

        The first line is indented once, the continuation lines are indented twice.

        :return: the lines of the section item, without line ending.
        """
        initial_indent = f"{_INDENT}{self.version}: "
        subsequent_indent = _INDENT * 2
        width = self.line_length if self.line_length > len(subsequent_indent) else 2**16
        reason = textwrap.dedent(self.reason).strip()
        if not reason:
            return [f"{_INDENT}{self.version}"]
        item_lines: list[str] = []
        for paragraph in reason.splitlines():
            if not paragraph:
                item_lines.append("")
                continue
            item_lines.extend(
                textwrap.fill(
                    paragraph,
                    width=width,
                    initial_indent=subsequent_indent if item_lines else initial_indent,
                    subsequent_indent=subsequent_indent,
                ).splitlines()
            )
        return item_lines

    def __call__[T: Deprecatable](self, wrapped: T) -> T:
        """
        Add the Google docstring section to your class or function.

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


def add_section_item(docstring: str | None, header: str, item_lines: list[str]) -> str:
    """
    Add an item to a section of a Google docstring.

    The docstring is normalized first: the lines following the summary line are dedented,
    so that the section headers are not indented.

    - If the section already exists, the item is appended to the end of the section.
    - Otherwise, the section is added to the end of the docstring,
      separated from the previous text by an empty line.

    :param docstring: The docstring to update (can be ``None`` or empty).

    :param header: The section header (without the trailing colon).

    :param item_lines: The lines of the section item, indented, without line ending.

    :return: the updated docstring.
    """
    # -- get the docstring, normalize the trailing newlines
    # keep a consistent behaviour if the docstring starts with newline
    # or directly on the first one
    lines = (docstring or "").splitlines(True) or [""]
    docstring = lines[0] + (textwrap.dedent("".join(lines[1:])) if len(lines) > 1 else "")
    doc_lines = docstring.rstrip().splitlines()

    # -- search the section, at the first level (not indented)
    header_line = f"{header}:"
    start = next((i for i, line in enumerate(doc_lines) if line.rstrip() == header_line), None)
    if start is None:
        # An empty line must separate the original docstring and the new section.
        if any(line.strip() for line in doc_lines):
            doc_lines.append("")
        doc_lines.append(header_line)
        doc_lines.extend(item_lines)
    else:
        # The section ends before the next line which is not indented (or at the end).
        end = next(
            (
                i
                for i in range(start + 1, len(doc_lines))
                if doc_lines[i].strip() and not doc_lines[i][0].isspace()
            ),
            len(doc_lines),
        )
        while end > start + 1 and not doc_lines[end - 1].strip():
            end -= 1
        doc_lines[end:end] = item_lines
    return "".join(f"{line}\n" for line in doc_lines)


def versionadded(
    reason: str | None = "", version: str | None = "", line_length: int = 70
) -> GoogleAdapter:
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
        Max line length of the section item. If non nul, a long text is wrapped in several lines.

    :return: the decorated function.
    """
    return GoogleAdapter(
        "versionadded",
        reason=reason,
        version=version,
        line_length=line_length,
    )


def versionchanged(
    reason: str | None = "", version: str | None = "", line_length: int = 70
) -> GoogleAdapter:
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
        Max line length of the section item. If non nul, a long text is wrapped in several lines.

    :return: the decorated function.
    """
    return GoogleAdapter(
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
        Max line length of the section item. If non nul, a long text is wrapped in several lines.

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
    adapter_cls = kwargs.pop("adapter_cls", GoogleAdapter)
    kwargs["reason"] = reason
    kwargs["version"] = version
    kwargs["line_length"] = line_length
    return _classic_deprecated(section=section, adapter_cls=adapter_cls, **kwargs)
