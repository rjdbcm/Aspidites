
Examples
========

.. tabs::

    .. tab::

        First Class Functions

        .. code:: woma

            #cython.binding(True)
            (Add(x = 3 -> int; y = 3 -> int)) int
                <*>x+y

    .. tab::

        Generators and Procedures

        .. code:: woma

            `generators`
            (Yield123()) coroutine
                <^>Add(0, 1)
                <^>Add(0, 2)
                <^>Add(0, 3)

            `procedures`
            (Hello()) procedure
                print("Hello, World!")



.. tabs::

    .. tab::

        Persistent or Evolver Iterables

        .. code:: woma

            `persistent vectors`
            D = [2, 4, 6, 8, 10]
            `evolver vectors`
            E = [12, 14, 16, 18]...

            `persistent sets`
            G = {'a', 'b', 'c'}
            `evolver sets`
            F = {'e', 'f', 'g'}...

            `persistent mappings`
            C = {'a': (3+5), 'b': 8, 'c': True, 4: None, 'd': 6**2*5+3}
            `evolver mappings`
            B = {'a': (3+5), 'b': 8, 'c': True, 4: None, 'd': 6**2*5+3}...

        This is implemented using the library `pyrsistent <https://github.com/tobgu/pyrsistent>`_.

    .. tab::

        Refinement Types use Contract Clauses

        .. code:: woma

            `new contracts can impose more complex contractual clauses`
            colors <- list[3](np_uint8, int, <256, >=0)

.. tabs::

    .. tab::

        Closures and Lambdas

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

    .. tab::

        nullit as the Nullity Element

        .. code:: woma

            `modulus and division by 0 handled by returning nullit/Undefined()`
            denom = 0
            div_by_zero = 1 / denom
            mod_zero = 1 % denom
            div_by_zero2 = 1 / 0
            mod_zero2 = 1 % 0
            a_truth = div_by_zero2 == nullit
