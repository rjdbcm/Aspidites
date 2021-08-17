from Aspidites._vendor.RestrictedPython.Utilities import reorder
from Aspidites._vendor.RestrictedPython.Utilities import test
import math
import random
import string


def test_string_in_utility_builtins():
    from Aspidites._vendor.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['string'] is string


def test_math_in_utility_builtins():
    from Aspidites._vendor.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['math'] is math


def test_whrandom_in_utility_builtins():
    from Aspidites._vendor.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['whrandom'] is random


def test_random_in_utility_builtins():
    from Aspidites._vendor.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['random'] is random


def test_set_in_utility_builtins():
    from Aspidites._vendor.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['set'] is set


def test_frozenset_in_utility_builtins():
    from Aspidites._vendor.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['frozenset'] is frozenset


def test_DateTime_in_utility_builtins_if_importable():
    try:
        import DateTime  # type: ignore
    except ImportError:
        pass
    else:
        from Aspidites._vendor.RestrictedPython.Utilities import utility_builtins
        assert DateTime.__name__ in utility_builtins


def test_same_type_in_utility_builtins():
    from Aspidites._vendor.RestrictedPython.Utilities import same_type
    from Aspidites._vendor.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['same_type'] is same_type


def test_test_in_utility_builtins():
    from Aspidites._vendor.RestrictedPython.Utilities import test
    from Aspidites._vendor.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['test'] is test


def test_reorder_in_utility_builtins():
    from Aspidites._vendor.RestrictedPython.Utilities import reorder
    from Aspidites._vendor.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['reorder'] is reorder


def test_sametype_only_one_arg():
    from Aspidites._vendor.RestrictedPython.Utilities import same_type
    assert same_type(object())


def test_sametype_only_two_args_same():
    from Aspidites._vendor.RestrictedPython.Utilities import same_type
    assert same_type(object(), object())


def test_sametype_only_two_args_different():
    from Aspidites._vendor.RestrictedPython.Utilities import same_type

    class Foo(object):
        pass
    assert same_type(object(), Foo()) is False


def test_sametype_only_multiple_args_same():
    from Aspidites._vendor.RestrictedPython.Utilities import same_type
    assert same_type(object(), object(), object(), object())


def test_sametype_only_multipe_args_one_different():
    from Aspidites._vendor.RestrictedPython.Utilities import same_type

    class Foo(object):
        pass
    assert same_type(object(), object(), Foo()) is False


def test_test_single_value_true():
    from Aspidites._vendor.RestrictedPython.Utilities import test
    assert test(True) is True


def test_test_single_value_False():
    from Aspidites._vendor.RestrictedPython.Utilities import test
    assert test(False) is False


def test_test_even_values_first_true():
    from Aspidites._vendor.RestrictedPython.Utilities import test
    assert test(True, 'first', True, 'second') == 'first'


def test_test_even_values_not_first_true():
    from Aspidites._vendor.RestrictedPython.Utilities import test
    assert test(False, 'first', True, 'second') == 'second'


def test_test_odd_values_first_true():
    from Aspidites._vendor.RestrictedPython.Utilities import test
    assert test(True, 'first', True, 'second', False) == 'first'


def test_test_odd_values_not_first_true():
    from Aspidites._vendor.RestrictedPython.Utilities import test
    assert test(False, 'first', True, 'second', False) == 'second'


def test_test_odd_values_last_true():
    from Aspidites._vendor.RestrictedPython.Utilities import test
    assert test(False, 'first', False, 'second', 'third') == 'third'


def test_test_odd_values_last_false():
    from Aspidites._vendor.RestrictedPython.Utilities import test
    assert test(False, 'first', False, 'second', False) is False


def test_reorder_with__None():
    from Aspidites._vendor.RestrictedPython.Utilities import reorder
    before = ['a', 'b', 'c', 'd', 'e']
    without = ['a', 'c', 'e']
    after = reorder(before, without=without)
    assert after == [('b', 'b'), ('d', 'd')]


def test_reorder_with__not_None():
    from Aspidites._vendor.RestrictedPython.Utilities import reorder
    before = ['a', 'b', 'c', 'd', 'e']
    with_ = ['a', 'd']
    without = ['a', 'c', 'e']
    after = reorder(before, with_=with_, without=without)
    assert after == [('d', 'd')]


def test_Utilities__test_1():
    """It returns the first arg after the first argument which is True"""
    assert test(True, 1, False, 2) == 1
    assert test(False, 1, True, 2) == 2
    assert test(False, 1, False, 2, True, 3) == 3


def test_Utilities__test_2():
    """If the above is not met, and there is an extra argument
    it returns it."""
    assert test(False, 1, False, 2, 3) == 3
    assert test(False, 1, 2) == 2
    assert test(1) == 1
    assert not test(False)


def test_Utilities__test_3():
    """It returns None if there are only False args followed by something."""
    assert test(False, 1) is None
    assert test(False, 1, False, 2) is None


def test_Utilities__reorder_1():
    """It also supports 2-tuples containing key, value."""
    s = [('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')]
    _with = [('k2', 'v2'), ('k3', 'v3')]
    without = [('k2', 'v2'), ('k4', 'v4')]
    assert reorder(s, _with, without) == [('k3', 'v3')]
