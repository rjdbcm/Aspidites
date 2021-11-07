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
Options.annotate=$annotate
Options.annotate_coverage_xml=$annotate_coverage_xml
Options.buffer_max_dims=$buffer_max_dims
Options.cache_builtins=$cache_builtins
Options.cimport_from_pyx=$cimport_from_pyx
Options.clear_to_none=$clear_to_none
Options.closure_freelist_size=$closure_freelist_size
Options.convert_range=$convert_range
Options.docstrings=$docstrings
Options.embed_pos_in_docstring=$embed_pos_in_docstring
Options.generate_cleanup_code=$generate_cleanup_code
Options.fast_fail=$fast_fail
Options.warning_errors=$warning_errors
Options.error_on_unknown_names=$error_on_unknown_names
Options.error_on_uninitialized=$error_on_uninitialized
Options.gcc_branch_hints=$gcc_branch_hints
Options.lookup_module_cpdef=$lookup_module_cpdef
Options.embed=$embed
exts=[Extension('$app_name',['$src_file'],include_dirs=$inc_dirs,libraries=$libs,extra_compile_args=['-Wall','-O2'],library_dirs=$lib_dirs),]
setup(name='$app_name',ext_modules=cythonize(exts,include_path=[numpy.get_include()]))
if Options.embed: BuildExecutable.build('$src_file')

""")
"""A setup.py template for woma compilation."""

woma_template = Template("""#cython: language_level=3, annotation_typing=False, c_string_encoding=utf-8, binding=True
# THIS FILE IS GENERATED - DO NOT EDIT #
from typing import Any
from collections.abc import Generator
import cython  # type: ignore
from cython import declare as decl,address as addr,sizeof,typeof,struct,cfunc,ccall,nogil,no_gc,inline,union,typedef,cast,char,short,int as cint,bint,short,double,long,longdouble,longdoublecomplex,longlong,complex,float as cfloat
from Aspidites._vendor.pyrsistent import pset as __pset,pmap as __pmap,pvector as __pvector,s,v,m
from Aspidites.woma import *
from Aspidites._vendor import take,drop,takelast,droplast,consume,nth,first_true,iterate,padnone,ncycles,repeatfunc,grouper,group_by,roundrobin,partition,splitat,splitby,powerset,pairwise,iter_suppress,flatten,accumulate,reduce,filterfalse,zip_longest,call,apply,flip,curry,curried,zipwith,foldl,foldr,unfold,Capture,Strict,OneOf,AllOf,NoneOf,Not,Each,EachItem,Some,Between,Length,Contains,Regex,Check,InstanceOf,SubclassOf,Arguments,Returns,Transformed,At,Object,match as __match,_
from Aspidites.monads import Maybe as __maybe,Surely as __surely
from Aspidites.math import Undefined as __undefined,SafeDiv as __safeDiv,SafeExp as __safeExp,SafeMod as __safeMod,SafeFloorDiv as __safeFloorDiv,SafeUnaryAdd as __safeUnaryAdd,SafeUnarySub as __safeUnarySub,SafeFactorial as __safeFactorial
from Aspidites._vendor.contracts import contract as __contract,new_contract as __new_contract
from Aspidites._vendor.RestrictedPython import safe_builtins as __safe_builtins
from Aspidites._vendor.RestrictedPython import compile_restricted as compile
__safe_builtins['compile'] = compile
__safe_builtins['print'] = print
__safe_builtins['take']=take
__safe_builtins['drop']=drop
__safe_builtins['takelast']=takelast
__safe_builtins['droplast']=droplast
__safe_builtins['consume']=consume
__safe_builtins['nth']=nth
__safe_builtins['first_true']=first_true
__safe_builtins['iterate']=iterate
__safe_builtins['padnone']=padnone
__safe_builtins['ncycles']=ncycles
__safe_builtins['repeatfunc']=repeatfunc
__safe_builtins['grouper']=grouper
__safe_builtins['group_by']=group_by
__safe_builtins['roundrobin']=roundrobin
__safe_builtins['partition']=partition
__safe_builtins['splitat']=splitat
__safe_builtins['splitby']=splitby
__safe_builtins['powerset']=powerset
__safe_builtins['pairwise']=pairwise
__safe_builtins['iter_suppress']=iter_suppress
__safe_builtins['flatten']=flatten
__safe_builtins['accumulate']=accumulate
__safe_builtins['reduce']=reduce
__safe_builtins['filterfalse']=filterfalse
__safe_builtins['zip_longest']=zip_longest
__safe_builtins['call']=call
__safe_builtins['apply']=apply
__safe_builtins['flip']=flip
__safe_builtins['curry']=curry
__safe_builtins['curried']=curried
__safe_builtins['zipwith']=zipwith
__safe_builtins['foldl']=foldl
__safe_builtins['foldr']=foldr
__safe_builtins['unfold']=unfold
__safe_builtins['Capture']=Capture
__safe_builtins['Strict']=Strict
__safe_builtins['OneOf']=OneOf
__safe_builtins['AllOf']=AllOf
__safe_builtins['NoneOf']=NoneOf
__safe_builtins['Not']=Not
__safe_builtins['Each']=Each
__safe_builtins['EachItem']=EachItem
__safe_builtins['Some']=Some
__safe_builtins['Between']=Between
__safe_builtins['Length']=Length
__safe_builtins['Contains']=Contains
__safe_builtins['Regex']=Regex
__safe_builtins['Check']=Check
__safe_builtins['InstanceOf']=InstanceOf
__safe_builtins['SubclassOf']=SubclassOf
__safe_builtins['Arguments']=Arguments
__safe_builtins['Returns']=Returns
__safe_builtins['Transformed']=Transformed
__safe_builtins['At']=At
__safe_builtins['Object']=Object
__safe_builtins['_']=_
globals().update(dict(__builtins__=__pmap(__safe_builtins)))  # add all imports to globals
procedure: None
coroutine: Generator
number: Any

$code

""")
"""A template where python-converted Woma code goes."""

default_template = f"# THIS FILE IS GENERATED BY ASPIDITES v{__version__} - DO NOT EDIT #"
"""A default empty file template."""

pyproject_template = Template("""[build-system]
requires = ["setuptools", "wheel", "Cython", $build_requires]""")
"""A pyproject.toml file template."""
