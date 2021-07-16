import os
import pprint
import sys
from warnings import warn
import traceback
from pyrsistent import PClass
from Aspidites.libraries.contracts import contract, new_contract, ContractNotRespected
from pyparsing import ParseResults
import py_compile
from Cython.Compiler import Options
from Aspidites import final
from contextlib import suppress
from Aspidites.templates import lib, setup
from Aspidites.monads import Maybe, Undefined

# TODO: REPLACE WITH ACTUAL IO


code = new_contract('code', lambda x: isinstance(x, ParseResults))


@contract()
def compile_module(code: 'code', fname: 'str' = "compiled.pyx", bytecode: 'bool' = False,
                   c: 'bool' = True, verbose: 'int' = 0, **kwargs):
    app_name = os.path.splitext(fname)[0]
    with open(fname, 'w') as f:
        print(lib.substitute(code='\n'.join(code)), file=f)

    if bytecode:
        quiet = tuple(reversed(range(3))).index(verbose if verbose < 2 else 2)
        print(quiet)
        py_compile.compile(fname, app_name + ".pyc", quiet=quiet)

    if c:
        verb = int(bool(verbose))
        os.popen(f'cython {fname} --force {"--verbose" * verb}')
        file = app_name + ".c"
        dir = os.path.dirname(file)
        module_name = app_name.replace('/', '.')
        with open('setup.py', 'w') as f:
            f.write(setup.substitute(app_name=module_name, ext_name=app_name,
                                     src_file=file, inc_dirs=[], libs=[], lib_dirs=[], **kwargs))
        with os.popen(f'{sys.executable} setup.py build build_ext --inplace') as p:
            print(p.read())
