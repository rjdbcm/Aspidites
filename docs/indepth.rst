Woma In Depth
=============

Functions
~~~~~~~~~

.. code:: woma

    (Identity(x = \0 -> number, str)) number, str
        <*>x

Here we have defined a function called ``Identity`` that takes a single argument ``x`` that respects a contract with two
clauses in union ``number`` and ``str``. When called with a ``number`` or ``str`` argument this function will return the
argument ``x``. This is a pure function in the traditional sense and in the Womatic sense. In Woma, a pure function is a
function where any two contracts can be switched and the output remains unchanged for all inputs.

Data Model
~~~~~~~~~~

Types
-----
Woma comes with a standard set of built-in data types. Broadly, they can be categorized as numerics and collections.
These types can further be constrained by additional contract clauses.

Numerics
^^^^^^^^

- int
- float
- complex

Collections
^^^^^^^^^^^

- dict
- list
- string
- set
- tuple

Contract clauses
----------------
Contract clauses are used to specify the built-in data types.
Most commonly this takes the form of the ``and`` operator ``,`` e.g. ``int,>0,<5``.

In the case of collections we can also specify length and type:

- ``dict[length_contract](key_contract:value_contract)``
- ``list[length_contract](type_contract)``

Complex contracts can always be aliased to make them easier to handle.
e.g. the built-in ``number <- int|float|complex``

Contracts can also contain bound variables. This allows for an additional level of specificity when used with
the ``type`` operator:

.. code-block:: woma

    (func(l = [] -> list(type(t)))) type(t)
        <*>l[0]

Immutables
~~~~~~~~~~

All sequences, mappings, and sets are immutable and hashable. `Evolvers <https://github.com/tobgu/pyrsistent#evolvers>`_
are the only mechanism for changing items or elements in place. This is accomplished in woma by assigning a sequence,
map, or set with a trailing ellipsis ``...``


Ellipsis
~~~~~~~~

The ellipsis is a contextual shorthand for several assigment operations:
 - In calling a function a trailing ``...`` indicates that the function is to be invoked in a different scope.
 - In creating an immutable collection a trailing ``...`` indicates that the values can be evolved.
 - In making a ``coroutine`` respecting function a true coroutine at call time.

Trigrams
~~~~~~~~

Rather than keywords Woma makes use of three character symbols called trigrams. Two of the most basic are ``<*>`` and
``<^>``, meaning ``return`` and ``yield`` respectively.

**Table of Trigrams**

+------------+------------+--------------------+-----------------+
| Arity      | Trigram    | Meaning            | Associativity   |
+============+============+====================+=================+
| 0          |    ``<#>`` |    ``pass``        |   ``none``      |
+------------+------------+--------------------+-----------------+
| 0          |    ``<$>`` |  ``continue``      |   ``none``      |
+------------+------------+--------------------+-----------------+
| 0          |    ``<%>`` |  ``break``         |   ``none``      |
+------------+------------+--------------------+-----------------+
| 1          |    ``<*>`` |    ``return``      |   ``right``     |
+------------+------------+--------------------+-----------------+
| 1          |    ``<^>`` |    ``yield``       |   ``right``     |
+------------+------------+--------------------+-----------------+
| 2          |    ``<@>`` |    ``loop over``   |   ``both``      |
+------------+------------+--------------------+-----------------+

Operators
~~~~~~~~~

The operators in Woma are identical to their python counterparts. Their implementation is different in some cases to
avoid raising errors.

**Table of Operators**

+------------+------------+----------------+
| Arity      | Operator   | Associativity  |
+============+============+================+
| 1          |    ``+``   |    ``right``   |
+------------+------------+----------------+
| 1          |    ``-``   |    ``right``   |
+------------+------------+----------------+
| 1          |    ``!``   |    ``left``    |
+------------+------------+----------------+
| 2          |    ``+``   |    ``left``    |
+------------+------------+----------------+
| 2          |    ``-``   |    ``left``    |
+------------+------------+----------------+
| 2          |    ``*``   |    ``left``    |
+------------+------------+----------------+
| 2          |    ``/``   |    ``left``    |
+------------+------------+----------------+
| 2          |    ``**``  |    ``right``   |
+------------+------------+----------------+

