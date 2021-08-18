import pytest

from Aspidites._vendor.contracts.test_registrar import (good_examples, semantic_fail_examples,
                                                        contract_fail_examples)
from Aspidites._vendor.contracts import parse, ContractSyntaxError

import hypothesis
from hypothesis import strategies as st

# went from 89.9% to 95.7% contracts

# def main():
#     examples = test_get_all_strings()
#
#     differences = run_joker(examples)
#
#     diff = list(differences)
#     unfriendliness = sum(diff) / len(diff)
#
#     friendliness = 100 - 100 * unfriendliness
#     print("Friendliness: %.2f%% " % friendliness)


def replace_one(s, i, c):
    assert i >= 0 and i < len(s)
    return s[:i] + c + s[i + 1:]


@hypothesis.given(st.characters(whitelist_categories=['Me']))
def test_replace_one(c):
    assert replace_one('python', 1, c) == 'p%sthon' % c
    s = 'python'
    for i in range(len(s)):
        s2 = replace_one(s, i, c)
        s3 = replace_one(s2, i, s[i])
        assert s == s3, 'i=%d  %r -> %r -> %r' % (i, s, s2, s3)


all_strings = (good_examples + semantic_fail_examples + contract_fail_examples)
pre = (contract for contract, _, _ in all_strings)
strings = []
for i in pre:
    if isinstance(i, list):
        for j in i:
            strings += [j]
    else:
        strings += [i]


@pytest.mark.parametrize('s', strings)
def test_joke(s):
    parse(s)
    # now alter one letter
    for i in range(len(s)):
        s2 = replace_one(s, i, '~')
        try:
            parse(s2)
        except ContractSyntaxError as e:
            detected = e.where.col - 1
            displacement = i - detected
            #                if  displacement < 0:
            #                    print displacement
            #                    print e
            assert displacement >= 0

