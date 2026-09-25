(white_paper)=

# White Paper

This white paper shows some examples of how function deprecation is implemented in the Python Standard Library and Famous Open Source libraries.

You will see which kind of deprecation you can find in such libraries, and how it is documented in the user manuel.

(python standard library)=

## The Python Standard Library

:Library: [Python]
:GitHub: [python/cpython](https://github.com/python/cpython).
:Version: v3.8.dev

An example of function deprecation can be found in the {mod}`urllib` module ({file}`Lib/urllib/parse.py`):

```python
def to_bytes(url):
    warnings.warn("urllib.parse.to_bytes() is deprecated as of 3.8",
                  DeprecationWarning, stacklevel=2)
    return _to_bytes(url)
```

In the Python library, a warning is emitted in the function body using the function {func}`warnings.warn`.
This implementation is straightforward, it uses the category {exc}`DeprecationWarning` for warning filtering.

Another example is the deprecation of the *collections* ABC, which are now moved in the {mod}`collections.abc` module.
This example is available in the {mod}`collections` module ({file}`Lib/collections/__init__.py`):

```python
def __getattr__(name):
    if name in _collections_abc.__all__:
        obj = getattr(_collections_abc, name)
        import warnings
        warnings.warn("Using or importing the ABCs from 'collections' instead "
                      "of from 'collections.abc' is deprecated, "
                      "and in 3.8 it will stop working",
                      DeprecationWarning, stacklevel=2)
        globals()[name] = obj
        return obj
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
```

The warning is only emitted when an ABC is accessed from the {mod}`collections` instead of {mod}`collections.abc` module.

We can also see an example of keyword argument deprecation in the {class}`~collections.UserDict` class:

```python
def __init__(*args, **kwargs):
    if not args:
        raise TypeError("descriptor '__init__' of 'UserDict' object "
                        "needs an argument")
    self, *args = args
    if len(args) > 1:
        raise TypeError('expected at most 1 arguments, got %d' % len(args))
    if args:
        dict = args[0]
    elif 'dict' in kwargs:
        dict = kwargs.pop('dict')
        import warnings
        warnings.warn("Passing 'dict' as keyword argument is deprecated",
                      DeprecationWarning, stacklevel=2)
    else:
        dict = None
    self.data = {}
    if dict is not None:
        self.update(dict)
    if len(kwargs):
        self.update(kwargs)
```

Again, this implementation is straightforward: if the *dict* keyword argument is used, a warning is emitted.

Python make also use of the category {exc}`PendingDeprecationWarning` for instance in the {mod}`asyncio.tasks` module
({file}`Lib/asyncio/tasks.py`):

```python
@classmethod
def current_task(cls, loop=None):
    warnings.warn("Task.current_task() is deprecated, "
                  "use asyncio.current_task() instead",
                  PendingDeprecationWarning,
                  stacklevel=2)
    if loop is None:
        loop = events.get_event_loop()
    return current_task(loop)
```

The category {exc}`FutureWarning` is also used to emit a warning when the functions is broken and will be
fixed in a "future" release. We can see for instance the method {meth}`~xml.etree.ElementTree.ElementTree.find`
of the class {class}`~xml.etree.ElementTree.ElementTree` ({file}`Lib/xml/etree/ElementTree.py`):

```python
def find(self, path, namespaces=None):
    if path[:1] == "/":
        path = "." + path
        warnings.warn(
            "This search is broken in 1.3 and earlier, and will be "
            "fixed in a future version.  If you rely on the current "
            "behaviour, change it to %r" % path,
            FutureWarning, stacklevel=2
            )
    return self._root.find(path, namespaces)
```

As a conclusion:

- Python library uses {func}`warnings.warn` to emit a deprecation warning in the body of functions.
- 3 categories are used: {exc}`DeprecationWarning`, {exc}`PendingDeprecationWarning` and {exc}`FutureWarning`.
- The docstring doesn't show anything about deprecation.
- The documentation warns about some, but not all, deprecated usages.

(flask library)=

## The Flask Library

:Library: [Flask]
:GitHub: [pallets/flask](https://github.com/pallets/flask).
:Version: v1.1.dev

In the source code of Flask, we find only few deprecations: in the {mod}`~flask.app` ({file}`flask/app.py`)
and in the {mod}`~flask.helpers` ({file}`flask/helpers.py`) modules.

In the Flask Library, like in the {ref}`Python Standard Library <python standard library>`, deprecation warnings are emitted during function calls.
The implementation make use of the category {exc}`DeprecationWarning`.

Unlike the {ref}`Python Standard Library <python standard library>`, the docstring documents explicitly the deprecation.
Flask uses [Sphinx]’s [deprecated directive]:

The bellow example shows the deprecation of the {meth}`~flask.Flask.open_session` method:

```python
def open_session(self, request):
    """Creates or opens a new session.  Default implementation stores all
    session data in a signed cookie.  This requires that the
    :attr:`secret_key` is set.  Instead of overriding this method
    we recommend replacing the :class:`session_interface`.

    .. deprecated: 1.0
        Will be removed in 1.1. Use ``session_interface.open_session``
        instead.

    :param request: an instance of :attr:`request_class`.
    """

    warnings.warn(DeprecationWarning(
        '"open_session" is deprecated and will be removed in 1.1. Use'
        ' "session_interface.open_session" instead.'
    ))
    return self.session_interface.open_session(self, request)
```

:::{hint}
When the function {func}`warnings.warn` is called with a {exc}`DeprecationWarning` instance,
the instance class is used like a warning category.
:::

The documentation also mention a {exc}`flask.exthook.ExtDeprecationWarning` (which is not found in Flask’s source code):

``````````````````rst
Extension imports
`````````````````

Extension imports of the form ``flask.ext.foo`` are deprecated, you should use
``flask_foo``.

The old form still works, but Flask will issue a
``flask.exthook.ExtDeprecationWarning`` for each extension you import the old
way. We also provide a migration utility called `flask-ext-migrate
<https://github.com/pallets/flask-ext-migrate>`_ that is supposed to
automatically rewrite your imports for this.
``````````````````

As a conclusion:

- Flask library uses {func}`warnings.warn` to emit a deprecation warning in the body of functions.
- Only one category is used: {exc}`DeprecationWarning`.
- The docstring use [Sphinx]’s [deprecated directive].
- The API documentation contains the deprecated usages.

(django library)=

## The Django Library

:Library: Django
:GitHub: [django/django](https://github.com/django/django).
:Version: v3.0.dev

The [Django] Library defines several categories for deprecation in the module {mod}`django.utils.deprecation`:

- The category {exc}`~django.utils.deprecation.RemovedInDjango31Warning` which inherits
  from {exc}`DeprecationWarning`.
- The category {exc}`~django.utils.deprecation.RemovedInDjango40Warning` which inherits
  from {exc}`PendingDeprecationWarning`.
- The category {exc}`~django.utils.deprecation.RemovedInNextVersionWarning` which is an alias
  of {exc}`~django.utils.deprecation.RemovedInDjango40Warning`.

The [Django] Library don't use {exc}`DeprecationWarning` or {exc}`PendingDeprecationWarning` directly,
but always use one of this 2 classes. The category {exc}`~django.utils.deprecation.RemovedInNextVersionWarning`
is only used in unit tests.

There are a lot of class deprecation examples. The deprecation warning is emitted during the call
of the `__init__` method. For instance in the class {class}`~django.contrib.postgres.forms.ranges.FloatRangeField`
({file}`django/contrib/staticfiles/storage.py`):

```python
class FloatRangeField(DecimalRangeField):
    base_field = forms.FloatField

    def __init__(self, **kwargs):
        warnings.warn(
            'FloatRangeField is deprecated in favor of DecimalRangeField.',
            RemovedInDjango31Warning, stacklevel=2,
        )
        super().__init__(**kwargs)
```

The implementation in the Django Library is similar to the one done in the {ref}`Python Standard Library <python standard library>`:
deprecation warnings are emitted during function calls.
The implementation use the category {exc}`~django.utils.deprecation.RemovedInDjango31Warning`.

In the Django Library, we also find an example of property deprecation:
The property {meth}`~django.conf.LazySettings.FILE_CHARSET` of the class {class}`django.conf.LazySettings`.
The implementation of this property is:

```python
@property
def FILE_CHARSET(self):
    stack = traceback.extract_stack()
    # Show a warning if the setting is used outside of Django.
    # Stack index: -1 this line, -2 the caller.
    filename, _line_number, _function_name, _text = stack[-2]
    if not filename.startswith(os.path.dirname(django.__file__)):
        warnings.warn(
            FILE_CHARSET_DEPRECATED_MSG,
            RemovedInDjango31Warning,
            stacklevel=2,
        )
    return self.__getattr__('FILE_CHARSET')
```

We also find function deprecations, mainly with the category {exc}`~django.utils.deprecation.RemovedInDjango40Warning`.
For instance, the function {func}`~django.utils.encoding.smart_text` emits a deprecation warning as follow:

```python
def smart_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    warnings.warn(
        'smart_text() is deprecated in favor of smart_str().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return smart_str(s, encoding, strings_only, errors)
```

The Django Library also define a decorator {class}`~django.utils.deprecation.warn_about_renamed_method`
which is used internally in the metaclass {class}`~django.utils.deprecation.RenameMethodsBase`.
This metaclass is only used in unit tests to check renamed methods.

As a conclusion:

- The Django library uses {func}`warnings.warn` to emit a deprecation warning in the body of functions.
- It uses two categories which inherits the standard categories {exc}`DeprecationWarning`
  and {exc}`PendingDeprecationWarning`.
- The source code of the Django Library doesn't contains much docstring.
  The deprecation never appears in the docstring anyway.
- The release notes contain information about deprecated features.

## The lxml Library

:Library: [lxml]
:GitHub: [lxml/lxml](https://github.com/lxml/lxml).
:Version: v4.3.2.dev

The [lxml] Library is developed in Cython, not Python. But, it is a similar language.
This library mainly use comments or docstring to mark function as deprecated.

For instance, in the class {class}`lxml.xpath._XPathEvaluatorBase` ({file}`src/lxml/xpath.pxi`),
the `evaluate` method is deprecated as follow:

```python
def evaluate(self, _eval_arg, **_variables):
    u"""evaluate(self, _eval_arg, **_variables)

    Evaluate an XPath expression.

    Instead of calling this method, you can also call the evaluator object
    itself.

    Variables may be provided as keyword arguments.  Note that namespaces
    are currently not supported for variables.

    :deprecated: call the object, not its method.
    """
    return self(_eval_arg, **_variables)
```

There is only one example of usage of the function {func}`warnings.warn`:
in the {class}`~lxml.etree._ElementTree` class ({file}`src/lxml/etree.pyx`):

```python
if docstring is not None and doctype is None:
    import warnings
    warnings.warn(
        "The 'docstring' option is deprecated. Use 'doctype' instead.",
        DeprecationWarning)
    doctype = docstring
```

As a conclusion:

- Except in one example, the lxml library doesn't use {func}`warnings.warn` to emit a deprecation warnings.
- The deprecations are described in the function docstrings.
- The release notes contain information about deprecated features.

## The openpyxl Library

:Library: openpyxl
:Bitbucket: [openpyxl/openpyxl](https://bitbucket.org/openpyxl/openpyxl).
:Version: v2.6.1.dev

[openpyxl] is a Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.
Tu warn about deprecation, this library uses a home-made `@deprecated` decorator.

The implementation of this decorator is an adapted copy of the first version of Tantale’s `@deprecated` decorator.
It has the enhancement to update the docstring of the decorated function.
So, this is similar to the function {func}`deprecated.sphinx.deprecated`.

```python
string_types = (type(b''), type(u''))
def deprecated(reason):

    if isinstance(reason, string_types):

        def decorator(func1):

            if inspect.isclass(func1):
                fmt1 = "Call to deprecated class {name} ({reason})."
            else:
                fmt1 = "Call to deprecated function {name} ({reason})."

            @wraps(func1)
            def new_func1(*args, **kwargs):
                #warnings.simplefilter('default', DeprecationWarning)
                warnings.warn(
                    fmt1.format(name=func1.__name__, reason=reason),
                    category=DeprecationWarning,
                    stacklevel=2
                )
                return func1(*args, **kwargs)

            # Enhance docstring with a deprecation note
            deprecationNote = "\n\n.. note::\n    Deprecated: " + reason
            if new_func1.__doc__:
                new_func1.__doc__ += deprecationNote
            else:
                new_func1.__doc__ = deprecationNote
            return new_func1

        return decorator

    elif inspect.isclass(reason) or inspect.isfunction(reason):
        raise TypeError("Reason for deprecation must be supplied")

    else:
        raise TypeError(repr(type(reason)))
```

As a conclusion:

- The openpyxl library uses a decorator to deprecate functions.
- It uses the category {exc}`DeprecationWarning`.
- The decorator update the docstring and add a `.. note::` directive,
  which is visible in the documentation.

[deprecated directive]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-deprecated
[django]: https://docs.djangoproject.com/
[flask]: http://flask.pocoo.org/docs/
[lxml]: https://lxml.de
[openpyxl]: https://openpyxl.readthedocs.io/
[python]: https://docs.python.org/fr/3/
[sphinx]: http://www.sphinx-doc.org/en/stable/index.html
