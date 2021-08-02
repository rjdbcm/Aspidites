import inspect
from collections.abc import Callable as ACallable
from collections.abc import Iterable, Mapping
from enum import Enum
from itertools import zip_longest
from typing import Any, Callable, Generic
from typing import Pattern as RegexPattern
from typing import Tuple, TypeVar

from pyrsistent import PVector, ny, pvector, v

from Aspidites._vendor.pampy.helpers import (BoxedArgs, HeadType, PaddedValue,
                                             TailType, UnderscoreType,
                                             get_extra,
                                             get_lambda_args_error_msg,
                                             get_real_type, is_dataclass,
                                             is_generic, is_newtype,
                                             is_typing_stuff, is_union,
                                             pairwise, peek)
from Aspidites.monads import Undefined

T = TypeVar('T')
ANY = ny
HEAD = HeadType()
REST = TAIL = TailType()


def run(action, var):
    if callable(action):
        if isinstance(var, Iterable):
            try:
                return action(*var)
            except TypeError as err:
                raise MatchError(get_lambda_args_error_msg(action, var, err))
        elif isinstance(var, BoxedArgs):
            return action(var.get())
        else:
            return action(var)
    else:
        return action


def match_value(pattern, value) -> Tuple[bool, PVector]:
    if value is PaddedValue:
        return False, v()
    elif is_typing_stuff(pattern):
        return match_typing_stuff(pattern, value)
    elif isinstance(pattern, (int, float, str, bool, Enum)):
        eq = pattern == value
        type_eq = type(pattern) == type(value)
        return eq and type_eq, v()
    elif pattern is None:
        return value is None, v()
    elif isinstance(pattern, type):
        if isinstance(value, pattern):
            return True, pvector([value])
    elif isinstance(pattern, (list, tuple)):
        return match_iterable(pattern, value)
    elif isinstance(pattern, dict):
        return match_dict(pattern, value)
    elif callable(pattern):
        return_value = pattern(value)

        if isinstance(return_value, bool):
            return return_value, pvector([value])
        elif isinstance(return_value, tuple) and len(return_value) == 2 \
                and isinstance(return_value[0], bool) and isinstance(return_value[1], list):
            return return_value
        else:
            raise MatchError("Warning! pattern function %s is not returning a boolean "
                             "nor a tuple of (boolean, list), but instead %s" %
                             (pattern, return_value))
    elif isinstance(pattern, RegexPattern):
        rematch = pattern.search(value)
        if rematch is not None:
            return True, pvector(rematch.groups())
    elif pattern is ANY:
        return True, pvector([value])
    elif pattern is HEAD or pattern is TAIL:
        raise MatchError("HEAD or TAIL should only be used inside an Iterable (list or tuple).")
    elif is_dataclass(pattern) and pattern.__class__ == value.__class__:
        return match_dict(pattern.__dict__, value.__dict__)
    return False, v()


def match_dict(pattern, value) -> Tuple[bool, PVector]:
    if not isinstance(value, dict) or not isinstance(pattern, dict):
        return False, v()

    total_extracted = []
    still_usable_value_keys = set(value.keys())
    still_usable_pattern_keys = set(pattern.keys())
    for pkey, pval in pattern.items():
        if pkey not in still_usable_pattern_keys:
            continue
        matched_left_and_right = False
        for vkey, vval in value.items():
            if vkey not in still_usable_value_keys:
                continue
            if pkey not in still_usable_pattern_keys:
                continue
            key_matched, key_extracted = match_value(pkey, vkey)
            if key_matched:
                value_matched, value_extracted = match_value(pval, vval)
                if value_matched:
                    total_extracted += key_extracted + value_extracted
                    matched_left_and_right = True
                    still_usable_pattern_keys.remove(pkey)
                    still_usable_value_keys.remove(vkey)
                    break
        if not matched_left_and_right:
            return False, v()
    return True, pvector(total_extracted)


def only_padded_values_follow(padded_pairs, i):
    i += 1
    while i < len(padded_pairs):
        pattern, value = padded_pairs[i]
        if pattern is not PaddedValue:
            return False
        i += 1
    return True


def match_iterable(patterns, values) -> Tuple[bool, PVector]:
    if not isinstance(patterns, Iterable) or not isinstance(values, Iterable):
        return False, v()

    total_extracted = []
    padded_pairs = list(zip_longest(patterns, values, fillvalue=PaddedValue))

    for i, (pattern, value) in enumerate(padded_pairs):
        if pattern is HEAD:
            if i != 0:
                raise MatchError("HEAD can only be in first position of a pattern.")
            else:
                if value is PaddedValue:
                    return False, v()
                else:
                    total_extracted += [value]
        elif pattern is TAIL:
            if not only_padded_values_follow(padded_pairs, i):
                raise MatchError("TAIL must me in last position of the pattern.")
            else:
                tail = [value for (pattern, value) in padded_pairs[i:] if value is not PaddedValue]
                total_extracted.append(tail)
                break
        else:
            matched, extracted = match_value(pattern, value)
            if not matched:
                return False, v()
            else:
                total_extracted += extracted
    return True, pvector(total_extracted)


