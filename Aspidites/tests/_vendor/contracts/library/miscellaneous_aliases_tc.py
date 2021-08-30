from . import good, fail
import hypothesis
import hypothesis.strategies as st
import pytest as pt
from pyrsistent import pvector, pmap, pset


fail('Container', 1)
good('Hashable', 1)
fail('Iterable', 1)
fail('Sized', lambda: None)
good('Sequence', '')
good('Sized', '')
good('Callable', lambda: None)


@hypothesis.given(x=st.lists(st.text() | st.binary()))
def random_sequence(x):
    good('Container', [*x])
    good('Hashable', pvector([*x]))
    # counterexample?
    good('Iterable', [*x])
    good('Iterable', pvector([*x]))
    good('Iterator', [*x].__iter__())
    fail('Iterator', [*x])
    good('Sized', [*x])
    good('Sized', pvector([*x]))
    fail('Callable', [*x])
    good('Sequence', [*x])
    good('Sequence', pvector([*x]))
    good('Sequence', set(x))
    good('Set', {*x})
    good('Set', pset([*x]))
    fail('Set', [*x])
    good('MutableSequence', [*x])
    good('MutableSequence', pvector([*x]).evolver())
    fail('MutableSequence', (*x, ))
    good('MutableSet', {*x})
    good('MutableSet', pset([*x]).evolver())
    fail('MutableSet', pset([*x]))
    fail('MutableSet', frozenset([*x]))


random_sequence()


@hypothesis.given(x=st.dictionaries(st.text(), st.binary()) | st.fixed_dictionaries({}))
def random_mappings(x):
    good('Mapping', {**x})
    good('Mapping', pmap({**x}))
    fail('Mapping', [x])
    fail('Mapping', pvector([x]))
    good('MutableMapping', {**x})
    good('MutableMapping', pmap({**x}).evolver())
    good('Iterable', pmap({**x}))
    good('Iterable', {**x})
    fail('Sequence', {**x})
    fail('Sequence', pmap({**x}))
    good('Sized', pmap({**x}))
    good('Sized', {**x})
    # good('MappingView', {}.keys())
    good('Sized', {**x}.keys())
    good('Sized', pmap({**x}).keys())
    # good('ItemsView', {}.items())
    good('Sized', {**x}.items())
    good('Sized', pmap({**x}).items())
    # good('ValuesView', {}.values())
    good('Sized', {**x}.values())
    good('Sized', pmap({**x}).values())


random_mappings()
