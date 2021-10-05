import sys
from warnings import warn
from typing import Any, Union, TypeVar, ItemsView
from inspect import isfunction, signature, getouterframes
from cmath import inf, isinf, nan, isnan
import numbers
import numpy as np
from ._vendor.fn.underscore import _Callable
from pyrsistent import v, pvector
from .templates import _warning
from .api import bordered
N = TypeVar('N')
Numeric: N = Union[int, float, complex, np.number]


class Undefined:
    """A monad for a failed programmatic unit; like NoneType but hashable.
    Falsy singleton acts as an absorbing element for division."""

    __slots__ = v("__weakref__", "__instance__")
    __instance = None

    def __hash__(self):
        # noinspection PyUnresolvedReferences
        return hash(self.__weakref__)

    def __eq__(self, other: Any):
        return self.__hash__ == other.__hash__

    def __add__(self, other: Any):
        return self

    def __sub__(self, other: Any):
        return self

    def __mul__(self, other: Any):
        return self

    def __truediv__(self, other: Any):
        return self

    def __floordiv__(self, other):
        return self

    def __neg__(self):
        return self

    def __invert__(self):
        return self

    def __str__(self):
        return self.__repr__()

    def __float__(self):
        return nan

    def __complex__(self):
        return complex(nan)

    def __oct__(self):
        return self

    def __index__(self):
        return 0

    def __len__(self):
        # Undefined has 0 elements
        return 0

    def __repr__(self):
        return self.__class__.__name__ + "()"

    # noinspection PyMethodMayBeStatic
    def __nonzero__(self):
        return True

    def __call__(self, *args, **kwargs):
        return self.__new__(self.__class__, *args, **kwargs)

    # noinspection PyMethodParameters
    def __new__(mcs, *args, **kwargs):
        if mcs.__instance is None:
            mcs.__instance = super(Undefined, mcs).__new__(mcs, *args, **kwargs)
            mcs.__instance__ = mcs.__instance
        # noinspection PyUnresolvedReferences
        return mcs.__instance__  # instance descriptor from __slots__ -> actual instance


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
def SafeUnaryAdd(a: Numeric) -> Union[Numeric, Undefined]:
    a: Numeric
    if isnan(a) or not isinstance(a, numbers.Number):
        stack = pvector(getouterframes(sys._getframe(0), 1))
        exc = ZeroDivisionError(f"Unary Add is Undefined for {type(a)}")
        w = Warn(stack, stack[0][3], [a], {}).create(exc)
        warn(w, category=RuntimeWarning, stacklevel=0)
        return Undefined()
    return +a


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
def SafeUnarySub(a: Numeric) -> Union[Numeric, Undefined]:
    a: Numeric
    if isnan(a) or not isinstance(a, numbers.Number):
        stack = pvector(getouterframes(sys._getframe(0), 1))
        exc = ZeroDivisionError(f"Unary Sub is Undefined for {type(a)}")
        w = Warn(stack, stack[0][3], [a], {}).create(exc)
        warn(w, category=RuntimeWarning, stacklevel=0)
        return Undefined()
    return -a


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
def SafeFloorDiv(a: Numeric, b: Numeric) -> Union[Numeric, Undefined]:
    """IEEE 754-1985 evaluates an expression and replaces indeterminate forms with Undefined instances"""
    a: Numeric
    b: Numeric
    if isinf(a) or b == 0 or (isinf(a) and isinf(b)):
        stack = pvector(getouterframes(sys._getframe(0), 1))
        exc = ZeroDivisionError("Division by zero is Undefined; this behavior diverges from IEEE 754-1985.")
        w = Warn(stack, stack[0][3], [a, b], {}).create(exc)
        warn(w, category=RuntimeWarning, stacklevel=0)
        return Undefined()
    return a // b


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
def SafeDiv(a: Numeric, b: Numeric) -> Union[Numeric, Undefined]:
    """IEEE 754-1985 evaluates an expression and replaces indeterminate forms with Undefined instances"""
    a: Numeric
    b: Numeric
    if b == 0 or (isinf(a) and isinf(b)):
        stack = pvector(getouterframes(sys._getframe(0), 1))
        exc = ZeroDivisionError("Division by zero is Undefined; this behavior diverges from IEEE 754-1985.")
        w = Warn(stack, stack[0][3], [a, b], {}).create(exc)
        warn(w, category=RuntimeWarning, stacklevel=0)
        return Undefined()
    return a / b


