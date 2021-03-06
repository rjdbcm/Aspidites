# cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=True, initializedcheck=False
import re

from .reserved import *
from Aspidites._vendor.pyparsing import ParserElement

pmap_re = re.compile(r"(pmap\(\{.*\}\))")
end = lit_rparen + lit_lparen + lit_rparen


def factorial(expr):
    expr = "__maybe(__safeFactorial, " + expr.replace("!", "", 1) + end
    if expr.count(end) > 1:
        expr = "__maybe(__safeFactorial, " + expr
    return expr


def expon(expr):
    a, op, b = expr.partition("**")
    expr = a + op + b.replace("**", end, 1) + sep
    if '__maybe' in expr:  # nesting
        expr = "__maybe(__safeExp, " + expr.replace("**", end + sep, 1) + end
        expr = ''.join(expr.rsplit(end + sep, 1))
    else:
        expr = "__maybe(__safeExp, " + expr.replace("**", sep, 1) + end
        if expr.count(end) > 1:
            expr = "__maybe(__safeExp, " + expr
    return expr


def floordiv(expr):
    a, op, b = expr.partition("//")
    expr = a + op + b.replace("//", end, 1) + sep
    if '__maybe' in expr:  # nesting
        expr = "__maybe(__safeFloorDiv, " + expr.replace("//", end + sep, 1) + end
        expr = ''.join(expr.rsplit(end + sep, 1))
    else:
        expr = "__maybe(__safeFloorDiv, " + expr.replace("//", sep, 1) + end
        if expr.count(end) > 1:
            expr = "__maybe(__safeFloorDiv, " + expr
    return expr


def div(expr):
    a, op, b = expr.partition("/")
    expr = a + op + b.replace("/", end + sep, 1)
    if '__maybe' in expr:  # nesting
        expr = "__maybe(__safeDiv, " + expr.replace("/", end + sep, 1) + end
        expr = ''.join(expr.rsplit(end + sep, 1))
    else:
        expr = "__maybe(__safeDiv, " + expr.replace("/", sep, 1) + end
        if expr.count(end) > 1:
            expr = "__maybe(__safeDiv, " + expr
    return expr


def mod(expr):
    a, op, b = expr.partition("%")
    expr = a + op + b.replace("%", end, 1) + sep
    if '__maybe' in expr:  # nesting
        expr = "__maybe(__safeMod, " + expr.replace("%", end + sep, 1) + end
        expr = ''.join(expr.rsplit(end + sep, 1))
    else:
        expr = "__maybe(__safeMod, " + expr.replace("%", sep, 1) + end
        if expr.count(end) > 1:
            expr = "__maybe(__safeMod, " + expr
    return expr


def mult(expr):
    a, op, b = expr.partition("*")
    expr = a + op + b.replace("*", end, 1) + sep
    if '__maybe' in expr:  # nesting
        expr = "__maybe(__safeMul, " + expr.replace("*", end + sep, 1) + end
        expr = ''.join(expr.rsplit(end + sep, 1))
    else:
        expr = "__maybe(__safeMul, " + expr.replace("*", sep, 1) + end
        if expr.count(end) > 1:
            expr = "__maybe(__safeMul, " + expr
    return expr


def sub(expr):
    a, op, b = expr.partition("-")
    expr = a + op + b.replace("-", end, 1) + sep
    if '__maybe' in expr:  # nesting
        expr = "__maybe(__safeSub, " + expr.replace("-", end + sep, 1) + end
        expr = ''.join(expr.rsplit(end + sep, 1))
    else:
        expr = "__maybe(__safeSub, " + expr.replace("-", sep, 1) + end
        if expr.count(end) > 1:
            expr = "__maybe(__safeSub, " + expr
    return expr


def add(expr):
    a, op, b = expr.partition("+")
    expr = a + op + b.replace("+", end, 1) + sep
    if '__maybe' in expr:  # nesting
        expr = "__maybe(__safeAdd, " + expr.replace("+", end + sep, 1) + end
        expr = ''.join(expr.rsplit(end + sep, 1))
    else:
        expr = "__maybe(__safeAdd, " + expr.replace("+", sep, 1) + end
        if expr.count(end) > 1:
            expr = "__maybe(__safeAdd, " + expr
    return expr


def double_negation(expr):
    return "__maybe(__safeUnaryAdd, " + expr.replace("+", "") + end


def single_negation(expr):
    return "__maybe(__safeUnarySub, " + expr.replace("-", "") + end


