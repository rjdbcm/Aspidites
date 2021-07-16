# contents of app_main.py
import os
import sys
import argparse as ap
import pytest_cov
from functools import partial
from Cython import __version__ as cy_version
from Cython.Compiler import Options
import pytest_mypy
import pytest_mock
import pytest_sugar
import pytest_pylint
from semantic_version import Version
from Aspidites.parser import parse_module
from Aspidites.compiler import compile_module
from Aspidites.features.pampy import match

cy_version = Version.coerce(cy_version)


def main():
    if cy_version.major == 3:
        from Cython.Compiler.CmdLine import create_cython_argparser
        cy_parser = create_cython_argparser()
    else:
        cy_parser = ap.ArgumentParser(add_help=False)

    if len(sys.argv) > 1 and sys.argv[1] == "--pytest" or sys.argv[1] == '-t':
        import pytest
        sys.exit(
            pytest.main(sys.argv[2:], plugins=[pytest_pylint, pytest_mock, pytest_cov]))
    else:
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

        def add_pre_cy3_args(parser):
            cy_arg_group = parser.add_argument_group("optional Cython arguments")
            for k, v in cy_kwargs.items():
                cy_arg_group.add_argument(
                        f'--{k.replace("_", "-")}',
                        default=v,
                        action='store_true' if type(v) == bool else 'store'
                )

        asp_parser = ap.ArgumentParser(description=__doc__,
                                       formatter_class=ap.RawDescriptionHelpFormatter,
                                       parents=[cy_parser],
                                       add_help=not bool(cy_version.major)
                                       )
        asp_parser.add_argument('-pt', '--pytest',
                                help="run pytest with options", metavar='pytest args')
        asp_parser.add_argument("target",
                                help="source to compile")
        # Compatible with Cython 0.X:
        # 3.0 switched to using the argparse module
        if cy_version.major == 0:
            asp_parser.add_argument('-o', '--output')
            asp_parser.add_argument("-p", "--compile-pyc", action="store_true",
                                    help="compile to python bytecode")
            asp_parser.add_argument('-c', '--compile-c', action="store_true",
                                    help="compile to C")
            asp_parser.add_argument('-v', "--verbose",
                                    default=0,
                                    action='count',
                                    help="increase output verbosity (default: %(default)s)")
            add_pre_cy3_args(asp_parser)
            args, other_args = asp_parser.parse_known_args()
            for k in cy_kwargs.keys():
                cy_kwargs[k] = args.__getattribute__(k)
        else:
            args = asp_parser.parse_args()

        if args.verbose >= 2:
            print(asp_parser.__repr__())
        with open(args.target, 'r') as t:
            code = parse_module(t.read())
            compile_module(code, fname=args.output, bytecode=args.compile_pyc,
                           c=args.compile_c, verbose=args.verbose, **cy_kwargs)


if __name__ == '__main__':
    main()
