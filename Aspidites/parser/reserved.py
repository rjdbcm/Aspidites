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
    'curried'
]
indent = '    '
nl_indent = '\n' + indent
sep = ", "
pragma = Literal("#").setParseAction(replaceWith('@')).setName('pragma')
private_def_decl = Literal("(").setParseAction(replaceWith("def ")).setName("function declarator")
args_end = Group(Literal(")") + Literal(")")).setParseAction(replaceWith(") -> ")).setName("return annotation")
underscore = Literal("_").setName("lambda variable")
lparen, rparen, lbrack, rbrack, lbrace, rbrace, colon, comma = map(Suppress, "()[]{}:,")
lit_lparen, lit_rparen, lit_lbrack, lit_rbrack, lit_lbrace, lit_rbrace, lit_colon, lit_comma = map(str, "()[]{}:,")
bool_literal = oneOf("True False", asKeyword=True).setParseAction(lambda s, l, t: t[0] == "True").setName('boolean literal')
nullit = oneOf("/0 ø Ø").setParseAction(replaceWith("__undefined()")).setName('nullity')
signop = Literal("+") | Literal("-")
multop = Literal("*") | oneOf("/ //") | Literal("%") | Literal("@")
plusop = Literal("+") | Literal("-")
exponp = Literal("**")
factop = Literal("!")
bitwiseop = Regex(r"<<|>>|&|\||\^").setName("bitwise operator")
andop = Literal('&&').setParseAction(replaceWith(' and '))
orop = Literal('||').setParseAction(replaceWith(' or '))
comparisonop = andop | orop | Regex(">=|<=|>|<|==").setName("comparison operator")
assign_eq = Literal("=").setName('assignment')
noclosure = Literal("...").setName('ellipsis')  # That's no closure
index_items = Literal("[!]").setName('index trigram')
keys = Literal("[@]").setName('keys trigram')
persist = Literal("[.]").setParseAction(replaceWith('.persistent()')).setName('persist trigram')
count_vals = Literal("[#]").setName('count trigram')
set_add = Literal("[$]").setName('set trigram')
discard = Literal("[%]").setName('discard trigram')
copy = Literal("[&]").setName('copy trigram')
append = Literal("[^]").setName('copy trigram')
update = Literal("[+]").setName('update trigram')
remove = Literal("[*]").setName('remove trigram')
match_none = Literal("(!)").setParseAction(replaceWith('__match')).setName('match trigram')
context_stmt = Literal("<!>").setParseAction(replaceWith("with ")).setName('context trigram')
return_none = Literal("<*>").setParseAction(replaceWith("return ")).setName('return trigram')
yield_none = Literal("<^>").setParseAction(replaceWith("yield ")).setName('yield trigram')
for_none = Literal("<@>").setParseAction(replaceWith('for ')).setName('loop trigram')
pass_stmt = Literal("<#>").setParseAction(replaceWith('pass')).setName('pass trigram')
cont_stmt = Literal("<$>").setParseAction(replaceWith('continue')).setName('continue trigram')
break_stmt = Literal("<%>").setParseAction(replaceWith('break')).setName('break trigram')
if_cond = Literal('<?>').setParseAction(replaceWith('if ')).setName('conditional trigram')
respects = Keyword("->").setParseAction(lambda s, l, t: ":").setName('contract assignment')
imposes = Keyword("<-").setParseAction(lambda s, l, t: "__new_contract").setName('contract imposition')
struct_main = Keyword("main:").setParseAction(replaceWith('if __name__ == "__main__":'))