def cvt_arith_expr(s, loc, t):
    expr = "".join((str(i) for i in t))
    substr = ["!", "**", "//", "/", "%", '*' '-', '+']
    handler = {
        lambda x: "!" in x: factorial,
        lambda x: "**" in x: expon,
        lambda x: "*" in x: mult,
        lambda x: "//" in x: floordiv,
        lambda x: "/" in x: div,
        lambda x: "%" in x: mod,
        lambda x: x.startswith('-'): single_negation,
        lambda x: x.startswith('+'): double_negation,
        lambda x: "-" in x: sub,
        lambda x: "+" in x: add,
    }
    while any([s in expr for s in substr]):
        for k, v in handler.items():
            if k(expr):
                expr = v(expr)
    else:
        for k, v in handler.items():
            if k(expr):
                expr = v(expr)
    return expr


def cvt_pragma(s, loc, t):
    t: list = t.asList()
    return "\n".join(t) + "\n"


def cvt_int(s, loc, t):
    return int(t[0])


def cvt_real(s, loc, t):
    return float(t[0])


def cvt_tuple(s, loc, t):
    return "(" + ", ".join(t.asList()) + ")"


def cvt_comment_line(s, loc, t):
    return "# comment_line %s:" % (len([c for c in s[:loc] if c == "\n"]) + 1) + t[0]


def cvt_for_loop_decl(s, loc, t):
    t = t[0]
    if len(t) == 5:
        r = pmap_re.match(t[4])
        if r:
            m = r.group(1) + ".items()"
        else:
            m = t[4]
        s = str(t[3] + "".join(t[:3]) + " in __maybe(__safeLoop, " + m + end + lit_colon).encode("UTF-8")
    else:
        s = str(t[1] + t[0] + " in __maybe(__safeLoop, " + t[2] + end + lit_colon).encode("UTF-8")
    return s.decode("UTF-8")


def cvt_dict(s, loc, t):
    t: list = t.asList()
    s: bytes
    for i, v in enumerate(t):
        key, val = v
        if isinstance(key, str):  # string keys only
            t[i] = f"{key}: {val}"
        else:  # integer key
            t[i] = f"{key}: {val}"
    s = f'{", ".join(t)}'.encode("UTF-8")
    return f"__pmap({{{s.decode('UTF-8')}}})"


def cvt_list(s, loc, t):
    t: list = t.asList()
    s: bytes
    for i, v in enumerate(t):
        if isinstance(v, str):  # string keys only
            t[i] = v
        else:  # integer key
            t[i] = int(v)
    s = f'{", ".join(t)}'.encode("UTF-8")
    return f"__pvector([{s.decode('UTF-8')}])"


def cvt_list_index(s, loc, t):
    t = t.asList()
    arg = ''.join(t[2:])
    fn = ''.join(t[:2])
    return f"__maybe({fn}, {arg})()"


def cvt_set(s, loc, t):
    t: list = t.asList()
    s: bytes
    for i, v in enumerate(t):
        if isinstance(v, str):  # string keys only
            t[i] = v
        else:  # integer key
            t[i] = int(v)
    s = f'{", ".join(t)}'.encode("UTF-8")
    return f"__pset({{{s.decode('UTF-8')}}})"


def cvt_contract_assign(s, loc, t):
    t: list = t.asList()
    s: str
    i: str
    t = swap_val_to_idx(t, ":", 1)
    t[2], t[4] = t[4], t[2]
    s = " ".join((str(i) for i in t))
    return s


def cvt_contract_define(s, loc, t):
    t[0], t[1] = t[1], t[0]
    t[1] = "'" + t[1] + "'"
    args = f"({', '.join(t[1:])})"
    t = t[0] + args
    return "".join(t)


def swap_val_to_idx(lst: list, val, idx: int) -> list:
    val_idx = lst.index(val)
    if val_idx == idx:
        pass  # maybe error?
    lst[val_idx], lst[idx] = lst[idx], lst[val_idx]
    return lst


def cvt_clos_call(s, loc, t):
    return "__maybe" + t[0][1] + t[0][0] + sep + sep.join(t[0][2:-1]) + t[0][-1]


def cvt_func_call(s, loc, t):
    return (
        "__maybe"
        + t[0][1]
        + t[0][0]
        + sep
        + sep.join(t[0][2:-1])
        + t[0][-1]
        + lit_lparen
        + lit_rparen
    )
