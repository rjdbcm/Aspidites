import operator
import pytest
from hypothesis import given, strategies as st
from Aspidites._vendor.fn import F, _
from Aspidites._vendor.fn import iters


def test_take():
    assert [0, 1] == list(iters.take(2, range(10)))
    assert [0, 1] == list(iters.take(10, range(2)))


def test_drop():
    assert [3, 4] == list(iters.drop(3, range(5)))
    assert [] == list(iters.drop(10, range(2)))


def test_takelast():
    assert [8, 9] == list(iters.takelast(2, range(10)))
    assert [0, 1] == list(iters.takelast(10, range(2)))


def test_droplast():
    assert [0, 1] == list(iters.droplast(3, range(5)))
    assert [] == list(iters.droplast(10, range(2)))


def test_consume():
    # full consuming, without limitation
    r = range(10)
    assert 10 == len(list(r))
    itr = iter(r)
    iters.consume(itr)
    assert 0 == len(list(itr))


def test_consume_limited():
    r = range(10)
    assert 10 == len(list(r))
    itr = iter(r)
    iters.consume(itr, 5)
    assert 5 == len(list(itr))


def test_nth():
    assert 1 == iters.nth(range(5), 1)
    assert None == iters.nth(range(5), 10)
    assert "X" == iters.nth(range(5), 10, "X")


def test_head():
    assert 0 == iters.head([0, 1, 2])
    assert None == iters.head([])

    def gen():
        yield 1
        yield 2
        yield 3

    assert 1, iters.head(gen())


def test_tail():
    assert [1, 2] == list(iters.tail([0, 1, 2]))
    assert [] == list(iters.tail([]))

    def gen():
        yield 1
        yield 2
        yield 3

    assert [2, 3] == list(iters.tail(gen()))


def test_padnone():
    it = iters.padnone([10, 11])
    assert 10 == next(it)
    assert 11 == next(it)
    assert None == next(it)
    assert None == next(it)


def test_ncycles():
    it = iters.ncycles([10, 11], 2)
    assert 10 == next(it)
    assert 11 == next(it)
    assert 10 == next(it)
    assert 11 == next(it)
    with pytest.raises(StopIteration):
        next(it)

@given(st.integers())
def test_repeatfunc(x):
    def f():
        return "test"

    # unlimited count
    it = iters.repeatfunc(f)
    assert "test" == next(it)
    assert "test" == next(it)
    assert "test" == next(it)

    # limited
    it = iters.repeatfunc(f, 2)
    assert "test" == next(it)
    assert "test" == next(it)
    with pytest.raises(StopIteration):
        next(it)


def test_grouper():
    # without fill value (default should be None)
    a, b, c = iters.grouper(3, "ABCDEFG")
    assert ["A", "B", "C"] == list(a)
    assert ["D", "E", "F"] == list(b)
    assert ["G", None, None] == list(c)

    # with fill value
    a, b, c = iters.grouper(3, "ABCDEFG", "x")
    assert ["A", "B", "C"] == list(a)
    assert ["D", "E", "F"] == list(b)
    assert ["G", "x", "x"] == list(c)


def test_roundrobin():
    r = iters.roundrobin('ABC', 'D', 'EF')
    assert ["A", "D", "E", "B", "F", "C"] == list(r)


def test_partition():
    def is_odd(x):
        return x % 2 == 1

    before, after = iters.partition(is_odd, range(5))
    assert [0, 2, 4] == list(before)
    assert [1, 3] == list(after)


def test_splitat():
    before, after = iters.splitat(2, range(5))
    assert [0, 1] == list(before)
    assert [2, 3, 4] == list(after)


def test_splitby():
    def is_even(x):
        return x % 2 == 0

    before, after = iters.splitby(is_even, range(5))
    assert [0] == list(before)
    assert [1, 2, 3, 4] == list(after)


def test_powerset():
    ps = iters.powerset([1, 2])
    assert [tuple(), (1,), (2,), (1, 2)] == list(ps)


def test_pairwise():
    ps = iters.pairwise([1, 2, 3, 4])
    assert [(1, 2), (2, 3), (3, 4)] == list(ps)


def test_iter_except():
    d = ["a", "b", "c"]
    it = iters.iter_suppress(d.pop, IndexError)
    assert ["c", "b", "a"] == list(it)


def test_flatten():
    # flatten nested lists
    assert [1, 2, 3, 4] == list(iters.flatten([[1, 2], [3, 4]]))
    assert [1, 2, 3, 4, 5, 6] == list(iters.flatten([[1, 2], [3, [4, 5, 6]]]))
    # flatten nested tuples, sets, and frozen sets
    assert [1, 2, 3, 4, 5, 6] == list(iters.flatten(((1, 2), (3, (4, 5, 6)))))
    assert [1, 2, 3] == list(iters.flatten(set([1, frozenset([2, 3])])))
    # flatten nested generators
    generators = ((num + 1 for num in range(0, n)) for n in range(1, 4))
    assert [1, 1, 2, 1, 2, 3] == list(iters.flatten(generators))
    # flat list should return it
    assert [1, 2, 3] == list(iters.flatten([1, 2, 3]))
    # Don't flatten strings, bytes, or bytearrays
    assert [2, "abc", 1] == list(iters.flatten([2, "abc", 1]))
    assert [2, b'abc', 1] == list(iters.flatten([2, b'abc', 1]))
    assert [2, bytearray(b'abc'), 1] == list(iters.flatten([2, bytearray(b'abc'), 1]))


def test_accumulate():
    assert [1, 3, 6, 10, 15] == list(iters.accumulate([1, 2, 3, 4, 5]))
    assert [1, 2, 6, 24, 120] == list(iters.accumulate([1, 2, 3, 4, 5], operator.mul))


def test_filterfalse():
    l = iters.filterfalse(lambda x: x > 10, [1, 2, 3, 11, 12])
    assert [1, 2, 3] == list(l)


def test_iterate():
    f = F() << _ * 2
    it = iters.iterate(f, 2)
    assert 2 == next(it)
    assert 4 == next(it)
    assert 8 == next(it)
    assert 16 == next(it)
