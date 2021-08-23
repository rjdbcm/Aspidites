import pytest


def pytest_collection_modifyitems(items):
    """moves tests with raw shell output to the end."""

    fast_items = []
    slow_items = []
    end_items = []
    _items = items[:]

    for item in _items:
        if item.get_closest_marker("uses_stdout"):
            end_items.append(_items.pop(_items.index(item)))
            continue

        if item.get_closest_marker("parametrize"):
            slow_items.append(_items.pop(_items.index(item)))
            continue

        fast_items.append(_items.pop(_items.index(item)))

    items[:] = fast_items + slow_items + end_items
