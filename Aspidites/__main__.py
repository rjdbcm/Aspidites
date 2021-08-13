# contents of app_main.py
import argparse as ap
import os
import sys
import traceback
import warnings
from contextlib import suppress

from Cython import __version__ as cy_version
from Cython.Compiler import Options
from pyrsistent import pmap, v, PMap

with suppress(ImportError):
    import pytest
    import pytest_cov
    import pytest_mock
    import pytest_pylint

from ._vendor.semantic_version import Version
from .compiler import compile_module
from .parser import parse_module

cy_version = Version.coerce(cy_version)

def get_cy_kwargs():
    cy_opt = v(
        "annotate",
        "annotate_coverage_xml",
        "buffer_max_dims",
        "cache_builtins",
        "cimport_from_pyx",
        "clear_to_none",
        "closure_freelist_size",
        "convert_range",
        "docstrings",
        "embed_pos_in_docstring",
        "generate_cleanup_code",
        "fast_fail",
        "warning_errors",
        "error_on_unknown_names",
        "error_on_uninitialized",
        "gcc_branch_hints",
        "lookup_module_cpdef",
        "embed",
    )
    cy_kwargs = dict(
        zip(cy_opt,
            map(lambda x: getattr(Options, x), cy_opt)))
    return cy_kwargs

def main(argv=sys.argv):
    # any failure results in falling back to the `Cython.Compiler.Options` API
    cy3_fallback_mode: bool = False
    dummy = ap.ArgumentParser(add_help=False)
    cy_kwargs = get_cy_kwargs()
    if cy_version.major == 3: # pragma: no cover
        try:
            from Cython.Compiler.CmdLine import create_cython_argparser
            cy_parser = create_cython_argparser()
        except Exception as e:
            warnings.warn(
                '\n' + ''.join(traceback.format_tb(e.__traceback__)) + 'Falling back to Cython 0.X Options API',
                ImportWarning)
            cy3_fallback_mode = True
            cy_parser = dummy
    else:
        cy_parser = dummy
    if len(argv) == 1:
        print("%s called without arguments. Next time try --help or -h." % sys.argv[0])
        sys.exit(1)
    if len(argv) > 1 and argv[1] == "--pytest" or argv[1] == '-pt':
        with suppress(ImportError):
            sys.exit(
                pytest.main(argv[2:], plugins=[pytest_pylint, pytest_mock, pytest_cov]))

    def add_pre_cy3_args(parser: ap.ArgumentParser) -> None: # pragma: no cover
        cy_arg_group = parser.add_argument_group("optional Cython arguments")
        for k, v in cy_kwargs.items():
            cy_arg_group.add_argument(
                f'--{k.replace("_", "-")}',
                default=v,
                action='store_true' if isinstance(v, (bool,)) else 'store'
            )

    asp_parser = ap.ArgumentParser(description=__doc__,
                                   parents=[cy_parser],
                                   add_help=not bool(cy_version.major)
                                   )
    asp_parser.add_argument('-pt', '--pytest',
                            help="run pytest with args", metavar='ARGS')
    asp_parser.add_argument('-mp', '--mypy',
                            help="run mypy with args", metavar='ARGS')
    asp_parser.add_argument("target",
                            help="source to compile")
    # Compatible with Cython 0.X:
    # 3.0 switched to using the argparse module
    if cy_version.major == 0 or cy3_fallback_mode:
        asp_parser.add_argument('-o', '--output', metavar='PATH/TO/FILE',
                                help='filename to compile to')
        asp_parser.add_argument('-f', '--force', action='store_true',
                                help='forcibly overwrite existing files')
        asp_parser.add_argument("-p", "--compile-pyc", action="store_true",
                                help="compile to python bytecode")
        asp_parser.add_argument('-c', '--compile-c', action="store_true",
                                help="compile to C and execute setup")
        asp_parser.add_argument('--embed-python', action='store_true',
                                help='')
        asp_parser.add_argument('--build-requires', default='', metavar='',
                                help='additional requirements needed to execute setup (default: %(default)s)')
        asp_parser.add_argument('-v', "--verbose",
                                default=0,
                                action='count',
                                help="increase output verbosity (default: %(default)s) e.g. -v, -vv, -vvv ")
        add_pre_cy3_args(asp_parser)
        args, other_args = asp_parser.parse_known_args()
        for k in cy_kwargs.keys():
            cy_kwargs[k] = args.__getattribute__(k)
    else:
        args, other_args = asp_parser.parse_known_args()

    if args.verbose >= 2:
        print(asp_parser.__repr__())
    with open(args.target, 'r') as source:
        code = parse_module(source.read())
        if args.output is None:
            args.output = os.path.join(os.path.dirname(args.target), 'compiled.py')
        compile_module(code,
                       fname=args.output,
                       force=args.force,
                       embed_python=args.embed_python,
                       bytecode=args.compile_pyc,
                       c=args.compile_c,
                       build_requires=args.build_requires,
                       verbose=args.verbose,
                       *other_args,
                       **cy_kwargs)

