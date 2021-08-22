# Aspidites is Copyright 2021, Ross J. Duff.
# See LICENSE.txt for more info.

from typing import Callable, Tuple

from pyrsistent import pmap

from Aspidites._vendor.contracts import check, contract, new_contract


@new_contract
@contract
def heritable(bases: 'tuple') -> 'bool':
    """Convenience clause for a tuple of heritable bases"""
    return not bool(len(tuple(b for b in bases if isinstance(b, _Final))))


# noinspection PyPep8Naming
class _Final(type):
    def __new__(mcs, name, bases, classdict):
        check('heritable', bases)
        return type.__new__(mcs, name, bases, dict(classdict))


def final(_=_Final):
    if _ != _Final:
        meta = _Final
    else:
        meta = _

    def metaclass_wrapper(cls):
        __name = str(cls.__name__)
        __bases = tuple(cls.__bases__)
        __dict = dict(cls.__dict__)

        for each_slot in __dict.get("__slots__", tuple()):
            __dict.pop(each_slot, None)

        __dict["__metaclass__"] = meta

        __dict["__wrapped__"] = cls

        return meta(__name, __bases, __dict)
    return metaclass_wrapper
