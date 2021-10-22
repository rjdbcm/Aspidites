Known Limitations
=================

Literal Arithmetic
~~~~~~~~~~~~~~~~~~

 - ``--N != N``
  - Workaround: don't use ``--``
 - Chained arithmetic doesn't parse properly.
  - Example: ``2/1/2 == 2/(1/2)``
  - Workaround 1: Don't chain arithmetic prefer explicit assignment.
  - Workaround 2: Use ``(2/1)/2`` for python-style evaluation.