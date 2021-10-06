
# class Extra:
#     loading = False
#
# def load_extra():
#     if not Extra.loading:
#         Extra.loading = True
# #         from . import useful_contracts
#         from .library import miscellaneous_aliases
#         # And after everything else is loaded, load the  utils
#     else:
#         print('already loading...')

def new_contract_impl(identifier, condition):
    from .._compat import basestring
    from .syntax import ParseException
    from .library.extensions import CheckCallableWithSelf
    from .library import (CheckCallable, Extension, SeparateContext,
        identifier_expression)
    from .interface import describe_value, Where, ContractSyntaxError
    from .inspection import can_accept_self, can_be_used_as_a_type, can_accept_at_least_one_argument

    # Be friendly
    if not isinstance(identifier, basestring):
        msg = 'I expect the identifier to be a string; received %s.' % describe_value(identifier)
        raise ValueError(msg)

    # Make sure it is not already an expression that we know.
    # (exception: allow redundant definitions. To this purpose,
    #   skip this test if the identifier is already known, and catch
    #   later if the condition changed.)
    if identifier in Extension.registrar:
        # already known as identifier; check later if the condition
        # remained the same.
        pass
    else:
        # check it does not redefine list, tuple, etc.
        try:
            c = parse_contract_string_actual(identifier)
            msg = ('Invalid identifier %r; it overwrites an already known '
                   'expression. In fact, I can parse it as %s (%r).' %
                   (identifier, c, c))
            raise ValueError(msg)
        except ContractSyntaxError:
            pass

    # Make sure it corresponds to our idea of identifier
    try:
        c = identifier_expression.parseString(identifier, parseAll=True)
    except ParseException as e:
        loc = e.loc
        if loc >= len(identifier):
            loc -= 1
        where = Where(identifier, character=loc)  #line=e.lineno, column=e.col)
        # msg = 'Error in parsing string: %s' % e
        msg = ('The given identifier %r does not correspond to my idea '
               'of what an identifier should look like;\n%s\n%s'
               % (identifier, e, where))
        raise ValueError(msg)

    # Now let's check the condition
    if isinstance(condition, basestring):
        # We assume it is a condition that should parse cleanly
        try:
            # could call parse_flexible_spec as well here
            bare_contract = parse_contract_string_actual(condition)
        except ContractSyntaxError as e:
            msg = ('The given condition %r does not parse cleanly: %s' %
                   (condition, e))
            raise ValueError(msg)
    # Important: types are callable, so check this first.
    elif can_be_used_as_a_type(condition):
        from .main import parse_flexible_spec
        # parse_flexible_spec can take care of types
        bare_contract = parse_flexible_spec(condition)
    # Lastly, it should be a callable
    elif hasattr(condition, '__call__'):
        # Check that the signature is right
        if can_accept_self(condition):
            bare_contract = CheckCallableWithSelf(condition)
        elif can_accept_at_least_one_argument(condition):
            bare_contract = CheckCallable(condition)
        else:
            raise ValueError("The given callable %r should be able to accept "
                             "at least one argument" % condition)
    else:
        raise ValueError('I need either a string or a callable for the '
                         'condition; found %s.' % describe_value(condition))

    # Separate the context if needed
    if isinstance(bare_contract, (CheckCallable, CheckCallableWithSelf)):
        contract = bare_contract
    else:
        contract = SeparateContext(bare_contract)

    # It's okay if we define the same thing twice
    if identifier in Extension.registrar:
        old = Extension.registrar[identifier]
        if not (contract == old):
            msg = ('Tried to redefine %r with a definition that looks '
                   'different to me.\n' % identifier)
            msg += ' - old: %r\n' % old
            msg += ' - new: %r\n' % contract
            raise ValueError(msg)
    else:
        Extension.registrar[identifier] = contract

    # Before, we check that we can parse it now
    # - not anymore, because since there are possible args/kwargs,
    # - it might be that the keyword alone is not a valid contract
    # if False:
    #     try:
    #         c = parse_contract_string(identifier)
    #         expected = Extension(identifier)
    #         assert c == expected, \
    #             'Expected %r, got %r.' % (c, expected)  # pragma: no cover
    #     except ContractSyntaxError:  # pragma: no cover
    #         #assert False, 'Cannot parse %r: %s' % (identifier, e)
    #         raise

    return contract


def parse_contract_string_actual(string):
    from .interface import (Contract, ContractDefinitionError, ContractSyntaxError,
        Where)
    from .main import Storage, _cacheable, check_param_is_string
    from .syntax import ParseException, ParseFatalException, contract_expression

    check_param_is_string(string)

    if string in Storage.string2contract:
        return Storage.string2contract[string]
    # TODO: This needs a total rewrite to avoid exception handling
    try:
        c = contract_expression.parseString(string,
                                            parseAll=True)[0]
        assert isinstance(c, Contract), 'Want Contract, not %r' % c
        if _cacheable(string, c):
            Storage.string2contract[string] = c
        return c
    except ContractDefinitionError as e:
        raise
    except ParseException as e:
        where = Where(string, character=e.loc)
        msg = '%s' % e
        raise ContractSyntaxError(msg, where=where)
    except ParseFatalException as e:
        where = Where(string, character=e.loc)
        msg = '%s' % e
        raise ContractSyntaxError(msg, where=where)


