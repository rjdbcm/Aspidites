import os
import warnings
from pathlib import Path

import hypothesis
import pytest as pt
from hypothesis import given, assume, strategies as st

try:
    from numpy import inf, nan, isinf, isnan
except ImportError:
    from math import inf, nan, isinf, isnan


from .._vendor.contracts import ContractNotRespected
from ..__main__ import get_cy_kwargs, main
from ..parser import parse_module
from ..templates import woma_template
from ..monads import Maybe, Surely
from ..math import SafeFloorDiv, SafeMod, SafeDiv, SafeExp, Undefined
from ..compiler import Compiler, CompilerArgs

docker = os.getenv("ASPIDITES_DOCKER_BUILD")

woma_file = str(Path('examples/examples.wom'))


@pt.fixture(autouse=True)
def inject_config(request):
    return request.config.rootpath


def setup_code(inject_config):
    if Path(woma_file).exists():
        code_ = parse_module(open(woma_file, 'r').read())
    else:
        try:
            code_ = parse_module(open(str(Path("Aspidites/tests") / woma_file), 'r').read())
            warnings.warn("Aspidites is being tested in source mode")
        except FileNotFoundError:
            code_ = parse_module(open(Path(inject_config) / woma_file, 'r').read())
    return code_


def test_compile_module(inject_config):
    try:
        compile(woma_template.substitute(code='\n'.join(setup_code(inject_config))), '', 'exec')
    except FileNotFoundError:  # ????
        compile(woma_template.substitute(code='\n'.join(os.path.join(inject_config(), woma_file))), '',
                'exec')

def test_cli_help_exit():
    with pt.raises(SystemExit):
        main(['Aspidites', '-h'])


def test_cli_no_arg_exit():
    with pt.raises(SystemExit):
        main(['Aspidites' , ''])


def test_cli_no_target_exit():
    with pt.raises(SystemExit):
        main(['Aspidites', '-fpc'])


def test_cli_examples():
    python_file_ = Path('examples/compiled.py')
    python_file = python_file_ if Path(woma_file).exists() else (Path('Aspidites/tests') / python_file_)
    with pt.raises(SystemExit):
        main(['Aspidites', woma_file, f'-o={python_file}', '-c'])


# @pt.mark.filterwarnings('ignore::RuntimeWarning')
def test_compile_to_shared_object(inject_config):
    python_file_ = str(Path('examples/compiled.pyx'))
    full_path = Path('Aspidites/tests') / python_file_
    python_file = python_file_ if Path(woma_file).exists() else str(full_path)
    kwargs = get_cy_kwargs()
    code = setup_code(inject_config)
    kwargs.update(code=code, fname=python_file, bytecode=True, force=True, c=True, build_requires='', verbose=False)
    compile_args = CompilerArgs(**kwargs)
    try:
        Compiler(compile_args)
    except (FileNotFoundError, ValueError):
        kwargs.update(code=code, fname=Path(inject_config) / python_file_, bytecode=True)
        compile_args = CompilerArgs(**kwargs)
        Compiler(compile_args)

    from .examples.compiled import (Add, x, y, z, val, div_by_zero, Yield123, Hello, test_unary_sub, test_unary_add,
                                    test_factorial)


    with pt.raises(ContractNotRespected):
        # noinspection PyTypeChecker
        Add(x=6.5, y=12)

    assert [1, 2, 3] == [i for i in Yield123()]
    assert Maybe(Add, 6.5, 12)() == Undefined()
    assert x() == 6
    assert y() == Undefined()
    assert z == 9
    assert Add(x=3, y=2) == 5
    assert val() == Undefined()
    assert div_by_zero == Undefined()
    Hello()

#
# def teardown_function():
#     for file in glob.glob('examples/compiled.*'):
#         os.remove(file)
#     try:
#         os.remove('examples/setup.py')
#     except FileNotFoundError:
#         pass
