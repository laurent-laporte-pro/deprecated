# coding: utf-8
"""
Sphinx directive integration
============================

We usually need to document the life-cycle of functions and classes:
when they are created, modified or deprecated.

To do that, `Sphinx <http://www.sphinx-doc.org>`_ has a set
of `Paragraph-level markups <http://www.sphinx-doc.org/en/stable/markup/para.html>`_:

- ``versionadded``: to document the version of the project which added the described feature to the library,
- ``versionchanged``: to document changes of a feature,
- ``deprecated``: to document a deprecated feature.

The purpose of this module is to defined decorators which adds this Sphinx directives
to the docstring of your function and classes.

Of course, the ``@deprecated`` decorator will emit a deprecation warning
when the function/method is called or the class is constructed.
"""
import inspect
import textwrap
import warnings

import wrapt

string_types = (type(b''), type(u''))


class HistoryAdapter(wrapt.AdapterFactory):
    template = textwrap.dedent("""\

    .. {directive}:: {version}
       {reason}
    """)

    def __init__(self, directive, reason=None, version=None):
        self.directive = directive
        self.reason = reason
        self.version = version

    def __call__(self, wrapped):
        reason = textwrap.dedent(self.reason).strip()
        reason = '\n'.join(textwrap.fill(line, width=70, initial_indent='   ', subsequent_indent='   ')
                           for line in reason.splitlines()).strip()
        attrs = {'directive': self.directive, 'version': self.version, 'reason': reason}
        docstring = self.template.format(**attrs)
        wrapped.__doc__ = textwrap.dedent(wrapped.__doc__ or "")
        wrapped.__doc__ += docstring
        return wrapped


def versionadded(reason=None, version=None):
    @wrapt.decorator(adapter=HistoryAdapter('versionadded', reason=reason, version=version))
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)

    return wrapper


def versionchanged(reason=None, version=None):
    @wrapt.decorator(adapter=HistoryAdapter('versionchanged', reason=reason, version=version))
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)

    return wrapper


def _get_deprecated_msg(reason, wrapped, instance):
    if instance is None:
        if inspect.isclass(wrapped):
            fmt = "Call to deprecated class {{name}}{reason}."
        else:
            fmt = "Call to deprecated function (or staticmethod) {{name}}{reason}."
    else:
        if inspect.isclass(instance):
            fmt = "Call to deprecated class method {{name}}{reason}."
        else:
            fmt = "Call to deprecated method {{name}}{reason}."
    reason = " ({0})".format(reason) if reason else ""
    return fmt.format(reason=reason)


def deprecated(reason=None, version=None):
    @wrapt.decorator(adapter=HistoryAdapter('deprecated', reason=reason, version=version))
    def wrapper(wrapped, instance, args, kwargs):
        msg_fmt = _get_deprecated_msg(reason, wrapped, instance)
        msg = msg_fmt.format(name=wrapped.__name__)
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)
        return wrapped(*args, **kwargs)

    return wrapper
