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

from typing import Union, ItemsView
from textwrap import wrap
from Aspidites._vendor.pyparsing import ParseResults
from inspect import isfunction, signature
from ._vendor.contracts import new_contract
from ._vendor.fn.underscore import ArityError, _Callable
from .templates import warning_template
import cython


def _wrap_lines(text, padchar, width, wrapped_lines, pad):
    for l in text.splitlines():
        line = wrap(l, width, replace_whitespace=False)
        for s in line:
            s += padchar * width * pad
        wrapped_lines.extend(line)
    return wrapped_lines


def _wrap(text, width, pad, padchar):
    """
    Do not remove whitespaces in string but still wrap text to max width.
    Instead of passing the entire text to textwrap.wrap, split and pass each
    line instead. This way list formatting is not mangled by textwrap.wrap.
    """
    pad = pad or True
    padchar = padchar or ' '.encode('UTF-8')
    width = width or 160

    wrapped_lines = []
    try:
        _wrap_lines(text, padchar, width, wrapped_lines, pad)
    except ArityError:
        wrapped_lines.extend([str(text)])

    return wrapped_lines


def bordered(text, width=160) -> str:
    """Create a fancy bordered textbox as used in :class:`Aspidites.api.Warn`."""
    i: str
    lines: list = [t for t in _wrap(text, width=width, pad=True, padchar=" ")]
    lens: list = [len(i) for i in lines]
    width = max(lens, default=width) or width
    res = ["╭" + "┉" * width + "╮"]
    for s in lines:
        while len(s) < width:
            s += " "
        res.append("┊" + s + "┊")
    res.append("╰" + "┉" * width + "╯")
    return "\n".join(res)


def _format_locals(lokals: dict):
    d = {k: v for k, v in lokals.items() if not str(k).startswith('@')}
    str_locals = _format_items(d)
    return str_locals


def _format_items(x):
    str_locals = ''.encode('UTF-8')
    for k, v in x.items():
        if isfunction(v):
            s = str(signature(v)).replace("'", "")
            str_locals += f"{k}: {s}\n".encode('UTF-8')
        else:
            str_locals += f"{k}: {str(v)}\n".encode('UTF-8')
    return str_locals


class Warn:
    """Creates a nice human-readable warning with a fancy border."""
    sig: cython.p_char
    name: Union[_Callable, cython.p_char]
    local_items: ItemsView
    str_locals: bytes
    at_fault: bytes
    func_name: cython.p_char
    fname: cython.p_char
    # noinspection PyUnresolvedReferences
    lineno: cython.int
    fkwargs: cython.p_char

    def __init__(self, stack, func, *args, **kwargs):
        self.stack = stack
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def create(self, exc=Exception()) -> str:
        local_items = self.stack[1][0].f_locals.items()
        str_locals = self.format_locals(local_items, exc)
        func_name = self.stack[1][0].f_code.co_name
        fname = self.stack[1][0].f_code.co_filename
        lineno = self.stack[1][0].f_code.co_firstlineno
        fkwargs = str(self.format_kwargs()).lstrip("b'").rstrip("'")
        name = self.func.__name__ if hasattr(self.func, "__name__") else str(self.func)
        sig = f"{name}({str(self.args).strip('()')}{fkwargs})"
        at_fault = str(name).encode('UTF-8') if isinstance(exc, TypeError) else sig.encode('UTF-8')
        return warning_template.safe_substitute(
            file=fname,
            lineno=lineno,
            func=bordered(func_name),
            atfault=bordered(at_fault.decode('UTF-8')),
            bound=bordered(str_locals.decode('UTF-8')),
            tb=bordered(str(exc)),
        )

    def format_kwargs(self, sep: str = ", ") -> bytes:
        return f'{sep}{str(self.kwargs).strip("{} ").replace(":", "=") if len(self.kwargs) else ""}'.encode('UTF-8')

        # noinspection PyMethodMayBeStatic

    def format_locals(self, local_vars, exc: Exception) -> bytes:
        lokals: dict = dict(filter(lambda x: x[1] != str(exc), local_vars))
        str_locals: bytes = _format_locals(lokals)
        return str_locals.rstrip("\n".encode('UTF-8'))


code = new_contract("code", lambda x: isinstance(x, ParseResults))
