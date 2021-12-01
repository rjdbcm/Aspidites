# cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=False, initializedcheck=False
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
import cython

from .syntax import ParseException
from .library.extensions import CheckCallableWithSelf
from .library import CheckCallable, Extension, SeparateContext, identifier_expression, CheckType
from .inspection import can_accept_self, can_accept_at_least_one_argument
from .interface import (
    ContractException,
    ContractSyntaxError,
    Where,
    describe_value,
)
from .parser import parse_contract_string_actual, Storage
from .syntax import contract_expression
from .inspection import getfullargspec


def get_annotations(function):
    return getfullargspec(function).annotations


def get_all_arg_names(function):
    spec = getfullargspec(function)
    possible = spec.args + [spec.varargs, spec.varkw] + spec.kwonlyargs
    all_args = [x for x in possible if x]
    return all_args


@cython.ccall
@cython.inline
def new_contract_impl(identifier, condition):
    msg: str

    # Be friendly
    if not isinstance(identifier, str):
        msg = "I expect the identifier to be a string; received %s." % describe_value(
            identifier
        )
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
            msg = (
                "Invalid identifier %r; it overwrites an already known "
                "expression. In fact, I can parse it as %s (%r)." % (identifier, c, c)
            )
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
        where = Where(identifier, character=loc)  # line=e.lineno, column=e.col)
        # msg = 'Error in parsing string: %s' % e
        msg = (
            "The given identifier %r does not correspond to my idea "
            "of what an identifier should look like;\n%s\n%s" % (identifier, e, where)
        )
        raise ValueError(msg)

    # Now let's check the condition
    if isinstance(condition, str):
        # We assume it is a condition that should parse cleanly
        try:
            # could call parse_flexible_spec as well here
            if condition in Storage.string2contract:
                bare_contract = Storage.string2contract[condition]
            try:
                c = contract_expression.parseString(condition, parseAll=True)[0]
                assert hasattr(c, "__contract__"), "Want Contract, not %r" % c
                if '$' not in condition:
                    Storage.string2contract[condition] = c
                bare_contract = c
            except Exception as e:
                msg = "%s" % e
                if hasattr(e, "loc"):  # ParseBaseException
                    where = Where(condition, character=e.loc)
                    raise ContractSyntaxError(msg, where=where)
                else:
                    raise  # ContractDefinitionError
        except ContractSyntaxError as e:
            msg = "The given condition %r does not parse cleanly: %s" % (condition, e)
            raise ValueError(msg)
    # Important: types are callable, so check this first.
    elif hasattr(condition, "__weakrefoffset__"):
        # parse_flexible_spec can take care of types
        if hasattr(
                condition, "__contract__"
        ):  # isinstance(spec, Contract) substitute using the __contract__ slot
            bare_contract = condition
        elif hasattr(condition, "__weakrefoffset__"):  # isinstance(spec, type)
            bare_contract = CheckType(condition)
        elif isinstance(condition, str):
            bare_contract = parse_contract_string_actual(condition)
        else:
            msg = "I want either a string or a type, not %s." % describe_value(condition)
            raise ContractException(msg)

    # Lastly, it should be a callable
    elif hasattr(condition, "__call__"):
        # Check that the signature is right
        if can_accept_self(condition):
            bare_contract = CheckCallableWithSelf(condition)
        elif can_accept_at_least_one_argument(condition):
            bare_contract = CheckCallable(condition)
        else:
            raise ValueError(
                "The given callable %r should be able to accept "
                "at least one argument" % condition
            )
    else:
        raise ValueError(
            "I need either a string or a callable for the "
            "condition; found %s." % describe_value(condition)
        )

    # Separate the context if needed
    if isinstance(bare_contract, (CheckCallable, CheckCallableWithSelf)):
        contract = bare_contract
    else:
        contract = SeparateContext(bare_contract)

    # It's okay if we define the same thing twice
    if identifier in Extension.registrar:
        old = Extension.registrar[identifier]
        if not (contract == old):
            msg = (
                "Tried to redefine %r with a definition that looks "
                "different to me.\n" % identifier
            )
            msg += " - old: %r\n" % old
            msg += " - new: %r\n" % contract
            raise ValueError(msg)
    else:
        Extension.registrar[identifier] = contract

    return contract
