# -*- coding: utf-8 -*-
"""\

The :class:`set` type brings the practical expressiveness of
set theory to Python. It has a very rich API overall, but lacks a
couple of fundamental features. For one, sets are not ordered. On top
of this, sets are not indexable, i.e, ``my_set[8]`` will raise an
:exc:`TypeError`. The :class:`IndexedSet` type remedies both of these
issues without compromising on the excellent complexity
characteristics of Python's built-in set implementation.
"""

from __future__ import print_function

from bisect import bisect_left
from itertools import chain, islice
import operator
from pyrsistent import PSet

try:
    from collections.abc import MutableSet
except ImportError:
    from collections import MutableSet

try:
    from typeutils import make_sentinel

    _MISSING = make_sentinel(var_name='_MISSING')
except ImportError:
    _MISSING = object()

__all__ = ['complement']

_COMPACTION_FACTOR = 8


# TODO: inherit from set()
# TODO: .discard_many(), .remove_many()
# TODO: raise exception on non-set params?
# TODO: technically reverse operators should probably reverse the
# order of the 'other' inputs and put self last (to try and maintain
# insertion order)


def complement(wrapped):
    """Given a :class:`set`, convert it to a **complement set**.

    Whereas a :class:`set` keeps track of what it contains, a
    `complement set
    <https://en.wikipedia.org/wiki/Complement_(set_theory)>`_ keeps
    track of what it does *not* contain. For example, look what
    happens when we intersect a normal set with a complement set::

    >>> list(set(range(5)) & complement(set([2, 3])))
    [0, 1, 4]

    We get the everything in the left that wasn't in the right,
    because intersecting with a complement is the same as subtracting
    a normal set.

    Args:
        wrapped (set): A set or any other iterable which should be
           turned into a complement set.

    All set methods and operators are supported by complement sets,
    between other :func:`complement`-wrapped sets and/or regular
    :class:`set` objects.

    Because a complement set only tracks what elements are *not* in
    the set, functionality based on set contents is unavailable:
    :func:`len`, :func:`iter` (and for loops), and ``.pop()``. But a
    complement set can always be turned back into a regular set by
    complementing it again:

    >>> s = set(range(5))
    >>> complement(complement(s)) == s
    True

    .. note::

       An empty complement set corresponds to the concept of a
       `universal set <https://en.wikipedia.org/wiki/Universal_set>`_
       from mathematics.

    Complement sets by example
    ^^^^^^^^^^^^^^^^^^^^^^^^^^

    Many uses of sets can be expressed more simply by using a
    complement. Rather than trying to work out in your head the proper
    way to invert an expression, you can just throw a complement on
    the set. Consider this example of a name filter::

        >>> class NamesFilter(object):
        ...    def __init__(self, allowed):
        ...        self._allowed = allowed
        ...
        ...    def filter(self, names):
        ...        return [name for name in names if name in self._allowed]
        >>> NamesFilter(set(['alice', 'bob'])).filter(['alice', 'bob', 'carol'])
        ['alice', 'bob']

    What if we want to just express "let all the names through"?

    We could try to enumerate all of the expected names::

       ``NamesFilter({'alice', 'bob', 'carol'})``

    But this is very brittle -- what if at some point over this
    object is changed to filter ``['alice', 'bob', 'carol', 'dan']``?

    Even worse, what about the poor programmer who next works
    on this piece of code?  They cannot tell whether the purpose
    of the large allowed set was "allow everything", or if 'dan'
    was excluded for some subtle reason.

    A complement set lets the programmer intention be expressed
    succinctly and directly::

       NamesFilter(complement(set()))

    Not only is this code short and robust, it is easy to understand
    the intention.

    """
    if type(wrapped) is _ComplementSet:
        return wrapped.complemented()
    if type(wrapped) is frozenset:
        return _ComplementSet(excluded=wrapped)
    return _ComplementSet(excluded=set(wrapped))


