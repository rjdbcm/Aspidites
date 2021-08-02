# contents of app_main.py
import argparse as ap
import os
import sys
import traceback
import warnings
from contextlib import suppress

import pyparsing
from Cython import __version__ as cy_version
from Cython.Compiler import Options
from pyparsing import ParseBaseException

with suppress(ImportError):
    import pytest_cov
    import pytest_mock
    import pytest_pylint

from Aspidites._vendor.RestrictedPython import safe_globals
from Aspidites._vendor.semantic_version import Version
from Aspidites.compiler import compile_module
from Aspidites.parser import parse_module

cy_version = Version.coerce(cy_version)

cy_kwargs = {
            "annotate"              : Options.annotate,
            "annotate_coverage_xml" : Options.annotate_coverage_xml,
            "buffer_max_dims"       : Options.buffer_max_dims,
            "cache_builtins"        : Options.cache_builtins,
            "cimport_from_pyx"      : Options.cimport_from_pyx,
            "clear_to_none"         : Options.clear_to_none,
            "closure_freelist_size" : Options.closure_freelist_size,
            "convert_range"         : Options.convert_range,
            "docstrings"            : Options.docstrings,
            "embed_pos_in_docstring": Options.embed_pos_in_docstring,
            "generate_cleanup_code" : Options.generate_cleanup_code,
            "fast_fail"             : Options.fast_fail,
            "warning_errors"        : Options.warning_errors,
            "error_on_unknown_names": Options.error_on_unknown_names,
            "error_on_uninitialized": Options.error_on_uninitialized,
            "gcc_branch_hints"      : Options.gcc_branch_hints,
            "lookup_module_cpdef"   : Options.lookup_module_cpdef,
            "embed"                 : Options.embed
        }


def main():
    # any failure results in falling back to the `Cython.Compiler.Options` API
    cy3_fallback_mode: bool = False
    dummy = ap.ArgumentParser(add_help=False)
    if cy_version.major == 3:
        try:
            from Cython.Compiler.CmdLine import create_cython_argparser
            cy_parser = create_cython_argparser()
        except Exception as e:
            warnings.warn('\n' + ''.join(traceback.format_tb(e.__traceback__)) + 'Falling back to Cython 0.X Options API', ImportWarning)
            cy3_fallback_mode = True
            cy_parser = dummy
    else:
        cy_parser = dummy
    if len(sys.argv) == 1:
        print("%s called without arguments. Next time try --help or -h." % sys.argv[0])
        exit(1)
    if len(sys.argv) > 1 and sys.argv[1] == "--pytest" or sys.argv[1] == '-pt':
        with suppress(ImportError):
            import pytest
            sys.exit(
                pytest.main(sys.argv[2:], plugins=[pytest_pylint, pytest_mock, pytest_cov]))
    else:
        def add_pre_cy3_args(parser):
            cy_arg_group = parser.add_argument_group("optional Cython arguments")
            for k, v in cy_kwargs.items():
                cy_arg_group.add_argument(
                        f'--{k.replace("_", "-")}',
                        default=v,
                        action='store_true' if type(v) == bool else 'store'
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
        with open(args.target, 'r') as t:
            code = parse_module(t.read())
            if args.output is None:
                args.output = os.path.join(os.path.dirname(args.target), 'compiled.py')
            compile_module(code,
                           fname=args.output,
                           force=args.force,
                           embed_python=args.embed_python,
                           bytecode=args.compile_pyc,
                           c=args.compile_c,
                           build_requires=args.build_requires,
                           verbose=args.verbose, *other_args, **cy_kwargs)

            # # reassign builtin collections contracts to check for pyrsistent version
            # new_contract('pmap', lambda x: isinstance(x, PMap))
            # new_contract('pvec', lambda x: isinstance(x, PVector))
            # new_contract('pset', lambda x: isinstance(x, PSet))
            # safe_globals.update(
            #         {'contract': contract, 'pvec': PVector, 'pmap': PMap, 'pset': PSet})

