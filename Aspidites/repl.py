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
import subprocess
import sys
from itertools import cycle
import threading
import os
import curses
import re
import warnings
from contextlib import suppress
import time
from pathlib import Path
from traceback import print_exc
from typing import List, AnyStr, Union

# noinspection PyUnresolvedReferences
from pyrsistent import pvector, pmap, pset
# noinspection PyUnresolvedReferences
from Aspidites._vendor.contracts import contract, new_contract
from Aspidites._vendor.pyparsing import ParseException, ParseResults
# noinspection PyUnresolvedReferences
from cmath import inf
# noinspection PyUnresolvedReferences
from Aspidites import *
import Aspidites.parser.parser
from Aspidites.api import _format_locals

try:
    import readline
except ImportError:
    readline = None
histfile = Path('~/.woma_shell_history').expanduser()
histfile_size = 1000
START_PROMPT = '>>> '
CONTINUE_PROMPT = '... '


class Spinner:  # pragma: no cover
    busy = False
    delay = 0.25

    def __init__(self, delay=None, stdout=sys.stdout):
        self.spinner_generator = (i for i in cycle('|/-\\'))
        self.stdout = stdout
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            self.stdout.write(next(self.spinner_generator))
            self.stdout.flush()
            time.sleep(self.delay)
            self.stdout.write('\b')
            self.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False


single_arg_help = re.compile(r'(?:help[\(])(\w+)(?:[\)])')


