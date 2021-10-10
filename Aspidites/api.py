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

from textwrap import wrap as _wrap
from typing import List
from Aspidites._vendor.pyparsing import ParseResults

from ._vendor.contracts import new_contract
from ._vendor.fn.underscore import ArityError, _Callable


def wrap_lines(text, padchar, width, wrapped_lines, pad):
    for l in text.splitlines():
        line = _wrap(l, width, replace_whitespace=False)
        for s in line:
            s += padchar * width * pad
        wrapped_lines.extend(line)
    return wrapped_lines


def wrap(text, width, pad, padchar):
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
        wrap_lines(text, padchar, width, wrapped_lines, pad)
    except ArityError:
        wrapped_lines.extend([str(text)])

    return wrapped_lines


def bordered(text, width=160) -> str:
    i: str
    lines: list = [t for t in wrap(text, width=width, pad=True, padchar=" ")]
    lens: list = [len(i) for i in lines]
    width = max(lens, default=width) or width
    res = ["╭" + "┉" * width + "╮"]
    for s in lines:
        while len(s) < width:
            s += " "
        res.append("┊" + s + "┊")
    res.append("╰" + "┉" * width + "╯")
    return "\n".join(res)


code = new_contract("code", lambda x: isinstance(x, ParseResults))

