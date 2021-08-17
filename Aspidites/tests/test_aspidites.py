import os
import warnings

from Aspidites._vendor.contracts import ContractNotRespected
from hypothesis import given, assume, strategies as st
import pytest as pt
from Aspidites.__main__ import get_cy_kwargs
from Aspidites.parser import parse_module
from Aspidites.templates import lib, setup
from Aspidites.monads import Maybe, Undefined, Surely
from Aspidites.compiler import compile_module

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