# noinspection PyPep8Naming, PyProtectedMember,PyUnresolvedReferences
def SafeMod(a: Numeric, b: Numeric) -> Union[Numeric, Undefined]:
    """IEEE 754-1985 evaluates an expression and replaces indeterminate forms with Undefined instances"""
    a: Numeric
    b: Numeric
    if isinf(a) or b == 0:
        stack = pvector(getouterframes(sys._getframe(0), 1))
        exc = ZeroDivisionError("Modulus by zero is Undefined; this behavior diverges from IEEE 754-1985.")
        w = Warn(stack, stack[0][3], [a, b], {}).create(exc)
        warn(w, category=RuntimeWarning, stacklevel=0)
        return Undefined()
    return a % b


# noinspection PyPep8Naming, PyProtectedMember,PyUnresolvedReferences
def SafeExp(a: Numeric, b: Numeric) -> Union[Numeric, Undefined]:
    a: Numeric
    b: Numeric
    if (a == 0 and b == 0) or (isinf(a) and b == 0) or (isinf(b) and a == 0):  # 0**0, inf**0, 0**inf
        stack = pvector(getouterframes(sys._getframe(0), 1))
        exc = ArithmeticError(
            f"{str(a)}**{str(b)} == Undefined; this behavior diverges from IEEE 754-1985."
        )
        w = Warn(stack, stack[0][3], [a, b], {}).create(exc)
        warn(w, category=RuntimeWarning, stacklevel=0)
        return Undefined()
    try:
        return a**b
    except OverflowError:
        return inf  # just a really big number on most systems


class Warn:

    def __init__(self, stack, func, *args, **kwargs):
        self.stack = stack
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def create(self, exc=Exception()):
        _locals: ItemsView = self.stack[1][0].f_locals.items()
        str_locals: bytes = self.format_locals(_locals, exc)
        func_name: str = self.stack[1][0].f_code.co_name
        fname: str = self.stack[1][0].f_code.co_filename
        lineno: int = self.stack[1][0].f_code.co_firstlineno
        fkwargs = str(self.format_kwargs()).lstrip("b'").rstrip("'")
        name: Union[_Callable, str]
        if hasattr(self.func, "__name__"):
            name = self.func.__name__
        else:
            name = str(self.func)
        atfault = str(name).encode('UTF-8') if isinstance(exc, TypeError) else f"{name}({str(self.args).strip('()')}{fkwargs})".encode('UTF-8')
        return _warning.safe_substitute(
            file=fname,
            lineno=lineno,
            func=bordered(func_name),
            atfault=bordered(atfault.decode('UTF-8')),
            bound=bordered(str_locals.decode('UTF-8')),
            tb=bordered(str(exc)),
        )

    def format_kwargs(self, sep: str = ", "):
        return f'{sep}{str(self.kwargs).strip("{} ").replace(":", "=") if len(self.kwargs) else ""}'.encode('UTF-8')

    # noinspection PyMethodMayBeStatic
    def format_locals(self, local_vars, exc: Exception):
        locals_: dict = dict(filter(lambda x: x[1] != str(exc), local_vars))
        str_locals: bytes = ''.encode('UTF-8')
        for k, v_ in locals_.items():
            if str(k).startswith("@"):  # skip @py_assert
                continue
            if isfunction(v_):
                s = str(signature(v_)).replace("'", "")
                str_locals += f"{k}: {s}\n".encode('UTF-8')
            else:
                str_locals += f"{k}: {str(v_)}\n".encode('UTF-8')
        return str_locals.rstrip("\n".encode('UTF-8'))

