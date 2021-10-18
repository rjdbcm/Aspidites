import hypothesis
import pytest
from hypothesis import given, assume
import hypothesis.strategies as st
import pytest as pt
from ..monads import Maybe, Surely
from ..math import SafeFloorDiv, SafeMod, SafeDiv, SafeExp, Undefined, SafeFactorial, SafeUnarySub, SafeUnaryAdd
from math import inf, nan, isinf, isnan, factorial

MAX = 100000
MIN = -MAX

@given(x=st.integers(min_value=MIN, max_value=MAX) | st.floats(allow_nan=False),
       y=st.integers(min_value=MIN, max_value=MAX) | st.floats(allow_nan=False))
@hypothesis.settings(deadline=None)
@pt.mark.filterwarnings('ignore::RuntimeWarning')
def test_safe_div(x, y):
    # TODO SafeDiv/SafeExp/SafeMod: the specific edge case x=1 y=1 is slow
    assert SafeDiv(x, 0) == Undefined()
    assert SafeFloorDiv(x, 0) == Undefined()
    assume(x != 0 and y != 0)

    if isnan(x / y) and isnan(x // y):
        assert SafeDiv(x, y) == Undefined()
        assert SafeFloorDiv(x, y) == Undefined()
    else:
        assume(not isinf(x) and not isinf(y))
        assert SafeDiv(x, y) == x / y
        assert SafeFloorDiv(x, y) == x // y


@given(x=st.integers(min_value=MIN, max_value=MAX) | st.floats(allow_nan=False),
       y=st.integers(min_value=MIN, max_value=MAX) | st.floats(allow_nan=False))
@hypothesis.settings(deadline=None)
@pt.mark.filterwarnings('ignore::RuntimeWarning')
def test_safe_exp(x, y):
    assert SafeExp(0, 0) == Undefined()
    assert SafeExp(0, inf) == Undefined()
    assert SafeExp(inf, 0) == Undefined()
    assume(x != 0 and y != 0)
    try:
        x ** y
    except OverflowError:  # really big number
        assert SafeExp(x, y) == inf
    else:
        assert SafeExp(x, y) == x ** y


@given(x=st.integers(min_value=MIN, max_value=MAX) | st.floats(allow_nan=False),
       y=st.integers(min_value=MIN, max_value=MAX) | st.floats(allow_nan=False))
@hypothesis.settings(deadline=None)
@pt.mark.filterwarnings('ignore::RuntimeWarning')
def test_safe_mod(x, y):
    assert SafeMod(x, 0) == Undefined()
    assert SafeMod(inf, x) == Undefined()
    assume(x != 0 and y != 0)
    assume(not isinf(x))
    assert SafeMod(x, y) == x % y


@given(x=st.integers(min_value=0, max_value=MAX))
@hypothesis.settings(deadline=None)
@pt.mark.filterwarnings('ignore::RuntimeWarning')
def test_safe_factorial(x):
    assert SafeFactorial(inf) == Undefined()
    assert SafeFactorial(nan) == Undefined()
    assert SafeFactorial(x) == factorial(x)
    assume(x > 0)
    assert SafeFactorial(-x) == Undefined()


@given(x=st.integers(min_value=MIN, max_value=MAX))
@hypothesis.settings(deadline=None)
@pt.mark.filterwarnings('ignore::RuntimeWarning')
def test_safe_unary(x):
    assert SafeUnarySub(x) == -x
    assert SafeUnarySub(nan) == Undefined()
    assert SafeUnaryAdd(x) == +x
    assert SafeUnaryAdd(nan) == Undefined()


def test_undefined_sanity():
    assert Undefined() == Undefined()
    assert Undefined() + Undefined() == Undefined()
    assert Undefined() - Undefined() == Undefined()
    assert Undefined() * Undefined() == Undefined()
    assert Undefined() / Undefined() == Undefined()
    assert Undefined().__hash__() == hash(Undefined())
    assert Undefined().__nonzero__() is True
    assert Undefined().__index__() == 0
    assert Undefined().__oct__() == Undefined()
    # noinspection PyTypeChecker
    with pytest.raises(TypeError):
        from math import isnan
        assert isnan(complex(Undefined())) == isnan(complex(nan))
    from numpy import isnan
    assert isnan(complex(Undefined())) == isnan(complex(nan))
    del isnan
    from math import isnan
    assert isnan(float(Undefined())) == isnan(float(nan))
    assert Surely() == Surely()
    assert Surely() + Surely() == Surely()
    assert Surely() - Surely() == Surely()
    assert Surely() * Surely() == Surely()
    assert Surely() / Surely() == Surely()


@given(x=st.integers(min_value=MIN, max_value=MAX) | st.floats() | st.complex_numbers())
def test_number_undefined_sanity(x):
    assert Undefined() + x  == Undefined()
    assert Undefined() - x  == Undefined()
    assert Undefined() * x  == Undefined()
    assert Undefined() / x  == Undefined()
    assert Undefined() // x == Undefined()
    assert Surely() + x     == Surely()
    assert Surely() - x     == Surely()
    assert Surely() * x     == Surely()
    assert Surely() / x     == Surely()
    assert Undefined(x)     != Surely(x)


@given(x=st.text() | st.characters())
def test_text_undefined_sanity(x):
    assert Undefined() + x == Undefined()
    assert Undefined() - x == Undefined()
    assert Undefined() * x == Undefined()
    assert Undefined() / x == Undefined()
    assert Undefined() // x == Undefined()
    assert Surely() + x == Surely()
    assert Surely() - x == Surely()
    assert Surely() * x == Surely()
    assert Surely() / x == Surely()
    assert Undefined(x) != Surely(x)


@given(x=st.lists(st.randoms()))
def test_list_undefined_sanity(x):
    assert Undefined() + x == Undefined()
    assert Undefined() - x == Undefined()
    assert Undefined() * x == Undefined()
    assert Undefined() / x == Undefined()
    assert Undefined() // x == Undefined()
    assert Surely() + x == Surely()
    assert Surely() - x == Surely()
    assert Surely() * x == Surely()
    assert Surely() / x == Surely()
    assert Undefined(x) != Surely(x)


@given(x=st.dictionaries(st.randoms(), st.randoms()))
def test_dict_undefined_sanity(x):
    assert Undefined() + x == Undefined()
    assert Undefined() - x == Undefined()
    assert Undefined() * x == Undefined()
    assert Undefined() / x == Undefined()
    assert Undefined() // x == Undefined()
    assert Surely() + x == Surely()
    assert Surely() - x == Surely()
    assert Surely() * x == Surely()
    assert Surely() / x == Surely()
    assert Undefined(x) != Surely(x)


@given(x=st.integers(min_value=MIN, max_value=MAX))
@hypothesis.settings(deadline=None)
def test_integer_monad_sanity(x):
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
    assert (not not Surely(x)) == bool(x)
    assert Surely(x) // 1 == x // 1
    assert Surely(x) / 1 == x / 1
    assert Surely(x) * 1 == x * 1
    assert ~Surely(x) == ~x
    assert -Surely(x) == -x
    assert Surely(x) - 1 == x - 1
    assert Surely(x) + 1 == x + 1
    assert (Surely(x) == 1) == (x == 1)
    assert hash(Surely(x)) == hash(x)
