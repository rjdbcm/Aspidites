# Aspidites is Copyright 2021, Ross J. Duff.
# See LICENSE.txt for more info.
from string import Template

makefile = Template("""clean: clean-build clean-pyc clean-sha256 ## remove all build, test, coverage and Python artifacts

project = $project

uninstall: distclean
	rm -fr py.typed
	rm -fr setup.py
	rm -fr pyproject.toml
	find . -name '$$(project)*' -not -name '*.wom' -exec rm -fr {} +

distclean: clean-build clean-pyc clean-sha256
	rm -fr Makefile

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-sha256:
	find . -name '*.sha256' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
""")

_warning = Template("""
$file:$lineno:
$func
Statement:
$atfault
Bound Variables:
$bound
Complaint Information:
$tb
""")

setup = Template("""
# THIS FILE IS GENERATED - DO NOT EDIT #
from setuptools import setup, Extension
from Cython.Build import cythonize
from Cython.Compiler import Options
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
         extra_compile_args=['-Wall'],
         library_dirs=$lib_dirs
    ),
]

setup(
    name='$app_name',
    ext_modules=cythonize(exts))
""")

lib = Template("""# cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8
# THIS FILE IS GENERATED - DO NOT EDIT #
import cython  # type: ignore
from typing import Any
from collections.abc import Generator
from pyrsistent import (
    pset, 
    pmap, 
    pvector, 
    s, v, m, 
    PRecord,
    PClass
)
from Aspidites.woma import *
from Aspidites._vendor import F, _
from Aspidites.monads import Maybe, Surely, Undefined, SafeDiv, SafeMod, SafeExp
from Aspidites._vendor.contracts import contract, new_contract
from Aspidites._vendor.RestrictedPython import safe_builtins
safe_builtins['print'] = print
# DECLARATIONS TO ALLOW CONTRACTS TO TYPE CHECK #
procedure: None
coroutine: Generator
number: Any
globals().update(dict(__builtins__=safe_builtins))  # add all imports to globals


$code

""")

pyproject = Template("""[build-system]
requires = ["setuptools", "wheel", "Cython", $build_requires]""")
