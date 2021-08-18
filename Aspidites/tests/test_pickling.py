import warnings

import pytest

from .utils import check_contracts_fail, contract_strings,contract_fails_val
from Aspidites._vendor.contracts import parse, Contract
import pickle


@pytest.mark.parametrize('contract, values', contract_fails_val)
def test_exception_pickable(contract, values):
    exception = check_contracts_fail(contract, values)
    assert isinstance(exception, Exception)
    try:
        s = pickle.dumps(exception)
        pickle.loads(s)
    except (TypeError, AttributeError) as e:
        warnings.warn('While pickling: %s' % exception)
        if isinstance(e, AttributeError):
            return
        else:
            raise Exception(str(exception))
        # msg = 'Could not pickle exception.\n'
        # msg += str(exception)
        # msg += 'Raised: %s' % e
        # raise Exception(msg)


# def test_exceptions_are_pickable():
#     for contract, value, exact in semantic_fail_examples:  # @UnusedVariable
#         yield check_contracts_fail, contract, value, ContractNotRespected
#         #ContractSemanticError
#     for contract, value, exact in contract_fail_examples:  # @UnusedVariable
#         yield check_contracts_fail, contract, value, ContractNotRespected

@pytest.mark.parametrize('contract', contract_strings)
def test_contract_pickable(contract):
    c = parse(contract)
    assert isinstance(c, Contract)
    try:
        s = pickle.dumps(c)
        c2 = pickle.loads(s)
    except TypeError as e:
        msg = 'Could not pickle contract.\n'
        msg += '- string: %s\n' % c
        msg += '-   repr: %r\n' % c
        msg += 'Exception: %s' % e
        raise Exception(msg)

    assert c == c2


# def test_contracts_are_pickable():
#     allc = (good_examples + semantic_fail_examples + contract_fail_examples)
#     for contract, _, _ in allc:
#         if isinstance(contract, list):
#             for c in contract:
#                 yield check_contract_pickable, c
#         else:
#             yield check_contract_pickable, contract
