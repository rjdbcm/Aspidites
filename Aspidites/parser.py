import os.path
import sys

from Cython.Build import cythonize
from os import PathLike
from pyparsing import (
    ParseElementEnhance, oneOf, Optional, OneOrMore, OnlyOnce, Word,  alphanums, alphas,
    Suppress, unicodeString, quotedString, replaceWith, nums, Combine, Forward,
    FollowedBy, Literal, infixNotation, Keyword, opAssoc, Group, delimitedList, Regex, col,
    matchOnlyAtCol, Empty, conditionAsParseAction
)
from string import Template
from pyrsistent import pvector, pset, pmap, PVector, PSet, PMap
from Aspidites.libraries.contracts.syntax import contract_expression, EqualTo
from Aspidites.libraries.contracts import new_contract, contract, ContractNotRespected
from Aspidites.libraries.RestrictedPython import safe_globals

_contract_expression = contract_expression.copy()
_contract_expression.setParseAction(lambda tks: f"'{''.join((str(t) for t in tks))}'")


class IndentedBlock(ParseElementEnhance):
    """
    Expression to match one or more expressions at a given indentation level.
    Useful for parsing text where structure is implied by indentation (like Python source code).
    """

    def __init__(self, expr, recursive=True):
        super().__init__(expr, savelist=True)
        self._recursive = recursive
        self.skipWhitespace = False

    def parseImpl(self, instring, loc, doActions=True):
        # see if self.expr matches at the current location - if not it will raise an exception
        # and no further work is necessary
        self.expr.parseImpl(instring, loc, doActions)

        indent_col = col(loc, instring)
        peer_parse_action = matchOnlyAtCol(indent_col)
        peer_expr = FollowedBy(self.expr).addParseAction(peer_parse_action)
        inner_expr = Empty() + peer_expr.suppress() + self.expr

        if self._recursive:
            indent_parse_action = conditionAsParseAction(
                lambda s, l, t, relative_to_col=indent_col: col(l, s) > relative_to_col
            )
            indent_expr = FollowedBy(self.expr).addParseAction(indent_parse_action)
            inner_expr += Optional(indent_expr + self)

        return OneOrMore(inner_expr).parseImpl(instring, loc, doActions)


def cvtBool(t):
    return t[0] == "True"


def cvtInt(t):
    return int(t[0])


def cvtReal(t):
    return float(t[0])


def cvtTuple(t):
    return '(' + ', '.join(t.asList()) + ')'


def cvtDict(t):
    t = t.asList()
    for i, v in enumerate(t):
        key, val = v
        if isinstance(key, str):  # string keys only
            t[i] = f"{key}: {val}"
        else:  # integer key
            t[i] = f"{key}: {val}"
    t = f'{", ".join(t)}'
    return f'pmap({{{t}}})'


def cvtList(t):
    return pvector(t.asList())


def cvtSet(t):
    pset(t.asList())


def cvtContractAssign(t):
    t = swap_val_to_idx(list(t), COL, 1)
    t[2], t[4] = t[4], t[2]
    return ''.join((str(t) for t in t))


def cvtContractDefine(t):
    t[0], t[1] = t[1], t[0]
    t[1] = "'" + t[1] + "'"
    args = f"({','.join(t[1:])})"
    t = t[0] + args
    return ''.join(t)

# TODO: ADD cvtSimpleDefine


def swap_val_to_idx(lst: list, val, idx: int) -> list:
    val_idx = lst.index(val)
    if val_idx == idx:
        pass # maybe error?
    lst[val_idx], lst[idx] = lst[idx], lst[val_idx]
    return lst


lparen, rparen, lbrack, rbrack, lbrace, rbrace, colon, comma = map(
    Suppress, "()[]{}:,"
)
unistr = unicodeString().setParseAction(lambda t: t[0][2:-1])
quoted_str = quotedString().setParseAction(lambda t: t[0])
boolLiteral = oneOf("True False", asKeyword=True).setParseAction(cvtBool)
null = Keyword("None").setParseAction(replaceWith(None))
integer = Word(nums).setParseAction(cvtInt)
real = Combine(Word(nums) + "." + Word(nums))
listStr = Forward()
dictStr = Forward()
tupleStr = Forward()
simple_assign = Forward()
for_stmt = Forward()
pass_stmt = Forward()
suite = Forward()
rvalue = Forward()
stmt = Forward()


identifier = Word(alphas + "-_", alphanums + "-_").setName('VAR_ID')
operand = real | integer | identifier

