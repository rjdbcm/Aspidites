Known Limitations
=================

Literal Arithmetic
~~~~~~~~~~~~~~~~~~

 - Chained arithmetic doesn't parse properly when using the same operator.
  - Issue: `#40 <https://github.com/rjdbcm/Aspidites/issues/40>`_
  - Example: ``2/1/2`` ``2/(1/2)``
  - Workaround: Don't chain arithmetic prefer explicit assignment.
