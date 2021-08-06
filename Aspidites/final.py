# Aspidites is Copyright 2021, Ross J. Duff.
# See LICENSE.txt for more info.

from typing import Callable, Tuple

from pyrsistent import pmap

from Aspidites._vendor.contracts import check, contract, new_contract


@new_contract
@contract
def heritable(bases: 'tuple') -> 'bool':
    """Convenience clause for a tuple of heritable bases"""
    return not bool(len(tuple(b for b in bases if isinstance(b, final))))


# noinspection PyPep8Naming
class final(type):
    def __new__(mcs, name, bases, classdict):
        check('heritable', bases)
        return type.__new__(mcs, name, bases, dict(classdict))
