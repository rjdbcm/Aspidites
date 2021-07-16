from string import Template

_warning = Template("""
File:      $file - $lineno
Function:  $func
Statement: $atfault
-------------------------------------------------------------------------------------------
$tb
""")

setup = Template("""# THIS FILE IS GENERATED - DO NOT EDIT #
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

setup(
    name='$app_name',
    ext_modules=[Extension('$ext_name', ['$src_file'], include_dirs=$inc_dirs,
                           libraries=$libs, library_dirs=$lib_dirs)],)
""")

lib = Template("""# cython language_level=3
# THIS FILE IS GENERATED - DO NOT EDIT #
import cython
from pyrsistent import (
                        pset, 
                        pmap, 
                        pvector, 
                        s, v, m, 
                        PRecord,
                        PClass
                        )
from Aspidites.features import *
from Aspidites.monads import Maybe, Surely, Undefined
from Aspidites.libraries.contracts import contract, new_contract
from Aspidites.libraries.RestrictedPython import safe_globals
safe_globals.update(globals()) # add all imports to globals
globals().update(safe_globals)
$code
""")
