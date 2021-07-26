import pytest as pt

from Aspidites._vendor.fn import _
from Aspidites._vendor.fn import underscore
from Aspidites._vendor.fn import reduce



def test_identity_default():
    assert 10, _(10)

def test_arithmetic():
    # operator +
    assert 7 == (_ + 2)(5)
    assert [10, 11, 12], list(map(_ + 10, [0, 1, 2]))
    # operator -
    assert 3 == (_ - 2)(5)
    assert 13 == (_ - 2 + 10)(5)
    assert [0, 1, 2], list(map(_ - 10, [10, 11, 12]))
    # operator *
    assert 10 == (_ * 2)(5)
    assert 50 == (_ * 2 + 40)(5)
    assert [0, 10, 20], list(map(_ * 10, [0, 1, 2]))
    # operator /
    assert 5 == (_ / 2)(10)
    assert 6 == (_ / 2 + 1)(10)
    assert [1, 2, 3], list(map(_ / 10, [10, 20, 30]))
    # operator **
    assert 100 == (_ ** 2)(10)
    # operator %
    assert 1 == (_ % 2)(11)
    # operator <<
    assert 32 == (_ << 2)(8)
    # operator >>
    assert 2 == (_ >> 2)(8)
    # operator (-a)
    assert 10,  (-_)(-10)
    assert -10 == (-_)(10)
    # operator (+a)
    assert 10,  (+_)(10)
    assert -10 == (+_)(-10)
    # operator (~a)
    assert -11 == (~_)(10)

def test_arithmetic_multiple():
    assert 10 == (_ + _)(5, 5)
    assert 0 == (_ - _)(5, 5)
    assert 25 == (_ * _)(5, 5)
    assert 1 == (_ / _)(5, 5)

def test_arithmetic_swap():
    # operator +
    assert 7 == (2 + _)(5)
    assert [10, 11, 12], list(map(10 + _, [0, 1, 2]))
    # operator -
    assert 3 == (8 - _)(5)
    assert 13 == (8 - _ + 10)(5)
    assert [10, 9, 8], list(map(10 - _, [0, 1, 2]))
    # operator *
    assert 10 == (2 * _)(5)
    assert 50 == (2 * _ + 40)(5)
    assert [0, 10, 20], list(map(10 * _, [0, 1, 2]))
    # operator /
    assert 5 == (10 / _)(2)
    assert 6 == (10 / _ + 1)(2)
    assert [10, 5, 2], list(map(100 / _, [10, 20, 50]))
    # operator **
    assert 100 == (10**_)(2)
    # operator %
    assert 1 == (11 % _)(2)
    # operator <<
    assert 32 == (8 << _)(2)
    # operator >>
    assert 2 == (8 >> _)(2)


def test_bitwise():
    # and
    assert bool((_ & 1)(1)) is True
    assert bool((_ & 1)(0)) is False
    assert bool((_ & 0)(1)) is False
    assert bool((_ & 0)(0)) is False
    # or
    assert bool((_ | 1)(1)) is True
    assert bool((_ | 1)(0)) is True
    assert bool((_ | 0)(1)) is True
    assert bool((_ | 0)(0)) is False
    # xor
    assert bool((_ ^ 1)(0)) is True
    assert bool((_ ^ 0)(1)) is True
    assert bool((_ ^ 1)(1)) is False
    assert bool((_ ^ 0)(0)) is False


def test_bitwise_swap():
    # and
    assert bool((1 & _)(1)) is True
    assert bool((1 & _)(0)) is False
    assert bool((0 & _)(1)) is False
    assert bool((0 & _)(0)) is False
    # or
    assert bool((1 | _)(1)) is True
    assert bool((1 | _)(0)) is True
    assert bool((0 | _)(1)) is True
    assert bool((0 | _)(0)) is False
    # xor
    assert bool((1 ^ _)(0)) is True
    assert bool((0 ^ _)(1)) is True
    assert bool((1 ^ _)(1)) is False
    assert bool((0 ^ _)(0)) is False