def match_typing_stuff(pattern, value) -> Tuple[bool, PVector]:
    if pattern == Any:
        return match_value(ANY, value)
    elif is_union(pattern):
        for subpattern in pattern.__args__:
            is_matched, extracted = match_value(subpattern, value)
            if is_matched:
                return True, extracted
        else:
            return False, v()
    elif is_newtype(pattern):
        return match_value(pattern.__supertype__, value)
    elif is_generic(pattern):
        return match_generic(pattern, value)
    else:
        return False, v()


def match_generic(pattern: Generic[T], value) -> Tuple[bool, PVector]:
    if get_extra(pattern) == type:       # Type[int] for example
        real_value = None
        if is_newtype(value):
            real_value = value
            value = get_real_type(value)
        if not inspect.isclass(value):
            return False, pvector([])

        type_ = pattern.__args__[0]
        if type_ == Any:
            return True, pvector([real_value or value])
        if is_newtype(type_):   # NewType case
            type_ = get_real_type(type_)

        if issubclass(value, type_):
            return True, pvector([real_value or value])
        else:
            return False, pvector([])

    elif get_extra(pattern) == ACallable:
        if callable(value):
            spec = inspect.getfullargspec(value)
            annotations = spec.annotations
            artgtypes = [annotations.get(arg, Any) for arg in spec.args]
            ret_type = annotations.get('return', Any)
            if pattern == Callable[[*artgtypes], ret_type]:
                return True, pvector([value])
            else:
                return False, pvector([])
        else:
            return False, pvector([])

    elif get_extra(pattern) == tuple:
        return match_value(pattern.__args__, value)

    elif issubclass(get_extra(pattern), Mapping):
        type_matched, _captured = match_value(get_extra(pattern), value)
        if not type_matched:
            return False, pvector([])
        k_type, v_type = pattern.__args__

        key_example = peek(value)
        key_matched, _captured = match_value(k_type, key_example)
        if not key_matched:
            return False, pvector([])

        value_matched, _captured = match_value(v_type, value[key_example])
        if not value_matched:
            return False, pvector([])
        else:
            return True, pvector([value])

    elif issubclass(get_extra(pattern), Iterable):
        type_matched, _captured = match_value(get_extra(pattern), value)
        if not type_matched:
            return False, pvector([])
        v_type, = pattern.__args__
        v = peek(value)
        value_matched, _captured = match_value(v_type, v)
        if not value_matched:
            return False, pvector([])
        else:
            return True, pvector([value])
    else:
        return False, pvector([])


def match(var, *args, **kwargs):  # , default=NoDefault, strict=True
    """
    Match `var` against a number of potential patterns.

    Example usage:
    ```
    match(x,
        3,              "this matches the number 3",
        int,            "matches any integer",
        (str, int),     lambda a, b: "a tuple (a, b) you can use in a function",
        [1, 2, ANY],      "any list of 3 elements that begins with [1, 2]",
        {'x': ANY},       "any dict with a key 'x' and any value associated",
        ANY,              "anything else"
    )
    ```

    :param var: The variable to test patterns against.
    :param args: Alternating patterns and actions. There must be an action for every pattern specified.
                 Patterns can take many forms, see README.md for examples.
                 Actions can be either a literal value or a callable which will be called with the arguments that were
                    matched in corresponding pattern.
    :param default: If `default` is specified then it will be returned if none of the patterns match.
                    If `default` is unspecified then a `MatchError` will be thrown instead depending on the setting of strict.
    :return: The result of the action which corresponds to the first matching pattern.
    """
    if len(args) % 2 != 0:
        raise MatchError("Every guard must have an action.")

    default = False if 'default' not in kwargs.keys() else kwargs['default']
    strict = True if 'strict' not in kwargs.keys() else kwargs['strict']

    pairs = list(pairwise(args))
    patterns = [patt for (patt, action) in pairs]

    for patt, action in pairs:
        matched_as_value, args = match_value(patt, var)

        if matched_as_value:
            lambda_args = args if len(args) > 0 else BoxedArgs(var)
            return run(action, lambda_args)

    if default is False and strict:
        if ANY not in patterns:
            return Undefined()
    else:
        return default


class MatchError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
