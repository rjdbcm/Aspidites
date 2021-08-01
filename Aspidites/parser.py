import contextlib
import os.path
import sys

from Cython.Build import cythonize
from os import PathLike
from pyparsing import (
    ParseElementEnhance, oneOf, Optional, OneOrMore, OnlyOnce, Word,  alphanums, alphas,
    Suppress, unicodeString, quotedString, replaceWith, nums, Combine, Forward,
    FollowedBy, Literal, infixNotation, Keyword, opAssoc, Group, delimitedList, Regex, col,
    matchOnlyAtCol, Empty, conditionAsParseAction, ParseException
)
from string import Template
from pyrsistent import pvector, pset, pmap, PVector, PSet, PMap
from Aspidites._vendor.contracts.syntax import contract_expression, EqualTo
from Aspidites._vendor.contracts import new_contract, contract, ContractNotRespected

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


def cvt_bool(t):
    return t[0] == "True"


def cvt_int(t):
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
    t = t.asList()
    for i, v in enumerate(t):
        if isinstance(v, str):  # string keys only
            t[i] = v
        else:  # integer key
            t[i] = int(v)
    t = f'{", ".join(t)}'
    return f'pvector([{t}])'


def cvtSet(t):
    t = t.asList()
    for i, v in enumerate(t):
        if isinstance(v, str):  # string keys only
            t[i] = v
        else:  # integer key
            t[i] = int(v)
    t = f'{", ".join(t)}'
    return f'pset({{{t}}})'


def cvtContractAssign(t):
    t = swap_val_to_idx(list(t), COL, 1)
    t[2], t[4] = t[4], t[2]
    return ' '.join((str(t) for t in t))


def cvtContractDefine(t):
    t[0], t[1] = t[1], t[0]
    t[1] = "'" + t[1] + "'"
    args = f"({', '.join(t[1:])})"
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
boolLiteral = oneOf("True False", asKeyword=True).setParseAction(cvt_bool)
null = Keyword("None").setParseAction(replaceWith(None))
integer = Word(nums).setParseAction(cvt_int)
real = Combine(Word(nums) + "." + Word(nums))
complex_ = Combine(real | integer + "+" + real | integer + "j")
list_str = Forward()
set_str = Forward()
dict_str = Forward()
tuple_str = Forward()
simple_assign = Forward()
# for_stmt = Forward()
pass_stmt = Forward()
suite = Forward()
rvalue = Forward()
stmt = Forward()
underscore = Literal("_")
funcCall = Forward()
identifier = Word(alphas + "-_", alphanums + "-_").setName('VAR_ID')
operand = complex_ | real | integer | identifier | underscore

signop = oneOf("+ -")
multop = oneOf("* / %")
plusop = oneOf("+ -")
exponp = Literal("**")
factop = Literal("!")


def pre_eval(expr):
    if '/' in expr:
        return 'Maybe(SafeDiv, ' + expr.replace('/', ', ') + ')'
    elif '%' in expr:
        return 'Maybe(SafeMod, ' + expr.replace('%', ', ') + ')'


def cvt_arith_expr(tks):
    expr = ''.join((str(t) for t in tks))
    try:
        return pre_eval(expr)
    except ZeroDivisionError:
        return 'Undefined()'


arith_expr = Combine(infixNotation(
    operand,
    [
        (factop, 1, opAssoc.LEFT),
        (exponp,  2, opAssoc.RIGHT),
        (signop, 1, opAssoc.RIGHT),
        (multop, 2, opAssoc.LEFT),
        (plusop, 2, opAssoc.LEFT),
    ], lpar="(", rpar=")"
)).setParseAction(cvt_arith_expr)


comparisonop = oneOf("< <= > >= != ==")
comp_expr = infixNotation(
    arith_expr, [(comparisonop, 2, opAssoc.LEFT),]
)

listItem = (
        real
        | arith_expr
        | integer
        | identifier
        | complex_
        | quoted_str
        | unistr
        | boolLiteral
        | null
        | list_str
        | set_str
        | tuple_str
        | dict_str
        | comp_expr
)

EQ = Literal("=")
COL = ":"
respects = Keyword("->").setParseAction(lambda t: COL)
imposes = Keyword("<-").setParseAction(lambda t: 'new_contract')


