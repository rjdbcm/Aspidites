Woma In Depth
=============

Functions
~~~~~~~~~

.. code:: woma

    (Identity(x -> number, str)) number, str
        <*>x

Here we have defined a function called ``Identity`` that takes a single argument ``x`` that respects a contract with two
clauses in union ``number`` and ``str``. When called with a ``number`` or ``str`` argument this function will return the
argument ``x``. This is a pure function in the traditional sense and in the Womatic sense. In Woma, a pure function is a
function where any two contracts can be switched and the output remains unchanged for all inputs.

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

Trigrams
~~~~~~~~

Rather than keywords Woma makes use of three character symbols called trigrams. Two of the most basic are ``<*>`` and
``<^>``, meaning ``return`` and ``yield`` respectively.

**Table of Trigrams**


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

Rather than raising an error Woma will always prefer to return ``nullit``, the absorbing, or nullity, element.
Unlike NaN, where it is undefined but not equal to itself, all nullity elements are undefined but equal. Their identity,
likewise, is always the same. However, the conditions under which it was created can be cached into the nullit instance.
This is the case in the internal implementation of mathematical operations.