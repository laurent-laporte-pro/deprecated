.. _tutorial:

Tutorial
========

In this tutorial, we will use the Deprecated Library to mark pieces of codes as deprecated.
We will also see what's happened when a user tries to call deprecated codes.

Deprecated function
-------------------

First, we have this little library composed of a single module: ``liberty.py``:

.. literalinclude:: tutorial/v0/liberty.py

You decided to write a more powerful function called ``better_print()``
which will become a replacement of ``print_value()``.
And you decided that the later function is deprecated.

To mark the ``print_value()`` as deprecated, you can use the :meth:`~deprecated` decorator:

.. literalinclude:: tutorial/v1/liberty.py

If the user tries to use the deprecated functions, he will have a warning for each call:

.. literalinclude:: tutorial/v1/using_liberty.py

.. code-block:: sh

   $ python use_liberty.py

   using_liberty.py:4: DeprecationWarning: Call to deprecated function (or staticmethod) print_value.
     liberty.print_value("hello")
   'hello'
   using_liberty.py:5: DeprecationWarning: Call to deprecated function (or staticmethod) print_value.
     liberty.print_value("hello again")
   'hello again'
   'Hi Tom!'

As you can see, the deprecation warning is displayed like a stack trace.
You have the source code path, the line number and the called function.
This is very useful for debugging.
But, this doesn't help the developer to choose a alternative: which function could he use instead?

To help the developer, you can add a "reason" message. For instance:

.. literalinclude:: tutorial/v2/liberty.py

When the user calls the deprecated functions, he will have a more useful message:

.. code-block:: sh

   $ python use_liberty.py

   using_liberty.py:4: DeprecationWarning: Call to deprecated function (or staticmethod) print_value. (This function is rotten, use 'better_print' instead)
     liberty.print_value("hello")
   'hello'
   using_liberty.py:5: DeprecationWarning: Call to deprecated function (or staticmethod) print_value. (This function is rotten, use 'better_print' instead)
     liberty.print_value("hello again")
   'hello again'
   'Hi Tom!'


Deprecated method
-----------------

Decorating a deprecated method works like decorating a function.

.. literalinclude:: tutorial/v3/liberty.py

When the user calls the deprecated methods, like this:

.. literalinclude:: tutorial/v3/using_liberty.py

He will have:

.. code-block:: sh

   $ python use_liberty.py

   using_liberty.py:5: DeprecationWarning: Call to deprecated method print_value. (This method is rotten, use 'better_print' instead)
     obj.print_value()
   'Greeting'
   using_liberty.py:6: DeprecationWarning: Call to deprecated method print_value. (This method is rotten, use 'better_print' instead)
     obj.print_value()
   'Greeting'
   'Greeting'

.. note:: The call is done to the same object, so we have 3 times 'Greeting'.


Deprecated class
----------------

You can also decide that a class is deprecated.

For instance:

.. literalinclude:: tutorial/v4/liberty.py

When the user use the deprecated class like this:

.. literalinclude:: tutorial/v4/using_liberty.py

He will have a warning at object instantiation.
Once the object is initialised, no more warning are emitted.

.. code-block:: sh

   $ python use_liberty.py

   using_liberty.py:4: DeprecationWarning: Call to deprecated class Liberty. (This class is not perfect)
     obj = liberty.Liberty("Salutation")
   'Salutation'
   'Salutation'

If a deprecated class is used, then a warning message is emitted during class instantiation.
In other word, deprecating a class is the same as deprecating it's ``__new__`` class method.

As a reminder, the magic method ``__new__`` will be called when instance is being created.
Using this method you can customize the instance creation.
the :func:`~deprecated.deprecated` decorator patches the ``__new__`` method in order to
emmit the warning message before instance creation.


Controlling warnings
--------------------

.. _Python warning control: https://docs.python.org/3/library/warnings.html
.. _-W: https://docs.python.org/3/using/cmdline.html#cmdoption-w
.. _PYTHONWARNINGS: https://docs.python.org/3/using/cmdline.html#envvar-PYTHONWARNINGS

Warnings are emitted using the `Python warning control`_. By default, Python installs several warning filters,
which can be overridden by the `-W`_ command-line option, the `PYTHONWARNINGS`_ environment variable and
calls to :func:`warnings.filterwarnings`. The warnings filter controls whether warnings are ignored, displayed,
or turned into errors (raising an exception).

For instance:

.. literalinclude:: tutorial/warning_ctrl/filter_warnings_demo.py

When the user runs this script, the deprecation warnings are ignored in the main program,
so no warning message are emitted:

