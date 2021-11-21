# cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=False, initializedcheck=False
from .interface import Where
from .syntax import contract_expression
from .interface import ContractSyntaxError


class Storage:
    # Cache storage
    string2contract = {}


def check_param_is_string(x):
    if not isinstance(x, str):
        msg = "Expected a string, obtained %s" % type(x)
        raise ValueError(msg)


def _cacheable(string, c):
    """Returns whether the contract c defined by string string is cacheable."""
    # XXX need a more general way of indicating
    #     whether a contract is safely cacheable
    return "$" not in string


def parse_contract_string_actual(string):
    msg: str
    where: Where
    check_param_is_string(string)
    if string in Storage.string2contract:
        return Storage.string2contract[string]
    try:
        c = contract_expression.parseString(string, parseAll=True)[0]
        assert hasattr(c, "__contract__"), "Want Contract, not %r" % c
        if _cacheable(string, c):
            Storage.string2contract[string] = c
        return c
    except Exception as e:
        msg = "%s" % e
        if hasattr(e, "loc"):  # ParseBaseException
            where = Where(string, character=e.loc)
            raise ContractSyntaxError(msg, where=where)
        else:
            raise  # ContractDefinitionError


def check_contracts(contracts, values, context_variables=None):
    """
    Checks that the values respect the contract.
    Not a public function -- no friendly messages.

    :param contracts: List of contracts.
    :type contracts:  ``list[N](str),N>0``

    :param values: Values that should match the contracts.
    :type values: ``list[N]``

    :param context_variables: Initial context
    :type context_variables: ``dict(str[1]: *)``

    :return: a Context variable
    :rtype: type(Context)

    :raise: ContractSyntaxError
    :raise: ContractNotRespected
    :raise: ValueError
    """
    assert isinstance(contracts, list)
    assert isinstance(contracts, list)
    assert len(contracts) == len(values)

    if context_variables is None:
        context_variables = {}

    for var in context_variables:
        if not (isinstance(var, str) and len(var) == 1):  # XXX: isalpha
            msg = (
                "Invalid name %r for a variable. "
                "I expect a string of length 1." % var
            )
            raise ValueError(msg)

    C = []
    for x in contracts:
        assert isinstance(x, str)
        C.append(parse_contract_string_actual(x))

    context = context_variables.copy()
    for i in range(len(contracts)):
        C[i]._check_contract(context, values[i], silent=False)

    return context

