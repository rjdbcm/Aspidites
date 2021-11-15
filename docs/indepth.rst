Woma In Depth
=============

Modules
~~~~~~~

A woma module is the entirety of a text file. The body of a module can have 3 citizens:

- Functions
- Contracted Assignment i.e. ``a = 2 -> int``
- Simple Assignment i.e. ``b = 'foo'``


Functions
~~~~~~~~~

.. code:: woma

    (Identity(x = \0 -> number, str)) number, str
        <*>x

Here we have defined a function called ``Identity`` that takes a single argument ``x`` that respects a contract with two
clauses in union ``number`` and ``str``. When called with a ``number`` or ``str`` argument this function will return the
argument ``x``. This is a pure function in the traditional sense and in the Womatic sense. In Woma, a pure function is a
function where any two contracts can be switched and the output remains unchanged for all inputs.

.. note::

    In addition to user-defined functions woma provides some standard built-in functions.
    See :ref:`builtins`

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

There is also a 'match any' contract called ``*``. So lets say we want to make an identity function again, we can do it like so:

.. code-block:: woma

    (identity(x = /0 -> *)) *
        <*>x

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
 - As a catch-all case for the `(!)` (match) trigram.

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

+------------+------------+----------------+---------------------+
| Arity      | Operator   | Associativity  | Operation           |
+============+============+================+=====================+
| 1          |    ``+``   |    ``right``   |  ``positive``       |
+------------+------------+----------------+---------------------+
| 1          |    ``-``   |    ``right``   | ``negative``        |
+------------+------------+----------------+---------------------+
| 1          |    ``!``   |    ``left``    | ``factorial``       |
+------------+------------+----------------+---------------------+
| 2          |    ``+``   |    ``left``    | ``addition``        |
+------------+------------+----------------+---------------------+
| 2          |    ``-``   |    ``left``    | ``subtraction``     |
+------------+------------+----------------+---------------------+
| 2          |    ``*``   |    ``left``    | ``multiplication``  |
+------------+------------+----------------+---------------------+
| 2          |    ``/``   |    ``left``    | ``division``        |
+------------+------------+----------------+---------------------+
| 2          |    ``**``  |    ``right``   | ``exponentiation``  |
+------------+------------+----------------+---------------------+
| 2          |    ``<<``  |    ``left``    |  ``bitshift left``  |
+------------+------------+----------------+---------------------+
| 2          |    ``>>``  |    ``left``    |  ``bitshift right`` |
+------------+------------+----------------+---------------------+
| 2          |    ``&``   |    ``left``    | ``bitwise and``     |
+------------+------------+----------------+---------------------+
| 2          |    ``|``   |    ``left``    | ``bitwise or``      |
+------------+------------+----------------+---------------------+
| 2          |    ``^``   |    ``left``    | ``bitwise not``     |
+------------+------------+----------------+---------------------+
| 2          |    ``||``  |    ``left``    |  ``logical or``     |
+------------+------------+----------------+---------------------+
| 2          |    ``&&``  |    ``left``    |  ``logical and``    |
+------------+------------+----------------+---------------------+
| 2          |    ``>=``  |    ``left``    |``greater or equal`` |
+------------+------------+----------------+---------------------+
| 2          |    ``<=``  |    ``left``    |``lesser or equal``  |
+------------+------------+----------------+---------------------+
| 2          |    ``>``   |    ``left``    |``greater than``     |
+------------+------------+----------------+---------------------+
| 2          |    ``>``   |    ``left``    |``less than``        |
+------------+------------+----------------+---------------------+
| 2          |    ``==``  |    ``left``    | ``equal to``        |
+------------+------------+----------------+---------------------+

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

