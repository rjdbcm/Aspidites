from Aspidites._vendor._compat import basestring

from Aspidites._vendor.contracts.interface import (
    ContractSyntaxError,
    describe_value,
    ContractNotRespected,
)
from Aspidites._vendor.contracts.main import parse_contract_string, check_contracts

from Aspidites._vendor.contracts.test_registrar import (
    good_examples,
    semantic_fail_examples,
    contract_fail_examples,
)

all_strings = good_examples + semantic_fail_examples + contract_fail_examples
pre = (contract for contract, _, _ in all_strings)
contract_strings = []
for i in pre:
    if isinstance(i, list):
        for j in i:
            contract_strings += [j]
    else:
        contract_strings += [i]

pre = (contract for contract, _, _ in contract_fail_examples)
contract_fails = []
for i in pre:
    if isinstance(i, list):
        for j in i:
            contract_fails += [j]
    else:
        contract_fails += [i]

pre = ((contract, value) for contract, value, _ in contract_fail_examples)
contract_fails_val = []
for i, v in pre:
    if isinstance(i, list):
        for j in i:
            contract_fails_val += [(j, v)]
    else:
        contract_fails_val += [(i, v)]


def check_contracts_ok(contract, value):
    if isinstance(contract, basestring):
        contract = [contract]
        value = [value]
    context = check_contracts(contract, value)

    assert isinstance(context, dict)
    "%s" % context
    "%r" % context


def check_contracts_fail(contract, value, error=ContractNotRespected):
    """Returns the exception"""
    if isinstance(contract, basestring):
        contract = [contract]
        value = [value]

    try:
        context = check_contracts(contract, value)

        msg = "I was expecting that the values would not not" " satisfy the contract.\n"

        for v in value:
            msg += "      value: %s\n" % describe_value(v)

        for c in contract:
            cp = parse_contract_string(c)
            msg += "   contract: %r, parsed as %r (%s)\n" % (c, cp, cp)

        msg += "    context:  %r\n" % context

        raise Exception(msg)

    except error as e:
        # Try generation of strings:
        s = "%r" % e  # @UnusedVariable
        s = "%s" % e  # @UnusedVariable
        return e


def check_syntax_fail(string):
    assert isinstance(string, basestring)

    try:
        parsed_contract = parse_contract_string(string)
        msg = "I would not expect to parse %r." % string
        msg += " contract:         %s\n" % parsed_contract
        raise Exception(msg)

    except ContractSyntaxError as e:
        # Try generation of strings:
        s = "%r" % e  # @UnusedVariable
        s = "%s" % e  # @UnusedVariable
        pass