class ReadEvalParse:  # pragma: no cover
    intro = "Welcome to the Woma Interactive Shell. Use the 'help()' or '?' command to see a list of commands.\nThis is experimental and mainly aims to help developers to sandbox " \
            "Woma without compilation."
    ruler = "┉"
    doc_leader = ""
    nohelp = "*** No help on %s"
    doc_header = "Documented commands (type help <topic>):"
    misc_header = "Miscellaneous help topics:"
    undoc_header = "Undocumented commands:"
    _globals = globals().copy()

    def __init__(self, stdout=None):
        if stdout is not None:
            self.stdout = stdout
        else:
            self.stdout = sys.stdout
        self.warn = lambda x: sys.stderr.write(x) and sys.stderr.flush()
        self.__locals__ = dict(locals(), **globals())

    def input(self):
        self.stdout.flush()

        line = input(START_PROMPT)
        if ';' in line:
            line = line.replace(';', '\n    ')
            self.stdout.write(line + '\n')
            self.stdout.flush()
        return line

    def get_names(self):
        # This method used to pull in base class attributes
        # at a time dir() didn't do it yet.
        return dir(self.__class__)

    def find_token(self, token: str, text: str) -> bool:
        return text.find(token) != -1

    def displayhook(self, text):
        if text is None:
            return
        try:
            self.stdout.write(str(text))
        except UnicodeEncodeError:
            bytes = text.encode(sys.stdout.encoding, 'backslashreplace')
            if hasattr(self.stdout, 'buffer'):
                self.stdout.buffer.write(bytes)
            else:
                text = bytes.decode(sys.stdout.encoding, 'strict')
                self.stdout.write(text)
        self.stdout.write("\n")

    def eval_exec(self, x: Union[List, AnyStr]):
        # noinspection PyBroadException
        if isinstance(x, ParseResults):
            x = x[0]
        # noinspection PyBroadException
        warnings.resetwarnings()
        try:
            out = eval(compile(x, filename='<inline code>', mode='eval'),
                       self.__locals__,
                       self.__locals__)
        except Exception:
            out = exec(compile(x, filename='<inline code>', mode='exec'), self.__locals__, self.__locals__)
            self.stdout.write('\n')
            # if out is not None:
            #     print(out)
        self.displayhook(out)

    def preloop(self):
        if readline and Path(histfile).exists():
            readline.read_history_file(histfile)

    def postloop(self):
        if readline:
            readline.set_history_length(histfile_size)
            readline.write_history_file(histfile)

    def loop(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        self.stdout.write(self.intro + '\n')
        try:
            while True:
                self.postloop()
                self.preloop()
                try:
                    line = self.input()
                    if line == '':
                        continue
                    if line == 'exit()':
                        raise SystemExit
                    if self.find_token('?', line):
                        self.do_help(line.lstrip('? '))
                        continue
                    if self.find_token('help ', line):
                        self.do_help(line.split(' ')[1])
                        continue
                    if single_arg_help.match(line):
                        self.do_help(single_arg_help.search(line).group(1))
                        continue
                    if hasattr(self, 'do_' + line):
                        getattr(self, 'do_' + line)()
                        continue
                    if str(line).isidentifier():
                        self.eval_exec(line)
                        continue
                    try:
                        with Spinner():
                            p = Aspidites.parser.parser.parse_module(line)
                    except ParseException:
                        self.warn(f'Warning: Failed to parse "{line}" as Woma.\n'
                              f'Remember that Woma does not allow literal evaluation, try assigning to a variable.\n'
                              f'Falling back to python with suppressed exceptions.\n')
                        with suppress(Exception):
                            self.eval_exec(line)
                        continue
                    else:
                        self.eval_exec(p)
                        continue

                except Exception as e:
                    self.stdout.write(f"Error: {e}\n")
                    continue
        except KeyboardInterrupt as e:
            self.do_exit()

    def do_exit(self, arg=None):
        """Exit the woma interactive interpreter."""
        self.stdout.write("\nExiting...")
        raise SystemExit

    def do_copyright(self):
        """Copyright Ross J. Duff 2021 licensed under the GNU Public License v3."""
        pass

    def do_locals(self, arg=None):
        """Print local variables"""
        hidden = ['self', 'stdout', 'ReadEvalParse', '__warningregistry__']
        visible = dict()
        for k, v in self.__locals__.items():
            if k in self._globals.keys() or k in hidden:
                continue
            else:
                visible[k] = v

        self.stdout.write(_format_locals(visible).decode('UTF-8'))

    def do_flush(self):
        """forcibly flush stdout"""
        self.stdout.flush()

    def do_help(self, arg=None):
        """List available commands with "help" or detailed help with "help cmd"."""
        if arg:
            # XXX check arg syntax
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc = getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.stdout.write("%s\n" % str(doc))
                        return
                except AttributeError:
                    pass
                self.stdout.write("%s\n" % str(self.nohelp % (arg,)))
                return
            func()
        else:
            names = self.get_names()
            cmds_doc = []
            cmds_undoc = []
            help = {}
            for name in names:
                if name[:5] == 'help_':
                    help[name[5:]] = 1
            names.sort()
            # There can be duplicates if routines overridden
            prevname = ''
            for name in names:
                if name[:3] == 'do_':
                    if name == prevname:
                        continue
                    prevname = name
                    cmd = name[3:]
                    if cmd in help:
                        cmds_doc.append(cmd)
                        del help[cmd]
                    elif getattr(self, name).__doc__:
                        cmds_doc.append(cmd)
                    else:
                        cmds_undoc.append(cmd)
            self.stdout.write("%s\n" % str(self.doc_leader))
            self.print_topics(self.doc_header, cmds_doc, 15, 80)
            self.print_topics(self.misc_header, list(help.keys()), 15, 80)
            self.print_topics(self.undoc_header, cmds_undoc, 15, 80)

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            self.stdout.write("%s\n" % str(header))
            if self.ruler:
                self.stdout.write("╭%s╮\n" % str(self.ruler * len(header)))
            self.columnize(cmds, maxcol - 1)
            self.stdout.write("\n")

    def columnize(self, list, displaywidth=80):
        """Display a list of strings as a compact set of columns.

        Each column is only as wide as necessary.
        Columns are separated by two spaces (one was not legible enough).
        """
        if not list:
            self.stdout.write("<empty>\n")
            return

        nonstrings = [i for i in range(len(list))
                      if not isinstance(list[i], str)]
        if nonstrings:
            raise TypeError("list[i] not a string for i in %s"
                            % ", ".join(map(str, nonstrings)))
        size = len(list)
        if size == 1:
            self.stdout.write(' %s\n' % str(list[0]))
            return
        # Try every row count from 1 upwards
        for nrows in range(1, len(list)):
            ncols = (size + nrows - 1) // nrows
            colwidths = []
            totwidth = -2
            for col in range(ncols):
                colwidth = 0
                for row in range(nrows):
                    i = row + nrows * col
                    if i >= size:
                        break
                    x = list[i]
                    colwidth = max(colwidth, len(x))
                colwidths.append(colwidth)
                totwidth += colwidth + 2
                if totwidth > displaywidth:
                    break
            if totwidth <= displaywidth:
                break
        else:
            nrows = len(list)
            ncols = 1
            colwidths = [0]
        for row in range(nrows):
            texts = []
            for col in range(ncols):
                i = row + nrows * col
                if i >= size:
                    x = ""
                else:
                    x = list[i]
                texts.append(x)
            while texts and not texts[-1]:
                del texts[-1]
            for col in range(len(texts)):
                texts[col] = texts[col].ljust(colwidths[col])
            self.stdout.write(" %s\n" % str("  ".join(texts)))


if __name__ == "__main__":
    rep = ReadEvalParse()
    rep.loop()
