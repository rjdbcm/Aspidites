import contextlib
import functools
import os
import pprint
import sys
from glob import glob
from typing import Union, Text, List
import warnings
from warnings import warn
import traceback
from hashlib import md5
from pyrsistent import PClass, pmap, PMap
from Aspidites._vendor.contracts import contract, new_contract, ContractNotRespected
from Aspidites._vendor.fn import _, F
from pyparsing import ParseResults
import py_compile
from Cython.Compiler import Options
from Aspidites import final
from contextlib import suppress
from Aspidites.templates import lib, setup, pyproject, makefile
from Aspidites.monads import Maybe, Undefined
from mypy import api

MD5 = '.md5'

code = new_contract('code', lambda x: isinstance(x, ParseResults))


@contextlib.contextmanager
def working_directory(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    Usage:
    > # Do something in original directory
    > with working_directory('/my/new/path'):
    >     # Do something in new directory
    > # Back to old directory
    """

    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def checksum(fname, write=True, check=False):
    base, name = os.path.split(fname)
    fname_md5 = os.path.join(base, '.' + name) + '.md5'

    def read_md5(data):
        curr_hash = md5()
        chunk = data.read(8192)
        while chunk:
            curr_hash.update(chunk)
            chunk = data.read(8192)
        return curr_hash

    if write:
        with open(fname, 'rb') as data:
            curr_hash = read_md5(data)
            with open(fname_md5, 'wb') as digest:
                digest.write(curr_hash.digest())
            return pmap({curr_hash.digest(): fname}).items()[0]  # immutable
    if check:
        with open(fname_md5, 'rb') as digest:
            with open(fname, 'rb') as data:
                curr_hash = read_md5(data)
                old = digest.read()
                new = curr_hash.digest()
                if new == old:
                    print('md5 digest check successful: %s, %s == %s' % (fname, new.hex(), old.hex()))
                    return new
                else:
                    print('md5 digest failure: %s, %s != %s' % (fname, new.hex(), old.hex()))
                    return ''


class CheckedFileStack:
    def __init__(self, initial=None, pre_size=8192):
        if initial is None:
            initial = {}
        self._files = pmap(initial, pre_size)
        self.all_files = self._files.evolver()

    def register(self, fname):
        self.all_files.set(*checksum(fname))

    def finalize(self):
        return self.all_files.persistent()


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
    project = os.path.basename(app_name)
    module_name = app_name.replace('/', '.')
    file_c = app_name + ".c"
    dir = os.path.dirname(file_c)
    glob_so = app_name + '.*.so'
    init_py = os.path.join(dir, '__init__.py')
    make_ = os.path.join(dir, 'Makefile')
    py_typed = os.path.join(dir, 'py.typed')
    stack = CheckedFileStack()
    mode = 'x' if force else 'w'
    open(fname, mode).write(lib.substitute(code='\n'.join(code)))
    stack.register(fname)
    open(py_typed, 'w').write('# THIS FILE IS GENERATED - DO NOT EDIT #')
    stack.register(py_typed)
    open(init_py, 'w').write('# THIS FILE IS GENERATED - DO NOT EDIT #')
    stack.register(init_py)
    open(make_, mode).write(makefile.substitute(project=project))
    stack.register(make_)
    verb = int(bool(verbose))
    mypy_args = [
        '-m', module_name,
        '--follow-imports=skip',
        '--show-error-context',
        '--show-error-codes',
        '--allow-incomplete-defs',
        '--disable-error-code=valid-type',
        # '--disallow-untyped-defs',
        # '--disallow-untyped-calls',
    ]
    print('running mypy', ' '.join(mypy_args))
    type_report = None
    error_report = None
    return_code = 0
    try:
        type_report, error_report, return_code = api.run(mypy_args)
    except AttributeError:
        warn('mypy api call failed')

    finally:
        print('mypy type report: ', type_report) if type_report else None
        print('mypy error report: ', error_report) if error_report else None
        print('mypy returned with exit code:', return_code) if return_code else None
        exit(return_code) if return_code != 0 else print('running compile')

    if bytecode:
        fname_pyc = app_name + ".pyc"
        quiet = tuple(reversed(range(3))).index(verbose if verbose < 2 else 2)
        py_compile.compile(fname, fname_pyc, quiet=quiet)
        stack.register(fname_pyc)

    if c:
        os.popen('cython %s %s %s' % (fname, "--force" * force, "--verbose" * verb))
        setup_py = os.path.join(dir, 'setup.py')
        pyproject_toml = os.path.join(dir, 'pyproject.toml')
        with open(setup_py, mode) as f:
            f.write(setup.substitute(app_name=module_name, ext_name=app_name,
                                     src_file=file_c, inc_dirs=[], libs=[], lib_dirs=[], **kwargs))
        stack.register(setup_py)
        setup_runner = '%s %s build_ext -b .' % (sys.executable, setup_py)
        print('running', setup_runner)
        with os.popen(setup_runner) as p:
            print(p.read())
        stack.register(file_c)
        for i in glob(glob_so):
            stack.register(i)
        with open(pyproject_toml, mode) as f:
            f.write(pyproject.substitute(build_requires=build_requires))
        stack.register(pyproject_toml)
    all_file_checksums = stack.finalize()
    print('running checksums')
    for k, v in all_file_checksums.items():
        digest = checksum(v, write=False, check=True)
        try:
            all_file_checksums.get(digest)
        except AttributeError:                    #449779cbdc60682faf8b1327d1d315ca
            raise RuntimeError('\nfor file %s\n%s\n  did not match cached digest\n%s')
