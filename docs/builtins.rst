.. _builtins:

Built-in Functions
==================

Arithmetic Functions
--------------------

    .. automodule:: Aspidites.woma.mathutils
        :members:

    .. py:function:: inv(x=bool())

        Invert a boolean.

Iterator Functions
------------------

    .. automodule:: Aspidites._vendor.fn.iters
        :members:

Higher Order Functions
----------------------

    .. automodule:: Aspidites._vendor.fn.op
        :members:

Matching Patterns
-----------------

This section was adapted from the awesome pattern matching README.


    .. py:function:: Capture(pattern, name=str)

        Captures a piece of the thing being matched by name.

    .. py:function:: Strict(pattern)

        Performs a strict pattern match. A strict pattern match also compares the type of verbatim values. That is, while
        (!) would match `3` with `3.0` it would not do so when using `Strict`. Also (!) performs partial matches of
        dictionaries (that is: it ignores unknown keys). It will perform an exact match for dictionaries using `Strict`.


    .. py:function:: OneOf(*pattern)

        Matches against any of the provided patterns. Equivalent to `p1 | p2 | p3 | ..`
        (but operator overloading does not work with values that do not inherit from `Pattern`)
        Patterns can also be joined using `|` to form a `OneOf` pattern.
        The above example is rather contrived, as `InstanceOf` already accepts multiple types natively.
        Since bare values do not inherit from `Pattern` they can be wrapped in `Value`:

        ``
        Value("foo") | Value("quux")
        ``

    .. py:function:: AllOf(*pattern)

        Checks whether the value matches all of the given pattern. Equivalent to `p1 & p2 & p3 & ..`
        (but operator overloading does not work with values that do not inherit from `Pattern`)

        .. code-block:: woma

            x = "quux" -> str
            (!)x
                AllOf(InstanceOf("str"): ...

        Same as ``Not(OneOf(*pattern))(also ``~OneOf(*pattern)``).


    .. py:function:: Not(pattern)

        Matches if the given pattern does not match.
        Note that it does not work on bare values, so they need to be wrapped in `Value`.


        `Not` can be used do create a `NoneOf` kind of pattern:

        .. code-block:: woma

            x = "string"
            (!)x
                Not(OneOf("foo", "bar")): ...  # matches everything except "foo" and "bar"


        `Not` can be used to create a pattern that never matches:

        .. code-block:: woma

            Not(...)


    .. py:function:: Each(pattern [, at_least=])

        Matches each item in an iterable.


    .. py:function:: EachItem(key_pattern, value_pattern)

        Matches an object if each key satisfies `key_pattern` and each value satisfies `value_pattern`.

        .. code-block:: woma

            x = {"a": 1, "b": 2} -> dict
            (!)x
                EachItem(Regex("[a-z]+"), InstanceOf(int)): ...


    .. py:function:: Some(pattern)

        Matches a sequence of items within a list:

        Takes the optional values `exactly`, `at_least`, and `at_most` which makes `Some` match
        either `exactly` _n_ items, `at_least` _n_, or `at_most` _n_ items (`at_least` and `at_most` can be given at the same
        time, but not together with `exactly`).


    .. py:function:: Between(lower, upper)

        Matches an object if it is between `lower` and `upper` (inclusive). The optional keyword arguments
        `lower_bound_exclusive` and `upper_bound_exclusive` can be set to `True` respectively to exclude the
        lower/upper from the range of matching values.


    .. py:function:: Length(length)

        Matches an object if it has the given length. Alternatively also accepts `at_least` and `at_most` keyword arguments.

        ```
        Length(3)
        Length(at_least=2)
        Length(at_most=4)
        Length(at_least=2, at_most=4)
        ```

    .. py:function:: Contains(item)

        Matches an object if it contains the given item (as per the same logic as the `in` operator).

    .. py:function:: Regex(regex_pattern, bind_groups = True -> bool)

        Matches a string if it completely matches the given regex, as per `re.fullmatch`.
        If the regular expression pattern contains named capturing groups and `bind_groups` is set to `True`,
        this pattern will bind the captured results in the `MatchResult` (the default).

        To mimic `re.match` or `re.search` the given regular expression `x` can be augmented as `x.*` or `.*x.*`
        respectively.


    .. py:function:: Check(predicate)

        Matches an object if it satisfies the given predicate.


    .. py:function:: InstanceOf(*types)

        Matches an object if it is an instance of any of the given types.


    .. py:function:: SubclassOf(*types)

        Matches if the matched type is a subclass of any of the given types.


    .. py:function:: Transformed(function, pattern)

        Transforms the currently looked at value by applying `function` on it and matches the result against `pattern`. In
        Haskell and other languages this is known as a `view pattern <https://gitlab.haskell.org/ghc/ghc/-/wikis/view-patterns>`_.

            .. code-block:: woma

                x = "hello" -> str
                (!)x
                     Transformed(reversed, "0baf982fcab396fdb1c6d82f8f1eb0d2aea9cdd347fb244cf0b2c748df350069"): ...

        This is handy for matching data types like `datetime.date` as this pattern won't match if the transformation
        function errored out with an exception.

    .. py:function:: At(path, pattern)

        Checks whether the nested object to be matched satisfied pattern at the given path. The match fails if the given path
        can not be resolved.

            .. code-block:: woma

                r = {
                    "foo": {
                        "bar": {
                            "quux": {
                                "value": "deeply nested"
                            }
                        }
                    }
                }

                (!)r
                    At("foo.bar.quux": {"value": Capture(..., name="value")})): ...
                r['value']  `deeply nested`