identifier = Word(alphas + "_", alphanums + "_")
contract_define = identifier + imposes + _contract_expression #  ^ funcCall
contract_define.setParseAction(cvtContractDefine)
contract_respect = respects + _contract_expression
contract_assign = identifier + EQ + listItem + contract_respect
contract_assign.setParseAction(cvtContractAssign)

tuple_str <<= (
    lparen + Optional(delimitedList(listItem)) + Optional(comma) + rparen
).setParseAction(cvtTuple)

list_str <<= (
    lbrack + Optional(delimitedList(listItem) + Optional(comma)) + rbrack
).setParseAction(cvtList)

set_str <<= (
    lbrace + Optional(delimitedList(listItem) + Optional(comma)) + rbrace
).setParseAction(cvtSet)

dictEntry = Group(listItem + colon + listItem)
dict_str <<= (
    lbrace + Optional(delimitedList(dictEntry) + Optional(comma)) + rbrace
).setParseAction(cvtDict)


private_def_decl = Literal("(").setParseAction(replaceWith('def '))
def_args = Optional(delimitedList(contract_assign, delim=';')).setParseAction(lambda t:
                                                                              ', '.join(t))
args_end = Group(Literal(")") + Literal(")")).setParseAction(replaceWith(') -> '))
def_args = Group("(" + def_args + args_end).setParseAction(lambda t: ''.join(*t))

std_decor = '@contract()\n@cython.binding(True)\n'

funcDecl = Group(private_def_decl
                 + identifier
                 + def_args
                 + _contract_expression
                 ).setParseAction(lambda t: std_decor + ''.join(*t) + COL)
comment_line = Combine(
        Regex(
                r"`(?:[^`\n\r\\]|(?:``)|(?:\\(?:[^x]|x[0-9a-fA-F]+)))*") + "`"
    ).setParseAction(
        lambda t: t[0]
    ).setParseAction(
        lambda s, loc, t: '# comment_line %s:' % (len([c for c in s[:loc] if c == '\n']) + 1) + t[0])
for_loop = Literal("<@>").setParseAction(replaceWith('for '))
return_none = Literal("<*>").setParseAction(replaceWith('return '))
yield_none = Literal("<^>").setParseAction(replaceWith('yield '))
return_value = return_none + rvalue
yield_value = yield_none + rvalue
ret_stmt = Group(return_value).setParseAction(lambda t: ''.join(*t))
yield_stmt = Group(yield_value).setParseAction(lambda t: ''.join(*t))
funcDef = Group(funcDecl + suite).setParseAction(lambda t: '\n    '.join(t[0]) + '\n\n')
pass_stmt = Keyword("pass").setParseAction(lambda t: str(*t))
suite << IndentedBlock((comment_line | pass_stmt | ret_stmt | yield_stmt | funcCall | funcDef | contract_assign)).setParseAction(lambda t: ('\n    '.join(t.asList())))
sep = ', '
lambda_def = Combine(Group("(" + arith_expr | comp_expr + ")"))
funcCall = Group(identifier + "(" + Optional(delimitedList(rvalue)) + ")").setParseAction(lambda t: "Maybe" + t[0][1] + t[0][0] + sep + sep.join(t[0][2:-1]) + t[0][-1] + '()')  # if len(t[0]) != 3 else t[0][0] + '()')
closCall = Group(identifier + "(" + Optional(delimitedList(rvalue)) + ")").setParseAction(lambda t: "Maybe" + t[0][1] + t[0][0] + sep + sep.join(t[0][2:-1]) + t[0][-1]) + Suppress(Literal("..."))


def cvt_for_stmt(toks):
    for t in toks:
        t[0], t[1] = t[1], t[0]
        t.insert(2, " in ")
        t.append(":")
    return ''.join(*toks)


# for_stmt = Group(delimitedList(identifier) + for_loop + tuple_str | list_str |
#                  funcCall).setParseAction(cvt_for_stmt)
rvalue << (closCall | funcCall | listItem | lambda_def)
simple_assign << Group(identifier + "=" + rvalue).setParseAction(lambda t: ' '.join(t[0]))
stmt << (funcDef | contract_define | simple_assign | comment_line)

module_body = OneOrMore(stmt)


def parse_module(module, window_size=80):
    try:
        return module_body.parseString(module, parseAll=True)
    except ParseException as e:
        raise SyntaxError(str(e))


# if __name__ == "__main__":
#     print(parse_module(open('../examples/math.wom').read()))
