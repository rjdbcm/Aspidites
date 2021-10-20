# -*- coding: utf-8 -*-

import platform

from pytest import raises

from Aspidites.woma.setutils import _MISSING, complement


_IS_26 = platform.python_version().startswith('2.6')


def test_complement_set():
    '''exercises a bunch of code-paths but doesn't really confirm math identities'''
    assert complement(complement(set())) == set()
    sab = set('ab')
    sbc = set('bc')
    cab = complement('ab')
    cbc = complement('bc')
    cc = complement('c')
    sc = set('c')
    u = complement(set())
    assert repr(sab) in repr(cab)
    # non-mutating tests
    assert cab != cbc
    assert complement(cab) == sab
    assert complement(cbc) == sbc
    assert 'a' not in cab
    assert 'c' in cab
    assert (sab & cbc) == (sab - sbc)  # set theory invariant
    assert not (cab < sab)  # complement never subset of set
    if not _IS_26: assert not (sab < cab)
    assert not (cbc < sab)
    assert not (cbc < cab)  # not subsets of each other
    if not _IS_26: assert sab < cc
    assert cab < (cab | cbc)
    assert (cab | cbc) > cab
    assert cc > sab
    assert not (cab > sab)
    assert not cab.isdisjoint(cc)  # complements never disjoint
    assert cab.isdisjoint(sab)
    assert not cab.isdisjoint(sc)
    assert (cab | sab) == u
    assert (cab | cc) == u
    assert (cab | cbc) == complement('b')
    assert (sab | cab) == (cbc | sbc)
    assert (sab & cab) == (cbc & sbc)
    assert (sab ^ cab) == (cbc ^ sbc)
    assert cab - cc == sc
    assert cab - sab == cab
    assert sab - cab == sab
    assert (cab ^ cbc | set('b')) == (sab | sbc)
    everything = complement(frozenset())
    assert everything in everything  # https://en.wikipedia.org/wiki/Russell%27s_paradox
    assert bool(cab)
    assert not complement(u)
    # destructive testing
    cab ^= sab
    cab ^= sab
    cab &= sab
    cab &= cbc
    cab |= sab
    cab |= cbc
    cab -= sab
    cab.add(5)
    cab.remove(5)
    cab.update(sab)
    cab.discard(sab)
    cab.update(cbc)
    cab.add(complement(frozenset()))  # frozen complement can be a member of complement set
    assert len({complement(frozenset()): 1, complement(frozenset()): 2}) == 1  # hash works
    with raises(NotImplementedError): cab.pop()
    with raises(NotImplementedError): len(cab)
    with raises(NotImplementedError): iter(cab)
    ~cab
    cab.complement()
    cab.complemented()
    class OpOverloader(object):
        # tests that operators properly return NotImplemented so they will defer to
        # another class implementation if available
        def __and__(self, other): return self
        __rand__ = __iand__ = __or__ = __ror__ = __ior__ = __xor__ = __rxor__ = __sub__ = __isub__ = __and__
        def __le__(self, other): return True
        __lt__ = __ge__ = __gt__ = __le__

    ops = OpOverloader()
    def opsmash(a, b):
        a &= b; a |= b; a -= b; a ^= b
        a > b; a >= b; a < b; a <= b
        return (((a & b) | b) - b) ^ b

    with raises(TypeError): opsmash(cab, object())
    assert opsmash(ops, cab) == ops
    assert opsmash(cab, ops) == ops
