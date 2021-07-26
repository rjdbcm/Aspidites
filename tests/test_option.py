import operator
import itertools
from Aspidites._vendor.fn import _, F
from Aspidites._vendor.fn import op


def test_unfold():
    doubler = op.unfold(lambda x: (x * 2, x * 2))
    assert list(itertools.islice(doubler(10), 0, 10)) == [20, 40, 80, 160, 320, 640,
                                                          1280, 2560, 5120, 10240]


def test_currying():
    def add(first):
        def add(second):
            return first + second

        return add

    assert 1 == op.curry(add, 0, 1)


def test_apply():
     assert 10, op.apply(operator.add, [2, 8])


def test_flip():
     assert 10 == op.flip(operator.sub)(2, 12)
     assert -10 == op.flip(op.flip(operator.sub))(2, 12)
    # flipping of flipped function should use optimization
     assert bool(operator.sub is op.flip(op.flip(operator.sub))) is True


def test_flip_with_shortcut():
     assert 10 == op.flip(_ - _)(2, 12)


def test_zipwith():
    zipper = op.zipwith(operator.add)
    assert [10, 11, 12] == list(zipper([0, 1, 2], itertools.repeat(10)))

    zipper = op.zipwith(_ + _)
    assert [10, 11, 12] == list(zipper([0, 1, 2], itertools.repeat(10)))

    zipper = F() << list << op.zipwith(_ + _)
    assert [10, 11, 12] == zipper([0, 1, 2], itertools.repeat(10))


def test_foldl():
    assert 10 == op.foldl(operator.add)([0, 1, 2, 3, 4])
    assert 20 == op.foldl(operator.add, 10)([0, 1, 2, 3, 4])
    assert 20 == op.foldl(operator.add, 10)(range(5))
    assert 10 == op.foldl(_ + _)(range(5))


def test_foldr():
    summer = op.foldr(operator.add)
    assert 10 == op.foldr(operator.add)([0, 1, 2, 3, 4])
    assert 20 == op.foldr(operator.add, 10)([0, 1, 2, 3, 4])
    assert 20 == op.foldr(operator.add, 10)(range(5))
    # specific case for right-side folding
    assert 100 == op.foldr(op.call, 0)([lambda s: s ** 2, lambda k: k + 10])
