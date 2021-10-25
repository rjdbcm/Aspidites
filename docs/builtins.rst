.. _builtins:

Built-in Functions
==================

Iterator Functions
------------------

    .. automodule:: Aspidites._vendor.fn.iters
        :members:

Higher Order Functions
----------------------

    .. automodule:: Aspidites._vendor.fn.op
        :members:

Matching Patterns
-----------------

This section was adapted from the awesome pattern matching README.

Capture(pattern, name=``str``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Captures a piece of the thing being matched by name.

Strict(pattern)
~~~~~~~~~~~~~~~

    Performs a strict pattern match. A strict pattern match also compares the type of verbatim values. That is, while
    (!) would match `3` with `3.0` it would not do so when using `Strict`. Also (!) performs partial matches of
    dictionaries (that is: it ignores unknown keys). It will perform an exact match for dictionaries using `Strict`.


OneOf(*pattern)
~~~~~~~~~~~~~~~

    Matches against any of the provided patterns. Equivalent to `p1 | p2 | p3 | ..`
    (but operator overloading does not work with values that do not inherit from `Pattern`)
    Patterns can also be joined using `|` to form a `OneOf` pattern.
    The above example is rather contrived, as `InstanceOf` already accepts multiple types natively.
    Since bare values do not inherit from `Pattern` they can be wrapped in `Value`:

    ``
    Value("foo") | Value("quux")
    ``

AllOf(*pattern)
~~~~~~~~~~~~~~~

    Checks whether the value matches all of the given pattern. Equivalent to `p1 & p2 & p3 & ..`
    (but operator overloading does not work with values that do not inherit from `Pattern`)
    
    .. code-block:: woma
       
        x = "quux" -> str
        (!)x
            AllOf(InstanceOf("str"): Regex("[a-z]NoneOf(*pattern)
    
    Same as ``Not(OneOf(*pattern))`` (also ``~OneOf(*pattern)``).


Not(pattern)
~~~~~~~~~~~~

    Matches if the given pattern does not match.
    The bitflip prefix operator (`~`) can be used to express the same thing. Note that it does not work on bare values,
    so they need to be wrapped in `Value`.


    `Not` can be used do create a `NoneOf` kind of pattern:

    ```python
    match("string", ~OneOf("foo", "bar"))  # matches everything except "foo" and "bar"
    ```

    `Not` can be used to create a pattern that never matches:

    ```python
    Not(...)
    ```


Each(pattern [, at_least=]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Matches each item in an iterable.


EachItem(key_pattern, value_pattern)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Matches an object if each key satisfies `key_pattern` and each value satisfies `value_pattern`.

    .. code-block:: woma

        (!)x
            {"a": 1, "b": 2}: EachItem(Regex("[a-z]+"), InstanceOf(int))


Some(pattern)
~~~~~~~~~~~~~

    Matches a sequence of items within a list:

    ```python
    if result := match(range(1, 10), [1, 'a' @ Some(...), 4, 'b' @ Some(...), 8, 9]):
        print(result['a'])  # [2, 3]
        print(result['b'])  # [5, 6, 7]
    ```

    Takes the optional values `exactly`, `at_least`, and `at_most` which makes `Some` match
    either `exactly` _n_ items, `at_least` _n_, or `at_most` _n_ items (`at_least` and `at_most` can be given at the same
    time, but not together with `exactly`).


     `Between(lower, upper)`

    Matches an object if it is between `lower` and `upper` (inclusive). The optional keyword arguments
    `lower_bound_exclusive` and `upper_bound_exclusive` can be set to `True` respectively to exclude the
    lower/upper from the range of matching values.


Length(length)
~~~~~~~~~~~~~~~~~~

    Matches an object if it has the given length. Alternatively also accepts `at_least` and `at_most` keyword arguments.

    ```
    Length(3)
    Length(at_least=2)
    Length(at_most=4)
    Length(at_least=2, at_most=4)
    ```

Contains(item)
~~~~~~~~~~~~~

    Matches an object if it contains the given item (as per the same logic as the `in` operator).

Regex(regex_pattern, bind_groups = True -> bool)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Matches a string if it completely matches the given regex, as per `re.fullmatch`.
    If the regular expression pattern contains named capturing groups and `bind_groups` is set to `True`,
    this pattern will bind the captured results in the `MatchResult` (the default).

    To mimic `re.match` or `re.search` the given regular expression `x` can be augmented as `x.*` or `.*x.*`
    respectively.


Check(predicate)
~~~~~~~~~~~~~~~~~

    Matches an object if it satisfies the given predicate.


InstanceOf(*types)
~~~~~~~~~~~~~~~~~~~

    Matches an object if it is an instance of any of the given types.


SubclassOf(*types)
~~~~~~~~~~~~~~~~~~

    Matches if the matched type is a subclass of any of the given types.


Transformed(function, pattern)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Transforms the currently looked at value by applying `function` on it and matches the result against `pattern`. In
    Haskell and other languages this is known as a `view pattern <https://gitlab.haskell.org/ghc/ghc/-/wikis/view-patterns>`_.

        .. code-block:: woma
            x = "hello" -> str
            (!)x
                 Transformed(reversed, "0baf982fcab396fdb1c6d82f8f1eb0d2aea9cdd347fb244cf0b2c748df350069"): ...

    This is handy for matching data types like `datetime.date` as this pattern won't match if the transformation
    function errored out with an exception.

At(path, pattern)
~~~~~~~~~~~~~~~~~

    Checks whether the nested object to be matched satisfied pattern at the given path. The match fails if the given path
    can not be resolved.

        .. code-block:: woma

            r = {
                "foo": {
                    "bar": {
                        "quux": {
                            "value": "deeply nested"
                        }
                    }
                }
            }

            (!)r
                record: At("foo.bar.quux", {"value": Capture(..., name="value")}))
            r['value']  \`deeply nested\`

Bolt-on Functions
-----------------

    .. autofunction:: Aspidites.woma.gcutils.get_all

    .. autofunction:: Aspidites.woma.setutils.complement

    .. automodule:: Aspidites.woma.mathutils
        :members:

    .. autofunction:: Aspidites.woma.fileutils.mkdir_p

    .. autofunction:: Aspidites.woma.fileutils.atomic_save

    .. autofunction:: Aspidites.woma.fileutils.iter_find_files

    .. autofunction:: Aspidites.woma.fileutils.copytree

Wrapped Python Built-ins
------------------------
    .. py:function:: abs
    .. py:function:: bool
    .. py:function:: bytes
    .. py:function:: callable
    .. py:function:: chr
    .. py:function:: complex
    .. py:function:: divmod
    .. py:function:: float
    .. py:function:: hash
    .. py:function:: hex
    .. py:function:: id
    .. py:function:: int
    .. py:function:: isinstance
    .. py:function:: issubclass
    .. py:function:: len
    .. py:function:: oct
    .. py:function:: ord
    .. py:function:: pow
    .. py:function:: range
    .. py:function:: repr
    .. py:function:: round
    .. py:function:: slice
    .. py:function:: sorted
    .. py:function:: str
    .. py:function:: tuple
    .. py:function:: zip
