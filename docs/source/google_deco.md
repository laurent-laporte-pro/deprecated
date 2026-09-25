(google_deco)=

# The "Google" decorators

## Overview

If you write your docstrings with the [Google Python Style Guide] format, the "Sphinx" decorators
(see {ref}`sphinx_deco`) are not the best fit: they append reStructuredText directives
to your docstrings, whereas a Google docstring is organized in *sections*,
like `Args:`, `Returns:` or `Raises:`.

The "Google" decorators have the same function as the "Sphinx" decorators, but they add
*sections* to your functions or classes documentation (inside the [docstring]):

- {func}`~deprecated.google.deprecated`: insert a `Deprecated:` section in docstring, and emit a warning on each call.
- {func}`~deprecated.google.versionadded`: insert a `Version added:` section in docstring, don't emit warning.
- {func}`~deprecated.google.versionchanged`: insert a `Version changed:` section in docstring, don't emit warning.

Each item of these sections has the format `version: reason`, like the items of the `Raises:` section.
The *reason* is optional, and long lines are wrapped (see the *line_length* parameter).

## Using the "Google" decorators

The decorators can be combined to reflect the life cycle of a function:

```{literalinclude} google/google_demo.py
```

The docstring of the *successor()* function looks like this:

```text
Calculate the successor of a number.

Args:
    n: a number

Returns:
    number + 1

Version added:
    0.1.0: Here is my new function.

Version changed:
    0.2.0: Well, I add a new feature in this function. It is very
        useful as you can see in the example below, so try it. This is
        a very very very very very long sentence.

Deprecated:
    0.3.0: This is deprecated, really. So you need to use another
        function.
        But I don't know which one.

           - The first,
           - The second.

        Just guess!
```

The sections are added at the end of the docstring. If a section already exists
(for instance when the `@versionchanged` decorator is used several times, or when the section
is already written in the docstring), the new item is appended to this section.

:::{note}
Decorators must be writen in reverse order: recent first, older last.
:::

## Building the documentation

The [Napoleon] extension of Sphinx parses the Google docstrings, but it doesn't know
the life cycle sections: declare them as custom sections in your {file}`conf.py`:

```python
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

napoleon_custom_sections = ["Version added", "Version changed", "Deprecated"]
```

As for the "Sphinx" decorators, your modules must be imported during the build:
the Deprecated decorators must be interpreted (see {ref}`sphinx_deco`).

[docstring]: https://docs.python.org/3/glossary.html#term-docstring
[google python style guide]: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[napoleon]: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
