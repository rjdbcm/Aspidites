import os
import warnings
from pathlib import Path

import hypothesis
import pytest as pt
from hypothesis import given, assume, strategies as st

try:
    from numpy import inf, nan, isinf, isnan
except ImportError:
    from math import inf, nan, isinf, isnan


from .._vendor.contracts import ContractNotRespected
from ..__main__ import get_cy_kwargs, main
from ..parser import parse_module
from ..templates import woma_template
from ..monads import Maybe, Surely
from ..math import SafeFloorDiv, SafeMod, SafeDiv, SafeExp, Undefined
from ..compiler import Compiler

MAX = 100000
MIN = -MAX
docker = os.getenv("ASPIDITES_DOCKER_BUILD")

woma_file = str(Path('examples/examples.wom'))


@pt.fixture(autouse=True)
def inject_config(request):
    return request.config.rootpath


def setup_code(inject_config):
    if Path(woma_file).exists():
        code_ = parse_module(open(woma_file, 'r').read())
    else:
        try:
            code_ = parse_module(open(str(Path("Aspidites/tests") / woma_file), 'r').read())
            warnings.warn("Aspidites is being tested in source mode")
        except FileNotFoundError:
            code_ = parse_module(open(Path(inject_config) / woma_file, 'r').read())
    return code_


def test_compile_module(inject_config):
    try:
        compile(woma_template.substitute(code='\n'.join(setup_code(inject_config))), '', 'exec')
    except FileNotFoundError:  # ????
        compile(woma_template.substitute(code='\n'.join(os.path.join(inject_config(), woma_file))), '',
                'exec')


@given(x=st.integers(min_value=MIN, max_value=MAX) | st.floats(allow_nan=False),
       y=st.integers(min_value=MIN, max_value=MAX) | st.floats(allow_nan=False))
@hypothesis.settings(deadline=None)  # TODO: SafeDiv/SafeExp/SafeMod: the specific edge case x=1 y=1 is slow
@pt.mark.filterwarnings('ignore::RuntimeWarning')
def test_safe_div(x, y):
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
    assert isnan(complex(Undefined())) == isnan(complex(nan))
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


def test_cli_help_exit():
    with pt.raises(SystemExit):
        main(['Aspidites', '-h'])


def test_cli_no_arg_exit():
    with pt.raises(SystemExit):
        main(['Aspidites' , ''])


def test_cli_no_target_exit():
    with pt.raises(SystemExit):
        main(['Aspidites', '-fpc'])


def test_cli_examples():
    python_file_ = Path('examples/compiled.py')
    python_file = python_file_ if Path(woma_file).exists() else (Path('Aspidites/tests') / python_file_)
    with pt.raises(SystemExit):
        main(['Aspidites', woma_file, f'-o={python_file}', '-c'])


# @pt.mark.filterwarnings('ignore::RuntimeWarning')
def test_compile_to_shared_object(inject_config):
    python_file_ = str(Path('examples/compiled.pyx'))
    full_path = Path('Aspidites/tests') / python_file_
    python_file = python_file_ if Path(woma_file).exists() else str(full_path)
    kwargs = get_cy_kwargs()
    code = setup_code(inject_config)
    kwargs.update(code=code, fname=python_file, bytecode=True, force=True, c=True, build_requires='', verbose=False)
    try:
        Compiler(**kwargs)
    except (FileNotFoundError, ValueError):
        kwargs.update(code=code, fname=Path(inject_config) / python_file_, bytecode=True)
        Compiler(**kwargs)

    from .examples.compiled import Add, x, y, z, val, div_by_zero, Yield123, Hello

    with pt.raises(ContractNotRespected):
        # noinspection PyTypeChecker
        Add(x=6.5, y=12)

    assert [1, 2, 3] == [i for i in Yield123()]
    assert Maybe(Add, 6.5, 12)() == Undefined()
    assert x() == 6
    assert y() == Undefined()
    assert z == 9
    assert Add(x=3, y=2) == 5
    assert val() == Undefined()
    assert div_by_zero() == Undefined()
    Hello()

#
# def teardown_function():
#     for file in glob.glob('examples/compiled.*'):
#         os.remove(file)
#     try:
#         os.remove('examples/setup.py')
#     except FileNotFoundError:
#         pass
