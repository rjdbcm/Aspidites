# contents of app_main.py
import argparse as ap
import os
import sys
import traceback
import warnings
import typing as t
from contextlib import suppress

from Cython import __version__ as cy_version
from Cython.Compiler import Options
from pyrsistent import pmap, v, PMap

import pytest

from ._vendor.semantic_version import Version
from .compiler import compile_module
from .parser import parse_module
from . import __description__

cy_version = Version.coerce(cy_version)


def get_cy_kwargs() -> dict:
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


def get_cython_parser(dummy: ap.ArgumentParser) -> t.Tuple[ap.ArgumentParser, dict, ap.ArgumentParser, bool]:
    cy3_fallback_mode: bool = False
    cy_kwargs = get_cy_kwargs()
    if cy_version.major == 3:  # pragma: no cover
        try:
            from Cython.Compiler.CmdLine import create_cython_argparser
            cy_parser = create_cython_argparser()
        except Exception as e:
            warnings.warn(
                '\n' + ''.join(traceback.format_tb(
                    e.__traceback__)) + 'Falling back to Cython 0.X Options API',
                ImportWarning)
            cy3_fallback_mode = True
            cy_parser = dummy
    else:
        cy_parser = dummy
    return dummy, cy_kwargs, cy_parser, cy3_fallback_mode


def parse_from_dummy(argv: list,
                     dummy: ap.ArgumentParser,
                     __test: bool = False) -> t.Tuple[ap.Namespace, list, dict]:
    dummy, cy_kwargs, cy_parser, cy3_fallback_mode = get_cython_parser(dummy)
    if len(argv) == 1:
        if not __test:  # pragma: no cover
            print("%s called without arguments. Next time try --help or -h." % argv[0])
        sys.exit(1)
    if len(argv) >= 2 and argv[1] == "--pytest" or argv[1] == '-pt':  # pragma: no cover
        if not os.getenv("ASPIDITES_DOCKER_BUILD"):
            argv = [os.path.dirname(os.path.realpath(__file__)) + '/tests'] + argv[2:]
        else:
            argv = argv[2:]
        sys.exit(pytest.main(argv))

    def add_pre_cy3_args(parser: ap.ArgumentParser) -> None:  # pragma: no cover
        cy_arg_group = parser.add_argument_group("optional cython arguments")
        for k, v in cy_kwargs.items():
            cy_arg_group.add_argument(
                f'--{k.replace("_", "-")}',
                default=v,
                action='store_true' if isinstance(v, (bool,)) else 'store'
            )

    asp_parser = ap.ArgumentParser(prog='aspidites',
                                   description=__description__,
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
                                help='filename to compile to'),
        asp_parser.add_argument('-f', '--force', action='store_true',
                                help='forcibly overwrite existing files')
        asp_parser.add_argument("-p", "--compile-pyc", action="store_true",
                                help="compile to python bytecode")
        asp_parser.add_argument('-c', '--compile-c', action="store_true",
                                help="compile to C and run setup")
        asp_parser.add_argument('--build-requires', default='', metavar='',
                                help='additional requirements needed to run setup (default: %(default)s)')
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
    return args, other_args, cy_kwargs


def main(argv=sys.argv) -> None:
    # any failure results in falling back to the `Cython.Compiler.Options` API
    args, other_args, cy_kwargs = parse_from_dummy(argv,
                                                   ap.ArgumentParser(add_help=False))
    if args.target == "Aspidites/tests":
        raise SystemExit()
    code = parse_module(open(args.target, 'r').read())
    if args.output is None:
        args.output = os.path.join(os.path.dirname(args.target), 'compiled.py')

    cy_kwargs.update({
        'code': code,
        'fname': args.output or "compiled.py",
        'force': args.force or False,
        'bytecode': args.compile_pyc,
        'c': args.compile_c,
        'build_requires': args.build_requires,
        'verbose': args.verbose
    })
    compile_module(**cy_kwargs)
