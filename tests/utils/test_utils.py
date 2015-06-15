import numpy

from imgfilter.utils.utils import *


def test_partition_matrix_returns_correct_number_of_partitions():
    mat = numpy.random.randn(100).reshape((10, 10))
    assert len(partition_matrix(mat, 3)) == 10


def test_flatten_returns_empty_list_for_empty_list():
    assert flatten([]) == []


def test_flatten_correctly_flattens_list():
    assert flatten([[1], [2, 3], [4, 5, 6]]) == [1, 2, 3, 4, 5, 6]


def test_normalize_returns_correct_values():
    assert (normalize([1., 1., 2., 3., 4., 4.]) ==
                      [0., 0., 1 / 3., 2 / 3., 1., 1.]).all()


def test_normalize_returns_ones_for_all_same_values():
    assert (normalize([5, 5, 5]) == [1, 1, 1]).all()
