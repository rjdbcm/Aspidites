# #########################     LICENSE     ############################ #

# Copyright (c) 2005-2021, Michele Simionato
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

#   Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#   Redistributions in bytecode form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

"""
Decorator module, see
https://github.com/micheles/decorator/blob/master/docs/documentation.md
for the documentation.
"""
import operator
from contextlib import _GeneratorContextManager, suppress
from typing import cast
from inspect import signature, isgeneratorfunction, iscoroutinefunction
from .decorator_extension import F, EMPTY, POS, fix


def decorator(caller: F, _func: F = None, kwsyntax=False) -> F:
    """
    decorator(caller) converts a caller function into a decorator
    """
    if _func is not None:  # return a decorated function
        # this is obsolete behavior; you should use decorate instead
        return cast(F, decorate(_func, caller, (), kwsyntax))
    # else return a decorator function
    sig = signature(caller)
    dec_params = [p for p in sig.parameters.values() if p.kind is POS]

    def dec(func=None, *args, **kw):
        na = len(args) + 1
        extras = args + tuple(kw.get(p.name, p.default)
                              for p in dec_params[na:]
                              if p.default is not EMPTY)
        if func is None:
            return lambda func: decorate(func, caller, extras, kwsyntax)
        else:
            return decorate(func, caller, extras, kwsyntax)
    dec.__signature__ = sig.replace(parameters=dec_params)
    dec.__name__ = caller.__name__
    dec.__doc__ = caller.__doc__
    dec.__wrapped__ = caller
    dec.__qualname__ = caller.__qualname__
    dec.__kwdefaults__ = getattr(caller, '__kwdefaults__', None)
    dec.__dict__.update(caller.__dict__)
    return cast(F, dec)


# ####################### contextmanager ####################### #


class ContextManager(_GeneratorContextManager):
    def __init__(self, g, *a, **k):
        # noinspection PyReturnFromInit
        return _GeneratorContextManager.__init__(self, g, a, k)

    def __call__(self, func):
        def caller(f, *a, **k):
            with self:
                return f(*a, **k)
        return decorate(func, caller)


_contextmanager = decorator(ContextManager)


def contextmanager(func):
    # Enable Pylint config: contextmanager-decorators=decorator.contextmanager
    return _contextmanager(func)


def decorate(func: F, caller, extras=(), kwsyntax=False) -> F:
    """
    Decorates a function/generator/coroutine using a caller.
    If kwsyntax is True calling the decorated functions with keyword
    syntax will pass the named arguments inside the ``kw`` dictionary,
    even if such argument are positional, similarly to what functools.wraps
    does. By default kwsyntax is False and the the arguments are untouched.
    """
    sig = signature(func)
    if iscoroutinefunction(caller):
        async def fun(*args, **kw):
            if not kwsyntax:
                args, kw = fix(args, kw, sig)
            return await caller(func, *(extras + args), **kw)
    elif isgeneratorfunction(caller):
        def fun(*args, **kw):
            if not kwsyntax:
                args, kw = fix(args, kw, sig)
            for res in caller(func, *(extras + args), **kw):
                yield res
    else:
        def fun(*args, **kw):
            if not kwsyntax:
                args, kw = fix(args, kw, sig)
            return caller(func, *(extras + args), **kw)
    fun.__name__ = func.__name__
    fun.__doc__ = func.__doc__
    fun.__wrapped__ = func
    fun.__signature__ = sig
    fun.__qualname__ = func.__qualname__
    # builtin functions like defaultdict.__setitem__ lack many attributes
    with suppress(AttributeError):
        fun.__defaults__ = func.__defaults__
        fun.__kwdefaults__ = func.__kwdefaults__
        fun.__annotations__ = func.__annotations__
        fun.__module__ = func.__module__
        fun.__dict__.update(func.__dict__)

    return cast(F, fun)