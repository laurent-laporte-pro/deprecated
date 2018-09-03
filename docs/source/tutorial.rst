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

   using_liberty.py:4: DeprecationWarning: Call to deprecated function print_value.
     liberty.print_value("hello")
   'hello'
   using_liberty.py:5: DeprecationWarning: Call to deprecated function print_value.
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

   using_liberty.py:4: DeprecationWarning: Call to deprecated function print_value (This function is rotten, use 'better_print' instead).
     liberty.print_value("hello")
   'hello'
   using_liberty.py:5: DeprecationWarning: Call to deprecated function print_value (This function is rotten, use 'better_print' instead).
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

   using_liberty.py:5: DeprecationWarning: Call to deprecated function print_value (This method is rotten, use 'better_print' instead).
     obj.print_value()
   'Greeting'
   using_liberty.py:6: DeprecationWarning: Call to deprecated function print_value (This method is rotten, use 'better_print' instead).
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

   using_liberty.py:4: DeprecationWarning: Call to deprecated class Liberty (This class is not perfect).
     obj = liberty.Liberty("Salutation")
   'Salutation'
   'Salutation'

If a deprecated class is used, then a warning message is emitted during class instantiation.
In other word, deprecating a class is the same as deprecating it's ``__new__`` class method.

As a reminder, the magic method ``__new__`` will be called when instance is being created.
Using this method you can customize the instance creation.
the :func:`~deprecated.deprecated` decorator patches the ``__new__`` method in order to
emmit the warning message before instance creation.
