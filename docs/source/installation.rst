.. _installation:

Installation
============

Python Version
--------------

Our project supports Python 2.7 (for historical reasons), Python 3.4 and newer versions, as well as PyPy 2.7 and
PyPy 3.6 and newer. We recommend using the latest version of Python 3 whenever possible.

Dependencies
------------

This library uses the `Wrapt`_ library as a basis to construct
function wrappers and decorator functions.

.. _Wrapt: http://wrapt.readthedocs.io/en/latest/

The table below shows the compatibility matrix between Python versions and the `wrapt` versions that have been
tested to date. Recent versions are listed first.

.. list-table:: Compatibility matrix (tested versions)
   :header-rows: 1
   :widths: 25 9 9 9 9 9 9 9 9 9

   * - Python / wrapt
     - 2.0
     - 1.17
     - 1.16
     - 1.15
     - 1.14
     - 1.13
     - 1.12
     - 1.11
     - 1.10
   * - py3.13
     - ✓
     - ✓
     - ✗
     - ✗
     - ✗
     - ✗
     - ✗
     - ✗
     - ✗
   * - py3.12
     - ✓
     - ✓
     - ✓
     - ✗
     - ✗
     - ✗
     - ✗
     - ✗
     - ✗
   * - py3.11
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✗
     - ✗
     - ✗
     - ✗
   * - py3.10
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
   * - py3.9
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
   * - py3.8
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
   * - py3.7
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓

Legend: ✓ = tested and compatible ; ✗ = incompatible.

Development dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

These distributions will not be installed automatically.
You need to install them explicitly with `pip install -e .[dev]`.

*   `pytest`_ is a framework which makes it easy to write small tests,
    yet scales to support complex functional testing for applications and libraries…
*   `pytest-cov`_ is a `pytest`_ plugin used to produce coverage reports.
*   `tox`_ aims to automate and standardize testing in Python.
    It is part of a larger vision of easing the packaging, testing and release process of Python software…
*   `bump2version`_ is a small command line tool to simplify releasing software
    by updating all version strings in your source code by the correct increment.
    Also creates commits and tags…
*   `sphinx`_ is a tool that makes it easy to create intelligent and beautiful documentation.

.. _pytest: https://docs.pytest.org/en/latest/
.. _pytest-cov: http://pytest-cov.readthedocs.io/en/latest/
.. _tox: https://tox.readthedocs.io/en/latest/
.. _bump2version: https://github.com/c4urself/bump2version
.. _sphinx: http://www.sphinx-doc.org/en/stable/index.html


Virtual environments
--------------------

Use a virtual environment to manage the dependencies for your project, both in
development and in production.

What problem does a virtual environment solve? The more Python projects you
have, the more likely it is that you need to work with different versions of
Python libraries, or even Python itself. Newer versions of libraries for one
project can break compatibility in another project.

Virtual environments are independent groups of Python libraries, one for each
project. Packages installed for one project will not affect other projects or
the operating system's packages.

Python 3 comes bundled with the :mod:`venv` module to create virtual
environments. If you're using a modern version of Python, you can continue on
to the next section.

If you're using Python 2, see :ref:`install-install-virtualenv` first.

.. _install-create-env:

Create an environment
~~~~~~~~~~~~~~~~~~~~~

Create a project folder and a :file:`venv` folder within:

.. code-block:: sh

    mkdir myproject
    cd myproject
    python3 -m venv venv

On Windows:

.. code-block:: bat

    py -3 -m venv venv

If you needed to install virtualenv because you are on an older version of
Python, use the following command instead:

.. code-block:: sh

    virtualenv venv

On Windows:

.. code-block:: bat

    \Python27\Scripts\virtualenv.exe venv

Activate the environment
~~~~~~~~~~~~~~~~~~~~~~~~

Before you work on your project, activate the corresponding environment:

.. code-block:: sh

    . venv/bin/activate

On Windows:

.. code-block:: bat

    venv\Scripts\activate

Your shell prompt will change to show the name of the activated environment.

Install Deprecated
-------------------------

Within the activated environment, use the following command to install Deprecated:

.. code-block:: sh

    pip install Deprecated

Living on the edge
~~~~~~~~~~~~~~~~~~

If you want to work with the latest Deprecated code before it's released, install or
update the code from the master branch:

.. code-block:: sh

    pip install -U https://github.com/laurent-laporte-pro/deprecated/archive/master.tar.gz

.. _install-install-virtualenv:

Install virtualenv
------------------

If you are using Python 2, the venv module is not available. Instead,
install `virtualenv`_.

On Linux, virtualenv is provided by your package manager:

.. code-block:: sh

    # Debian, Ubuntu
    sudo apt-get install python-virtualenv

    # CentOS, Fedora
    sudo yum install python-virtualenv

    # Arch
    sudo pacman -S python-virtualenv

If you are on Mac OS X or Windows, download `get-pip.py`_, then:

.. code-block:: sh

    sudo python2 Downloads/get-pip.py
    sudo python2 -m pip install virtualenv

On Windows, as an administrator:

.. code-block:: bat

    \Python27\python.exe Downloads\get-pip.py
    \Python27\python.exe -m pip install virtualenv

Now you can continue to :ref:`install-create-env`.

.. _virtualenv: https://virtualenv.pypa.io/
.. _get-pip.py: https://bootstrap.pypa.io/get-pip.py