def test_getattr():
    class GetattrTest(object):
        def __init__(self):
            self.doc = "TestCase"

    assert "TestCase" == _.doc(GetattrTest())
    assert "TestCaseTestCase" == (_.doc * 2)(GetattrTest())
    assert "TestCaseTestCase" == (_.doc + _.doc)(GetattrTest(), GetattrTest())


def test_call_method():
    assert ["test", "case"] == (_.call("split"))("test case")
    assert "str", _.__name__(str)


def test_call_method_args():
    assert ["test", "case"] == (_.call("split", "-"))("test-case")
    assert ["test-case"] == (_.call("split", "-", 0))("test-case")


def test_call_method_kwargs():
    test_dict = {'num': 23}
    _.call("update", num=42)(test_dict)
    assert {'num': 42} == test_dict


def test_comparator():
    assert (_ < 7)(1) is True
    assert (_ < 7)(10) is False
    assert (_ > 20)(25) is True
    assert (_ > 20)(0) is False
    assert (_ <= 7)(6) is True
    assert (_ <= 7)(7) is True
    assert (_ <= 7)(8) is False
    assert (_ >= 7)(8) is True
    assert (_ >= 7)(7) is True
    assert (_ >= 7)(6) is False
    assert (_ == 10)(10) is True
    assert (_ == 10)(9) is False


# noinspection PyCallingNonCallable
def test_none():
    assert (_ == None)(None) is True  # noqa: E711

    class pushlist(list):
        def __lshift__(self, item):
            self.append(item)
            return self

    assert [None] == (_ << None)(pushlist())

# noinspection PyCallingNonCallable
def test_comparator_multiple():
    assert (_ < _)(1, 2) is True
    assert (_ < _)(2, 1) is False
    assert (_ > _)(25, 20) is True
    assert (_ > _)(20, 25) is False
    assert (_ <= _)(6, 7) is True
    assert (_ <= _)(7, 7) is True
    assert (_ <= _)(8, 7) is False
    assert (_ >= _)(8, 7) is True
    assert (_ >= _)(7, 7) is True
    assert (_ >= _)(6, 7) is False
    assert (_ == _)(10, 10) is True
    assert (_ == _)(9, 10) is False

def test_comparator_filter():
    assert [0, 1, 2] == list(filter(_ < 5, [0, 1, 2, 10, 11, 12]))

def test_slicing():
    assert 0 == (_[0])(list(range(10)))
    assert 9 == (_[-1])(list(range(10)))
    assert [3, 4, 5] == (_[3:])(list(range(6)))
    assert [0, 1, 2] == (_[:3])(list(range(10)))
    assert [1, 2, 3] == (_[1:4])(list(range(10)))
    assert [0, 2, 4] == (_[0:6:2])(list(range(10)))


def test_slicing_multiple():
    assert 0 == (_[_])(range(10), 0)
    assert 8 == (_[_ * (-1)])(range(10), 2)


def test_arity_error():
    with pt.raises(underscore.ArityError):
        _(1, 2)
        (_ + _)(1)
    with pt.raises(TypeError):
        _(1, 2)
        (_ + _)(1)


def test_more_than_2_operations():
    assert 12 == (_ * 2 + 10)(1)
    assert 6,  (_ + _ + _)(1, 2, 3)
    assert 10 == (_ + _ + _ + _)(1, 2, 3, 4)
    assert 7,  (_ + _ * _)(1, 2, 3)


def test_string_converting():
    assert "(x1) => x1", str(_)

    assert "(x1) => (x1 + 2)" == str(_ + 2)
    assert "(x1) => (x1 - 2)" == str(_ - 2)
    assert "(x1) => (x1 * 2)" == str(_ * 2)
    assert "(x1) => (x1 / 2)" == str(_ / 2)
    assert "(x1) => (x1 % 2)" == str(_ % 2)
    assert "(x1) => (x1 ** 2)" == str(_ ** 2)

    assert "(x1) => (x1 & 2)" == str(_ & 2)
    assert "(x1) => (x1 | 2)" == str(_ | 2)
    assert "(x1) => (x1 ^ 2)" == str(_ ^ 2)

    assert "(x1) => (x1 >> 2)" == str(_ >> 2)
    assert "(x1) => (x1 << 2)" == str(_ << 2)

    assert "(x1) => (x1 < 2)" == str(_ < 2)
    assert "(x1) => (x1 > 2)" == str(_ > 2)
    assert "(x1) => (x1 <= 2)" == str(_ <= 2)
    assert "(x1) => (x1 >= 2)" == str(_ >= 2)
    assert "(x1) => (x1 == 2)" == str(_ == 2)
    assert "(x1) => (x1 != 2)" == str(_ != 2)
    assert "(x1) => ((x1 * 2) + 1)" == str((_ * 2 + 1))