Literals
~~~~~~~~

The only named literals defined currently are the booleans ``True`` & ``False`` and the nullity element ``nullit``.
Technically ``_``, the anonymous function generic, could also be considered a literal.

Nullity
~~~~~~~

Rather than raising an error Woma will always prefer to return ``Undefined``, the absorbing, or nullity, element.
Unlike NaN, where it is undefined but not equal to itself, all nullity elements are undefined but equal. Their identity,
likewise, is always the same. However, the conditions under which it was created can be cached into the nullit instance.
This is the case in the internal implementation of mathematical operations.

Pragmas
~~~~~~~

Pragmas are directives for the compiler and other integral components of the Woma Programming Language that alter it's
behavior. Pragmas are activated by prepending ``#`` to name of the pragma. Available pragmas are listed below.

Cython
------
The following paragraphs and subsections have been adapted from Cython v0.29.24 documentation:

``cython.binding`` (True / False)
    Controls whether free functions behave more like Python's CFunctions
    (e.g. :func:`len`) or, when set to True, more like Python's functions.
    When enabled, functions will bind to an instance when looked up as a
    class attribute (hence the name) and will emulate the attributes
    of Python functions, including introspections like argument names and
    annotations.
    Default is True.

``cython.boundscheck``  (True / False)
    If set to False, Cython is free to assume that indexing operations
    ([]-operator) in the code will not cause any IndexErrors to be
    raised. Lists, tuples, and strings are affected only if the index
    can be determined to be non-negative (or if ``cython.wraparound`` is False).
    Conditions which would normally trigger an IndexError may instead cause
    segfaults or data corruption if this is set to False.
    Default is True.

``cython.wraparound``  (True / False)
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

``cython.initializedcheck`` (True / False)
    If set to True, Cython checks that a memoryview is initialized
    whenever its elements are accessed or assigned to. Setting this
    to False disables these checks.
    Default is True.

``cython.nonecheck``  (True / False)
    If set to False, Cython is free to assume that native field
    accesses on variables typed as an extension type, or buffer
    accesses on a buffer variable, never occurs when the variable is
    set to ``None``. Otherwise a check is inserted and the
    appropriate exception is raised. This is off by default for
    performance reasons.  Default is False.

``cython.overflowcheck`` (True / False)
    If set to True, raise errors on overflowing C integer arithmetic
    operations.  Incurs a modest runtime penalty, but is much faster than
    using Python ints.  Default is False.

``cython.overflowcheck.fold`` (True / False)
    If set to True, and overflowcheck is True, check the overflow bit for
    nested, side-effect-free arithmetic expressions once rather than at every
    step.  Depending on the compiler, architecture, and optimization settings,
    this may help or hurt performance.  A simple suite of benchmarks can be
    found in ``Demos/overflow_perf.pyx``.  Default is True.

``cython.embedsignature`` (True / False)
    If set to True, Cython will embed a textual copy of the call
    signature in the docstring of all Python visible functions and
    classes. Tools like IPython and epydoc can thus display the
    signature, which cannot otherwise be retrieved after
    compilation.  Default is False.

``cython.cdivision`` (True / False)
    If set to False, Cython will adjust the remainder and quotient
    operators C types to match those of Python ints (which differ when
    the operands have opposite signs) and raise a
    ``ZeroDivisionError`` when the right operand is 0. This has up to
    a 35% speed penalty. If set to True, no checks are performed.  See
    `CEP 516 <https://github.com/cython/cython/wiki/enhancements-division>`_.  Default
    is False.

``cython.cdivision_warnings`` (True / False)
    If set to True, Cython will emit a runtime warning whenever
    division is performed with negative operands.  See `CEP 516
    <https://github.com/cython/cython/wiki/enhancements-division>`_.  Default is
    False.

