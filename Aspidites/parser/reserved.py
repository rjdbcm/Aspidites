#cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=False, initializedcheck=False
from Aspidites._vendor.pyparsing import oneOf, Keyword, replaceWith, Literal, Suppress, Group, Regex

available_bool_pragmas = [
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
available_pragmas = [
    'cfunc',
    'ccall',
    'nogil',
    'no_gc',
    'inline',
]
indent = '    '
nl_indent = '\n' + indent
sep = ", "
pragma = Literal("#").setParseAction(replaceWith('@'))
private_def_decl = Literal("(").setParseAction(replaceWith("def "))
args_end = Group(Literal(")") + Literal(")")).setParseAction(replaceWith(") -> "))
underscore = Literal("_")
lparen, rparen, lbrack, rbrack, lbrace, rbrace, colon, comma = map(Suppress, "()[]{}:,")
lit_lparen, lit_rparen, lit_lbrack, lit_rbrack, lit_lbrace, lit_rbrace, lit_colon, lit_comma = map(str, "()[]{}:,")
bool_literal = oneOf("True False", asKeyword=True).setParseAction(lambda t: t[0] == "True")
nullit = Literal("/0").setParseAction(replaceWith("Undefined()"))
signop = Literal("+") | Literal("-")
multop = Literal("*") | oneOf("/ //") | Literal("%")
plusop = Literal("+") | Literal("-")
exponp = Literal("**")
factop = Literal("!")
bitwiseop = Regex(r"<<|>>|&|\||~|^").setName("bitwise operator")
comparisonop = Regex(">=|<=|!=|>|<|==").setName("operator")
assign_eq = Literal("=")
noclosure = Literal("...")  # That's no closure
match_none = Literal("(!)").setParseAction(replaceWith('__match'))
context_stmt = Literal("<!>").setParseAction(replaceWith("with "))
return_none = Literal("<*>").setParseAction(replaceWith("return "))
yield_none = Literal("<^>").setParseAction(replaceWith("yield "))
for_none = Literal("<@>").setParseAction(replaceWith('for '))
pass_stmt = Keyword("<#>").setParseAction(replaceWith('pass'))
cont_stmt = Keyword("<$>").setParseAction(replaceWith('continue'))
break_stmt = Keyword("<%>").setParseAction(replaceWith('break'))
respects = Keyword("->").setParseAction(lambda t: ":")
imposes = Keyword("<-").setParseAction(lambda t: "new_contract")
struct_main = Keyword("main:").setParseAction(replaceWith('if __name__ == "__main__":'))

