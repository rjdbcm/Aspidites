
Examples
========

.. tabs::

    .. tab::

        Functions

        .. code:: woma

            (Add(x = 3 -> int; y = 3 -> int)) int
                <*>x+y

    .. tab::

        Generators

        .. code:: woma

            (Yield123()) coroutine
                <^>1
                <^>2
                <^>3
            
    .. tab::
    
        Procedures
        
        .. code:: woma
            
            (Hello()) procedure
               print("Hello, World!")
    

    .. tab::

        Coroutines

        .. code:: woma

            (Yield123()) coroutine
                <^>1
                <^>2
                <^>3
            `ellipsis calling creates a true coroutine`
            c = Yield123()...

.. tabs::

    .. tab::

        Collections

        .. code:: woma

            D = [2, 4, 6, 8, 10]
            

            G = {'a', 'b', 'c'}

            C = {'a': (3+5), 'b': 8, 'c': True, 4: None, 'd': 6**2*5+3}

        This is implemented using the library `pyrsistent <https://github.com/tobgu/pyrsistent>`_.
        
    .. tab::

        Evolvers
        
        .. code:: woma
            E = [12, 14, 16, 18]...
            F = {'e', 'f', 'g'}...
            B = {'a': (3+5), 'b': 8, 'c': True, 4: None, 'd': 6**2*5+3}...

        This is implemented using the library `pyrsistent <https://github.com/tobgu/pyrsistent>`_.
        
    .. tab::

        Contracts

        .. code:: woma

            `new contracts can impose more complex contractual clauses`
            colors <- list[3](np_uint8, int, <256, >=0)

.. tabs::

    .. tab::

        Lambdas

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

        Nullity

        .. code:: woma

            `modulus and division by 0 handled by returning /0 a.k.a. Undefined`
            denom = 0
            div_by_zero = 1 / denom
            mod_zero = 1 % denom
            div_by_zero2 = 1 / 0
            mod_zero2 = 1 % 0
            a_truth = div_by_zero2 == /0
