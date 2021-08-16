from Aspidites._vendor.contracts import ContractNotRespected
from hypothesis import given, assume, strategies as st
import pytest as pt
from Aspidites.__main__ import get_cy_kwargs
from Aspidites.parser import parse_module
from Aspidites.templates import lib, setup
from Aspidites.monads import Maybe, Undefined, Surely
from Aspidites.compiler import compile_module

with open('examples/examples.wom', 'r') as f:
    code_ = parse_module(f.read())


def test_compile_module():
    compile(lib.substitute(code='\n'.join(code_)), '', 'exec')


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


def test_compile_to_shared_object():

    compile_module(code_, 'examples/compiled.py', bytecode=True, **get_cy_kwargs())

    from examples.compiled import Add, x, y, z, scala, val, div_by_zero, Yield123, Hello, Hello2

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
