import dataclasses
import warnings
import os


@dataclasses.dataclass(frozen=True)
class Switches:
    # ALWAYS ON
    disable_all = False


def all_disabled():
    """ Returns true if all contracts checks are disabled. """
    return Switches.disable_all

