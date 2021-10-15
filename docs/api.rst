API Documentation
=================

API Proper
~~~~~~~~~~
.. autoclass:: Aspidites.api.bordered

.. autoclass:: Aspidites.api.Warn

Compiler
~~~~~~~~

.. autoclass:: Aspidites.compiler.CheckedFileStack
    :members:

.. autoclass:: Aspidites.compiler.CompilerArgs

    :attr:`~.Aspidites.compiler.CompilerArgs.code:` :class:`pyparsing.ParseResults`

    :attr:`~.Aspidites.compiler.CompilerArgs.fname:` :py:class:`pathlib.Path`

    :attr:`~.Aspidites.compiler.CompilerArgs.force:` :py:class:`bool`

    :attr:`~.Aspidites.compiler.CompilerArgs.bytecode:` :py:class:`bool`

    :attr:`~.Aspidites.compiler.CompilerArgs.build_requires:` :py:attr:`typing.Union[typing.List, str]`

    :attr:`~.Aspidites.compiler.CompilerArgs.verbose` :py:class:`int`

    :attr:`~.Aspidites.compiler.CompilerArgs.embed:` :py:class:`typing.Union[str, None]`


.. autoclass:: Aspidites.compiler.Compiler
    :members:

Monads
~~~~~~

.. autoclass:: Aspidites.monads.Maybe
    :members: __call__

.. autoclass:: Aspidites.monads.Surely

Math
~~~~

.. autoclass:: Aspidites.math.Undefined
    :members: __init__, __new__

.. autofunction:: Aspidites.math.SafeDiv
    :noindex:

.. autofunction:: Aspidites.math.SafeExp
    :noindex:

.. autofunction:: Aspidites.math.SafeFactorial
    :noindex:

.. autofunction:: Aspidites.math.SafeFloorDiv
    :noindex:

.. autofunction:: Aspidites.math.SafeMod
    :noindex:

.. autofunction:: Aspidites.math.SafeUnaryAdd
    :noindex:

.. autofunction:: Aspidites.math.SafeUnarySub
    :noindex:
