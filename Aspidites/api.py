# Aspidites is Copyright 2021, Ross J. Duff.
# See LICENSE.txt for more info.

import contextlib
import os
import typing
from hashlib import sha256
from inspect import isfunction, signature
from os import get_terminal_size
from textwrap import wrap as _wrap

from pyparsing import ParseResults
from pyrsistent import PVector, discard, inc, pmap, pvector, rex

from ._vendor.contracts import new_contract
from ._vendor.fn import F, _
from ._vendor.fn.underscore import ArityError, _Callable
from .templates import _warning


class ContractBreachWarning(RuntimeWarning):
    pass


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


def bordered(text, width=160):
    lines = [i for i in wrap(text, width=width)]
    width = max((len(s) for s in lines), default=width) or width
    res = ["╭" + "┉" * width + "╮"]
    for s in lines:
        while len(s) < width:
            s += " "
        res.append("┊" + s + "┊")
    res.append("╰" + "┉" * width + "╯")
    return "\n".join(res)


def format_kwargs(kwargs: "dict", sep=", "):
    return sep + str(kwargs).strip("{} ").replace(":", "=") if len(kwargs) else ""


def format_locals(locals, exc: "Exception"):
    locals_ = dict(filter(lambda x: x[1] != str(exc), locals))
    str_locals = str()
    for k, v_ in locals_.items():
        if str(k).startswith("@"):  # skip @py_assert
            continue
        if isfunction(v_):
            str_locals += k + ": " + str(signature(v_)).replace("'", "") + "\n"
        else:
            str_locals += k + ": " + str(v_) + "\n"
    return str_locals.rstrip("\n")


def create_warning(func, args, kwargs, stack, exc=Exception()):
    _locals = stack[1][0].f_locals.items()
    str_locals = format_locals(_locals, exc)
    func_name = stack[1][0].f_code.co_name
    fname = stack[1][0].f_code.co_filename
    lineno = stack[1][0].f_code.co_firstlineno
    fkwargs = format_kwargs(kwargs)
    if hasattr(func, "__name__"):
        name = func.__name__
    else:
        name = str(func)
    atfault = (
        name
        if isinstance(exc, ArityError)
        else name + "(" + str(args).strip("()") + fkwargs + ")"
    )
    return _warning.safe_substitute(
        file=fname,
        lineno=lineno,
        func=bordered(func_name),
        atfault=bordered(atfault),
        bound=bordered(str_locals),
        tb=bordered(str(exc)),
    )


MD5 = ".sha256"
code = new_contract("code", lambda x: isinstance(x, ParseResults))


@contextlib.contextmanager
def working_directory(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    Usage:
    > # Do something in original directory
    > with working_directory('/my/new/path'):
    >     # Do something in new directory
    > # Back to old directory
    """

    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def checksum(fname, write=True, check=False):
    base, name = os.path.split(fname)
    fname_sha256 = os.path.join(base, "." + name) + ".sha256"

    def read_sha256(data):
        curr_hash = sha256()
        chunk = data.read(8192)
        while chunk:
            curr_hash.update(chunk)
            chunk = data.read(8192)
        return curr_hash

    if write:
        with open(fname, "rb") as data:
            curr_hash = read_sha256(data)
            with open(fname_sha256, "wb") as digest:
                digest.write(curr_hash.digest())
            return pmap({curr_hash.digest(): fname}).items()[0]  # immutable
    if check:
        with open(fname_sha256, "rb") as digest:
            with open(fname, "rb") as data:
                curr_hash = read_sha256(data)
                old = digest.read()
                new = curr_hash.digest()
                if new == old:
                    print(
                        "sha256 digest check successful: %s, %s == %s"
                        % (fname, new.hex(), old.hex())
                    )
                    return new
                else:
                    print(
                        "sha256 digest failure: %s, %s != %s"
                        % (fname, new.hex(), old.hex())
                    )
                    return ""


class CheckedFileStack:
    def __init__(self, initial=None, pre_size=8192):
        if initial is None:
            initial = {}
        self._files = pmap(initial, pre_size)
        self.all_files = self._files.evolver()

    def register(self, fname):
        self.all_files.set(*checksum(fname))

    def finalize(self):
        return self.all_files.persistent()
