from Aspidites.tests._vendor.RestrictedPython.helper import restricted_exec


def test_RestrictingNodeTransformer__visit_Assert__1():
    """It allows assert statements."""
    restricted_exec('assert 1')
