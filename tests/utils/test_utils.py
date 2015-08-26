import numpy

from qualipy.utils.utils import *


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


def test_clipping_percentage_doesnt_fail_for_all_zeros():
    assert clipping_percentage(numpy.zeros(10), 8, False) == 0


def test_clipping_percentage_works_for_under_threshold():
    assert abs(2 / 10. - clipping_percentage(numpy.ones(10), 2, False)) <= 0.001


def test_clipping_percentage_works_for_over_threshold():
    assert abs(2 / 10. - clipping_percentage(numpy.ones(10), 8, True)) <= 0.001


def test_scaled_prediction_works_for_extreme_values():
    assert scaled_prediction(-2) == 1
    assert scaled_prediction(2) == 0


def test_scaled_prediction_works_for_normal_values():
    assert abs(0.75 - scaled_prediction(-0.5)) <= 0.001
    assert abs(0.25 - scaled_prediction(0.5)) <= 0.001
    assert abs(0.5 - scaled_prediction(0)) <= 0.001
