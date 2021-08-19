from Aspidites.parser import comparisonop, identifier, quoted_str
from Aspidites import __version__
from pygments.lexer import RegexLexer, bygroups, combined, include
from pygments import token
from sphinx.highlighting import lexers

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Aspidites'
copyright = '2021, Ross J. Duff'
author = 'Ross J. Duff'

# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_options = {}
html_theme_options.update(display_version=True,
                          style_external_links=True,
                          )

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_favicon = '_static/aspidites_logo_96_96.png'
html_logo = '_static/aspidites_logo_96_96.png'


class WomaLexer(RegexLexer):
    name = 'woma'

    def innerstring_rules(ttype):
        return [
            # the old style '%s' % (...) string formatting (still valid in Py3)
            (r'%(\(\w+\))?[-#0 +]*([0-9]+|[*])?(\.([0-9]+|[*]))?'
             '[hlL]?[E-GXc-giorsaux%]', token.String.Interpol),
            # the new style '{}'.format(...) string formatting
            (r'\{'
             r'((\w+)((\.\w+)|(\[[^\]]+\]))*)?'  # field name
             r'(\![sra])?'                       # conversion
             r'(\:(.?[<>=\^])?[-+ ]?#?0?(\d+)?,?(\.\d+)?[E-GXb-gnosx%]?)?'
             r'\}', token.String.Interpol),

            # backslashes, quotes and formatting signs must be parsed one at a time
            (r'[^\\\'"%{\n]+', ttype),
            (r'[\'"\\]', ttype),
            # unhandled string formatting sign
            (r'%|(\{{1,2})', ttype)
            # newlines are an error (use "nl" state)
        ]

    def fstring_rules(ttype):
        return [
            # Assuming that a '}' is the closing brace after format specifier.
            # Sadly, this means that we won't detect syntax error. But it's
            # more important to parse correct syntax correctly, than to
            # highlight invalid syntax.
            (r'\}', token.String.Interpol),
            (r'\{', token.String.Interpol, 'expr-inside-fstring'),
            # backslashes, quotes and formatting signs must be parsed one at a time
            (r'[^\\\'"{}\n]+', ttype),
            (r'[\'"\\]', ttype),
            # newlines are an error (use "nl" state)
        ]

    tokens = {
        'root': [
            (r'\*|\*\*|\+|\-|!|%|\/', token.Operator),
            (comparisonop.reString, token.Operator),
            (r'print', token.Name.Builtin),
            (r"\bmain:", token.Name.Label),
            (
            r'procedure|finite|number|np_scalar_uint|np_uint8|np_uint16|np_uint32|np_uint64|np_scalar_int|np_int8|np_int16|np_int32|np_int64',
            token.Keyword.Type),
            (identifier.reString, token.Name.Decorator),
            (r"`(?:[^`\n\r\\]|(?:``)|(?:\\(?:[^x]|x[0-9a-fA-F]+)))*`", token.Comment),
            (r'<\*>|<\^>|<@>|->|<-|\)\)', token.Keyword),
            (r'[]{}:(),;[]', token.Punctuation),
            (r'(\d(?:_?\d)*\.(?:\d(?:_?\d)*)?|(?:\d(?:_?\d)*)?\.\d(?:_?\d)*)([eE][+-]?\d(?:_?\d)*)?', token.Number.Float),
            (r'\d(?:_?\d)*[eE][+-]?\d(?:_?\d)*j?', token.Number.Float),
            (r'0[oO](?:_?[0-7])+', token.Number.Oct),
            (r'0[bB](?:_?[01])+', token.Number.Bin),
            (r'0[xX](?:_?[a-fA-F0-9])+', token.Number.Hex),
            (r'\d(?:_?\d)*', token.Number.Integer),
            ('([uUbB]?)(""")', bygroups(token.String.Affix, token.String.Double),
             combined('stringescape', 'tdqs')),
            ("([uUbB]?)(''')", bygroups(token.String.Affix, token.String.Single),
             combined('stringescape', 'tsqs')),
            ('([uUbB]?)(")', bygroups(token.String.Affix, token.String.Double),
             combined('stringescape', 'dqs')),
            ("([uUbB]?)(')", bygroups(token.String.Affix, token.String.Single),
             combined('stringescape', 'sqs')),

            (r'[^\S\n]+', token.Text),
        ],
        'strings-single': innerstring_rules(token.String.Single),
        'strings-double': innerstring_rules(token.String.Double),
        'stringescape': [
            (r'\\([\\abfnrtv"\']|\n|N\{.*?\}|u[a-fA-F0-9]{4}|'
             r'U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})', token.String.Escape)
        ],
        'tdqs': [
            (r'"""', token.String.Double, '#pop'),
            include('strings-double'),
            (r'\n', token.String.Double)
        ],
        'tsqs': [
            (r"'''", token.String.Single, '#pop'),
            include('strings-single'),
            (r'\n', token.String.Single)
        ],
        'dqs': [
            (r'"', token.String.Double, '#pop'),
            (r'\\\\|\\"|\\\n', token.String.Escape),  # included here for raw strings
            include('strings-double')
        ],
        'sqs': [
            (r"'", token.String.Single, '#pop'),
            (r"\\\\|\\'|\\\n", token.String.Escape),  # included here for raw strings
            include('strings-single')
        ],
    }


lexers['woma'] = WomaLexer(startinline=True)


def setup(app):
    app.add_js_file("js/script.js")
    app.add_css_file("css/styles.css")
    app.add_css_file("css/dark.css")
    app.add_css_file("css/light.css")
