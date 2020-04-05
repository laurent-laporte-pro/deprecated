.. _Sphinx: https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
.. _Sphinx directives: https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html
.. _Markdown: https://www.sphinx-doc.org/en/master/usage/markdown.html
.. _docstring: https://docs.python.org/3/glossary.html#term-docstring
.. _autodoc: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html

.. _sphinx_deco:

The "Sphinx" decorators
=======================

Overview
--------

Developers use the Deprecated library to decorate deprecated functions or classes. This is very practical,
but you know that this library does more: you can also document your source code! How?
It's very simple: instead of using the "classic" decorator, you can use one of the "Sphinx" decorators.

The "Sphinx" decorators have the same function as the "classic" decorator but also allow you to add
`Sphinx directives`_ in your functions or classes documentation (inside the docstring_).

.. attention::

   In Python 3.3 and previous versions, the docstring of a class is immutable [#f1]_, this means that you cannot
   use the "Sphinx" decorators. Naturally, this limitation does not exist in Python 3.4 and above.

What is a Sphinx directive?
---------------------------

Sphinx_ is a tool that makes it easy to create intelligent and beautiful documentation.
This tool uses the reStructuredText_ (or Markdown_) syntax to generate the documentation in different formats,
the most common being HTML. Developers generally use this syntax to document the source code of their applications.

Sphinx_ offers several directives allowing to introduce a text block with a predefined role.
Among all the directives, the ones that interest us are those related to the functions (or classes)
life cycle, namely: ``versionadded``, ``versionchanged`` and ``deprecated``.

In the following example, the *mean()* function can be documented as follows:

.. literalinclude:: sphinx/calc_mean.py

Therefore, the "Sphinx" decorators allow you to add a Sphinx directive to your functions
or classes documentation. In the case of the ``deprecated`` directive, it obviously allows you to emit a
:exc:`DeprecationWarning` warning.

Using the "Sphinx" decorators
-----------------------------

The previous example can be writen using a "Sphinx" decorator:

.. literalinclude:: sphinx/calc_mean_deco.py

You can see the generated documentation with this simple call:

.. literalinclude:: sphinx/use_calc_mean_deco.py

The documentation of the *mean()* function looks like this:

.. code-block:: rst

   Compute the arithmetic mean (“average”) of values.

   :type  values: list[float]
   :param values: List of floats
   :return: Mean of values.

   .. deprecated:: 2.5.0
      Since Python 3.4, you can use the standard function
      :func:`statistics.mean`.

More elaborate example
----------------------

The Deprecated library offers you 3 decorators:

- :func:`~deprecated.sphinx.deprecated`: insert a ``deprecated`` directive in docstring, and emit a warning on each call.
- :func:`~deprecated.sphinx.versionadded`: insert a ``versionadded`` directive in docstring, don't emit warning.
- :func:`~deprecated.sphinx.versionchanged`: insert a ``versionchanged`` directive in docstring, don't emit warning.

The decorators can be combined to reflect the life cycle of a function:

- When it is added in your API, with the ``@versionadded`` decorator,
- When it has an important change, with the ``@versionchanged`` decorator,
- When it is deprecated, with the ``@deprecated`` decorator.

The example bellow illustrate this life cycle:

.. literalinclude:: sphinx/sphinx_demo.py

To see the result, you can use the builtin function :func:`help` to display a formatted help message
of the *successor()* function. It is something like this:

.. code-block:: text

   Help on function successor in module __main__:

   successor(n)
       Calculate the successor of a number.

       :param n: a number
       :return: number + 1


       .. versionadded:: 0.1.0
          Here is my new function.


       .. versionchanged:: 0.2.0
          Well, I add a new feature in this function. It is very useful as
          you can see in the example below, so try it. This is a very very
          very very very long sentence.


       .. deprecated:: 0.3.0
          This is deprecated, really. So you need to use another function.
          But I don't know which one.

             - The first,
             - The second.

          Just guess!

.. note:: Decorators must be writen in reverse order: recent first, older last.

Building the documentation
--------------------------

The easiest way to build your API documentation is to use the autodoc_ plugin.
The directives like ``automodule``, ``autoclass``, ``autofunction`` scan your source code
and generate the documentation from your docstrings.

Usually, the first thing that we need to do is indicate where the Python package that contains your
source code is in relation to the ``conf.py`` file.

But here, that will not work! The reason is that your modules must be imported during build:
the Deprecated decorators must be interpreted.

So, to build the API documentation of your project with Sphinx_ you need to setup a virtualenv,
and install Sphinx, external themes and/or plugins and also your project.
Nowadays, this is the right way to do it.

For instance, you can configure a documentation building task in your ``tox.ini`` file, for instance:

.. code-block:: ini

   [testenv:docs]
   basepython = python
   deps =
       sphinx
   commands =
       sphinx-build -b html -d {envtmpdir}/doctrees docs/source/ {envtmpdir}/html


.. rubric:: Footnotes

.. [#f1] See Issue 12773: `classes should have mutable docstrings <https://bugs.python.org/issue12773>`_.