signop = oneOf("+ -")
multop = oneOf("* /")
plusop = oneOf("+ -")
exponp = Literal("**")
factop = Literal("!")

arith_expr = Combine(infixNotation(
    operand,
    [
        (factop, 1, opAssoc.LEFT),
        (exponp,  2, opAssoc.RIGHT),
        (signop, 1, opAssoc.RIGHT),
        (multop, 2, opAssoc.LEFT),
        (plusop, 2, opAssoc.LEFT),
    ], lpar="(", rpar=")"
)).setParseAction(lambda tks: ''.join((str(t) for t in tks)))

comparisonop = oneOf("< <= > >= != ==")
comp_expr = infixNotation(
    arith_expr, [(comparisonop, 2, opAssoc.LEFT),]
)

listItem = (
    real
    | arith_expr
    | integer
    | identifier
    | quoted_str
    | unistr
    | boolLiteral
    | null
    | Group(listStr)
    | tupleStr
    | dictStr
    | comp_expr
)

EQ = Literal("=")
COL = ":"
R_UMB = Keyword("->").setParseAction(lambda t: COL)
L_UMB = Keyword("<-").setParseAction(lambda t: 'new_contract')



identifier = Word(alphas + "-_", alphanums + "-_")
contract_define = identifier + L_UMB + _contract_expression #  ^ funcCall
contract_define.setParseAction(cvtContractDefine)
contract_respect = R_UMB + _contract_expression
contract_assign = identifier + EQ + listItem + contract_respect
contract_assign.setParseAction(cvtContractAssign)

tupleStr <<= (
    lparen + Optional(delimitedList(listItem)) + Optional(comma) + rparen
).setParseAction(cvtTuple)

listStr <<= (
    lbrack + Optional(delimitedList(listItem) + Optional(comma)) + rbrack
).setParseAction(cvtList, lambda t: t[0])

dictEntry = Group(listItem + colon + listItem)
dictStr <<= (
    lbrace + Optional(delimitedList(dictEntry) + Optional(comma)) + rbrace
).setParseAction(cvtDict)


private_def_decl = Literal("(").setParseAction(replaceWith('def '))
def_args = Optional(delimitedList(contract_assign, delim=';')).setParseAction(lambda t:
                                                                              ','.join(t))
args_end = Group(Literal(")") + Literal(")")).setParseAction(replaceWith(')'))
def_args = Group("(" + def_args + args_end).setParseAction(lambda t: ''.join(*t))

public = '@contract()\n@cython.binding(True)\n'

funcDecl = Group(private_def_decl + identifier + def_args).setParseAction(lambda t:
                                                                          public + ''.join(*t) + COL)
comment_line = Regex(r"^(?:.*)\`.*").suppress()
for_loop = Literal("<@>").setParseAction(replaceWith('for '))
return_none = Literal("<*>").setParseAction(replaceWith('return '))
return_value = return_none + rvalue
ret_stmt = Group(return_value).setParseAction(lambda t: ''.join(*t))
funcDef = Group(funcDecl + suite).setParseAction(lambda t: '\n\t'.join(t[0]))
pass_stmt = Keyword("pass").setParseAction(lambda t: str(*t))
suite << IndentedBlock((funcDef | contract_assign | for_stmt | ret_stmt | pass_stmt))
funcCall = Group(identifier + "(" + Optional(delimitedList(rvalue)) + ")").setParseAction(lambda t: "Maybe" + t[0][1] + t[0][0] + ',' + ','.join(t[0][2:-1]) + t[0][-1])


def cvt_for_stmt(toks):
    for t in toks:
        if t[0] in "pass":
            return "\tpass"
        t[0], t[1] = t[1], t[0]
        t.insert(2, " in ")
        t.append(":")
    return ''.join(*toks)


for_stmt = Group(delimitedList(identifier) + for_loop + tupleStr | listStr |
                 funcCall + suite | pass_stmt).setParseAction(cvt_for_stmt)
rvalue << (funcCall | listItem)
simple_assign << Group(identifier + "=" + rvalue).setParseAction(lambda t: ' '.join(t[0]))
stmt << (funcDef | contract_define | for_stmt | pass_stmt | simple_assign | comment_line)

module_body = OneOrMore(stmt)
parse_module = module_body.parseString

# reassign builtin collections contracts to check for pyrsistent version
new_contract('pmap', lambda x: isinstance(x, PMap))
new_contract('pvec', lambda x: isinstance(x, PVector))
new_contract('pset', lambda x: isinstance(x, PSet))
safe_globals.update({'contract': contract, 'pvec': PVector, 'pmap': PMap, 'pset': PSet})

