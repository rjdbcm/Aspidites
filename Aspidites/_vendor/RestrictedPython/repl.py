import sys
from traceback import print_exc
from typing import List, AnyStr, Union

from Aspidites._vendor.pyparsing import ParseException, ParseResults
import Aspidites.parser.parser
import compile
import Guards
START_PROMPT = '>>> '
CONTINUE_PROMPT = '... '
globals().update(Guards.safe_globals)


class ReadEvalParse:
    ruler = "┉"
    doc_leader = ""
    nohelp = "*** No help on %s"
    doc_header = "Documented commands (type help <topic>):"
    misc_header = "Miscellaneous help topics:"
    undoc_header = "Undocumented commands:"

    def __init__(self, stdout=None):
        if stdout is not None:
            self.stdout = stdout
        else:
            self.stdout = sys.stdout

        self.__locals__ = dict(locals(), **globals())

    def get_names(self):
        # This method used to pull in base class attributes
        # at a time dir() didn't do it yet.
        return dir(self.__class__)

    def find_token(self, token: str, text: str) -> bool:
        return text.find(token) != -1

    def eval_exec(self, x: Union[List, AnyStr]):
        # noinspection PyBroadException
        if isinstance(x, ParseResults):
            x = x[0]
        try:
            print(eval(compile.compile_restricted(x, filename='<inline code>', mode='eval')),
                  self.__locals__,
                  self.__locals__)
        except:
            out = exec(
                compile.compile_restricted(x, filename='<inline code>', mode='exec'),
                self.__locals__,
                self.__locals__
            )
            if out is not None:
                print(out)

    def loop(self) -> None:
        try:
            while True:
                try:
                    _in = input(START_PROMPT)
                    if _in == 'exit()':
                        raise SystemExit
                    elif self.find_token('?', _in):
                        self.do_help(_in.lstrip('? '))
                        continue
                    elif self.find_token('help ', _in):
                        self.do_help(_in.split(' ')[1])
                    elif _in == 'help()':
                        self.do_help()
                        continue
                    elif self.find_token('print,', _in):
                        print('Printing is not available in the Woma Interactive Shell.')
                        continue

                    p = Aspidites.parser.parser.parse_module(_in)
                    self.eval_exec(p)

                except Exception as e:
                    print(f"Error: {e}")
                    print_exc()
                    continue
        except KeyboardInterrupt as e:
            print("\nExiting...")
            self.do_exit()

    def do_exit(self, arg=None):
        'Exit the woma interactive interpreter.'
        raise SystemExit

    def do_copyright(self):
        """Copyright Ross J. Duff 2021 licensed under the GNU Public License v3."""
        pass

    def do_help(self, arg=None):
        'List available commands with "help" or detailed help with "help cmd".'
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

