import math
import random
import string


def test_string_in_utility_builtins():
    from Aspidites.features.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['string'] is string


def test_math_in_utility_builtins():
    from Aspidites.features.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['math'] is math


def test_whrandom_in_utility_builtins():
    from Aspidites.features.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['whrandom'] is random


def test_random_in_utility_builtins():
    from Aspidites.features.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['random'] is random


def test_set_in_utility_builtins():
    from Aspidites.features.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['set'] is set


def test_frozenset_in_utility_builtins():
    from Aspidites.features.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['frozenset'] is frozenset


def test_DateTime_in_utility_builtins_if_importable():
    try:
        import DateTime
    except ImportError:
        pass
    else:
        from Aspidites.features.RestrictedPython.Utilities import utility_builtins
        assert DateTime.__name__ in utility_builtins


def test_same_type_in_utility_builtins():
    from Aspidites.features.RestrictedPython.Utilities import same_type
    from Aspidites.features.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['same_type'] is same_type


def test_test_in_utility_builtins():
    from Aspidites.features.RestrictedPython.Utilities import test
    from Aspidites.features.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['test'] is test


def test_reorder_in_utility_builtins():
    from Aspidites.features.RestrictedPython.Utilities import reorder
    from Aspidites.features.RestrictedPython.Utilities import utility_builtins
    assert utility_builtins['reorder'] is reorder


def test_sametype_only_one_arg():
    from Aspidites.features.RestrictedPython.Utilities import same_type
    assert same_type(object())


def test_sametype_only_two_args_same():
    from Aspidites.features.RestrictedPython.Utilities import same_type
    assert same_type(object(), object())


def test_sametype_only_two_args_different():
    from Aspidites.features.RestrictedPython.Utilities import same_type

    class Foo(object):
        pass
    assert same_type(object(), Foo()) is False


def test_sametype_only_multiple_args_same():
    from Aspidites.features.RestrictedPython.Utilities import same_type
    assert same_type(object(), object(), object(), object())


def test_sametype_only_multipe_args_one_different():
    from Aspidites.features.RestrictedPython.Utilities import same_type

    class Foo(object):
        pass
    assert same_type(object(), object(), Foo()) is False


def test_test_single_value_true():
    from Aspidites.features.RestrictedPython.Utilities import test
    assert test(True) is True


def test_test_single_value_False():
    from Aspidites.features.RestrictedPython.Utilities import test
    assert test(False) is False


def test_test_even_values_first_true():
    from Aspidites.features.RestrictedPython.Utilities import test
    assert test(True, 'first', True, 'second') == 'first'


def test_test_even_values_not_first_true():
    from Aspidites.features.RestrictedPython.Utilities import test
    assert test(False, 'first', True, 'second') == 'second'


def test_test_odd_values_first_true():
    from Aspidites.features.RestrictedPython.Utilities import test
    assert test(True, 'first', True, 'second', False) == 'first'


def test_test_odd_values_not_first_true():
    from Aspidites.features.RestrictedPython.Utilities import test
    assert test(False, 'first', True, 'second', False) == 'second'


def test_test_odd_values_last_true():
    from Aspidites.features.RestrictedPython.Utilities import test
    assert test(False, 'first', False, 'second', 'third') == 'third'


def test_test_odd_values_last_false():
    from Aspidites.features.RestrictedPython.Utilities import test
    assert test(False, 'first', False, 'second', False) is False


def test_reorder_with__None():
    from Aspidites.features.RestrictedPython.Utilities import reorder
    before = ['a', 'b', 'c', 'd', 'e']
    without = ['a', 'c', 'e']
    after = reorder(before, without=without)
    assert after == [('b', 'b'), ('d', 'd')]


def test_reorder_with__not_None():
    from Aspidites.features.RestrictedPython.Utilities import reorder
    before = ['a', 'b', 'c', 'd', 'e']
    with_ = ['a', 'd']
    without = ['a', 'c', 'e']
    after = reorder(before, with_=with_, without=without)
    assert after == [('d', 'd')]
