# Aspidites is Copyright 2021, Ross J. Duff.
# See LICENSE.txt for more info.

import os
import py_compile
import sys
from glob import glob
from warnings import warn
import typing as t
from mypy import api
from Aspidites.templates import lib, makefile, pyproject, setup
from pyrsistent import pmap
from hashlib import sha256


def checksum(fname, write=True, check=False):
    base, name = os.path.split(fname)
    fname_sha256 = os.path.join(base, "." + name) + ".sha256"

    def read_sha256(data):
        curr_hash = sha256()
        chunk = data.read(8192)
        while chunk:
            curr_hash.update(chunk)
            chunk = data.read(8192)
        return curr_hash

    if write:
        with open(fname, "rb") as data:
            curr_hash = read_sha256(data)
            with open(fname_sha256, "wb") as digest:
                digest.write(curr_hash.digest())
            return pmap({curr_hash.digest(): fname}).items()[0]  # immutable
    if check:
        with open(fname_sha256, "rb") as digest:
            with open(fname, "rb") as data:
                curr_hash = read_sha256(data)
                old = digest.read()
                new = curr_hash.digest()
                if new == old:
                    print(
                        "sha256 digest check successful: %s, %s == %s"
                        % (fname, new.hex(), old.hex())
                    )
                    return new
                else:
                    print(
                        "sha256 digest failure: %s, %s != %s"
                        % (fname, new.hex(), old.hex())
                    )
                    return ""


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


_stack = CheckedFileStack()


def _finalize_stack():
    all_file_checksums = _stack.finalize()
    print("running checksums")
    for k, v in all_file_checksums.items():
        digest = checksum(v, write=False, check=True)
        try:
            all_file_checksums.get(digest)
        except AttributeError:
            raise RuntimeError("\nfor file %s\n%s\n  did not match cached digest\n%s")


class CompilerArgSpec(t.TypedDict):

    code: object
    fname: str
    force: bool
    bytecode: bool
    c: bool
    build_requires: t.Union[t.List, str]
    verbose: int


def create_file(fname, mode, stack=_stack, root='', text="# THIS FILE IS GENERATED - DO NOT EDIT #") -> None:

    if len(root) > 0:
        file = os.path.join(root, fname)
    else:
        file = fname
    try:
        open(file, mode).write(text)
    except FileExistsError:
        stack.register(file)


def compile_module(**kwargs):
    code = kwargs['code']
    fname = kwargs['fname']
    force = kwargs['force']
    bytecode = kwargs['bytecode']
    c = kwargs['c']
    build_requires = kwargs['build_requires']
    verbose = kwargs['verbose']
    app_name = os.path.splitext(fname)[0]
    project = os.path.basename(app_name)
    module_name = app_name.replace("/", ".")
    file_c = app_name + ".c"
    root = os.path.dirname(fname)
    mode = "x" if force else "w"
    create_file(fname, mode, root='', text=lib.substitute(code="\n".join(code)))
    create_file('__init__.py', mode=mode, root=root)
    create_file('py.typed', mode=mode, root=root)
    typecheck(module_name)
    create_stubs(fname, app_name)
    create_file('pyproject.toml', mode, root=root,
                text=pyproject.substitute(build_requires=build_requires))
    create_file('Makefile', mode, root=root, text=makefile.substitute(project=project))

    if bytecode:
        fname_pyc = app_name + ".pyc"
        quiet = tuple(reversed(range(3))).index(verbose if verbose < 2 else 2)
        py_compile.compile(fname, fname_pyc, quiet=quiet)
        _stack.register(fname_pyc)

    if c:
        compile_c(fname, force, verbose)
        create_setup(root, **kwargs)
        compile_object(app_name, file_c, root)

    _finalize_stack()


def typecheck(module_name):
    mypy_args = [
        "-m",
        module_name,
        "--follow-imports=skip",
        "--show-error-context",
        "--show-error-codes",
        "--allow-incomplete-defs",
        "--disable-error-code=valid-type",
        "--exclude=builtins"
        # '--disallow-untyped-defs',
        # '--disallow-untyped-calls',
    ]
    print("running mypy", " ".join(mypy_args))
    type_report = None
    error_report = None
    return_code = 0
    try:
        type_report, error_report, return_code = api.run(mypy_args)
    except AttributeError:
        warn("mypy api call failed")

    finally:
        print("mypy type report: ", type_report) if type_report else None
        print("mypy error report: ", error_report) if error_report else None
        print("mypy returned with exit code:", return_code) if return_code else None
        # exit(return_code) if return_code != 0 else print("running compile")


def create_stubs(fname, app_name):
    fname_pyi = app_name + '.pyi'
    stubgen_runner = 'stubgen %s -o .' % (fname)
    print("running %s" % stubgen_runner)
    with os.popen(stubgen_runner) as p:
        print(p.read())
    try:
        _stack.register(fname_pyi)
    except FileNotFoundError as e:
        warn(str(e))
        try:
            print("trying rename %s/__main__.pyi to %s" % (os.getcwd(), fname_pyi))
            os.rename(os.path.join(os.getcwd(), '__main__.pyi'), fname_pyi)
            _stack.register(fname_pyi)
        except FileNotFoundError:
            warn("failed to create stubs")


def compile_c(fname, force, verbose) -> None:
    verb = int(bool(verbose))
    os.popen("cython %s %s %s" % (fname, "--force" * force, "--verbose" * verb))


def create_setup(root, **kwargs) -> None:
    app_name = os.path.splitext(kwargs['fname'])[0]
    module_name = app_name.replace("/", ".")
    create_file('setup.py',
                "x" if kwargs['force'] else "w",
                root=root,
                text=setup.substitute(
                    app_name=module_name,
                    src_file=kwargs['fname'],
                    inc_dirs=[],
                    libs=[],
                    exe_name=app_name,
                    lib_dirs=[],
                    **kwargs))


def compile_object(app_name, file_c, root) -> None:
    glob_so = app_name + ".*.so"
    # TODO: get this working for docker builds
    #  (maybe executable param with os.path.relpath?)
    setup_runner = "%s %s build_ext -b ." % (sys.executable, os.path.join(root, 'setup.py'))
    print("running", setup_runner)
    with os.popen(setup_runner) as p:
        print(p.read())
    _stack.register(file_c)
    for i in glob(glob_so):
        _stack.register(i)
