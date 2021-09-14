import sys
from warnings import warn
from inspect import isfunction, signature, getouterframes
from cmath import inf, isinf, nan, isnan
import numbers
from pyrsistent import v, pvector
from .templates import _warning
from .api import bordered


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
def SafeUnaryAdd(a):
    if isnan(a) or not isinstance(a, numbers.Number):
        stack = pvector(getouterframes(sys._getframe(0), 1))
        exc = ZeroDivisionError("Unary Add is Undefined for %s" % type(a))
        w = Warn(stack, stack[0][3], [a], {}).create(exc)
        warn(w, category=RuntimeWarning, stacklevel=0)
        return Undefined()
    return +a


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
def SafeUnarySub(a):
    if isnan(a) or not isinstance(a, numbers.Number):
        stack = pvector(getouterframes(sys._getframe(0), 1))
        exc = ZeroDivisionError("Unary Sub is Undefined for %s" % type(a))
        w = Warn(stack, stack[0][3], [a], {}).create(exc)
        warn(w, category=RuntimeWarning, stacklevel=0)
        return Undefined()
    return -a


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
def SafeFloorDiv(a, b):
    """IEEE 754-1985 evaluates an expression and replaces indeterminate forms with Undefined instances"""
    if isinf(a) or b == 0 or (isinf(a) and isinf(b)):
        stack = pvector(getouterframes(sys._getframe(0), 1))
        exc = ZeroDivisionError("Division by zero is Undefined; this behavior diverges from IEEE 754-1985.")
        w = Warn(stack, stack[0][3], [a, b], {}).create(exc)
        warn(w, category=RuntimeWarning, stacklevel=0)
        return Undefined()
    return a // b


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
def SafeDiv(a, b):
    """IEEE 754-1985 evaluates an expression and replaces indeterminate forms with Undefined instances"""
    if b == 0 or (isinf(a) and isinf(b)):
        stack = pvector(getouterframes(sys._getframe(0), 1))
        exc = ZeroDivisionError("Division by zero is Undefined; this behavior diverges from IEEE 754-1985.")
        w = Warn(stack, stack[0][3], [a, b], {}).create(exc)
        warn(w, category=RuntimeWarning, stacklevel=0)
        return Undefined()
    return a / b


# noinspection PyPep8Naming, PyProtectedMember,PyUnresolvedReferences
def SafeMod(a, b):
    """IEEE 754-1985 evaluates an expression and replaces indeterminate forms with Undefined instances"""
    if isinf(a) or b == 0:
        stack = pvector(getouterframes(sys._getframe(0), 1))
        exc = ZeroDivisionError("Modulus by zero is Undefined; this behavior diverges from IEEE 754-1985.")
        w = Warn(stack, stack[0][3], [a, b], {}).create(exc)
        warn(w, category=RuntimeWarning, stacklevel=0)
        return Undefined()
    return a % b


# noinspection PyPep8Naming, PyProtectedMember,PyUnresolvedReferences
def SafeExp(a, b):
    if (a == 0 and b == 0) or (isinf(a) and b == 0) or (isinf(b) and a == 0):  # 0**0, inf**0, 0**inf
        stack = pvector(getouterframes(sys._getframe(0), 1))
        exc = ArithmeticError(
            "%s**%s" % (str(a), str(b),) + " == Undefined; this behavior diverges from IEEE 754-1985."
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
        _locals = self.stack[1][0].f_locals.items()
        str_locals = self.format_locals(_locals, exc)
        func_name = self.stack[1][0].f_code.co_name
        fname = self.stack[1][0].f_code.co_filename
        lineno = self.stack[1][0].f_code.co_firstlineno
        fkwargs = self.format_kwargs()
        if hasattr(self.func, "__name__"):
            name = self.func.__name__
        else:
            name = str(self.func)
        atfault = (
            name
            if isinstance(exc, TypeError)
            else name + "(" + str(self.args).strip("()") + fkwargs + ")"
        )
        return _warning.safe_substitute(
            file=fname,
            lineno=lineno,
            func=bordered(func_name),
            atfault=bordered(atfault),
            bound=bordered(str_locals),
            tb=bordered(str(exc)),
        )

    def format_kwargs(self, sep: str = ", "):
        return sep + str(self.kwargs).strip("{} ").replace(":", "=") if len(self.kwargs) else ""

    # noinspection PyMethodMayBeStatic
    def format_locals(self, local_vars, exc: Exception):
        locals_ = dict(filter(lambda x: x[1] != str(exc), local_vars))
        str_locals = str()
        for k, v_ in locals_.items():
            if str(k).startswith("@"):  # skip @py_assert
                continue
            if isfunction(v_):
                str_locals += k + ": " + str(signature(v_)).replace("'", "") + "\n"
            else:
                str_locals += k + ": " + str(v_) + "\n"
        return str_locals.rstrip("\n")


class Undefined:
    """A monad for a failed programmatic unit; like NoneType but hashable.
    Falsy singleton"""

    __slots__ = v("__weakref__", "__instance__")
    __instance = None

    def __hash__(self):
        # noinspection PyUnresolvedReferences
        return hash(self.__weakref__)

    def __eq__(self, other):
        return self.__hash__ == other.__hash__

    def __add__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __neg__(self):
        return self

    def __invert__(self):
        return self

    def __mul__(self, other):
        return self

    def __truediv__(self, other):
        return self

    def __floordiv__(self, other):
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
