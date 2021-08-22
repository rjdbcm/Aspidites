import pytest


def pytest_collection_modifyitems(items):
    """moves tests with raw shell output to the end."""

    slow_items = []
    end_items = []
    _items = items[:]

    for item in _items:
        if item.get_closest_marker("uses_stdout"):
            end_items.append(_items.pop(_items.index(item)))

        if item.get_closest_marker("parametrize"):
            slow_items.append(_items.pop(_items.index(item)))

    items[:] = _items + slow_items + end_items