def _norm_args_typeerror(other):
    '''normalize args and raise type-error if there is a problem'''
    if type(other) in (set, frozenset):
        inc, exc = other, None
    elif type(other) is _ComplementSet:
        inc, exc = other._included, other._excluded
    else:
        raise TypeError('argument must be another set or complement(set)')
    return inc, exc


def _norm_args_notimplemented(other):
    '''normalize args and return NotImplemented (for overloaded operators)'''
    if type(other) in (set, frozenset):
        inc, exc = other, None
    elif type(other) is _ComplementSet:
        inc, exc = other._included, other._excluded
    else:
        return NotImplemented, None
    return inc, exc


class _ComplementSet(object):
    """
    helper class for complement() that implements the set methods
    """
    __slots__ = ('_included', '_excluded')

    def __init__(self, included=None, excluded=None):
        if included is None:
            assert type(excluded) in (set, frozenset, PSet)
        elif excluded is None:
            assert type(included) in (set, frozenset, PSet)
        else:
            raise ValueError('one of included or excluded must be a set')
        self._included, self._excluded = included, excluded

    def __repr__(self):
        if self._included is None:
            return 'complement({0})'.format(repr(self._excluded))
        return 'complement(complement({0}))'.format(repr(self._included))

    def complemented(self):
        '''return a complement of the current set'''
        if type(self._included) is frozenset or type(self._excluded) is frozenset:
            return _ComplementSet(included=self._excluded, excluded=self._included)
        return _ComplementSet(
            included=None if self._excluded is None else set(self._excluded),
            excluded=None if self._included is None else set(self._included))

    __invert__ = complemented

    def complement(self):
        '''convert the current set to its complement in-place'''
        self._included, self._excluded = self._excluded, self._included

    def __contains__(self, item):
        if self._included is None:
            return not item in self._excluded
        return item in self._included

    def add(self, item):
        if self._included is None:
            if item in self._excluded:
                self._excluded.remove(item)
        else:
            self._included.add(item)

    def remove(self, item):
        if self._included is None:
            self._excluded.add(item)
        else:
            self._included.remove(item)

    def pop(self):
        if self._included is None:
            raise NotImplementedError  # self.missing.add(random.choice(gc.objects()))
        return self._included.pop()

    def intersection(self, other):
        try:
            return self & other
        except NotImplementedError:
            raise TypeError('argument must be another set or complement(set)')

    def __and__(self, other):
        inc, exc = _norm_args_notimplemented(other)
        if inc is NotImplemented:
            return NotImplemented
        if self._included is None:
            if exc is None:  # - +
                return _ComplementSet(included=inc - self._excluded)
            else:  # - -
                return _ComplementSet(excluded=self._excluded.union(other._excluded))
        else:
            if inc is None:  # + -
                return _ComplementSet(included=exc - self._included)
            else:  # + +
                return _ComplementSet(included=self._included.intersection(inc))

    __rand__ = __and__

    def __iand__(self, other):
        inc, exc = _norm_args_notimplemented(other)
        if inc is NotImplemented:
            return NotImplemented
        if self._included is None:
            if exc is None:  # - +
                self._excluded = inc - self._excluded  # TODO: do this in place?
            else:  # - -
                self._excluded |= exc
        else:
            if inc is None:  # + -
                self._included -= exc
                self._included, self._excluded = None, self._included
            else:  # + +
                self._included &= inc
        return self

    def union(self, other):
        try:
            return self | other
        except NotImplementedError:
            raise TypeError('argument must be another set or complement(set)')

    def __or__(self, other):
        inc, exc = _norm_args_notimplemented(other)
        if inc is NotImplemented:
            return NotImplemented
        if self._included is None:
            if exc is None:  # - +
                return _ComplementSet(excluded=self._excluded - inc)
            else:  # - -
                return _ComplementSet(excluded=self._excluded.intersection(exc))
        else:
            if inc is None:  # + -
                return _ComplementSet(excluded=exc - self._included)
            else:  # + +
                return _ComplementSet(included=self._included.union(inc))

    __ror__ = __or__

    def __ior__(self, other):
        inc, exc = _norm_args_notimplemented(other)
        if inc is NotImplemented:
            return NotImplemented
        if self._included is None:
            if exc is None:  # - +
                self._excluded -= inc
            else:  # - -
                self._excluded &= exc
        else:
            if inc is None:  # + -
                self._included, self._excluded = None, exc - self._included  # TODO: do this in place?
            else:  # + +
                self._included |= inc
        return self

    def update(self, items):
        if type(items) in (set, frozenset):
            inc, exc = items, None
        elif type(items) is _ComplementSet:
            inc, exc = items._included, items._excluded
        else:
            inc, exc = frozenset(items), None
        if self._included is None:
            if exc is None:  # - +
                self._excluded &= inc
            else:  # - -
                self._excluded.discard(exc)
        else:
            if inc is None:  # + -
                self._included &= exc
                self._included, self._excluded = None, self._excluded
            else:  # + +
                self._included.update(inc)

    def discard(self, items):
        if type(items) in (set, frozenset):
            inc, exc = items, None
        elif type(items) is _ComplementSet:
            inc, exc = items._included, items._excluded
        else:
            inc, exc = frozenset(items), None
        if self._included is None:
            if exc is None:  # - +
                self._excluded.update(inc)
            else:  # - -
                self._included, self._excluded = exc - self._excluded, None
        else:
            if inc is None:  # + -
                self._included &= exc
            else:  # + +
                self._included.discard(inc)

    def symmetric_difference(self, other):
        try:
            return self ^ other
        except NotImplementedError:
            raise TypeError('argument must be another set or complement(set)')

    def __xor__(self, other):
        inc, exc = _norm_args_notimplemented(other)
        if inc is NotImplemented:
            return NotImplemented
        if inc is NotImplemented:
            return NotImplemented
        if self._included is None:
            if exc is None:  # - +
                return _ComplementSet(excluded=self._excluded - inc)
            else:  # - -
                return _ComplementSet(included=self._excluded.symmetric_difference(exc))
        else:
            if inc is None:  # + -
                return _ComplementSet(excluded=exc - self._included)
            else:  # + +
                return _ComplementSet(included=self._included.symmetric_difference(inc))

    __rxor__ = __xor__

    def symmetric_difference_update(self, other):
        inc, exc = _norm_args_typeerror(other)
        if self._included is None:
            if exc is None:  # - +
                self._excluded |= inc
            else:  # - -
                self._excluded.symmetric_difference_update(exc)
                self._included, self._excluded = self._excluded, None
        else:
            if inc is None:  # + -
                self._included |= exc
                self._included, self._excluded = None, self._included
            else:  # + +
                self._included.symmetric_difference_update(inc)

    def isdisjoint(self, other):
        inc, exc = _norm_args_typeerror(other)
        if inc is NotImplemented:
            return NotImplemented
        if self._included is None:
            if exc is None:  # - +
                return inc.issubset(self._excluded)
            else:  # - -
                return False
        else:
            if inc is None:  # + -
                return self._included.issubset(exc)
            else:  # + +
                return self._included.isdisjoint(inc)

    def issubset(self, other):
        '''everything missing from other is also missing from self'''
        try:
            return self <= other
        except NotImplementedError:
            raise TypeError('argument must be another set or complement(set)')

    def __le__(self, other):
        inc, exc = _norm_args_notimplemented(other)
        if inc is NotImplemented:
            return NotImplemented
        if inc is NotImplemented:
            return NotImplemented
        if self._included is None:
            if exc is None:  # - +
                return False
            else:  # - -
                return self._excluded.issupserset(exc)
        else:
            if inc is None:  # + -
                return self._included.isdisjoint(exc)
            else:  # + +
                return self._included.issubset(inc)

    def __lt__(self, other):
        inc, exc = _norm_args_notimplemented(other)
        if inc is NotImplemented:
            return NotImplemented
        if inc is NotImplemented:
            return NotImplemented
        if self._included is None:
            if exc is None:  # - +
                return False
            else:  # - -
                return self._excluded > exc
        else:
            if inc is None:  # + -
                return self._included.isdisjoint(exc)
            else:  # + +
                return self._included < inc

    def issuperset(self, other):
        '''everything missing from self is also missing from super'''
        try:
            return self >= other
        except NotImplementedError:
            raise TypeError('argument must be another set or complement(set)')

    def __ge__(self, other):
        inc, exc = _norm_args_notimplemented(other)
        if inc is NotImplemented:
            return NotImplemented
        if self._included is None:
            if exc is None:  # - +
                return not self._excluded.intersection(inc)
            else:  # - -
                return self._excluded.issubset(exc)
        else:
            if inc is None:  # + -
                return False
            else:  # + +
                return self._included.issupserset(inc)

    def __gt__(self, other):
        inc, exc = _norm_args_notimplemented(other)
        if inc is NotImplemented:
            return NotImplemented
        if self._included is None:
            if exc is None:  # - +
                return not self._excluded.intersection(inc)
            else:  # - -
                return self._excluded < exc
        else:
            if inc is None:  # + -
                return False
            else:  # + +
                return self._included > inc

    def difference(self, other):
        try:
            return self - other
        except NotImplementedError:
            raise TypeError('argument must be another set or complement(set)')

    def __sub__(self, other):
        inc, exc = _norm_args_notimplemented(other)
        if inc is NotImplemented:
            return NotImplemented
        if self._included is None:
            if exc is None:  # - +
                return _ComplementSet(excluded=self._excluded | inc)
            else:  # - -
                return _ComplementSet(included=exc - self._excluded)
        else:
            if inc is None:  # + -
                return _ComplementSet(included=self._included & exc)
            else:  # + +
                return _ComplementSet(included=self._included.difference(inc))

    def __rsub__(self, other):
        inc, exc = _norm_args_notimplemented(other)
        if inc is NotImplemented:
            return NotImplemented
        # rsub, so the expression being evaluated is "other - self"
        if self._included is None:
            if exc is None:  # - +
                return _ComplementSet(included=inc & self._excluded)
            else:  # - -
                return _ComplementSet(included=self._excluded - exc)
        else:
            if inc is None:  # + -
                return _ComplementSet(excluded=exc | self._included)
            else:  # + +
                return _ComplementSet(included=inc.difference(self._included))

    def difference_update(self, other):
        try:
            self -= other
        except NotImplementedError:
            raise TypeError('argument must be another set or complement(set)')

    def __isub__(self, other):
        inc, exc = _norm_args_notimplemented(other)
        if inc is NotImplemented:
            return NotImplemented
        if self._included is None:
            if exc is None:  # - +
                self._excluded |= inc
            else:  # - -
                self._included, self._excluded = exc - self._excluded, None
        else:
            if inc is None:  # + -
                self._included &= exc
            else:  # + +
                self._included.difference_update(inc)
        return self

    def __eq__(self, other):
        return (
                       type(self) is type(other)
                       and self._included == other._included
                       and self._excluded == other._excluded) or (
                       type(other) in (set, frozenset) and self._included == other)

    def __hash__(self):
        return hash(self._included) ^ hash(self._excluded)

    def __len__(self):
        if self._included is not None:
            return len(self._included)
        raise NotImplementedError('complemented sets have undefined length')

    def __iter__(self):
        if self._included is not None:
            return iter(self._included)
        raise NotImplementedError('complemented sets have undefined contents')

    def __bool__(self):
        if self._included is not None:
            return bool(self._included)
        return True

    __nonzero__ = __bool__  # py2 compat
