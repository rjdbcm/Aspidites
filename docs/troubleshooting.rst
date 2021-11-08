Troubleshooting
###############

Expected end of text
--------------------

This is particularly common, unfortunately when you neglect certain parsable symbols you get this (rather unhelpful) error.
For these we have to look at the found context and look for whats missing.
In the following example we define a function but forgot to include a return annotation:

.. code-block:: woma

    (mul(x = 0 -> number; y = 0 -> number))
        <*> x * y

This is the error we get when we try to compile:

.. code-block::

    Aspidites._vendor.pyparsing_extension.ParseException: Expected end of text, found in '(mul(x = 0 -> number'...