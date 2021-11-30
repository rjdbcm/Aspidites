# cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8
import sys
from warnings import warn
from typing import Any, Union
from inspect import getouterframes
from math import inf, isinf, nan, isnan
from math import factorial
import numbers

import cython

try:
    import numpy as np

    Numeric = Union[int, float, complex, np.number]
except ModuleNotFoundError:
    Numeric = Union[int, float, complex]

from Aspidites.api import Warn


class Undefined:
    """A monad for a failed programmatic unit; like NoneType but hashable.
    Falsy singleton acts as an absorbing element for division."""

    __slots__ = ("__weakref__", "__instance__", "_consumed", "func", "args", "kwargs")

    def __hash__(self):
        # noinspection PyUnresolvedReferences
        return hash(self.__weakref__)

    def __eq__(self, other: Any):
        return type(other) == Undefined

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

    def __int__(self):
        return nan

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

    def __iter__(self):
        return Undefined(self)

    def __next__(self):
        if not self._consumed:
            self._consumed = True
            return Undefined(self)
        else:
            raise StopIteration

    def __repr__(self):
        if hasattr(self.func, "__name__"):
            r = (
                self.__class__.__name__
                + f"({self.func.__name__}, {self.args}, {self.kwargs})"
            )
        else:
            r = self.__class__.__name__ + f"({None}, {self.args}, {self.kwargs})"
        return r

    # noinspection PyMethodMayBeStatic
    def __nonzero__(self):
        return True

    def __init__(self, func=None, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._consumed = False


@cython.ccall
@cython.inline
def SafeSlice(x, start=None, stop=None, step=None):
    if not stop and not step:
        return x[start]
    else:
        return x[start:stop:step]


def SafeLoop(x: Any):
    return (i for i in x)


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
@cython.ccall
@cython.inline
def SafeFactorial(a):
    if a < 0 or isnan(a) or isinf(a) or isinstance(a, (float, complex)):
        return Undefined(SafeFactorial, a)
    return factorial(a)


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
@cython.ccall
@cython.inline
def SafeUnaryAdd(a):
    if isnan(a) or not isinstance(a, numbers.Number):
        return Undefined(SafeUnaryAdd, a)
    return +a


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
@cython.ccall
@cython.inline
def SafeUnarySub(a):
    if isnan(a) or not isinstance(a, numbers.Number):
        return Undefined(SafeUnarySub, a)
    return -a


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
@cython.ccall
@cython.inline
def SafeFloorDiv(a, b):
    if isinf(a) or b == 0 or (isinf(a) and isinf(b)):
        return Undefined(SafeFloorDiv, a, b)
    return a // b


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
@cython.ccall
@cython.inline
def SafeMul(a, b):
    return a * b


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
@cython.ccall
@cython.inline
def SafeSub(a, b):
    return a - b


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
@cython.ccall
@cython.inline
def SafeAdd(a, b):
    return a + b


# noinspection PyPep8Naming,PyProtectedMember,PyUnresolvedReferences
@cython.ccall
@cython.inline
def SafeDiv(a, b):
    if b == 0 or (isinf(a) and isinf(b)):
        return Undefined(SafeDiv, a, b)
    return a / b


# noinspection PyPep8Naming, PyProtectedMember,PyUnresolvedReferences
@cython.ccall
@cython.inline
def SafeMod(a, b):
    if isinf(a) or b == 0:
        return Undefined(SafeMod, a, b)
    return a % b


# noinspection PyPep8Naming, PyProtectedMember,PyUnresolvedReferences
@cython.ccall
@cython.inline
def SafeExp(a, b):
    if (
        (a == 0 and b == 0) or (isinf(a) and b == 0) or (isinf(b) and a == 0)
    ):  # pragma: no cover
        return Undefined(SafeExp, a, b)
    try:
        return a ** b
    except OverflowError:
        return inf  # just a really big number on most systems