``cython.always_allow_keywords`` (True / False)
    Avoid the ``METH_NOARGS`` and ``METH_O`` when constructing
    functions/methods which take zero or one arguments. Has no effect
    on special methods and functions with more than one argument. The
    ``METH_NOARGS`` and ``METH_O`` signatures provide faster
    calling conventions but disallow the use of keywords.

``cython.profile`` (True / False)
    Write hooks for Python profilers into the compiled C code.  Default
    is False.

``cython.linetrace`` (True / False)
    Write line tracing hooks for Python profilers or coverage reporting
    into the compiled C code.  This also enables profiling.  Default is
    False.  Note that the generated module will not actually use line
    tracing, unless you additionally pass the C macro definition
    ``CYTHON_TRACE=1`` to the C compiler (e.g. using the distutils option
    ``define_macros``).  Define ``CYTHON_TRACE_NOGIL=1`` to also include
    ``nogil`` functions and sections.

``cython.infer_types`` (True / False)
    Infer types of untyped variables in function bodies. Default is
    None, indicating that only safe (semantically-unchanging) inferences
    are allowed.
    In particular, inferring *integral* types for variables *used in arithmetic
    expressions* is considered unsafe (due to possible overflow) and must be
    explicitly requested.

``cython.c_string_type`` (bytes / str / unicode)
    Globally set the type of an implicit coercion from char* or std::string.

``cython.c_string_encoding`` (ascii, default, utf-8, etc.)
    Globally set the encoding to use when implicitly coercing char* or std:string
    to a unicode object.  Coercion from a unicode object to C type is only allowed
    when set to ``ascii`` or ``default``, the latter being utf-8 in Python 3.

``cython.type_version_tag`` (True / False)
    Enables the attribute cache for extension types in CPython by setting the
    type flag ``Py_TPFLAGS_HAVE_VERSION_TAG``.  Default is True, meaning that
    the cache is enabled for Cython implemented types.  To disable it
    explicitly in the rare cases where a type needs to juggle with its ``tp_dict``
    internally without paying attention to cache consistency, this option can
    be set to False.

``cython.unraisable_tracebacks`` (True / False)
    Whether to print tracebacks when suppressing unraisable exceptions.

``cython.iterable_coroutine`` (True / False)
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

``cython.optimize.use_switch`` (True / False)
    Whether to expand chained if-else statements (including statements like
    ``if x == 1 or x == 2:``) into C switch statements.  This can have performance
    benefits if there are lots of values but cause compiler errors if there are any
    duplicate values (which may not be detectable at Cython compile time for all
    C constants).  Default is True.

``cython.optimize.unpack_method_calls`` (True / False)
    Cython can generate code that optimistically checks for Python method objects
    at call time and unpacks the underlying function to call it directly.  This
    can substantially speed up method calls, especially for builtins, but may also
    have a slight negative performance impact in some cases where the guess goes
    completely wrong.
    Disabling this option can also reduce the code size.  Default is True.

warnings
^^^^^^^^

All warning directives take True / False as options
to turn the warning on / off.

``cython.warn.undeclared`` (default False)
    Warns about any variables that are implicitly declared without a ``cdef`` declaration

``cython.warn.unreachable`` (default True)
    Warns about code paths that are statically determined to be unreachable, e.g.
    returning twice unconditionally.

``cython.warn.maybe_uninitialized`` (default False)
    Warns about use of variables that are conditionally uninitialized.

``cython.warn.unused`` (default False)
    Warns about unused variables and declarations

``cython.warn.unused_arg`` (default False)
    Warns about unused function arguments

``cython.warn.unused_result`` (default False)
    Warns about unused assignment to the same name, such as
    ``r = 2; r = 1 + 2``

``cython.warn.multiple_declarators`` (default True)
   Warns about multiple variables declared on the same line with at least one pointer type.
   For example ``cdef double* a, b`` - which, as in C, declares ``a`` as a pointer, ``b`` as
   a value type, but could be mininterpreted as declaring two pointers.