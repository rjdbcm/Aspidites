import operator
from hypothesis import strategies as st
from hypothesis import given
from Aspidites._vendor.fn import F, _, curried


def test_curried():
    @curried
    def sum5(a, b, c, d, e):
        return a + b + c + d + e
    assert sum5(1)(2)(3)(4)(5) == sum5(1, 2, 3)(4, 5)


@given(st.integers())
def test_composition(x):
    def f(x_):
        return x_ * 2

    def g(x_):
        return x_ + 10

    assert (x + 10) * 2 == (F(f) << g)(x)

    def z(x_):
        return x_ * 20
    assert ((x * 20) + 10) * 2 == (F(f) << F(g) << F(z))(x)


@given(st.integers(), st.integers(), st.integers())
def test_partial(x, y, z):
    # Partial should work if we pass additional arguments to F constructor
    f = F(operator.add, y) << F(operator.add, z)
    assert x + y + z == f(x)


def test_underscore():
    assert [1, 4, 9] == list(map(F() << (_ ** 2) << _ + 1, range(3)))


@given(st.integers())
def test_pipe_composition(x):
    def f(x_):
        return x_ * 2

    def g(x_):
        return x_ + 10

    assert (x * 2) + 10 == (F() >> f >> g)(x)


def test_pipe_partial():
    func = F() >> (filter, _ < 6) >> sum
    assert 15 == func(range(10))
