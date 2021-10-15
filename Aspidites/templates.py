#cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=False, initializedcheck=False
# Aspidites
# Copyright (C) 2021 Ross J. Duff

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from string import Template
from . import __version__

makefile_template = Template(f"""
PYTHON := python
PYVERSION := $$(shell $$(PYTHON) -c "import sys; print(sys.version[:3])")
PYPREFIX := $$(shell $$(PYTHON) -c "import sys; print(sys.prefix)")

INCDIR := $$(shell $$(PYTHON) -c "import sysconfig; print(sysconfig.get_config_vars()['CONFINCLUDEPY'])")
PLATINCDIR := $$(shell $$(PYTHON) -c "import sysconfig; print(sysconfig.get_config_vars()['CONFINCLUDEPY'])")
LIBDIR1 := $$(shell $$(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))")
LIBDIR2 := $$(shell $$(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('LIBPL'))")
PYLIB := $$(shell $$(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('LIBRARY')[3:-2])")

CC := $$(shell $$(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('CC'))")
LINKCC := $$(shell $$(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('LINKCC'))")
LINKFORSHARED := $$(shell $$(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('LINKFORSHARED'))")
LIBS := $$(shell $$(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('LIBS'))")
SYSLIBS :=  $$(shell $$(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('SYSLIBS'))")
project = $$project

clean: clean-build clean-pyc clean-sha256 ## remove all build, test, coverage and Python artifacts

paths:
	@echo "PYTHON=$$(PYTHON)"
	@echo "PYVERSION=$$(PYVERSION)"
	@echo "PYPREFIX=$$(PYPREFIX)"
	@echo "INCDIR=$$(INCDIR)"
	@echo "PLATINCDIR=$$(PLATINCDIR)"
	@echo "LIBDIR1=$$(LIBDIR1)"
	@echo "LIBDIR2=$$(LIBDIR2)"
	@echo "PYLIB=$$(PYLIB)"
	@echo "CC=$$(CC)"
	@echo "LINKCC=$$(LINKCC)"
	@echo "LINKFORSHARED=$$(LINKFORSHARED)"
	@echo "LIBS=$$(LIBS)"
	@echo "SYSLIBS=$$(SYSLIBS)"

uninstall: distclean
	rm -fr py.typed
	rm -fr setup.py
	rm -fr pyproject.toml
	@rm -f *~ *.o *.so *.c $project
	find . -name '$$(project)*' -not -name '*.wom' -exec rm -fr {{}} +

distclean: clean-build clean-pyc clean-sha256
	rm -fr Makefile

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr *.pyx
	@rm -f *~ *.o *.so core core.* *.c
	find . -name '*.egg-info' -exec rm -fr {{}} +
	find . -name '*.egg' -exec rm -f {{}} +

clean-sha256:
	find . -name '*.sha256' -exec rm -f {{}} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {{}} +
	find . -name '*.pyo' -exec rm -f {{}} +
	find . -name '*~' -exec rm -f {{}} +
	find . -name '__pycache__' -exec rm -fr {{}} +
	

$project: $project.o
	$$(LINKCC) -o $$@ $$^ -L$$(LIBDIR1) -L$$(LIBDIR2) -l$$(PYLIB) $$(LIBS) $$(SYSLIBS) $$(LINKFORSHARED)

$project.o: $project.c
	$$(CC) -c $$^ -I$$(INCDIR) -I$$(PLATINCDIR)

""")
"""A Makefile template for woma compilation."""

warning_template = Template("""
$file:$lineno:
$func
Statement:
$atfault
Bound Variables:
$bound
Complaint Information:
$tb
""")
"""A warning template used by woma :class:`Aspidites.api.Warn`"""

setup_template = Template("""
# THIS FILE IS GENERATED - DO NOT EDIT #
from pathlib import Path
from setuptools import setup, Extension
from Cython.Build import cythonize, BuildExecutable
from Cython.Compiler import Options
import numpy

Options.annotate = $annotate
Options.annotate_coverage_xml = $annotate_coverage_xml
Options.buffer_max_dims = $buffer_max_dims
Options.cache_builtins = $cache_builtins
Options.cimport_from_pyx = $cimport_from_pyx
Options.clear_to_none = $clear_to_none
Options.closure_freelist_size = $closure_freelist_size
Options.convert_range = $convert_range
Options.docstrings = $docstrings
Options.embed_pos_in_docstring = $embed_pos_in_docstring
Options.generate_cleanup_code = $generate_cleanup_code
Options.fast_fail = $fast_fail
Options.warning_errors = $warning_errors
Options.error_on_unknown_names = $error_on_unknown_names
Options.error_on_uninitialized = $error_on_uninitialized
Options.gcc_branch_hints = $gcc_branch_hints
Options.lookup_module_cpdef = $lookup_module_cpdef
Options.embed = $embed

exts = [
Extension(
         '$app_name', 
         ['$src_file'],
         include_dirs=$inc_dirs,
         libraries=$libs, 
         extra_compile_args=['-Wall', '-O2'],
         library_dirs=$lib_dirs
    ),
]

setup(
    name='$app_name',
    ext_modules=cythonize(exts, include_path=[numpy.get_include()]))
    
if Options.embed:
    BuildExecutable.build('$src_file')

""")
"""A setup.py template for woma compilation."""

woma_template = Template("""#cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, binding=True
# THIS FILE IS GENERATED - DO NOT EDIT #

from typing import Any
from collections.abc import Generator
import cython  # type: ignore
from pyrsistent import (
    pset, 
    pmap, 
    pvector, 
    s, v, m, 
    PRecord,
    PClass
)
from Aspidites.woma import *
from Aspidites._vendor import (
    reduce,
    filterfalse,
    zip_longest,
    accumulate,
    take,
    drop,
    takelast,
    droplast,
    match,
    _,
    InstanceOf,
)
from Aspidites.monads import Maybe, Surely
from Aspidites.math import Undefined, SafeDiv, SafeExp, SafeMod, SafeFloorDiv, SafeUnaryAdd, SafeUnarySub, SafeFactorial
from Aspidites._vendor.contracts import contract, new_contract
from Aspidites._vendor.RestrictedPython import safe_builtins
safe_builtins['print'] = print
from Aspidites._vendor.RestrictedPython import compile_restricted as compile
safe_builtins['compile'] = compile
# DECLARATIONS TO ALLOW CONTRACTS TO TYPE CHECK #
procedure: None
coroutine: Generator
number: Any
globals().update(dict(__builtins__=safe_builtins))  # add all imports to globals

$code

""")
"""A template where python-converted Woma code goes."""

default_template = f"# THIS FILE IS GENERATED BY ASPIDITES v{__version__} - DO NOT EDIT #"
"""A default empty file template."""

pyproject_template = Template("""[build-system]
requires = ["setuptools", "wheel", "Cython", $build_requires]""")
"""A pyproject.toml file template."""