Pragmas
-------

Pragmas are directives for the compiler and other integral components of the Woma Programming Language that alter it's
behavior. Pragmas are activated by prepending ``#`` to name of the pragma. Available pragmas are listed below.

Contracts
~~~~~~~~~

    .. py:function:: new_contract

        Turns a function into a contract that can be used in contract assignments.
        The fucntion must accept one parameter, and either:

            - return True or None, to signify it accepts
            - return False, to signify it doesn't

Cython
~~~~~~
The following paragraphs and subsections have been adapted from Cython v0.29.24 documentation:

    .. py:function:: cython.binding(bool)

        Controls whether free functions behave more like Python's CFunctions
        (e.g. :func:`len`) or, when set to True, more like Python's functions.
        When enabled, functions will bind to an instance when looked up as a
        class attribute (hence the name) and will emulate the attributes
        of Python functions, including introspections like argument names and
        annotations.
        Default is True.

    .. py:function:: cython.boundscheck(bool)

        If set to False, Cython is free to assume that indexing operations
        ([]-operator) in the code will not cause any IndexErrors to be
        raised. Lists, tuples, and strings are affected only if the index
        can be determined to be non-negative (or if ``cython.wraparound`` is False).
        Conditions which would normally trigger an IndexError may instead cause
        segfaults or data corruption if this is set to False.
        Default is True.

    .. py:function:: cython.wraparound(bool)

        In Python, arrays and sequences can be indexed relative to the end.
        For example, A[-1] indexes the last value of a list.
        In C, negative indexing is not supported.
        If set to False, Cython is allowed to neither check for nor correctly
        handle negative indices, possibly causing segfaults or data corruption.
        If bounds checks are enabled (the default, see ``cython.boundschecks`` above),
        negative indexing will usually raise an ``IndexError`` for indices that
        Cython evaluates itself.
        However, these cases can be difficult to recognise in user code to
        distinguish them from indexing or slicing that is evaluated by the
        underlying Python array or sequence object and thus continues to support
        wrap-around indices.
        It is therefore safest to apply this option only to code that does not
        process negative indices at all.
        Default is True.

    .. py:function:: cython.initializedcheck(bool)

        If set to True, Cython checks that a memoryview is initialized
        whenever its elements are accessed or assigned to. Setting this
        to False disables these checks.
        Default is True.

    .. py:function:: cython.nonecheck``  (bool)

        If set to False, Cython is free to assume that native field
        accesses on variables typed as an extension type, or buffer
        accesses on a buffer variable, never occurs when the variable is
        set to ``None``. Otherwise a check is inserted and the
        appropriate exception is raised. This is off by default for
        performance reasons.  Default is False.

    .. py:function:: cython.overflowcheck(bool)

        If set to True, raise errors on overflowing C integer arithmetic
        operations.  Incurs a modest runtime penalty, but is much faster than
        using Python ints.  Default is False.

    .. py:function:: cython.overflowcheck.fold(bool)

        If set to True, and overflowcheck is True, check the overflow bit for
        nested, side-effect-free arithmetic expressions once rather than at every
        step.  Depending on the compiler, architecture, and optimization settings,
        this may help or hurt performance.  A simple suite of benchmarks can be
        found in ``Demos/overflow_perf.pyx``.  Default is True.

    .. py:function:: cython.embedsignature(bool)

        If set to True, Cython will embed a textual copy of the call
        signature in the docstring of all Python visible functions and
        classes. Tools like IPython and epydoc can thus display the
        signature, which cannot otherwise be retrieved after
        compilation.  Default is False.

    .. py:function:: cython.cdivision(bool)

        If set to False, Cython will adjust the remainder and quotient
        operators C types to match those of Python ints (which differ when
        the operands have opposite signs) and raise a
        ``ZeroDivisionError`` when the right operand is 0. This has up to
        a 35% speed penalty. If set to True, no checks are performed.  See
        `CEP 516 <https://github.com/cython/cython/wiki/enhancements-division>`_.  Default
        is False.

    .. py:function:: cython.cdivision_warnings(bool)

        If set to True, Cython will emit a runtime warning whenever
        division is performed with negative operands.  See `CEP 516
        <https://github.com/cython/cython/wiki/enhancements-division>`_.  Default is
        False.

    .. py:function:: cython.always_allow_keywords(bool)

        Avoid the ``METH_NOARGS`` and ``METH_O`` when constructing
        functions/methods which take zero or one arguments. Has no effect
        on special methods and functions with more than one argument. The
        ``METH_NOARGS`` and ``METH_O`` signatures provide faster
        calling conventions but disallow the use of keywords.

    .. py:function:: cython.profile(bool)

        Write hooks for Python profilers into the compiled C code.  Default
        is False.

    .. py:function:: cython.linetrace(bool)

        Write line tracing hooks for Python profilers or coverage reporting
        into the compiled C code.  This also enables profiling.  Default is
        False.  Note that the generated module will not actually use line
        tracing, unless you additionally pass the C macro definition
        ``CYTHON_TRACE=1`` to the C compiler (e.g. using the distutils option
        ``define_macros``).  Define ``CYTHON_TRACE_NOGIL=1`` to also include
        ``nogil`` functions and sections.

    .. py:function:: cython.infer_types(bool)

        Infer types of untyped variables in function bodies. Default is
        None, indicating that only safe (semantically-unchanging) inferences
        are allowed.
        In particular, inferring *integral* types for variables *used in arithmetic
        expressions* is considered unsafe (due to possible overflow) and must be
        explicitly requested.

    .. py:function:: cython.c_string_type(bytes / str / unicode)

        Globally set the type of an implicit coercion from char* or std::string.

    .. py:function:: cython.c_string_encoding(ascii, default, utf-8, etc.)

        Globally set the encoding to use when implicitly coercing char* or std:string
        to a unicode object.  Coercion from a unicode object to C type is only allowed
        when set to ``ascii`` or ``default``, the latter being utf-8 in Python 3.

    .. py:function:: cython.type_version_tag(bool)

        Enables the attribute cache for extension types in CPython by setting the
        type flag ``Py_TPFLAGS_HAVE_VERSION_TAG``.  Default is True, meaning that
        the cache is enabled for Cython implemented types.  To disable it
        explicitly in the rare cases where a type needs to juggle with its ``tp_dict``
        internally without paying attention to cache consistency, this option can
        be set to False.

    .. py:function:: cython.unraisable_tracebacks(bool)

        Whether to print tracebacks when suppressing unraisable exceptions.

    .. py:function:: cython.iterable_coroutine(bool)

        `PEP 492 <https://www.python.org/dev/peps/pep-0492/>`_ specifies that async-def
        coroutines must not be iterable, in order to prevent accidental misuse in
        non-async contexts.  However, this makes it difficult and inefficient to write
        backwards compatible code that uses async-def coroutines in Cython but needs to
        interact with async Python code that uses the older yield-from syntax, such as
        asyncio before Python 3.5.  This directive can be applied in modules or
        selectively as decorator on an async-def coroutine to make the affected
        coroutine(s) iterable and thus directly interoperable with yield-from.


