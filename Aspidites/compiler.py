import os
import pprint
import sys
from typing import Union, Text, List
import warnings
from warnings import warn
import traceback
import mypy
from pyrsistent import PClass
from Aspidites._vendor.contracts import contract, new_contract, ContractNotRespected
from pyparsing import ParseResults
import py_compile
from Cython.Compiler import Options
from Aspidites import final
from contextlib import suppress
from Aspidites.templates import lib, setup, pyproject
from Aspidites.monads import Maybe, Undefined

# TODO: REPLACE WITH ACTUAL IO


code = new_contract('code', lambda x: isinstance(x, ParseResults))


@contract()
def compile_module(code: 'code',
                   fname: 'str' = "compiled.py",
                   force: 'bool' = False,
                   bytecode: 'bool' = False,
                   c: 'bool' = True,
                   build_requires: 'list|str' = '',
                   verbose: 'int' = 0,
                   *args, **kwargs):
    app_name = os.path.splitext(fname)[0]
    module_name = app_name.replace('/', '.')
    file = app_name + ".c"
    dir = os.path.dirname(file)
    mode = 'x' if force else 'w'
    with open(fname, mode) as f:
        print(lib.substitute(code='\n'.join(code)), file=f)
    verb = int(bool(verbose))
    mypy_args = [
        '-m', module_name,
        '--follow-imports=skip',
        '--show-error-context',
        '--disallow-untyped-defs',
        '--disallow-untyped-calls',
    ]
    print('running mypy', ' '.join(mypy_args))
    type_report, error_report, return_code = mypy.api.run(mypy_args)

    print('mypy type report:', '\n', type_report) if type_report else None
    print('mypy error report:', '\n', error_report) if error_report else None
    print('mypy returned with exit code:', return_code)
    exit(return_code) if return_code != 0 else print('running compile')

    if bytecode:
        quiet = tuple(reversed(range(3))).index(verbose if verbose < 2 else 2)
        py_compile.compile(fname, app_name + ".pyc", quiet=quiet)

    if c:
        os.popen(f'cython {fname} {"--force" * force} {"--verbose" * verb}')
        setup_py = os.path.join(dir, 'setup.py')
        with open(setup_py, mode) as f:
            f.write(setup.substitute(app_name=module_name, ext_name=app_name,
                                     src_file=file, inc_dirs=[], libs=[], lib_dirs=[], **kwargs))
        with os.popen(f'{sys.executable} {setup_py} build build_ext --inplace') as p:
            print(p.read())
        with open(os.path.join(dir, 'pyproject.toml'), mode) as f:
            f.write(pyproject.substitute(build_requires=build_requires))
