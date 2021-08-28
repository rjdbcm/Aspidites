
Syntax
======

Lexicon
~~~~~~~

+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| Working?   | Symbol    | Verbage             | Example                                                                                                           |
+============+===========+=====================+===================================================================================================================+
| ✅         | ``->``    | respects            | ``identifier`` ``->`` ``constraining clauses``                                                                    |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| ✅         | ``<-``    | imposes             | ``identifier`` ``<-`` ``imposed clauses``                                                                         |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| ❌         | ``<@>``   | loops               | ``identifier`` ``<@>`` ``iterable container``\ \ ``indent`` ``...``                                               |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| ✅         | ``<*>``   | return              | ``<*>`` ``statement``                                                                                             |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| ✅         | ``#``     | pragma              | ``#`` ``compiler directive``                                                                                      |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| ✅         | ``))``    | return respects     | ``))`` ``return constraints``                                                                                     |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+
| ✅         | ``(G(``   | define G as function| ``(`` ``FuncName`` ``(`` ``identifier`` ``->`` ``constraining clauses`` ``))`` ``return constraints``             |
+------------+-----------+---------------------+-------------------------------------------------------------------------------------------------------------------+

Examples
~~~~~~~~

First Class Functions
^^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    #cython.binding(True)
    (Add(x = 3 -> int; y = 3 -> int)) int
        <*>x+y

Generators, Procedures, and Coroutines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    `generators`
    (Yield123()) coroutine
        <^>Add(0, 1)
        <^>Add(0, 2)
        <^>Add(0, 3)

    `procedures`
    (Hello()) procedure
        print("Hello, World!")

    `coroutines`
    (Hello2()) coroutine
        <^>Hello()

Persistent Evolvable Iterables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    `persistent vectors`
    D = [2, 4, 6, 8, 10]

    `persistent sets`
    G = {'a', 'b', 'c'}

    `persistent mappings`
    C = {'a': (3+5),
         'b': 8,
         'c': True,
           4: None,
         'd': 6**2*5+3}

Refinement Types use Contract Clauses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    `new contracts can impose more complex contractual clauses`
    colors <- list[3](int, <256, >=0)

Closures and Lambdas
^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    `any woma function can be closed in place to become an instance that complies with the`
    `type specification or Undefined for instances that breach the type specification contract`
    x = Add(3, 3)...

    `seamless exception handling allows tracing of undefined code branches`
    y = Add(4, 3.5)...

    `mixed usage of closure and regular function calls`
    z = Add(x(), 3)

    `Scala-style closure functions`
    scala = (_ * 2)
    val = scala(_ + _)
    val = val(scala)...

nullit as the Nullity Element
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    `modulus and division by 0 handled by returning nullit/Undefined()`
    denom = 0
    div_by_zero = 1 / denom
    mod_zero = 1 % denom
    div_by_zero2 = 1 / 0
    mod_zero2 = 1 % 0
    a_truth = div_by_zero2 == nullit

Optional Structured Entrypoint
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: woma

    `main: structure for executable actions when run as a binary`
    (Hello()) procedure
        print("Hello, World!")

    main:
    Hello()
    print("I'm a binary.")
