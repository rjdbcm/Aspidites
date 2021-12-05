# cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=False, initializedcheck=False
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
import functools
import sys

# ~ do not used the vendored version of getouterframes ~
from types import FunctionType
from inspect import getouterframes
from contextlib import suppress
from warnings import warn
from typing import Any, AnyStr, Union, Tuple, Dict, Callable

import cython

from Aspidites._vendor.pyrsistent import v, pvector, pmap

from .math import Undefined, Warn


@cython.ccall
@cython.inline
@functools.lru_cache
def maybe_call(instance, func, args, kwargs, _warn, warn_undefined):
    e: Exception
    w: str
    warn_undefined: bool
    try:
        with suppress(ValueError):
            val = instance or func(*(args or tuple()), **(kwargs or {}))
        with suppress(UnboundLocalError):
            instance = val
            return instance
        instance = Undefined(func, args, kwargs)
    except Exception as e:
        if warn_undefined:
            w = _warn.create(e)
            warn(w, category=RuntimeWarning, stacklevel=0)
        # UNDEFINED #
        instance = Undefined(func, args, kwargs)
        return instance


class Maybe:
    """Sandboxes a function call and handles Exceptions by returning an instance of
    :class:`Aspidites.math.Undefined`"""
    __slots__ = v("_func", "_args", "_kwargs", "_stack", "_warn", "__instance__")

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = pmap(kwargs)
        # noinspection PyUnresolvedReferences,PyProtectedMember
        self._stack = pvector(getouterframes(sys._getframe(0), 1))
        self._warn = Warn(self._stack, self._func, self._args, self._kwargs)
        self.__instance__ = Undefined()
        with suppress(Exception):
            self.__instance__ = self._func(*(self._args or tuple()), **(self._kwargs or {}))

    def __repr__(self) -> str:
        maybe = self.__class__.__name__
        inst = self.__instance__
        inst_undef = inst == Undefined()
        debug = " -> %s" % Undefined() if inst_undef else " -> %s" % str(inst)
        if hasattr(self._func, "__name__"):
            fname = str(self._func.__name__)
        else:
            fname = type(self._func).__name__
        args = str(self._args).strip("()")
        kwargs = [str(k) + " = " + str(v) for k, v in self._kwargs.items()]
        return maybe + "(" + ", ".join([fname, args, *kwargs]) + ")" + debug

    def __invert__(self):
        return ~self.__instance__

    def __neg__(self):
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

    def __call__(self, warn_undefined=True):
        return maybe_call(
            self.__instance__,
            self._func,
            self._args,
            self.kwargs,
            self._warn,
            warn_undefined)
