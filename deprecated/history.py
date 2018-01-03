# coding: utf-8
"""
Function Version history
========================

We usually need to document the life-cycle of functions and classes:
when they are created, modified or deprecated.

To do that, `Sphinx <http://www.sphinx-doc.org>`_ has a set
of `Paragraph-level markups <http://www.sphinx-doc.org/en/stable/markup/para.html>`_:

- ``versionadded``: to document the version of the project which added the described feature to the library,
- ``versionchanged``: to document changes of a feature,
- ``deprecated``: to document a deprecated feature.

The purpose of this module is to defined decorators which adds this Sphinx directives
to the docstring of your function and classes.
"""

import textwrap

import wrapt


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


def deprecated(reason=None, version=None):
    @wrapt.decorator(adapter=HistoryAdapter('deprecated', reason=reason, version=version))
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)

    return wrapper
