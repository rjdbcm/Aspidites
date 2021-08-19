# Aspidites is Copyright 2021, Ross J. Duff.
# See LICENSE.txt for more info.
from pyparsing import (
    Combine,
    Empty,
    FollowedBy,
    Forward,
    Group,
    Keyword,
    Literal,
    OneOrMore,
    OnlyOnce,
    Optional,
    ParseElementEnhance,
    ParseException,
    Regex,
    Suppress,
    Word,
    alphanums,
    alphas,
    col,
    conditionAsParseAction,
    delimitedList,
    infixNotation,
    matchOnlyAtCol,
    nums,
    oneOf,
    opAssoc,
    quotedString,
    replaceWith,
    unicodeString,
)

from Aspidites._vendor.contracts import contract, new_contract
from Aspidites._vendor.contracts.syntax import contract_expression

_contract_expression = contract_expression.copy()
_contract_expression.setParseAction(lambda tks: f"'{''.join((str(t) for t in tks))}'")

available_pragmas = [
    'cython.binding',
    'cython.boundscheck',
    'cython.wraparound',
    'cython.initializedcheck',
    'cython.nonecheck',
    'cython.overflowcheck',
    'cython.overflowcheck.fold',
    'cython.embedsignature',
    'cython.cdivision',
    'cython.cdivision_warnings',
    'cython.always_allow_keywords',
    'cython.c_api_binop_methods',
    'cython.profile',
    'cython.linetrace',
    'cython.infer_types',
    'cython.type_version_tag',
    'cython.unraisable_tracebacks',
    'cython.iterable_coroutine',
    'cython.emit_code_comments',
    'cython.cpp_locals',
    'cython.optimize.use_switch',
    'cython.optimize.unpack_method_calls',
    'cython.warn.undeclared',
    'cython.warn.unreachable',
    'cython.warn.maybe_uninitialized',
    'cython.warn.unused',
    'cython.warn.unused_arg',
    'cython.warn.unused_result',
    'cython.warn.multiple_declarators'
]


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


def cvt_real(t):
    return float(t[0])


def cvt_tuple(t):
    return "(" + ", ".join(t.asList()) + ")"


def cvt_dict(t):
    t = t.asList()
    for i, v in enumerate(t):
        key, val = v
        if isinstance(key, str):  # string keys only
            t[i] = f"{key}: {val}"
        else:  # integer key
            t[i] = f"{key}: {val}"
    t = f'{", ".join(t)}'
    return f"pmap({{{t}}})"


def cvt_list(t):
    t = t.asList()
    for i, v in enumerate(t):
        if isinstance(v, str):  # string keys only
            t[i] = v
        else:  # integer key
            t[i] = int(v)
    t = f'{", ".join(t)}'
    return f"pvector([{t}])"


def cvt_set(t):
    t = t.asList()
    for i, v in enumerate(t):
        if isinstance(v, str):  # string keys only
            t[i] = v
        else:  # integer key
            t[i] = int(v)
    t = f'{", ".join(t)}'
    return f"pset({{{t}}})"


def cvt_contract_assign(t):
    t = swap_val_to_idx(list(t), ":", 1)
    t[2], t[4] = t[4], t[2]
    return " ".join((str(t) for t in t))


def cvt_contract_define(t):
    t[0], t[1] = t[1], t[0]
    t[1] = "'" + t[1] + "'"
    args = f"({', '.join(t[1:])})"
    t = t[0] + args
    return "".join(t)


# TODO: ADD cvtSimpleDefine


def swap_val_to_idx(lst: list, val, idx: int) -> list:
    val_idx = lst.index(val)
    if val_idx == idx:
        pass  # maybe error?
    lst[val_idx], lst[idx] = lst[idx], lst[val_idx]
    return lst


lparen, rparen, lbrack, rbrack, lbrace, rbrace, colon, comma = map(Suppress, "()[]{}:,")
unistr = unicodeString().setParseAction(lambda t: t[0][2:-1])
quoted_str = quotedString().setParseAction(lambda t: t[0])
bool_literal = oneOf("True False", asKeyword=True).setParseAction(cvt_bool)
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
suite = Forward()
rvalue = Forward()
stmt = Forward()
underscore = Literal("_")
identifier = Word(alphas + "-_", alphanums + "-_").setName("VAR_ID")
operand = complex_ | real | integer | identifier | underscore

signop = oneOf("+ -")
multop = oneOf("* / %")
plusop = oneOf("+ -")
exponp = Literal("**")
factop = Literal("!")


def cvt_arith_expr(tks):
    expr = "".join((str(t) for t in tks))
    if "/" in expr:
        return "Maybe(SafeDiv, " + expr.replace("/", ", ") + ")"
    elif "%" in expr:
        return "Maybe(SafeMod, " + expr.replace("%", ", ") + ")"
    elif "**" in expr:
        return "Maybe(SafeExp, " + expr.replace("**", ", ") + ")"


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
        lpar="(",
        rpar=")",
    )
).setParseAction(cvt_arith_expr)


comparisonop = oneOf("< <= > >= != ==")
comp_expr = infixNotation(
    arith_expr,
    [
        (comparisonop, 2, opAssoc.LEFT),
    ],
)

list_item = (
    real
    | arith_expr
    | integer
    | identifier
    | complex_
    | quoted_str
    | unistr
    | bool_literal
    | null
    | list_str
    | set_str
    | tuple_str
    | dict_str
    | comp_expr
)

