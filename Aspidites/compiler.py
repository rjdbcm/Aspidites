# Aspidites is Copyright 2021, Ross J. Duff.
# See LICENSE.txt for more info.

import os
import py_compile
import sys
from glob import glob
from warnings import warn

from mypy import api

from Aspidites._vendor.contracts import contract
from Aspidites.api import CheckedFileStack, checksum
from Aspidites.templates import lib, makefile, pyproject, setup



@contract()
def compile_module(
    code: "code",
    fname: "str" = "compiled.py",
    force: "bool" = False,
    bytecode: "bool" = False,
    c: "bool" = True,
    build_requires: "list|str" = "",
    verbose: "int" = 0,
    *args,
    **kwargs
):
    app_name = os.path.splitext(fname)[0]
    project = os.path.basename(app_name)
    module_name = app_name.replace("/", ".")
    file_c = app_name + ".c"
    glob_so = app_name + ".*.so"

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

    stack = CheckedFileStack()
    root = os.path.dirname(fname)
    mode = "x" if force else "w"

    open(fname, mode).write(lib.substitute(code="\n".join(code)))
    stack.register(fname)

    py_typed = os.path.join(root, "py.typed")
    open(py_typed, mode).write("# THIS FILE IS GENERATED - DO NOT EDIT #")
    stack.register(py_typed)

    init_py = os.path.join(root, "__init__.py")
    open(init_py, mode).write("# THIS FILE IS GENERATED - DO NOT EDIT #")
    stack.register(init_py)

    make_ = os.path.join(root, "Makefile")
    open(make_, mode).write(makefile.substitute(project=project))
    stack.register(make_)

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

    fname_pyi = app_name + '.pyi'
    stubgen_runner = 'stubgen %s -o .' % (fname)
    print("running %s" % stubgen_runner)
    with os.popen(stubgen_runner) as p:
        print(p.read())
    try:
        stack.register(fname_pyi)
    except FileNotFoundError as e:
        warn(str(e))
        try:
            print("trying rename %s/__main__.pyi to %s" % (os.getcwd(), fname_pyi))
            os.rename(os.path.join(os.getcwd(), '__main__.pyi'), fname_pyi)
            stack.register(fname_pyi)
        except FileNotFoundError:
            warn("failed to create stubs")

    if bytecode:
        fname_pyc = app_name + ".pyc"
        quiet = tuple(reversed(range(3))).index(verbose if verbose < 2 else 2)
        py_compile.compile(fname, fname_pyc, quiet=quiet)
        stack.register(fname_pyc)

    if c:
        verb = int(bool(verbose))
        os.popen("cython %s %s %s" % (fname, "--force" * force, "--verbose" * verb))
        setup_py = os.path.join(root, "setup.py")
        pyproject_toml = os.path.join(root, "pyproject.toml")
        with open(setup_py, mode) as f:
            f.write(
                setup.substitute(
                    app_name=module_name,
                    src_file=fname,
                    inc_dirs=[],
                    libs=[],
                    exe_name=app_name,
                    lib_dirs=[],
                    **kwargs
                )
            )
        stack.register(setup_py)
        # TODO: get this working for docker builds
        #  (maybe executable param with os.path.relpath?)
        setup_runner = "%s %s build_ext -b ." % (sys.executable, setup_py)
        print("running", setup_runner)
        with os.popen(setup_runner) as p:
            print(p.read())
        stack.register(file_c)
        for i in glob(glob_so):
            stack.register(i)
        with open(pyproject_toml, mode) as f:
            f.write(pyproject.substitute(build_requires=build_requires))
        stack.register(pyproject_toml)
    all_file_checksums = stack.finalize()
    print("running checksums")
    for k, v in all_file_checksums.items():
        digest = checksum(v, write=False, check=True)
        try:
            all_file_checksums.get(digest)
        except AttributeError:  # 449779cbdc60682faf8b1327d1d315ca
            raise RuntimeError("\nfor file %s\n%s\n  did not match cached digest\n%s")
