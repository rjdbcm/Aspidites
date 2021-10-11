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

Trigrams
~~~~~~~~

Rather than keywords Woma makes use of three character symbols called trigrams. Two of the most basic are ``<*>`` and
``<^>``, meaning ``return`` and ``yield`` respectively.


Operators
~~~~~~~~~

The operators in Woma are identical to their python counterparts. Their implementation is different in some cases


Literals
~~~~~~~~

The only named literals defined currently are the booleans True & False and the nullity element nullit.


Nullity
~~~~~~~

Rather than raising an error Woma will always prefer to return ``nullit``, the absorbing, or nullity, element.
Unlike NaN, where it is undefined but not equal to itself, all nullity elements are undefined but equal. Their identity,
likewise, is always the same. However, the conditions under which it was created can be cached into the nullit instance.
This is the case in the internal implementation of mathematical operations.