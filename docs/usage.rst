Compiler Usage
~~~~~~~~~~~~~~

.. code-block:: text

    usage: aspidites [-h] [-pt ARGS] [-f] [-p] [-c] [--build-requires] [-v] [--annotate]
                 [--annotate-coverage-xml ANNOTATE_COVERAGE_XML]
                 [--buffer-max-dims BUFFER_MAX_DIMS] [--cache-builtins]
                 [--cimport-from-pyx] [--clear-to-none]
                 [--closure-freelist-size CLOSURE_FREELIST_SIZE] [--convert-range]
                 [--docstrings] [--embed-pos-in-docstring] [--generate-cleanup-code]
                 [--fast-fail] [--warning-errors] [--error-on-unknown-names]
                 [--error-on-uninitialized] [--gcc-branch-hints]
                 [--lookup-module-cpdef] [--embed EMBED]
                 target outpyx

    positional arguments:
      target                source to compile
      outpyx                filename to compile to

    options:
      -h, --help            show this help message and exit
      -pt ARGS, --pytest ARGS
                            run pytest with args
      -f, --force           forcibly overwrite existing files
      -p, --compile-pyc     compile to python bytecode
      -c, --compile-c       compile to C and run setup
      --build-requires      additional requirements needed to run setup (default: )
      -v, --verbose         increase output verbosity (default: 0) e.g. -v, -vv, -vvv

    optional cython arguments:
      --annotate
      --annotate-coverage-xml ANNOTATE_COVERAGE_XML
      --buffer-max-dims BUFFER_MAX_DIMS
      --cache-builtins
      --cimport-from-pyx
      --clear-to-none
      --closure-freelist-size CLOSURE_FREELIST_SIZE
      --convert-range
      --docstrings
      --embed-pos-in-docstring
      --generate-cleanup-code
      --fast-fail
      --warning-errors
      --error-on-unknown-names
      --error-on-uninitialized
      --gcc-branch-hints
      --lookup-module-cpdef
      --embed EMBED


