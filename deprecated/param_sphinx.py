# coding: utf-8
"""
Sphinx directive integration
============================

We usually need to document when a parameter is deprecated, to do this, we use `Sphinx <http://www.sphinx-doc.org>`_ directives:

- We use admonitions in sphinx to render warnings for every deprecated argument just below its description in docstring.
refer to `this <https://pradyunsg.me/furo/reference/admonitions/?highlight=warning#custom-titles>`_ link for more information.

The purpose of this module is to defined decorators which adds this Sphinx directives
to the docstring of your function and classes.

Of course, the ``@deprecated_param`` decorator will emit a deprecation warning
when the function/method is called or the class is constructed.
"""
import re
import textwrap

import wrapt

from deprecated.param import ClassicAdapterParam
from deprecated.param import deprecated_param as _classic_deprecated_param


class SphinxAdapterParam(ClassicAdapterParam):
    """
    Sphinx adapter -- *for advanced usage only*

    This adapter override the :class:`~deprecated.classic.ClassicAdapterParam`
    in order to add the Sphinx directives to the end of the function/class docstring.
    Such a directive is a `Paragraph-level markup <http://www.sphinx-doc.org/en/stable/markup/para.html>`_
    - The version number is added if provided.
    - The reason message is obviously added in the directive block if not empty.

    Warnings
    --------
    deprecated supports docstring modification for deprecated_args only in the numpydoc format, if your documentation uses any other format, this won't work. 
    """

    def __init__(
        self,
        action=None,
        category=DeprecationWarning,
        line_length=70,
        deprecated_args=None
    ):
        """
        Construct a wrapper adapter.
        :type  action: str
        :param action:
            A warning filter used to activate or not the deprecation warning.
            Can be one of "error", "ignore", "always", "default", "module", or "once".
            If ``None`` or empty, the the global filtering mechanism is used.
            See: `The Warnings Filter`_ in the Python documentation.

        :type  category: type
        :param category:
            The warning category to use for the deprecation warning.
            By default, the category class is :class:`~DeprecationWarning`,
            you can inherit this class to define your own deprecation warning category.

        :type  line_length: int
        :param line_length:
            Max line length of the directive text. If non nul, a long text is wrapped in several lines.

        :type deprecated_args: dict
        :param deprecated_args:
            Dictionary in the following format to deprecate `x` and `y`
            deprecated_args = {'x': {'reason': 'some reason','version': '1.0'},'y': {'reason': 'another reason','version': '2.0'}}

        """
        self.line_length = line_length
        self.deprecated_args = deprecated_args
        super(SphinxAdapterParam, self).__init__(action=action, category=category,deprecated_args = deprecated_args)

    def __call__(self, wrapped):
        """
        Add the Sphinx directive to your class or function.

        :param wrapped: Wrapped class or function.

        :return: the decorated class or function.
        """
        # -- build the directive division
        docstring = textwrap.dedent(wrapped.__doc__ or "")
        if docstring:
        # An empty line must separate the original docstring and the directive.
            docstring = re.sub(r"\n+$", "", docstring, flags=re.DOTALL) + "\n\n"
        else:
        # Avoid "Explicit markup ends without a blank line" when the decorated function has no docstring
            docstring = "\n"

        width = self.line_length - 3 if self.line_length > 3 else 2 ** 16
        if docstring=="\n":
            warnings.warn("Missing docstring, consider adding a numpydoc style docstring for the decorator to work (Sphinx directive won't be added)" , category=UserWarning, stacklevel=_class_stacklevel)
        else:
            for arg in set(self.deprecated_args.keys()):
                #first we search for the location of the parameters section
                search = re.search("Parameters[\s]*\n[\s]*----------", docstring)
                if search is None:
                    warnings.warn("Missing Parameter section, consider adding a numpydoc style parameters section in your docstring for the decorator to work (Sphinx directive won't be added)" , category=UserWarning, stacklevel=_class_stacklevel)
                else:
                    params_string = docstring[search.start():search.end()]

                    #we store the indentation of the values 
                    indentsize = re.search("----------", params_string).start() - re.search("Parameters[\s]*\n", params_string).end()
                    indent = ' '*indentsize

                    # we check if there is another section after parameters
                    if re.search(f"\n{indent}-----", docstring[search.end():]) is not None:
                        #if yes then we find the range of the parameters section
                        params_section_end = search.end() + re.search(f"\n{indent}-----", docstring[search.end():]).start()
                        dashes_in_next_section = docstring[params_section_end:].count('-')
                        params_section_end = params_section_end - dashes_in_next_section
                        params_section = docstring[search.start():params_section_end]
                    else:
                        #else the entire remaining docstring is in the parameters section
                        params_section = docstring[search.start():]

                    #we search for the description of the particular parameter we care about
                    if re.search(f"\n{indent}{arg}\s*:", params_section) is not None:
                        description_start = re.search(f"\n{indent}{arg}\s*:", params_section).end()
                        #we check whether there are more parameters after this one, or if its the last parameter described in the secion
                        #and store the position where we insert the warning

                        if re.search(f"\n{indent}\S", params_section[description_start:]):
                            insert_pos = re.search(f"\n{indent}\S", params_section[description_start:]).start()
                        else:
                            insert_pos = len(params_section[description_start:])
                        
                        #finally we store the warning fmt string
                        if self.deprecated_args[arg]['version']!="":
                            #the spaces are specifically cherrypicked for numpydoc docstrings
                            fmt = "\n\n    .. admonition:: Deprecated\n      :class: warning\n\n      Parameter {arg} deprecated since {version}"
                            div_lines = [fmt.format(version=self.deprecated_args[arg]['version'],arg=arg)]
                        else:
                            fmt = "\n\n    .. admonition:: Deprecated\n      :class: warning\n\n      Parameter {arg} deprecated"
                            div_lines = [fmt.format(version=self.deprecated_args[arg]['version'],arg=arg)]
                        width = 2**16
                        reason = textwrap.dedent(self.deprecated_args[arg]['reason']).strip()
                        reason = f'({reason})'
                        #formatting for docstring
                        for paragraph in reason.splitlines():
                            if paragraph:
                                div_lines.extend(
                                    textwrap.fill(
                                        paragraph,
                                        width=width,
                                        initial_indent='      ',
                                        subsequent_indent='',
                                    ).splitlines()
                                )
                            else:
                                div_lines.append("")
                        # -- append the directive division to the docstring
                        a=''
                        a += "".join("{}\n".format(line) for line in div_lines)
                        a = textwrap.indent(a, indent)
                        docstring = docstring[:search.start() + description_start+insert_pos]+"\n\n"+a+"\n\n"+docstring[search.start() + description_start+insert_pos:]
                        docstring = re.sub(r"[\n]{3,}", "\n\n", docstring)
                    else:
                        warnings.warn(f"Missing description for parameter {arg}, consider adding a numpydoc style description for the decorator to work (Sphinx directive won't be added)" , category=UserWarning, stacklevel=_class_stacklevel)

        wrapped.__doc__ = docstring
        return super(SphinxAdapterParam, self).__call__(wrapped)

    def get_deprecated_msg(self, wrapped, instance, kwargs):
        """
        Get the deprecation warning message (without Sphinx cross-referencing syntax) for the user.

        :param wrapped: Wrapped class or function.

        :param instance: The object to which the wrapped function was bound when it was called.

        :param kwargs: The keyword arguments passed to the wrapped function.

        :return: The warning message.e.

        """
        msg = super(SphinxAdapterParam, self).get_deprecated_msg(wrapped, instance, kwargs)
        # Strip Sphinx cross reference syntax (like ":function:", ":py:func:" and ":py:meth:")
        # Possible values are ":role:`foo`", ":domain:role:`foo`"
        # where ``role`` and ``domain`` should match "[a-zA-Z]+"
        
        #remember the msg variable is a dict
        if msg:
            for key in msg.keys():
                msg[key] = re.sub(r"(?: : [a-zA-Z]+ )? : [a-zA-Z]+ : (`[^`]*`)", r"\1", msg[key], flags=re.X)
                
        return msg

def deprecated_param(deprecated_args=None, line_length=70, **kwargs):
    """
    This decorator can be used to insert a "deprecated" warning
    in your function/class docstring.

    :type  line_length: int
    :param line_length:
        Max line length of the directive text. If non nul, a long text is wrapped in several lines.
    
    :type deprecated_args: dict
    :param deprecated_args: 
        A dictionary of the form ``{'parameter_name': {'version': 'version_number', 'reason': 'reason_for_deprecation'}}``.

    Keyword arguments can be:

    -   "action":
        A warning filter used to activate or not the deprecation warning.
        Can be one of "error", "ignore", "always", "default", "module", or "once".
        If ``None``, empty or missing, the the global filtering mechanism is used.

    -   "category":
        The warning category to use for the deprecation warning.
        By default, the category class is :class:`~DeprecationWarning`,
        you can inherit this class to define your own deprecation warning category.

    :return: a decorator used to deprecate a function.
    """
    adapter_cls = kwargs.pop('adapter_cls', SphinxAdapterParam)
    kwargs["line_length"] = line_length
    kwargs["deprecated_args"] = deprecated_args

    return _classic_deprecated_param(adapter_cls=adapter_cls, **kwargs)
