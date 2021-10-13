from pygments_woma_lexer import WomaLexer
from sphinx.highlighting import lexers

"""THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE. """
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from Aspidites.parser.parser import comparisonop, identifier
from Aspidites import __version__, __mimetype__

# -- Project information -----------------------------------------------------

project = 'Woma'
copyright = '2021, Ross J. Duff'
author = 'Ross J. Duff'

# The full version, including alpha/beta/rc tags
release = __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    "sphinx_rtd_theme",
    "sphinx_copybutton",
    "sphinx_tabs.tabs"
]
copybutton_only_copy_prompt_lines = True
copybutton_prompt_text = "$ "
copybutton_selector = "div.highlight-shell pre"
sphinx_tabs_disable_tab_closing = True
autodoc_typehints = "description"

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
html_favicon = '_static/aspidites_logo_wheelie.png'
html_logo = '_static/aspidites_logo_wheelie.png'
lexers.update(woma=WomaLexer())
pygments_style = "sphinx"


def setup(app):
    app.add_js_file("js/script.js")
    app.add_css_file("css/styles.css")
    app.add_css_file("css/dark.css")
    app.add_css_file("css/light.css")