eq = Literal("=")
respects = Keyword("->").setParseAction(lambda t: ":")
imposes = Keyword("<-").setParseAction(lambda t: "new_contract")


identifier = Word(alphas + "_", alphanums + "_")
contract_define = identifier + imposes + _contract_expression  #  ^ funcCall
contract_define.setParseAction(cvt_contract_define)
contract_respect = respects + _contract_expression
contract_assign = identifier + eq + list_item + contract_respect
contract_assign.setParseAction(cvt_contract_assign)

tuple_str <<= (
    lparen + Optional(delimitedList(list_item)) + Optional(comma) + rparen
).setParseAction(cvt_tuple)

list_str <<= (
    lbrack + Optional(delimitedList(list_item) + Optional(comma)) + rbrack
).setParseAction(cvt_list)

set_str <<= (
    lbrace + Optional(delimitedList(list_item) + Optional(comma)) + rbrace
).setParseAction(cvt_set)

dict_entry = Group(list_item + colon + list_item)
dict_str <<= (
    lbrace + Optional(delimitedList(dict_entry) + Optional(comma)) + rbrace
).setParseAction(cvt_dict)


private_def_decl = Literal("(").setParseAction(replaceWith("def "))
def_args = Optional(delimitedList(contract_assign, delim=";")).setParseAction(
    lambda t: ", ".join(t)
)
args_end = Group(Literal(")") + Literal(")")).setParseAction(replaceWith(") -> "))
def_args = Group("(" + def_args + args_end).setParseAction(lambda t: "".join(*t))

std_decor = "@contract()\n"


def cvt_pragma(tks):
    t: list = tks.asList()
    return '\n'.join(t) + '\n'

pragmas = Combine(
    Literal("#").setParseAction(replaceWith('@'))
    + oneOf(' '.join(available_pragmas))
    + '(' + oneOf('True False') + ')'
).setParseAction(cvt_pragma)
func_decl = Group(Optional(OneOrMore(pragmas)) +
    private_def_decl + identifier + def_args + _contract_expression
).setParseAction(lambda t: std_decor + "".join(*t) + ":")
comment_line = (
    Combine(Regex(r"`(?:[^`\n\r\\]|(?:``)|(?:\\(?:[^x]|x[0-9a-fA-F]+)))*") + "`")
    .setParseAction(lambda t: t[0])
    .setParseAction(
        lambda s, loc, t: "# comment_line %s:"
        % (len([c for c in s[:loc] if c == "\n"]) + 1)
        + t[0]
    )
)
for_loop = Literal("<@>").setParseAction(replaceWith("for "))
return_none = Literal("<*>").setParseAction(replaceWith("return "))
yield_none = Literal("<^>").setParseAction(replaceWith("yield "))
return_value = return_none + rvalue
yield_value = yield_none + rvalue
ret_stmt = Group(return_value).setParseAction(lambda t: "".join(*t))
yield_stmt = Group(yield_value).setParseAction(lambda t: "".join(*t))
func_def = Group(func_decl + suite).setParseAction(
    lambda t: "\n    ".join(t[0]) + "\n\n"
)
pass_stmt = Keyword("pass").setParseAction(lambda t: str(*t))
sep = ", "
lambda_def = Combine(Group("(" + arith_expr | comp_expr + ")"))
func_call = Group(
    identifier + "(" + Optional(delimitedList(rvalue)) + ")"
).setParseAction(
    lambda t: "Maybe" + t[0][1] + t[0][0] + sep + sep.join(t[0][2:-1]) + t[0][-1] + "()"
)  # if len(t[0]) != 3 else t[0][0] + '()')
clos_call = Group(
    identifier + "(" + Optional(delimitedList(rvalue)) + ")"
).setParseAction(
    lambda t: "Maybe" + t[0][1] + t[0][0] + sep + sep.join(t[0][2:-1]) + t[0][-1]
) + Suppress(
    Literal("...")
)

suite << IndentedBlock(
    (
        comment_line
        | pass_stmt
        | ret_stmt
        | yield_stmt
        | func_call
        | func_def
        | contract_assign
    )
).setParseAction(lambda t: ("\n    ".join(t.asList())))


def cvt_for_stmt(toks):
    for t in toks:
        t[0], t[1] = t[1], t[0]
        t.insert(2, " in ")
        t.append(":")
    return "".join(*toks)


# for_stmt = Group(delimitedList(identifier) + for_loop + tuple_str | list_str |
#                  funcCall).setParseAction(cvt_for_stmt)
rvalue << (clos_call | func_call | list_item | lambda_def)
simple_assign << Group(identifier + "=" + rvalue).setParseAction(
    lambda t: " ".join(t[0])
)
stmt << (func_def | contract_define | func_call | simple_assign | comment_line)

_main = Keyword("main:").setParseAction(replaceWith('if __name__ == "__main__":')) + OneOrMore(stmt).setParseAction(lambda t: '    ' + '\n    '.join(t))

module_body = OneOrMore(stmt) + Optional(_main)

@new_contract
def woma_module(text: 'str'):
    try:
        module_body.parseString(text, parseAll=True)
    except ParseException as e:
        raise ValueError(str(e))
    else:
        return True

@contract
def parse_module(module: 'woma_module'):
    return module_body.parseString(module, parseAll=True)


# if __name__ == "__main__":
#     print(parse_module(open('../examples/math.wom').read()))