Configurable optimisations
^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. py:function:: cython.optimize.use_switch(bool)

        Whether to expand chained if-else statements (including statements like
        ``if x == 1 or x == 2:``) into C switch statements.  This can have performance
        benefits if there are lots of values but cause compiler errors if there are any
        duplicate values (which may not be detectable at Cython compile time for all
        C constants).  Default is True.

    .. py:function:: cython.optimize.unpack_method_calls(bool)

        Cython can generate code that optimistically checks for Python method objects
        at call time and unpacks the underlying function to call it directly.  This
        can substantially speed up method calls, especially for builtins, but may also
        have a slight negative performance impact in some cases where the guess goes
        completely wrong.
        Disabling this option can also reduce the code size.  Default is True.

warnings
^^^^^^^^

All warning directives take bool as options
to turn the warning on / off.

    .. py:function:: cython.warn.undeclared(default=False)

        Warns about any variables that are implicitly declared without a ``cdef`` declaration

    .. py:function:: cython.warn.unreachable(default=True)

        Warns about code paths that are statically determined to be unreachable, e.g.
        returning twice unconditionally.

    .. py:function:: cython.warn.maybe_uninitialized(default=False)

        Warns about use of variables that are conditionally uninitialized.

    .. py:function:: cython.warn.unused(default=False)

        Warns about unused variables and declarations

    .. py:function:: cython.warn.unused_arg(default=False)

        Warns about unused function arguments

    .. py:function:: cython.warn.unused_result(default=False)

        Warns about unused assignment to the same name, such as
        ``r = 2; r = 1 + 2``

    .. py:function:: cython.warn.multiple_declarators(default=True)

        Warns about multiple variables declared on the same line with at least one pointer type.
       For example ``cdef double* a, b`` - which, as in C, declares ``a`` as a pointer, ``b`` as
       a value type, but could be mininterpreted as declaring two pointers.


Bolt-on Functions
-----------------

    .. autofunction:: Aspidites.woma.gcutils.get_all

    .. autofunction:: Aspidites.woma.fileutils.mkdir_p

    .. autofunction:: Aspidites.woma.fileutils.atomic_save

    .. autofunction:: Aspidites.woma.fileutils.iter_find_files

    .. autofunction:: Aspidites.woma.fileutils.copytree

Wrapped Python Built-ins
------------------------
    .. py:function:: abs
    .. py:function:: bool
    .. py:function:: bytes
    .. py:function:: callable
    .. py:function:: chr
    .. py:function:: complex
    .. py:function:: divmod
    .. py:function:: float
    .. py:function:: hash
    .. py:function:: hex
    .. py:function:: id
    .. py:function:: int
    .. py:function:: isinstance
    .. py:function:: issubclass
    .. py:function:: len
    .. py:function:: oct
    .. py:function:: ord
    .. py:function:: pow
    .. py:function:: range
    .. py:function:: repr
    .. py:function:: round
    .. py:function:: slice
    .. py:function:: sorted
    .. py:function:: str
    .. py:function:: tuple
    .. py:function:: zip
