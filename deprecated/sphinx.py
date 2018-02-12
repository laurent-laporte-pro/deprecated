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
import textwrap

import wrapt

from deprecated.classic import ClassicAdapter
from deprecated.classic import deprecated as _classic_deprecated


class SphinxAdapter(ClassicAdapter):
    # todo: add docstring
    def __init__(self, directive, reason="", version=""):
        self.directive = directive
        super(SphinxAdapter, self).__init__(reason=reason, version=version)

    def __call__(self, wrapped):
        reason = textwrap.dedent(self.reason).strip()
        reason = '\n'.join(textwrap.fill(line, width=70, initial_indent='   ', subsequent_indent='   ')
                           for line in reason.splitlines()).strip()
        docstring = textwrap.dedent(wrapped.__doc__ or "")
        if docstring:
            docstring += "\n\n"
        if self.version:
            docstring += ".. {directive}:: {version}\n".format(directive=self.directive, version=self.version)
        else:
            docstring += ".. {directive}::\n".format(directive=self.directive)
        if reason:
            docstring += "   {reason}\n".format(reason=reason)
        wrapped.__doc__ = docstring
        return wrapped


def versionadded(reason="", version=""):
    # todo: add docstring with examples
    adapter = SphinxAdapter('versionadded', reason=reason, version=version)

    # noinspection PyUnusedLocal
    @wrapt.decorator(adapter=adapter)
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)

    return wrapper


def versionchanged(reason="", version=""):
    # todo: add docstring with examples
    adapter = SphinxAdapter('versionchanged', reason=reason, version=version)

    # noinspection PyUnusedLocal
    @wrapt.decorator(adapter=adapter)
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)

    return wrapper


def deprecated(*args, **kwargs):
    # todo: add docstring with examples
    directive = kwargs.pop('directive', 'deprecated')
    adapter_cls = kwargs.pop('adapter_cls', SphinxAdapter)
    return _classic_deprecated(*args,
                               directive=directive,
                               adapter_cls=adapter_cls,
                               **kwargs)
