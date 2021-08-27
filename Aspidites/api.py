
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

from pyparsing import ParseResults

from ._vendor.contracts import new_contract
from ._vendor.fn.underscore import ArityError, _Callable


def wrap(text, width=160, pad=True, padchar=" "):
    """
    Do not remove whitespaces in string but still wrap text to max width.
    Instead of passing the entire text to textwrap.wrap, split and pass each
    line instead. This way list formatting is not mangled by textwrap.wrap.
    """
    wrapped_lines = []
    try:
        for l in text.splitlines():
            line = _wrap(l, width, replace_whitespace=False)
            if pad:
                for s in line:
                    s += padchar * width
            wrapped_lines.extend(line)
    except ArityError:
        wrapped_lines.extend([str(text)])

    return wrapped_lines


def bordered(text: str, width: int = 160):
    lines = [i for i in wrap(text, width=width)]
    width = max((len(s) for s in lines), default=width) or width
    res = ["╭" + "┉" * width + "╮"]
    for s in lines:
        while len(s) < width:
            s += " "
        res.append("┊" + s + "┊")
    res.append("╰" + "┉" * width + "╯")
    return "\n".join(res)


code = new_contract("code", lambda x: isinstance(x, ParseResults))

