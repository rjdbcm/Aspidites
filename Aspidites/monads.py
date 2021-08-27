
# Aspidites
# Copyright (C) 2021 Ross J. Duff

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import inspect
from math import inf, isinf
from contextlib import suppress
from _warnings import warn

from pyrsistent import v, pvector

from ._vendor.contracts import ContractNotRespected, contract
from ._vendor.fn import apply
from ._vendor.fn.underscore import ArityError
from .api import ContractBreachWarning, create_warning


# noinspection PyPep8Naming
def SafeDiv(a, b):
    """IEEE 754-1985 evaluates an expression and replaces indeterminate forms with Undefined instances"""
    if b == 0 or (isinf(a) and isinf(b)):
        stack = inspect.stack()
        w = create_warning(
            stack[0][3],
            [a, b],
            {},
            stack,
            ZeroDivisionError("Division by zero is Undefined; this behavior diverges from IEEE 754-1985.")
        )
        warn(w, category=RuntimeWarning)
        return Undefined(SafeDiv, a=a, b=b)
    return a / b


# noinspection PyPep8Naming
def SafeMod(a, b):
    """IEEE 754-1985 evaluates an expression and replaces indeterminate forms with Undefined instances"""
    if isinf(a) or b == 0:
        stack = inspect.stack()
        w = create_warning(
            stack[0][3],
            [a, b],
            {},
            stack,
            ZeroDivisionError("Modulus by zero is Undefined; this behavior diverges from IEEE 754-1985.")
        )
        warn(w, category=RuntimeWarning)
        return Undefined(SafeMod, a=a, b=b)
    return a % b


# noinspection PyPep8Naming
def SafeExp(a, b):
    if ((a == 0 and b == 0) or (isinf(a) and b == 0) or (isinf(b) and a == 0)):  # 0**0, inf**0, 0**inf
        stack = inspect.stack()
        w = create_warning(
            stack[0][3], [a, b], {}, stack,
            ArithmeticError("%s**%s" % (str(a), str(b),) + " == Undefined; this behavior diverges from IEEE 754-1985.")
        )
        warn(w, category=RuntimeWarning)
        return Undefined(SafeExp, a=a, b=b)
    try:
        return a**b
    except OverflowError:
        return inf  # just a really big number on most systems


class Maybe:
    """Sandboxes a Surely call and handles ContractNotRespected by returning Undefined"""

    __slots__ = v("_func", "_args", "_kwargs", "_stack", "__instance__")

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._stack = pvector(inspect.stack(1))
        self.__instance__ = Undefined()

    def __repr__(self):
        maybe = self.__class__.__name__
        inst = self.__instance__
        inst_undef = inst == Undefined()
        debug = (" -> %s" % Undefined() if inst_undef else " -> %s" % str(inst))
        fname = str(self._func.__name__)
        args = str(self._args).strip("()")
        kwargs = [str(k) + " = " + str(v) for k, v in self._kwargs.items()]
        return maybe + "(" + ", ".join([fname, args, *kwargs]) + ")" + debug

    def __invert__(self):
        return ~self.__instance__

    def __neg__(self):
        return -self.__instance__

    @property
    def func(self):
        return self._func

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    def __call__(self, warn_undefined=True):
        try:
            with suppress(ValueError):
                val = apply(self.func, self.args, self.kwargs)
            with suppress(UnboundLocalError):
                self.__instance__ = Surely(val)
                # SURELY #
                return self.__instance__
            self.__instance__ = Undefined(self.func, self.args, self.kwargs)
        except (ContractNotRespected, ArityError, ZeroDivisionError, Exception) as e:
            if warn_undefined:
                w = create_warning(self.func, self.args, self.kwargs, self._stack, e)
                warn(w, category=ContractBreachWarning if isinstance(e, ContractNotRespected) else RuntimeWarning)
            # UNDEFINED #
            self.__instance__ = Undefined(self.func, self.args, self.kwargs)
            return self.__instance__


class Undefined:
    """A monad for a failed programmatic unit; like NoneType but hashable.
    Falsy singleton"""

    __slots__ = v("__weakref__", "__instance__")
    __instance = None

    def __hash__(self):
        return self

    def __eq__(self, other):
        return self.__hash__ == other.__hash__

    def __add__(self, other):
        return other

    def __sub__(self, other):
        return -other

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
        return str(self.__repr__())

    def __float__(self):
        return float()

    def __complex__(self):
        return complex()

    def __oct__(self):
        return oct(0)

    def __index__(self):
        return 0

    def __len__(self):
        # Undefined has 0 elements
        return 0

    def __repr__(self):
        return self.__class__.__name__

    def __nonzero__(self):
        return False

    def __call__(self, *args, **kwargs):
        return self.__new__(self.__class__, *args, **kwargs)

    def __new__(mcs, *args, **kwargs):
        if mcs.__instance is None:
            mcs.__instance = super(Undefined, mcs).__new__(mcs, *args, **kwargs)
            mcs.__instance__ = mcs.__instance
        return mcs.__instance__  # instance descriptor from __slots__ -> actual instance


class Surely:
    """A monad for a successful programmatic unit
    Truthy, defers to an instance of a successful computation"""

    __slots__ = v(
        "__weakref__", "__instance__" "__str__", "__int__", "__float__", "__complex__"
    )

    # def __try_except_undefined__(self, other=None, call=None):
    #     if call:
    #         # noinspection PyComparisonWithNone
    #         return (
    #             call(self.__instance__)
    #             if other == None
    #             else call(self.__instance__, other)
    #         )
    #     else:
    #         return self.__instance__
    #
    # def __hash__(self):
    #     return self.__try_except_undefined__(call=hash)
    #
    # def __eq__(self, other):
    #     return self.__try_except_undefined__(other, op.eq)
    #
    # def __add__(self, other):
    #     return self.__try_except_undefined__(other, op.add)
    #
    # def __sub__(self, other):
    #     return self.__try_except_undefined__(other, op.sub)
    #
    # def __neg__(self):
    #     return self.__try_except_undefined__(call=op.neg)
    #
    # def __invert__(self):
    #     return self.__try_except_undefined__(call=op.invert)
    #
    # def __mul__(self, other):
    #     return self.__try_except_undefined__(other, op.mul)
    #
    # def __truediv__(self, other):
    #     return self.__try_except_undefined__(other, op.truediv)
    #
    # def __floordiv__(self, other):
    #     return self.__try_except_undefined__(other, op.floordiv)
    #
    # def __oct__(self):
    #     return self.__try_except_undefined__(call=oct)
    #
    # def __nonzero__(self):
    #     return self.__try_except_undefined__(call=bool)
    #
    # @classmethod
    # def __call__(cls, *args, **kwargs):
    #     return cls.__instance__

    def __new__(cls, instance__=Undefined(), *args, **kwargs):
        cls.__instance__ = instance__
        return cls.__instance__