def test_rigthside_string_converting():
    assert "(x1) => (2 + x1)" == str(2 + _)
    assert "(x1) => (2 - x1)" == str(2 - _)
    assert "(x1) => (2 * x1)" == str(2 * _)
    assert "(x1) => (2 / x1)" == str(2 / _)
    assert "(x1) => (2 % x1)" == str(2 % _)
    assert "(x1) => (2 ** x1)" == str(2 ** _)

    assert "(x1) => (2 & x1)" == str(2 & _)
    assert "(x1) => (2 | x1)" == str(2 | _)
    assert "(x1) => (2 ^ x1)" == str(2 ^ _)

    assert "(x1) => (2 >> x1)" == str(2 >> _)
    assert "(x1) => (2 << x1)" == str(2 << _)


def test_unary_string_converting():
    assert "(x1) => (+x1)" == str(+_)
    assert "(x1) => (-x1)" == str(-_)
    assert "(x1) => (~x1)" == str(~_)


def test_multiple_string_converting():
    assert "(x1, x2) => (x1 + x2)" == str(_ + _)
    assert "(x1, x2) => (x1 * x2)" == str(_ * _)
    assert "(x1, x2) => (x1 - x2)" == str(_ - _)
    assert "(x1, x2) => (x1 / x2)" == str(_ / _)
    assert "(x1, x2) => (x1 % x2)" == str(_ % _)
    assert "(x1, x2) => (x1 ** x2)" == str(_ ** _)

    assert "(x1, x2) => (x1 & x2)" == str(_ & _)
    assert "(x1, x2) => (x1 | x2)" == str(_ | _)
    assert "(x1, x2) => (x1 ^ x2)" == str(_ ^ _)

    assert "(x1, x2) => (x1 >> x2)" == str(_ >> _)
    assert "(x1, x2) => (x1 << x2)" == str(_ << _)

    assert "(x1, x2) => (x1 > x2)" == str(_ > _)
    assert "(x1, x2) => (x1 < x2)" == str(_ < _)
    assert "(x1, x2) => (x1 >= x2)" == str(_ >= _)
    assert "(x1, x2) => (x1 <= x2)" == str(_ <= _)
    assert "(x1, x2) => (x1 == x2)" == str(_ == _)
    assert "(x1, x2) => (x1 != x2)" == str(_ != _)

    assert "(x1, x2) => (((x1 / x2) - 1) * 100)" == str((_ / _ - 1) * 100)


def test_reverse_string_converting():
    assert "(x1, x2, x3) => ((x1 + x2) + x3)" == str(_ + _ + _)
    assert "(x1, x2, x3) => (x1 + (x2 * x3))" == str(_ + _ * _)

    assert "(x1) => (1 + (2 * x1))", str((1 + 2 * _))


def test_multi_underscore_string_converting():
    assert "(x1) => (x1 + '_')", str(_ + "_")
    assert "(x1, x2) => getattr((x1 + x2), '__and_now__')" == str((_ + _).__and_now__)
    assert "(x1, x2) => x1['__name__'][x2]" == str(_['__name__'][_])


def test_repr():
    assert _ / 2 == eval(repr(_ / 2))
    assert _ + _ == eval(repr(_ + _))
    assert _ + _ * _ == eval(repr(_ + _ * _))


def test_repr_parse_str():
    assert '=> ' + _ == eval(repr('=> ' + _))
    assert reduce(lambda f, n: f.format(n), ('({0} & _)',) * 11).format('_') == repr(reduce(_ & _, (_,) * 12))
