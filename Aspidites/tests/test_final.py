import pytest as pt
from Aspidites.final import final, heritable
from Aspidites._vendor.contracts import ContractNotRespected


@final()
class A:
    pass


class B:
    pass


class C:
    pass


c = final(C)


def test_final_classes():
    with pt.raises(ContractNotRespected):

        class D(A):
            pass

        class D(c(C)):
            pass


def test_heritable_clause():
    assert not heritable((A,))
    assert heritable((B,))
