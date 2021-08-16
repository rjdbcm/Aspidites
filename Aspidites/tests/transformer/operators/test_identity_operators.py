from Aspidites.tests.helper import restricted_eval
import warnings


def test_Is():
    assert restricted_eval('True is True') is True


def test_NotIs():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        assert restricted_eval('1 is not True') is True