.. code-block:: sh

   $ python filter_warnings_demo.py

   fun


Deprecation warning classes
---------------------------

The :func:`deprecated.classic.deprecated` and :func:`deprecated.sphinx.deprecated` functions
are using the :exc:`DeprecationWarning` category but you can customize them by using your own category
(or hierarchy of categories).

* *category* classes which you can use (among other) are:

  +----------------------------------+-----------------------------------------------+
  | Class                            | Description                                   |
  +==================================+===============================================+
  | :exc:`DeprecationWarning`        | Base category for warnings about deprecated   |
  |                                  | features when those warnings are intended for |
  |                                  | other Python developers (ignored by default,  |
  |                                  | unless triggered by code in ``__main__``).    |
  +----------------------------------+-----------------------------------------------+
  | :exc:`FutureWarning`             | Base category for warnings about deprecated   |
  |                                  | features when those warnings are intended for |
  |                                  | end users of applications that are written in |
  |                                  | Python.                                       |
  +----------------------------------+-----------------------------------------------+
  | :exc:`PendingDeprecationWarning` | Base category for warnings about features     |
  |                                  | that will be deprecated in the future         |
  |                                  | (ignored by default).                         |
  +----------------------------------+-----------------------------------------------+

You can define your own deprecation warning hierarchy based on the standard deprecation classes.

For instance:

.. literalinclude:: tutorial/warning_ctrl/warning_classes_demo.py

When the user runs this script, the deprecation warnings for the 3.0 version are ignored:

.. code-block:: sh

   $ python warning_classes_demo.py

    foo
    bar
    warning_classes_demo.py:30: DeprecatedIn26: Call to deprecated function (or staticmethod) foo. (deprecated function)
      foo()


Filtering warnings locally
--------------------------

The :func:`deprecated.classic.deprecated` and :func:`deprecated.sphinx.deprecated` functions
can change the warning filtering locally (at function calls).

* *action* is one of the following strings:

  +---------------+----------------------------------------------+
  | Value         | Disposition                                  |
  +===============+==============================================+
  | ``"default"`` | print the first occurrence of matching       |
  |               | warnings for each location (module +         |
  |               | line number) where the warning is issued     |
  +---------------+----------------------------------------------+
  | ``"error"``   | turn matching warnings into exceptions       |
  +---------------+----------------------------------------------+
  | ``"ignore"``  | never print matching warnings                |
  +---------------+----------------------------------------------+
  | ``"always"``  | always print matching warnings               |
  +---------------+----------------------------------------------+
  | ``"module"``  | print the first occurrence of matching       |
  |               | warnings for each module where the warning   |
  |               | is issued (regardless of line number)        |
  +---------------+----------------------------------------------+
  | ``"once"``    | print only the first occurrence of matching  |
  |               | warnings, regardless of location             |
  +---------------+----------------------------------------------+

You can define the *action* keyword parameter to override the filtering warnings locally.

For instance:

.. literalinclude:: tutorial/warning_ctrl/filter_action_demo.py

In this example, even if the global filter is set to "ignore", a call to the ``foo()``
function will raise an exception because the *action* is set to "error".

.. code-block:: sh

   $ python filter_action_demo.py

   Traceback (most recent call last):
     File "filter_action_demo.py", line 12, in <module>
       foo()
     File "path/to/deprecated/classic.py", line 274, in wrapper_function
       warnings.warn(msg, category=category, stacklevel=_stacklevel)
   DeprecationWarning: Call to deprecated function (or staticmethod) foo. (do not call it)


Modifying the deprecated code reference
---------------------------------------

By default, when a deprecated function or class is called, the warning message indicates the location of the caller.

The ``extra_stacklevel`` parameter allows customizing the stack level reference in the deprecation warning message.

This parameter is particularly useful in scenarios where you have a factory or utility function that creates deprecated
objects or performs deprecated operations. By specifying an ``extra_stacklevel`` value, you can control the stack level
at which the deprecation warning is emitted, making it appear as if the calling function is the deprecated one,
rather than the actual deprecated entity.

For example, if you have a factory function ``create_object()`` that creates deprecated objects, you can use
the ``extra_stacklevel`` parameter to emit the deprecation warning at the calling location. This provides clearer and
more actionable deprecation messages, allowing developers to identify and update the code that invokes the deprecated
functionality.

For instance:

.. literalinclude:: tutorial/warning_ctrl/extra_stacklevel_demo.py

Please note that the ``extra_stacklevel`` value should be an integer indicating the number of stack levels to skip
when emitting the deprecation warning.
