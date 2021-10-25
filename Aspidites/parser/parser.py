# cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=True, initializedcheck=False
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
from Aspidites._vendor.pyparsing import (
    IndentedBlock,
    Combine,
    Empty,
    FollowedBy,
    Forward,
    ZeroOrMore,
    OneOrMore,
    MatchFirst,
    Optional,
    ParseElementEnhance,
    ParseException,
    Regex,
    Char,
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

list_str = Forward()
list_str_evolver = Forward()
set_str = Forward()
set_str_evolver = Forward()
dict_str = Forward()
dict_str_evolver = Forward()
tuple_str = Forward()
slice_str = Forward()
simple_assign = Forward()
func_call = Forward()
suite = Forward()
rvalue = Forward()
stmt = Forward()

quoted_str = quotedString().setParseAction(lambda t: t[0])
integer = Word(nums).setParseAction(cvt_int)
real = Combine(Optional(Word(nums)) + "." + Word(nums))
complex_ = Combine(real | integer + "+" + real | integer + "j")
identifier = Word(alphas + "_", alphanums + "_")
operand = nullit | complex_ | real | bool_literal | integer | identifier | underscore
arith_expr = Combine(
    infixNotation(
        operand,
        [
            (factop, 1, opAssoc.LEFT),
            (exponp, 2, opAssoc.RIGHT),
            (signop, 1, opAssoc.RIGHT),  # Changing this to LEFT causes the entire parser to break
            (multop, 2, opAssoc.LEFT),
            (plusop, 2, opAssoc.LEFT),
            (bitwiseop, 2, opAssoc.LEFT),
        ],
        lpar=lit_lparen,
        rpar=lit_rparen,
    )
).setParseAction(cvt_arith_expr)
comp_expr = infixNotation(
    arith_expr,
    [
        (comparisonop, 2, opAssoc.LEFT),
    ],
).setParseAction(lambda t: ''.join(t[0]))

list_item = (  # Precedence important!!!
        slice_str
        | comp_expr  # Expressions
        | arith_expr
        | identifier
        | integer  # Literals
        | complex_
        | real
        | bool_literal
        | nullit
        | quoted_str
        | list_str_evolver
        | set_str_evolver
        | dict_str_evolver
        | list_str
        | set_str
        | tuple_str
        | dict_str
)

lit_ellipse = Literal("...").setParseAction(replaceWith('...'))
assignable = func_call | list_item | lit_ellipse

_contract_expression = contract_expression.copy()
_contract_expression.setParseAction(lambda tks: f"'{''.join((str(t) for t in tks))}'")
contract_define = identifier + imposes + _contract_expression
contract_define.setParseAction(cvt_contract_define)
contract_respect = respects + _contract_expression
contract_assign = identifier + assign_eq + assignable + contract_respect
contract_assign.setParseAction(cvt_contract_assign)

tuple_str <<= (lparen + Optional(delimitedList(list_item)) + Optional(comma) + rparen).setParseAction(cvt_tuple)
noclosure.setParseAction(replaceWith('.evolver()'))
list_str <<= (lbrack + Optional(delimitedList(list_item) + Optional(comma)) + rbrack).setParseAction(cvt_list)
list_str_evolver <<= ((lbrack + Optional(delimitedList(list_item) + Optional(comma)) + rbrack).setParseAction(
    cvt_list) + noclosure).setParseAction(lambda t: ''.join(t))
set_str <<= (lbrace + Optional(delimitedList(list_item) + Optional(comma)) + rbrace).setParseAction(cvt_set)
set_str_evolver <<= ((lbrace + Optional(delimitedList(list_item) + Optional(comma)) + rbrace).setParseAction(
    cvt_set) + noclosure).setParseAction(lambda t: ''.join(t))
dict_entry = Group(list_item + colon + list_item)
dict_str <<= (lbrace + Optional(delimitedList(dict_entry) + Optional(comma)) + rbrace).setParseAction(cvt_dict)
dict_str_evolver <<= ((lbrace + Optional(delimitedList(dict_entry) + Optional(comma)) + rbrace).setParseAction(
    cvt_dict) + noclosure).setParseAction(lambda t: ''.join(t))
slice_str <<= identifier + lit_lbrack + (integer | identifier) + Optional(
    lit_colon + (integer | identifier)) + lit_rbrack
slice_str.setParseAction(lambda t: ''.join(str(i) for i in t))
def_args = Optional(delimitedList(contract_assign, delim=";")).setParseAction(lambda t: sep.join(t))
def_args = Group(lit_lparen + def_args + args_end).setParseAction(lambda t: "".join(*t))

bool_pragmas = Combine(
    pragma + oneOf(' '.join(available_bool_pragmas)) + lit_lparen + oneOf('True False') + lit_rparen
).setParseAction(cvt_pragma)

pragmas = Combine(pragma + oneOf(' '.join(available_pragmas))).setParseAction(cvt_pragma)

func_decl = Group(
    Optional(OneOrMore(bool_pragmas) | OneOrMore(pragmas)) +
    private_def_decl + identifier + def_args + _contract_expression).setParseAction(lambda t: "\n@contract()\n" + "".join(*t) + lit_colon)
comment_line = (Combine(Regex(r"`(?:[^`\n\r\\]|(?:``)|(?:\\(?:[^x]|x[0-9a-fA-F]+)))*") + "`").setParseAction(lambda t: t[0]).setParseAction(cvt_comment_line))

return_value = return_none + rvalue
yield_value = yield_none + rvalue
ret_stmt = Group(return_value).setParseAction(lambda t: "".join(*t))
yield_stmt = Group(yield_value).setParseAction(lambda t: "".join(*t))

func_def = Group(func_decl + suite).setParseAction(lambda t: nl_indent.join(t[0]) + "\n")
lambda_def = Combine(Group(lit_lparen + arith_expr | comp_expr + lit_rparen))
func_call <<= Group(identifier + lit_lparen + Optional(delimitedList(rvalue)) + lit_rparen).setParseAction(
    cvt_func_call)  # if len(t[0]) != 3 else t[0][0] + '()')
clos_call = Group(identifier + lit_lparen + Optional(delimitedList(rvalue)) + lit_rparen).setParseAction(
    cvt_clos_call) + Suppress(noclosure)
context_suite = Forward()
context_def = Group(context_stmt + func_call).setParseAction(lambda t: ''.join(*t) + lit_colon)

context_decl = Group(context_def + context_suite).setParseAction(
    lambda t: ''.join(*t))

# TODO (!): trigram only binds a single letter variable identifier
case_stmt = Group(assignable + colon + func_call).setParseAction(lambda t: sep.join(t[0]))
match_suite = Group(IndentedBlock(OneOrMore(case_stmt))).setParseAction(lambda t: (sep.join(t.asList()[0])))
match_decl = Group(match_none + identifier).setParseAction(lambda t: t[0][1] + '=' + t[0][0] + lit_lparen + t[0][1])
match_def = Group(match_decl + match_suite).setParseAction(lambda t: sep.join(t[0]) + lit_rparen)

loop_suite = Forward()

ident_loop_decl = Group(identifier + Optional(lit_comma + identifier) + for_none + identifier).setParseAction(
    cvt_for_loop_decl)
ident_loop_def = Group(ident_loop_decl + loop_suite).setParseAction(base_parse_action)

list_loop_decl = Group(identifier + Optional(lit_comma + identifier) + for_none + list_str).setParseAction(
    cvt_for_loop_decl)
list_loop_def = Group(list_loop_decl + loop_suite).setParseAction(base_parse_action)

set_loop_decl = Group(identifier + Optional(lit_comma + identifier) + for_none + set_str).setParseAction(
    cvt_for_loop_decl)
set_loop_def = Group(set_loop_decl + loop_suite).setParseAction(base_parse_action)

tuple_loop_decl = Group(identifier + Optional(lit_comma + identifier) + for_none + tuple_str).setParseAction(
    cvt_for_loop_decl)
tuple_loop_def = Group(tuple_loop_decl + loop_suite).setParseAction(base_parse_action)

dict_loop_decl = Group(identifier + Optional(lit_comma + identifier) + for_none + dict_str).setParseAction(
    cvt_for_loop_decl)
dict_loop_def = Group(dict_loop_decl + loop_suite).setParseAction(base_parse_action)

string_loop_decl = Group(identifier + Optional(lit_comma + identifier) + for_none + quoted_str).setParseAction(
    cvt_for_loop_decl)
string_loop_def = Group(string_loop_decl + loop_suite).setParseAction(base_parse_action)

func_loop_decl = Group(identifier + Optional(lit_comma + identifier) + for_none + func_call).setParseAction(
    cvt_for_loop_decl)
func_loop_def = Group(func_loop_decl + loop_suite).setParseAction(lambda t: (nl_indent + indent).join(t[0]))

loop_suite <<= IndentedBlock(
    OneOrMore(pass_stmt
              | cont_stmt
              | break_stmt
              | func_call
              ))
# TODO context managers get eaten by the preceding code blocks
context_suite <<= IndentedBlock(OneOrMore(contract_assign
                                          | match_def
                                          | func_call)).setParseAction(
    lambda t: (nl_indent.join(t.asList())))

suite <<= IndentedBlock(
    OneOrMore(pass_stmt
              | ret_stmt
              | yield_stmt
              | ident_loop_def
              | string_loop_def
              | list_loop_def
              | set_loop_def
              | tuple_loop_def
              | dict_loop_def
              | func_loop_def
              | match_def
              | contract_assign)).setParseAction(
    lambda t: (nl_indent.join(t.asList())))
rvalue <<= clos_call | func_call | list_item | lambda_def
simple_assign << Group(identifier + assign_eq + rvalue).setParseAction(lambda t: " ".join(t[0]))
stmt <<= (func_def | contract_define | simple_assign)
module_body = OneOrMore(stmt) + Optional(
    struct_main + OneOrMore(stmt).setParseAction(lambda t: indent + nl_indent.join(t)))
module_body.ignore(comment_line)


def parse_module(module):
    return module_body.parseString(module, parseAll=True)


def parse_statement(s):
    return stmt.parseString(s)

# if __name__ == "__main__":
#     print(parse_module(open('../examples/math.wom').read()))
