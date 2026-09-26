(numpy_deco)=

# The "NumPy" decorators

## Overview

If you write your docstrings with the [numpydoc] format, the "Sphinx" decorators
(see {ref}`sphinx_deco`) are not the best fit: they append reStructuredText directives
at the end of your docstrings, whereas a NumPy docstring is organized in *sections*
(headers underlined with hyphens, like `Parameters` or `Returns`), and a directive appended
after the last section is considered as part of this section.

The "NumPy" decorators have the same function as the "Sphinx" decorators, but they add
*sections* to your functions or classes documentation (inside the [docstring]):

- {func}`~deprecated.numpy.deprecated`: insert a `Deprecated` section in docstring, and emit a warning on each call.
- {func}`~deprecated.numpy.versionadded`: insert a `Version added` section in docstring, don't emit warning.
- {func}`~deprecated.numpy.versionchanged`: insert a `Version changed` section in docstring, don't emit warning.

Each item of these sections is made of the version, followed by the indented reason message,
like the items of the `Raises` section. The *reason* is optional, and long lines are wrapped
(see the *line_length* parameter).

## Using the "NumPy" decorators

The decorators can be combined to reflect the life cycle of a function:

```{literalinclude} numpydoc/numpy_demo.py
```

The docstring of the *successor()* function looks like this:

```text
Calculate the successor of a number.

Parameters
----------
n : int
    A number.

Returns
-------
int
    The number + 1.

Version added
-------------
0.1.0
    Here is my new function.

Version changed
---------------
0.2.0
    Well, I add a new feature in this function. It is very useful as
    you can see in the example below, so try it. This is a very very
    very very very long sentence.

Deprecated
----------
0.3.0
    This is deprecated, really. So you need to use another function.
    But I don't know which one.

       - The first,
       - The second.

    Just guess!
```

The sections are added at the end of the docstring. If a section already exists
(for instance when the `@versionchanged` decorator is used several times, or when the section
is already written in the docstring), the new item is appended to this section.

:::{note}
Decorators must be written in reverse order: recent first, older last.
:::

## Building the documentation

The `Deprecated` section is understood by [Griffe], the docstring parser of [mkdocstrings].

The [Napoleon] extension of Sphinx parses the NumPy docstrings, but it doesn't know
the life cycle sections: declare them as custom sections in your {file}`conf.py`:

```python
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

napoleon_custom_sections = ["Version added", "Version changed", "Deprecated"]
```

As for the "Sphinx" decorators, your modules must be imported during the build:
the Deprecated decorators must be interpreted (see {ref}`sphinx_deco`).

[docstring]: https://docs.python.org/3/glossary.html#term-docstring
[griffe]: https://mkdocstrings.github.io/griffe/
[mkdocstrings]: https://mkdocstrings.github.io/
[napoleon]: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
[numpydoc]: https://numpydoc.readthedocs.io/en/latest/format.html
