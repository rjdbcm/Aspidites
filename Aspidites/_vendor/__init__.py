from pyrsistent import v
from .fn import *
from .apm import match, InstanceOf

__all__ = v("F",  # BEGIN func.py
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
            "tco",
            "stackless",
            "Stream",
            "_",
            "reduce",
            "filterfalse",
            "zip_longest",
            "match",
            "InstanceOf"
            )
