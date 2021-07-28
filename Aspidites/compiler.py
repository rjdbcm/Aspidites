import os
import pprint
import sys
from typing import Union, Text, List
import warnings
from warnings import warn
import traceback
from hashlib import md5
import mypy
from pyrsistent import PClass, pmap
from Aspidites._vendor.contracts import contract, new_contract, ContractNotRespected
from pyparsing import ParseResults
import py_compile
from Cython.Compiler import Options
from Aspidites import final
from contextlib import suppress
from Aspidites.templates import lib, setup, pyproject
from Aspidites.monads import Maybe, Undefined

MD5 = '.md5'

code = new_contract('code', lambda x: isinstance(x, ParseResults))


def checksum(fname, write=True, check=False):
    fname_md5 = fname + '.md5'
    if write:
        with open(fname, 'rb') as data:
            curr_hash = md5()
            chunk = data.read(8192)
            while chunk:
                curr_hash.update(chunk)
                chunk = data.read(8192)
            with open(fname_md5, 'w') as digest:
                digest.write(curr_hash.hexdigest())
            return pmap({curr_hash.hexdigest(): fname}).items()[0]  # immutable
    if check:
        with open(fname_md5, 'r') as digest:
            with open(fname, 'rb') as data:
                curr_hash = md5()
                chunk = data.read(8192)
                while chunk:
                    curr_hash.update(chunk)
                    chunk = data.read(8192)
                old = digest.read()
                new = curr_hash.hexdigest()
                if new == old:
                    print('md5 digest check successful: %s' % fname)
                    return new
                else:
                    print('md5 digest failure: %s' % fname)
                    return ''


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
    file_c = app_name + ".c"
    dir = os.path.dirname(file_c)
    init_py = os.path.join(dir, '__init__.py')
    py_typed = os.path.join(dir, 'py.typed')
    all_files = pmap().evolver()
    mode = 'x' if force else 'w'
    with open(fname, mode) as f:
        print(lib.substitute(code='\n'.join(code)), file=f)
    open(py_typed, 'w').write('# THIS FILE IS GENERATED - DO NOT EDIT #')
    open(init_py, 'w').write('# THIS FILE IS GENERATED - DO NOT EDIT #')
    all_files.set(*checksum(fname))
    verb = int(bool(verbose))
    mypy_args = [
        '-m', module_name,
        '--follow-imports=skip',
        '--show-error-context',
        # '--disallow-untyped-defs',
        # '--disallow-untyped-calls',
    ]
    print('running mypy', ' '.join(mypy_args))
    type_report, error_report, return_code = mypy.api.run(mypy_args)

    print('mypy type report:', '\n', type_report) if type_report else None
    print('mypy error report:', '\n', error_report) if error_report else None
    print('mypy returned with exit code:', return_code)
    all_files.set(*checksum(fname))
    exit(return_code) if return_code != 0 else print('running compile')

    if bytecode:
        fname_pyc = app_name + ".pyc"
        quiet = tuple(reversed(range(3))).index(verbose if verbose < 2 else 2)
        py_compile.compile(fname, fname_pyc, quiet=quiet)
        all_files.set(*checksum(fname_pyc))

    if c:
        os.popen(f'cython {fname} {"--force" * force} {"--verbose" * verb}')
        setup_py = os.path.join(dir, 'setup.py')
        pyproject_toml = os.path.join(dir, 'pyproject.toml')
        with open(setup_py, mode) as f:
            f.write(setup.substitute(app_name=module_name, ext_name=app_name,
                                     src_file=file_c, inc_dirs=[], libs=[], lib_dirs=[], **kwargs))
        all_files.set(*checksum(setup_py))
        with os.popen(f'{sys.executable} {setup_py} build build_ext --inplace') as p:
            print(p.read())
        all_files.set(*checksum(file_c))
        with open(pyproject_toml, mode) as f:
            f.write(pyproject.substitute(build_requires=build_requires))
        all_files.set(*checksum(pyproject_toml))
        all_files = all_files.persistent()
        print('running checksums')
        for k, v in all_files.items():
            digest = checksum(v, write=False, check=True)
            try:
                all_files.get(digest)
            except AttributeError:                    #449779cbdc60682faf8b1327d1d315ca
                raise RuntimeError('\nfor file %s\n%s\n  did not match cached digest\n%s')
