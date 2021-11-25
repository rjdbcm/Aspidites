from .func import F, curried
from .underscore import shortcut as _
from .iters import (
    take,
    drop,
    takelast,
    droplast,
    consume,
    nth,
    first_true,
    iterate,
    padnone,
    ncycles,
    repeatfunc,
    grouper,
    group_by,
    roundrobin,
    partition,
    splitat,
    splitby,
    powerset,
    pairwise,
    iter_suppress,
    flatten,
    accumulate,
    chain,
    combinations,
    cycle,
    dropwhile,
    islice,
    repeat,
    starmap,
    takewhile,
    tee,
)
from .op import call, apply, flip, curry, zipwith, foldl, foldr, unfold


from functools import reduce
from itertools import filterfalse
from itertools import zip_longest

__version__ = "0.5.2"

__all__ = [
    "F",  # BEGIN func.py
    "curried",  # END func.py
    "take",  # BEGIN iters.py
    "drop",
    "takelast",
    "droplast",
    "consume",
    "nth",
    "first_true",
    "iterate",
    "padnone",
    "ncycles",
    "repeatfunc",
    "grouper",
    "group_by",
    "roundrobin",
    "partition",
    "splitat",
    "splitby",
    "powerset",
    "pairwise",
    "iter_suppress",
    "flatten",
    "accumulate",  # END iters.py
    "call",  # BEGIN op.py
    "apply",
    "flip",
    "curry",
    "zipwith",
    "foldl",
    "foldr",
    "unfold",  # END op.py
    "_",
    "reduce",
    "filterfalse",
    "zip_longest",
    "chain",
    "combinations",
    "cycle",
    "dropwhile",
    "islice",
    "repeat",
    "starmap",
    "takewhile",
    "tee",
]
