# Aspidites
# Copyright (C) 2021 Ross J. Duff

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from pyparsing import (
    Combine,
    Empty,
    FollowedBy,
    Forward,
    OneOrMore,
    Optional,
    ParseElementEnhance,
    ParseException,
    Regex,
    Word,
    alphanums,
    alphas,
    col,
    conditionAsParseAction,
    delimitedList,
    infixNotation,
    matchOnlyAtCol,
    nums,
    opAssoc,
    quotedString,
    unicodeString,
)

from .._vendor.contracts.syntax import contract_expression
from ..parser.convert import *

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


unistr = unicodeString().setParseAction(lambda t: t[0][2:-1])
quoted_str = quotedString().setParseAction(lambda t: t[0])
integer = Word(nums).setParseAction(cvt_int)
real = Combine(Word(nums) + "." + Word(nums))
complex_ = Combine(real | integer + "+" + real | integer + "j")
list_str = Forward()
list_str_evolver = Forward()
set_str = Forward()
set_str_evolver = Forward()
dict_str = Forward()
dict_str_evolver = Forward()
tuple_str = Forward()
simple_assign = Forward()
# for_stmt = Forward()
suite = Forward()
rvalue = Forward()
stmt = Forward()
identifier = Word(alphas + "_", alphanums + "_")
operand = nullit | complex_ | real | bool_literal | integer | identifier | underscore
arith_expr = Combine(
    infixNotation(
        operand,
        [
            (factop, 1, opAssoc.LEFT),
            (exponp, 2, opAssoc.RIGHT),
            (signop, 1, opAssoc.RIGHT),
            (multop, 2, opAssoc.LEFT),
            (plusop, 2, opAssoc.LEFT),
        ],
        lpar=lit_lparen,
        rpar=lit_rparen,
    )
).setParseAction(cvt_arith_expr)
comp_expr = infixNotation( # This does not work dear god
    arith_expr,
    [
        (comparisonop, 2, opAssoc.LEFT),
    ],
)

list_item = (  # Precedence important!!!
    comp_expr  # Expressions
    | arith_expr
    | identifier
    | integer  # Literals
    | complex_
    | real
    | quoted_str
    | unistr
    | bool_literal
    | nullit
    | list_str_evolver
    | set_str_evolver
    | dict_str_evolver
    | list_str  # Collections
    | set_str
    | tuple_str
    | dict_str
)
contract_define = identifier + imposes + _contract_expression  #  ^ funcCall
contract_define.setParseAction(cvt_contract_define)
contract_respect = respects + _contract_expression
contract_assign = identifier + assign_eq + list_item + contract_respect
contract_assign.setParseAction(cvt_contract_assign)
tuple_str <<= (lparen + Optional(delimitedList(list_item)) + Optional(comma) + rparen).setParseAction(cvt_tuple)
list_str <<= (lbrack + Optional(delimitedList(list_item) + Optional(comma)) + rbrack).setParseAction(cvt_list)
list_str_evolver <<= ((lbrack + Optional(delimitedList(list_item) + Optional(comma)) + rbrack).setParseAction(cvt_list) + noclosure.setParseAction(replaceWith('.evolver()'))).setParseAction(lambda t: ''.join(t))
set_str <<= (lbrace + Optional(delimitedList(list_item) + Optional(comma)) + rbrace).setParseAction(cvt_set)
set_str_evolver <<= ((lbrace + Optional(delimitedList(list_item) + Optional(comma)) + rbrace).setParseAction(cvt_set) + noclosure.setParseAction(replaceWith('.evolver()'))).setParseAction(lambda t: ''.join(t))
dict_entry = Group(list_item + colon + list_item)
dict_str <<= (lbrace + Optional(delimitedList(dict_entry) + Optional(comma)) + rbrace).setParseAction(cvt_dict)
dict_str_evolver <<= ((lbrace + Optional(delimitedList(dict_entry) + Optional(comma)) + rbrace).setParseAction(cvt_dict) + noclosure.setParseAction(replaceWith('.evolver()'))).setParseAction(lambda t: ''.join(t))
def_args = Optional(delimitedList(contract_assign, delim=";")).setParseAction(lambda t: sep.join(t))
def_args = Group(lit_lparen + def_args + args_end).setParseAction(lambda t: "".join(*t))
bool_pragmas = Combine(
    pragma + oneOf(' '.join(available_bool_pragmas)) + lit_lparen + oneOf('True False') + lit_rparen
).setParseAction(cvt_pragma)
func_decl = Group(
    Optional(OneOrMore(bool_pragmas)) + private_def_decl + identifier + def_args + _contract_expression
).setParseAction(lambda t: "\n@contract()\n" + "".join(*t) + lit_colon)
comment_line = (
    Combine(Regex(r"`(?:[^`\n\r\\]|(?:``)|(?:\\(?:[^x]|x[0-9a-fA-F]+)))*") + "`")
    .setParseAction(lambda t: t[0])
    .setParseAction(cvt_comment_line)
)
return_value = return_none + rvalue
yield_value = yield_none + rvalue
ret_stmt = Group(return_value).setParseAction(lambda t: "".join(*t))
yield_stmt = Group(yield_value).setParseAction(lambda t: "".join(*t))
func_def = Group(func_decl + suite).setParseAction(lambda t: nl_indent.join(t[0]))
lambda_def = Combine(Group(lit_lparen + arith_expr | comp_expr + lit_rparen))
func_call = Group(identifier + lit_lparen + Optional(delimitedList(rvalue)) + lit_rparen).setParseAction(cvt_func_call)  # if len(t[0]) != 3 else t[0][0] + '()')
clos_call = Group(identifier + lit_lparen + Optional(delimitedList(rvalue)) + lit_rparen).setParseAction(cvt_clos_call) + Suppress(noclosure)
elif_stmt = Group(list_item + "?!").setParseAction(lambda t: ' '.join(list(reversed(t.asList()))) + ":") + suite
else_stmt = Keyword("?!?").setParseAction(replaceWith('else:')) + suite
if_stmt = Group(list_item + "?").setParseAction(lambda t: ' '.join(list(reversed(t.asList()))) + ":") + suite
cond_stmt = if_stmt + Optional(elif_stmt) + Optional(else_stmt)
suite <<= IndentedBlock(
    OneOrMore(comment_line | pass_stmt | ret_stmt | yield_stmt | cond_stmt | func_call | func_def | contract_assign)).setParseAction(
    lambda t: (nl_indent.join(t.asList())))
rvalue <<= clos_call | func_call | list_item | lambda_def
simple_assign << Group(identifier + assign_eq + rvalue).setParseAction(lambda t: " ".join(t[0]))
stmt <<= func_def | contract_define | cond_stmt | func_call | simple_assign | comment_line
module_body = OneOrMore(stmt) + Optional(struct_main + OneOrMore(stmt).setParseAction(lambda t: indent + nl_indent.join(t)))


def parse_module(module):
    return module_body.parseString(module, parseAll=True)


# if __name__ == "__main__":
#     print(parse_module(open('../examples/math.wom').read()))
