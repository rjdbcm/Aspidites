import operator
import sys
from datetime import timedelta as delta
import hypothesis
import pytest as pt
import hypothesis.strategies as st
from hypothesis import given, assume

from Aspidites._vendor.fn import recur


# no fuzzing just tested at 10x the recursion limit
def test_tco_decorator(limit=sys.getrecursionlimit() * 10):

    def recur_accumulate(origin, f=operator.add, acc=0):
        n = next(origin, None)
        if n is None:
            return acc
        return recur_accumulate(origin, f, f(acc, n))

    # this works normally
    assert 10 == recur_accumulate(iter(range(5)))

    # such count of recursive calls should fail on CPython,
    # for PyPy we skip this test cause on PyPy the limit is
    # approximative and checked at a lower level
    # if not hasattr(sys, 'pypy_version_info'):
    #     with pt.raises(RuntimeError):
    #         recur_accumulate(iter(range(limit)))

    # with recur decorator it should run without problems
    @recur.tco
    def tco_accumulate(origin, f=operator.add, acc=0):
        n = next(origin, None)
        if n is None:
            return False, acc
        return True, (origin, f, f(acc, n))

    assert sum(range(limit)) == tco_accumulate(iter(range(limit)))


@hypothesis.settings(deadline=delta(milliseconds=400))
@given(st.integers(min_value=2, max_value=1000))
def test_tco_different_functions(i: int):
    # noinspection PyUnusedLocal
    assume(not i % 2)  # even only

    @recur.tco
    def recur_inc2(curr, acc=0):
        if curr == 0:
            return False, acc
        return recur_dec, (curr-1, acc+2)

    @recur.tco
    def recur_dec(curr, acc=0):
        if curr == 0:
            return False, acc
        return recur_inc2, (curr-1, acc-1)

    assert i/2 == recur_inc2(i)


def test_stackless():
    @recur.stackless
    def fib(n):
        if n == 0:
            yield 1
            return
        if n == 1:
            yield 1
            return
        yield (yield fib.call(n - 1)) + (yield fib.call(n - 2))
    assert fib(9) == 55
