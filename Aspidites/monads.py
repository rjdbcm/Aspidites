#cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=False, initializedcheck=False
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
import sys
# ~ do not used the vendored version of getouterframes ~
from inspect import getouterframes
from contextlib import suppress
from warnings import warn
from typing import Any, AnyStr, Union, Tuple, Dict, Callable

from pyrsistent import v, pvector

from .math import Undefined, Warn


def _apply(f, args=None, kwargs=None):
    return f(*(args or tuple()), **(kwargs or {}))


class Surely:
    """A monad for a successful programmatic unit.
    Truthy, defers to an instance of a successful computation
    """

    __slots__ = v(
        "__weakref__", "__instance__" "__str__", "__int__", "__float__", "__complex__"
    )

    # def __try_except_undefined__(self, other=None, call=None):
    #     if call:
    #         # noinspection PyComparisonWithNone
    #         return (call(self.__instance__) if other is None else call(self.__instance__, other)
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

    # The default value for instance__ MUST BE Undefined()
    def __new__(cls, instance__=Undefined(), *args, **kwargs):
        cls.__instance__ = instance__
        # noinspection PyUnresolvedReferences
        return cls.__instance__


class Maybe:
    """Sandboxes a :class:`Aspidites.monads.Surely` call and handles ContractNotRespected by returning an instance of
     :class:`Aspidites.math.Undefined`"""

    __slots__ = v("_func", "_args", "_kwargs", "_stack", "_warn", "__instance__")

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        # noinspection PyUnresolvedReferences,PyProtectedMember
        self._stack = pvector(getouterframes(sys._getframe(0), 1))
        self._warn = Warn(self._stack, self._func, self._args, self._kwargs)
        self.__instance__ = Undefined()

    def __repr__(self) -> str:
        maybe = self.__class__.__name__
        inst = self.__instance__
        inst_undef = inst == Undefined()
        debug = (" -> %s" % Undefined() if inst_undef else " -> %s" % str(inst))
        if hasattr(self._func, '__name__'):
            fname = str(self._func.__name__)
        else:
            fname = type(self._func).__name__
        args = str(self._args).strip("()")
        kwargs = [str(k) + " = " + str(v) for k, v in self._kwargs.items()]
        return maybe + "(" + ", ".join([fname, args, *kwargs]) + ")" + debug

    def __invert__(self) -> Union[Surely, Undefined]:
        return ~self.__instance__

    def __neg__(self) -> Union[Surely, Undefined]:
        return -self.__instance__

    @property
    def func(self) -> Callable:
        return self._func

    @property
    def args(self) -> Tuple[Any]:
        return self._args

    @property
    def kwargs(self) -> Dict[AnyStr, Any]:
        return self._kwargs

    def __call__(self, warn_undefined=True) -> Union[Surely, Undefined, Any]:
        try:
            with suppress(ValueError):
                val = _apply(self.func, self.args, self.kwargs)
            with suppress(UnboundLocalError):
                self.__instance__ = Surely(val)
                # SURELY #
                return self.__instance__
            self.__instance__ = Undefined()
        except Exception as e:
            if warn_undefined:
                w = self._warn.create(e)
                warn(w, category=RuntimeWarning, stacklevel=0)
            # UNDEFINED #
            self.__instance__ = Undefined()
            return self.__instance__

