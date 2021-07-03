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


setup(
    name='$app_name',
    ext_modules=[Extension('$ext_name', ['$src_file'], include_dirs=$inc_dirs,
                           libraries=$libs, library_dirs=$lib_dirs)])
""")

env = Template("""# cython language_level=3
# THIS FILE IS GENERATED - DO NOT EDIT #
import cython
from Aspidites.features import *
from Aspidites.monads import Maybe, Surely, Undefined
from Aspidites.features.contracts import contract, new_contract
from pyrsistent import pset
from pyrsistent import pmap
from pyrsistent import pvector
from pyrsistent import PRecord
from pyrsistent import PClass

from Aspidites.features.RestrictedPython import safe_globals
safe_globals.update(globals()) # add all imports to globals
globals().update(safe_globals)

$code

""")
