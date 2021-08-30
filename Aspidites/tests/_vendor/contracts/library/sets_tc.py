from . import syntax_fail, good, fail, semantic_fail
from Aspidites._vendor.contracts.library.sets import ASet

good(repr(ASet.__init__(ASet(), length_contract='3', elements_contract='int')), {1, 2, 3})
good('set[3](int)', {1, 2, 3})
fail('set[3](int)', {1, 2})
semantic_fail('set[X](int)', 1)
syntax_fail('set')