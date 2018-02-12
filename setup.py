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


    @deprecated
    def some_old_function(x, y):
        return x + y


    class SomeClass(object):
        @deprecated
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
    hello.py:15: DeprecationWarning: Call to deprecated function some_old_function.
      some_old_function(12, 34)
    hello.py:17: DeprecationWarning: Call to deprecated function some_old_method.
      obj.some_old_method(5, 8)


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
    version='1.1.1',
    url='https://github.com/tantale/deprecated',
    license='MIT',
    author='Laurent LAPORTE',  # since v1.1.0
    author_email='tantate.solutions@gmail.com',
    description='Python @deprecated decorator to deprecate old python classes, functions or methods.',
    long_description=__doc__,
    keywords='deprecate,deprecated,deprecation,warning,warn,decorator',
    packages=['deprecated'],
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'tox',
            'bumpversion',
            'sphinx',
        ],
    },
)
