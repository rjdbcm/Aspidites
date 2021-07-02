import os
import pprint
import sys
import aiofiles as io
from warnings import warn
import traceback
from pyrsistent import PClass
from Aspidites.features.contracts import contract, new_contract, ContractNotRespected
from pyparsing import ParseResults
import py_compile
from Aspidites import final
from contextlib import suppress
from Aspidites.templates import env, setup
from Aspidites.monads import Maybe, Undefined
# TODO: REPLACE WITH ACTUAL IO
try:
    os.mkdir('build')
except FileExistsError:
    import shutil
    shutil.rmtree('build')
finally:
    os.mkdir('build')
os.chdir('build')


code = new_contract('code', lambda x: isinstance(x, ParseResults))


@contract()
def compile_to_pyx(code: 'code', fname: 'str' = "compiled.pyx", bytecode: 'bool' = False):
    with open(fname, 'w') as f:
        print(env.substitute(code='\n'.join(code)), file=f)
    if bytecode:
        py_compile.compile(fname, os.path.splitext(fname)[0] + ".pyc")


@contract()
def compile_to_c(app_name="compiled", fname: 'str'="compiled.pyx") -> 'None':

    os.popen(f'cython {fname} --embed --annotate --force')
    file = app_name + ".c"
    with open('setup.py', 'w') as f:
        f.write(setup.substitute(app_name=app_name, ext_name=app_name,
                                 src_file=file, inc_dirs=[], libs=[], lib_dirs=[]))
    with os.popen(f'{sys.executable} setup.py build_ext --inplace') as p:
        print(p.read())
