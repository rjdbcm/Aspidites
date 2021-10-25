import os
import sys
import warnings
from pathlib import Path
from keyword import iskeyword
from string import ascii_letters, digits, ascii_lowercase
import hypothesis
import pytest as pt
from hypothesis import given, assume, strategies as st
from Aspidites._vendor.contracts import contract

try:
    from numpy import inf, nan, isinf, isnan
except ImportError:
    from math import inf, nan, isinf, isnan


from .._vendor.contracts import ContractNotRespected
from ..__main__ import get_cy_kwargs, main
from ..parser.parser import parse_module, func_def, arith_expr
from ..templates import woma_template
from ..monads import Maybe, Surely
from ..math import SafeFloorDiv, SafeMod, SafeDiv, SafeExp, Undefined, SafeFactorial, SafeUnarySub, SafeUnaryAdd
from ..compiler import Compiler, CompilerArgs

docker = os.getenv("ASPIDITES_DOCKER_BUILD")

woma_file = str(Path('examples/examples.wom'))

valid_id = [c for c in ascii_letters + digits + '_']


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


@hypothesis.settings(suppress_health_check=[hypothesis.HealthCheck.filter_too_much], deadline=None)
@hypothesis.given(st.text([c for c in ascii_letters]),
                  st.text([c for c in ascii_lowercase]),
                  st.integers(),
                  st.integers(1, 10))
def test_parse_func_def(w, x, y, z):
    assume(str(w).isidentifier() and str(x).isidentifier())
    assume(not iskeyword(w) and not iskeyword(x))
    assume(w is not x)
    assume(y > 0)
    f = f"({w}({x} = {y} -> int)) int\n    <*>{x}"
    exec(''.join(func_def.parseString(f)))
    args = ''
    for i in range(z):
        args += f"{x + str(i)} = {y} -> int;"
    args = args[:-1]
    f2 = f"({w}({x} = {y} -> int; {args})) int\n    <*>{x}"
    print(f2)
    exec(''.join(func_def.parseString(f2)))


# TODO Stacking unary operators onto their respective positive/negative operands does not parse safely
#  line 105, in test_parse_arith
#     assert eval(stmt) == eval(''.join(arith_expr.parseString(stmt)))
# AssertionError: assert 1 == -1
#  +  where 1 = eval('--1-0//-1')
#  +  and   -1 = eval('Maybe(SafeFloorDiv, --1-0, -1)()')
#  +    where 'Maybe(SafeFloorDiv, --1-0, -1)()' = <built-in method join of str object at 0x1033f0030>((['Maybe(SafeFloorDiv, --1-0, -1)()'], {}))
#  +      where <built-in method join of str object at 0x1033f0030> = ''.join
#  +      and   (['Maybe(SafeFloorDiv, --1-0, -1)()'], {}) = <bound method ParserElement.parseString of Combine:(Forward: bitwise operator term)>('--1-0//-1')
#  +        where <bound method ParserElement.parseString of Combine:(Forward: bitwise operator term)> = arith_expr.parseString
#
# Falsifying example: test_parse_arith(
#     p=1, q=0, binop='-', unop='-',
# )

# TODO Stacking division and floor division does not parse safely
#  line 120, in test_parse_arith
#     assert eval(stmt) == eval(''.join(arith_expr.parseString(stmt)))
# AssertionError: assert -1.0 == Undefined(None, (), {})
#  +  where -1.0 = eval('-1/1//1')
#  +  and   Undefined(None, (), {}) = eval('Maybe(SafeDiv, Maybe(SafeFloorDiv, -1, 1, 1)())()')
#  +    where 'Maybe(SafeDiv, Maybe(SafeFloorDiv, -1, 1, 1)())()' = <built-in method join of str object at 0x10ac04030>((['Maybe(SafeDiv, Maybe(SafeFloorDiv, -1, 1, 1)())()'], {}))
#  +      where <built-in method join of str object at 0x10ac04030> = ''.join
#  +      and   (['Maybe(SafeDiv, Maybe(SafeFloorDiv, -1, 1, 1)())()'], {}) = <bound method ParserElement.parseString of Combine:(Forward: bitwise operator term)>('-1/1//1')
#  +        where <bound method ParserElement.parseString of Combine:(Forward: bitwise operator term)> = arith_expr.parseString
@hypothesis.settings(deadline=None)
@hypothesis.given(st.integers(min_value=1, max_value=255),  # exponent
                  st.integers(min_value=1),
                  st.text(['/', '*', '%', '+', '-'], min_size=1, max_size=1),
                  st.text(['+', '-'], min_size=1, max_size=1))
def test_parse_arith(p, q, binop, unop):
    stmt = str(p) + binop + str(q)
    assert eval(stmt) == eval(''.join(arith_expr.parseString(stmt)))


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

    from .examples.compiled import (Add, x, y, z, val, div_by_zero, Yield123, test_unary_sub, test_unary_add,
                                    test_factorial, Match, nullity)

    assert Match() == 1
    assert Match(0) == 1
    assert Match(1) == 3
    assert Match(4) == 7

    with pt.raises(ContractNotRespected):
        # noinspection PyTypeChecker
        Add(x=6.5, y=12)

    assert [1, 2, 3] == [i for i in Yield123()]
    assert Maybe(Add, 6.5, 12)() == Undefined()
    assert x() == 6
    assert y() == Undefined()
    assert nullity == Undefined()
    assert z == 9
    assert Add(x=3, y=2) == 5
    assert val() == Undefined()
    assert div_by_zero == Undefined()

#
# def teardown_function():
#     for file in glob.glob('examples/compiled.*'):
#         os.remove(file)
#     try:
#         os.remove('examples/setup.py')
#     except FileNotFoundError:
#         pass
