import hypothesis, hypothesis.strategies as st
from Aspidites._vendor.contracts.inspection import can_accept_exactly_one_argument, can_accept_self_plus_one_argument
from Aspidites._vendor.fn import _
from operator import add, sub, eq, ne, gt, lt, le, ge

class C1(object):

    arg_lambda = lambda self, x: x

    def __init__(self, arg):
        self._arg = arg

    @property
    def prop_(self):
        return self._arg

    @prop_.setter
    def prop_(self, arg):
        self._arg = arg

    def arg(self, arg):
        pass

    def arg_ret(self, arg):
        return arg


class C2(object):
    arg_lambda = lambda self, x, y: x

    def __init__(self, arg, arg2):
        self._arg = arg
        self._arg2 = arg2

    def arg(self, arg, arg2):
        pass

    def arg_ret(self, arg, arg2):
        return arg


@hypothesis.given(st.floats())
def test_single_underscore_in_binops_can_accept_one_arg(x):
    assert can_accept_exactly_one_argument(add(_, x)) == (True, None)
    assert can_accept_exactly_one_argument(sub(_, x)) == (True, None)
    assert can_accept_exactly_one_argument(eq(_, x)) == (True, None)
    assert can_accept_exactly_one_argument(ne(_, x)) == (True, None)
    assert can_accept_exactly_one_argument(gt(_, x)) == (True, None)
    assert can_accept_exactly_one_argument(lt(_, x)) == (True, None)
    assert can_accept_exactly_one_argument(le(_, x)) == (True, None)
    assert can_accept_exactly_one_argument(ge(_, x)) == (True, None)
    # TODO: fixme: bool accepts one arg but isn't a callable
    # assert can_accept_exactly_one_argument(is_(_, x)) == (True, None)
    # assert can_accept_exactly_one_argument(is_not(_, x)) == (True, None)


def test_class_self_plus_one_arg():
    assert can_accept_self_plus_one_argument(C1) is True
    assert can_accept_self_plus_one_argument(C1.prop_.fset) is True
    assert can_accept_self_plus_one_argument(C1.arg_lambda) is True
    assert can_accept_self_plus_one_argument(C1.arg) is True
    assert can_accept_self_plus_one_argument(C1.arg_ret) is True
    assert can_accept_self_plus_one_argument(C2.__init__) is False
    assert can_accept_self_plus_one_argument(C2.arg) is False
    assert can_accept_self_plus_one_argument(C2.arg_ret) is False