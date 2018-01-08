Introduction
============

What "Deprecated" Means
-----------------------

.. _Deprecated Library: https://pypi.python.org/pypi/deprecated

A function or class is deprecated when it is considered as it is no longer important. It is so unimportant, in fact, that you should no longer use it, since it has been superseded and may cease to exist in the future.

As a module, a class or function evolves, its API (Application Programming Interface) inevitably changes: functions are renamed for consistency, new and better methods are added, and attributes change. But such changes introduce a problem. You need to keep the old API around until developers make the transition to the new one, but you don't want them to continue programming to the old API.

The ability to deprecate a class or a function solves the problem. Python Standard Library does not provide a way to express deprecation easily. The Python `Deprecated Library`_ is here to fulfill this lack.

When to Deprecate
-----------------

When you design an API, carefully consider whether it supersedes an old API. If it does, and you wish to encourage developers (users of the API) to migrate to the new API, then deprecate the old API. Valid reasons to deprecate an API include:

- It is insecure, buggy, or highly inefficient;
- It is going away in a future release,
- It encourages bad coding practices.

Deprecation is a reasonable choice in all these cases because it preserves "backward compatibility" while encouraging developers to change to the new API. Also, the deprecation comments help developers decide when to move to the new API, and so should briefly mention the technical reasons for deprecation.

How to Deprecate
----------------

.. _Python warning control: https://docs.python.org/3/library/warnings.html

The Python Deprecated Library provides a ``@deprecated`` decorator to deprecate a class, method or function.

Using the decorator causes the Python interpreter to emit a warning at runtime, when an class instance is constructed, or a function is called. The warning is emitted using the `Python warning control`_. Warning messages are normally written to ``sys.stderr``, but their disposition can be changed flexibly, from ignoring all warnings to turning them into exceptions.

You are strongly recommended to use the ``@deprecated`` decorator with appropriate comments explaining how to use the new API. This ensures developers will have a workable migration path from the old API to the new API.

**Example:**

.. code-block:: python

    from deprecated import deprecated


    @deprecated(version='1.2.0', reason="You should use another function")
    def some_old_function(x, y):
        return x + y


    class SomeClass(object):
        @deprecated(version='1.3.0', reason="This method is deprecated")
        def some_old_method(self, x, y):
            return x + y


    some_old_function(12, 34)
    obj = SomeClass()
    obj.some_old_method(5, 8)

When you run this Python script, you will get something like this in the console:

.. code-block:: bash

    $ pip install Deprecated
    $ python hello.py
    hello.py:15: DeprecationWarning: Call to deprecated function (or staticmethod) some_old_function. (You should use another function) -- Deprecated since version 1.2.0.
      some_old_function(12, 34)
    hello.py:17: DeprecationWarning: Call to deprecated method some_old_method. (This method is deprecated) -- Deprecated since version 1.3.0.
      obj.some_old_method(5, 8)
