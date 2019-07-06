#!/usr/bin/env python
#  -*- coding: utf-8 -*-
u"""
Deprecated Library
------------------

Deprecated is Easy to Use
`````````````````````````

If you need to mark a function or a method as deprecated,
you can use the ``@deprecated`` decorator:

Save in a hello.py:

.. code:: python

    from deprecated import deprecated


    @deprecated(version='1.2.1', reason="You should use another function")
    def some_old_function(x, y):
        return x + y


    class SomeClass(object):
        @deprecated(version='1.3.0', reason="This method is deprecated")
        def some_old_method(self, x, y):
            return x + y


    some_old_function(12, 34)
    obj = SomeClass()
    obj.some_old_method(5, 8)


And Easy to Setup
`````````````````

And run it:

.. code:: bash

    $ pip install Deprecated
    $ python hello.py
    hello.py:15: DeprecationWarning: Call to deprecated function (or staticmethod) some_old_function.
    (You should use another function) -- Deprecated since version 1.2.0.
      some_old_function(12, 34)
    hello.py:17: DeprecationWarning: Call to deprecated method some_old_method.
    (This method is deprecated) -- Deprecated since version 1.3.0.
      obj.some_old_method(5, 8)


You can document your code
``````````````````````````

Have you ever wonder how to document that some functions, classes, methods, etc. are deprecated?
This is now possible with the integrated Sphinx directives:

For instance, in hello_sphinx.py:

.. code:: python

    from deprecated.sphinx import deprecated
    from deprecated.sphinx import versionadded
    from deprecated.sphinx import versionchanged


    @versionadded(version='1.0', reason="This function is new")
    def function_one():
        '''This is the function one'''


    @versionchanged(version='1.0', reason="This function is modified")
    def function_two():
        '''This is the function two'''


    @deprecated(version='1.0', reason="This function will be removed soon")
    def function_three():
        '''This is the function three'''


    function_one()
    function_two()
    function_three()  # warns

    help(function_one)
    help(function_two)
    help(function_three)


The result it immediate
```````````````````````

Run it:

.. code:: bash

    $ python hello_sphinx.py

    hello_sphinx.py:23: DeprecationWarning: Call to deprecated function (or staticmethod) function_three.
    (This function will be removed soon) -- Deprecated since version 1.0.
      function_three()  # warns

    Help on function function_one in module __main__:

    function_one()
        This is the function one

        .. versionadded:: 1.0
           This function is new

    Help on function function_two in module __main__:

    function_two()
        This is the function two

        .. versionchanged:: 1.0
           This function is modified

    Help on function function_three in module __main__:

    function_three()
        This is the function three

        .. deprecated:: 1.0
           This function will be removed soon


Links
`````

* `Python package index (PyPi) <https://pypi.python.org/pypi/deprecated>`_
* `GitHub website <https://github.com/tantale/deprecated>`_
* `Read The Docs <https://readthedocs.org/projects/deprecated>`_
* `EBook on Lulu.com <http://www.lulu.com/commerce/index.php?fBuyContent=21305117>`_
* `StackOverFlow Q&A <https://stackoverflow.com/a/40301488/1513933>`_
* `Development version
  <https://github.com/tantale/deprecated/zipball/master#egg=Deprecated-dev>`_

"""
from setuptools import setup

setup(
    name='Deprecated',
    version='1.2.6',
    url='https://github.com/tantale/deprecated',
    project_urls={
        "Documentation": "https://deprecated.readthedocs.io/en/latest/",
        "Source": "https://github.com/tantale/deprecated",
        "Bug Tracker": "https://github.com/tantale/deprecated/issues"},
    license='MIT',
    author='Laurent LAPORTE',  # since v1.1.0
    author_email='tantale.solutions@gmail.com',
    description='Python @deprecated decorator to deprecate old python classes, functions or methods.',
    long_description=__doc__,
    keywords='deprecate,deprecated,deprecation,warning,warn,decorator',
    packages=['deprecated'],
    install_requires=[
        'wrapt < 2, >= 1.10',
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    extras_require={
        'dev': [
            'tox',
            'PyTest             ; python_version >= "3.6"',
            'PyTest < 5         ; python_version < "3"',
            'PyTest-Cov         ; python_version >= "3.6"',
            'PyTest-Cov < 2.6   ; python_version < "3"',
            'bumpversion < 1',
            'sphinx < 2',
        ],
    },

    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
)
