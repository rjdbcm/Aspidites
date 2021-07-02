from typing import Callable, Tuple
from Aspidites.features.contracts import new_contract, contract, check
from pyrsistent import pmap
# very simple final classes without


@new_contract
@contract
def heritable(bases: 'tuple') -> 'bool':
    """Convenience clause for a tuple of heritable bases"""
    for b in bases:
        if isinstance(b, final):
            return False
    return True


class final(type):
    def __new__(mcs, name, bases, classdict):
        check('heritable', bases)
        return type.__new__(mcs, name, bases, dict(classdict))
