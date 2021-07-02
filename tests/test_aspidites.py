from Aspidites.features.contracts import ContractNotRespected
from hypothesis import given, assume, strategies as st
import pytest as pt
from Aspidites.parser import parse_module
from Aspidites.templates import env, setup
from Aspidites.monads import Maybe, Undefined, Surely
from Aspidites.compiler import compile_to_c, compile_to_pyx


code_ = parse_module("(Add(x = 3 -> int; y = 3 -> int))"
                     "\n\t<*>x+y"
                     "\ni<@>(1,2,3)"
                     "\n\tpass"
                     "\nC = {'a': (3+5), 'b': 8, 'c': True, 4: None, 'd': 5+3*(6**2)}"
                     "\ncolors <- list[3]"
                     "\nx = Add(3, 3)\ny = Add(4, 3.5)", parseAll=True)


def test_compile_module():

    compile(env.substitute(code='\n'.join(code_)), '', 'exec')


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

    compile_to_pyx(code_, 'compiled.pyx', bytecode=True)

    compile_to_c('compiled', 'compiled.pyx')

    from build.compiled import Add, x, y

    with pt.raises(ContractNotRespected):
        Add(x=6.5, y=12)

    cs = Maybe(Add, {'x': 6.5, 'y': 12})
    assert cs() == Undefined()
    assert x() == 6
    assert y() == Undefined()
    assert Add(x=3, y=2) == 5

