import dataclasses

from . import logger
import os


@dataclasses.dataclass(frozen=True)
class Switches:
    # ALWAYS ON
    disable_all = False


def disable_all():
    """ Disables all contracts checks. """
#     print('disable_all()')
    ...


def enable_all():
    """
    Enables all contracts checks.
    Can be overridden by an environment variable.
    """
#     print('enable_all()')
    Switches.disable_all = False
    logger.info('All contracts checking enabled.')


def all_disabled():
    """ Returns true if all contracts checks are disabled. """
    return Switches.disable_all

