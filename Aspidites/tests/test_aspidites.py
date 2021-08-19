import os
import sys
import warnings

from Aspidites._vendor.contracts import ContractNotRespected
from hypothesis import given, assume, strategies as st
import pytest as pt
from Aspidites.__main__ import get_cy_kwargs, parse_from_dummy
import argparse as ap
from Aspidites.parser import parse_module
from Aspidites.templates import lib, setup
from Aspidites.monads import Maybe, Undefined, Surely, SafeMod, SafeDiv, SafeExp
from Aspidites.compiler import compile_module
try:
    from numpy import inf, nan, isinf, isnan
except ImportError:
    from math import inf, nan, isinf, isnan

docker = os.getenv("ASPIDITES_DOCKER_BUILD")

wfile = 'examples/examples.wom'


@pt.fixture(autouse=True)
def inject_config(request):
    return request.config.rootpath


def setup_code(inject_config):
    if os.path.exists(wfile):
        code_ = parse_module(open(wfile, 'r').read())
    else:
        try:
            code_ = parse_module(open("Aspidites/tests/" + wfile, 'r').read())
            warnings.warn("Aspidites is being tested in source mode")
        except FileNotFoundError:
            code_ = parse_module(open(os.path.join(inject_config, wfile), 'r').read())
    return code_


def test_compile_module(inject_config):
    try:
        compile(lib.substitute(code='\n'.join(setup_code(inject_config))), '', 'exec')
    except FileNotFoundError:
        compile(lib.substitute(code='\n'.join(os.path.join(inject_config(), wfile))), '',
                'exec')


@given(x=st.integers(min_value=-10000,
                     max_value=10000) | st.floats(allow_nan=False),
       y=st.integers(min_value=-10000,
                     max_value=10000) | st.floats(allow_nan=False))
@pt.mark.filterwarnings('ignore::RuntimeWarning')
def test_safe_math_(x, y):
    assert SafeExp(0, 0) == Undefined()
    assert SafeExp(0, inf) == Undefined()
    assert SafeExp(inf, 0) == Undefined()
    assert SafeMod(x, 0) == Undefined()
    assert SafeDiv(x, 0) == Undefined()
    assert SafeMod(inf, x) == Undefined()
    assume(
        x != 0
        and
        y != 0
    )
    try:
        x ** y
    except OverflowError:  # really big number
        assert SafeExp(x, y) == inf
    else:
        assert SafeExp(x, y) == x ** y

    if isnan(x / y):
        assert SafeDiv(x, y) == Undefined()
    else:
        assert SafeDiv(x, y) == x / y
    assume(
        not isinf(x)
    )
    assert SafeMod(x, y) == x % y
    

@given(x=st.integers())
def test_integer_monad(x):
    assert Undefined() == Undefined()
    assert Undefined() + Undefined() == Undefined()
    assert Undefined() + x == x
    assert Undefined() - Undefined() == Undefined()
    assert Undefined() - x == -x
    assert Undefined() * x == Undefined()
    assert Undefined() * Undefined() == Undefined()
    assert Undefined() / x == Undefined()
    assert Undefined() / Undefined() == Undefined()
    assert Undefined() // x == Undefined()
    assert Undefined().__hash__() == Undefined()
    assert Undefined().__nonzero__() is False
    assert Undefined().__index__() == 0
    assert oct(Undefined()) == oct(0)
    assert complex(Undefined()) == complex()
    assert float(Undefined()) == float()
    assert Surely() == Surely()
    assert Surely() + Surely() == Surely()
    assert Surely() + x == x
    assert Surely() - Surely() == Surely()
    assert Surely() - x == -x
    assert Surely() * x == Surely()
    assert Surely() * Surely() == Surely()
    assert Surely() / x == Surely()
    assert Surely() / Surely() == Surely()
    assert Undefined(x) != Surely(x)
    assert Maybe(x) != x
    assert Surely(x) == Surely(x)
    assert Maybe(x) != Surely(x)
    assert Surely(Maybe(x)) != x
    assert Surely(Undefined()) == Undefined()
    assert Surely(x) == x
    assert -Surely(x) == -x
    assert ~Surely(x) == ~x
    assert ~Maybe(x) != ~x
    assert -Maybe(x) != -x
    assert ~Surely() == Undefined()
    assert oct(Surely(x)) == oct(x)
    assert bool(Surely(x)) == bool(x)
    assert Surely(x) // 1 == x // 1
    assert Surely(x) / 1 == x / 1
    assert Surely(x) * 1 == x * 1
    assert ~Surely(x) == ~x
    assert -Surely(x) == -x
    assert Surely(x) - 1 == x - 1
    assert Surely(x) + 1 == x + 1
    assert (Surely(x) == 1) == (x == 1)
    assert hash(Surely(x)) == hash(x)


@pt.mark.xfail(reason='This test will sometimes fail to raise SystemExit')
def test_cli_dummy_parser():
    with pt.raises(SystemExit):
        parse_from_dummy(['aspidites', '-h'],
                         ap.ArgumentParser(prog='aspidites', add_help=False),
                         __test=True)
    with pt.raises(SystemExit):
        parse_from_dummy(['aspidites'],
                         ap.ArgumentParser(prog='aspidites', add_help=False),
                         __test=True)


def test_compile_to_shared_object(inject_config):
    pfile_ = 'examples/compiled.py'
    pfile = pfile_ if os.path.exists(wfile) else 'Aspidites/tests/' + pfile_
    try:
        compile_module(setup_code(inject_config), pfile, bytecode=True, **get_cy_kwargs())
    except FileNotFoundError:
        compile_module(setup_code(inject_config), os.path.join(inject_config, pfile_),
                       bytecode=True, **get_cy_kwargs())

    from Aspidites.tests.examples.compiled import Add, x, y, z, scala, val, div_by_zero, \
        Yield123, Hello, Hello2

    with pt.raises(ContractNotRespected):
        Add(x=6.5, y=12)

    assert [1, 2, 3] == [i for i in Yield123()]
    assert Maybe(Add, 6.5, 12)() == Undefined()
    assert x() == 6
    assert y() == Undefined()
    assert z == 9
    assert Add(x=3, y=2) == 5
    assert val() == Undefined()
    assert div_by_zero() == Undefined()
    Hello()

#
# def teardown_function():
#     for file in glob.glob('examples/compiled.*'):
#         os.remove(file)
#     try:
#         os.remove('examples/setup.py')
#     except FileNotFoundError:
#         pass
