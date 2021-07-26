from hypothesis import given
from hypothesis import strategies as st
from Aspidites._vendor.fn import Stream
from Aspidites._vendor.fn import iters


@given(st.lists(st.integers(), min_size=1))
def test_from_list(list_: list):
    s = Stream() << list_
    assert list_ == list(s)
    s = Stream() << iter(list_)
    assert list_ == list(s)


def test_from_generator():
    def gen():
        yield 1
        yield 2
        yield 3

    s = Stream() << gen << (4, 5)
    assert list(s) == [1, 2, 3, 4, 5]


def test_lazy_slicing():
    s = Stream() << range(10)
    assert s.cursor() == 0

    s_slice = s[:5]
    assert s.cursor() == 0
    assert len(list(s_slice)) == 5


def test_lazy_slicing_recursive():
    s = Stream() << range(10)
    sf = s[1:3][0:2]

    assert s.cursor() == 0
    assert len(list(sf)) == 2


def test_fib_infinite_stream():
    from operator import add

    f = Stream()
    fib = f << [0, 1] << map(add, f, iters.drop(1, f))

    assert [0, 1, 1, 2, 3, 5, 8, 13, 21, 34] == list(iters.take(10, fib))
    assert 6765 == fib[20]
    assert [832040, 1346269, 2178309, 3524578, 5702887] == list(fib[30:35])
    # 35 elements should be already evaluated
    assert fib.cursor() == 35


def test_origin_param():
    assert [100] == list(Stream(100))
    assert [1, 2, 3] == list(Stream(1, 2, 3))
    assert [1, 2, 3, 10, 20, 30] == list(Stream(1, 2, 3) << [10, 20, 30])


@given(st.text())
def test_origin_param_string(s):
    assert [s] == list(Stream(s))
