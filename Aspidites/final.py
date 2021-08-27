
# Aspidites
# Copyright (C) 2021 Ross J. Duff

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ._vendor.contracts import check, contract, new_contract


@new_contract
@contract
def heritable(bases: 'tuple') -> 'bool':
    """Convenience clause for a tuple of heritable bases"""
    return not bool(len(tuple(b for b in bases if isinstance(b, _Final))))


# noinspection PyPep8Naming
class _Final(type):
    """Non public metaclass implementation for final classes"""
    def __new__(mcs, name, bases, classdict):
        check('heritable', bases)
        return type.__new__(mcs, name, bases, dict(classdict))


def final(_=_Final):  # This is 100% a hack: but it works.
    """Decorator to create final classes like:
    .. code:: python

        @final()
        class Foo(object):
            ...
    """
    if _ != _Final:
        meta = _Final
    else:
        meta = _

    def wrapper(mcs):
        __name = str(mcs.__name__)
        __bases = tuple(mcs.__bases__)
        __dict = dict(mcs.__dict__)

        for each_slot in __dict.get("__slots__", tuple()):
            __dict.pop(each_slot, None)

        __dict["__metaclass__"] = meta
        __dict["__wrapped__"] = mcs

        return meta(__name, __bases, __dict)
    return wrapper
