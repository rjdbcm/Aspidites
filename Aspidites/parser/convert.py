import Cython

from .reserved import *


def cvt_arith_expr(tks):
    expr = "".join((str(t) for t in tks))
    if "//" in expr:
        return "Maybe(SafeFloorDiv, " + expr.replace("//", sep) + lit_rparen
    elif "/" in expr:
        return "Maybe(SafeDiv, " + expr.replace("/", sep) + lit_rparen
    elif "%" in expr:
        return "Maybe(SafeMod, " + expr.replace("%", sep) + lit_rparen
    elif "**" in expr:
        return "Maybe(SafeExp, " + expr.replace("**", sep) + lit_rparen
    elif expr.startswith('+'):
        return "Maybe(SafeUnaryAdd, " + expr.replace("+", sep) + lit_rparen
    elif expr.startswith('-'):
        return "Maybe(SafeUnaryAdd, " + expr.replace("-", sep) + lit_rparen


def cvt_pragma(tks):
    t: list = tks.asList()
    return '\n'.join(t) + '\n'


def cvt_int(t):
    return int(t[0])


def cvt_real(t):
    return float(t[0])


def cvt_tuple(t):
    return "(" + ", ".join(t.asList()) + ")"


def cvt_comment_line(s, loc, t):
    return "# comment_line %s:" % (len([c for c in s[:loc] if c == "\n"]) + 1) + t[0]


def cvt_dict(t):
    t: list = t.asList()
    s: bytes
    for i, v in enumerate(t):
        key, val = v
        if isinstance(key, str):  # string keys only
            t[i] = f"{key}: {val}"
        else:  # integer key
            t[i] = f"{key}: {val}"
    s = f'{", ".join(t)}'.encode('UTF-8')
    return f"pmap({{{s.decode('UTF-8')}}})"


def cvt_list(t):
    t: list = t.asList()
    s: bytes
    for i, v in enumerate(t):
        if isinstance(v, str):  # string keys only
            t[i] = v
        else:  # integer key
            t[i] = int(v)
    s = f'{", ".join(t)}'.encode('UTF-8')
    return f"pvector([{s.decode('UTF-8')}])"


def cvt_set(t):
    t: list = t.asList()
    s: bytes
    for i, v in enumerate(t):
        if isinstance(v, str):  # string keys only
            t[i] = v
        else:  # integer key
            t[i] = int(v)
    s = f'{", ".join(t)}'.encode('UTF-8')
    return f"pset({{{s.decode('UTF-8')}}})"


def cvt_contract_assign(t):
    t: list = t.asList()
    s: str
    i: str
    t = swap_val_to_idx(t, ":", 1)
    t[2], t[4] = t[4], t[2]
    s = " ".join((str(i) for i in t))
    return s


def cvt_contract_define(t):
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


def cvt_clos_call(t):
    return "Maybe" + t[0][1] + t[0][0] + sep + sep.join(t[0][2:-1]) + t[0][-1]


def cvt_func_call(t):
    return "Maybe" + t[0][1] + t[0][0] + sep + sep.join(t[0][2:-1]) + t[0][-1] + lit_lparen + lit_rparen
