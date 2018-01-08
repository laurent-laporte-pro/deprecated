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
import warnings

import wrapt

from deprecated.basic import Annotation


class SphinxAdapter(Annotation, wrapt.AdapterFactory):
    template = textwrap.dedent("""\

    .. {directive}:: {version}
       {reason}
    """)

    def __init__(self, directive, reason="", version=""):
        self.directive = directive
        super(SphinxAdapter, self).__init__(reason=reason, version=version)

    def __call__(self, wrapped):
        reason = textwrap.dedent(self.reason).strip()
        reason = '\n'.join(textwrap.fill(line, width=70, initial_indent='   ', subsequent_indent='   ')
                           for line in reason.splitlines()).strip()
        attrs = {'directive': self.directive, 'version': self.version, 'reason': reason}
        docstring = self.template.format(**attrs)
        wrapped.__doc__ = textwrap.dedent(wrapped.__doc__ or "")
        wrapped.__doc__ += docstring
        return wrapped


def versionadded(reason="", version=""):
    adapter = SphinxAdapter('versionadded', reason=reason, version=version)

    @wrapt.decorator(adapter=adapter)
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)

    return wrapper


def versionchanged(reason="", version=""):
    adapter = SphinxAdapter('versionchanged', reason=reason, version=version)

    @wrapt.decorator(adapter=adapter)
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)

    return wrapper


def deprecated(reason="", version=""):
    adapter = SphinxAdapter('deprecated', reason=reason, version=version)

    @wrapt.decorator(adapter=adapter)
    def wrapper(wrapped, instance, args, kwargs):
        msg = adapter.get_deprecated_msg(wrapped, instance)
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)
        return wrapped(*args, **kwargs)

    return wrapper
