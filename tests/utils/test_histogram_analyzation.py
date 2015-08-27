import numpy

from qualipy.utils.histogram_analyzation import *


def arrayNpEquals(arr1, arr2):
    if arr1.shape[0] != arr2.shape[0]:
        return False

    comp = arr1 == arr2
    for i in range(0, comp.shape[0]):
        if comp[i] != True:
            return False

    return True


def arrayEquals(arr1, arr2):
    if len(arr1) != len(arr2):
        return False

    comp = arr1 == arr2

    if type(comp) == bool:
        return comp

    for i in range(0, len(comp)):
        if comp[i] != True:
            return False

    return True


def test_remove_from_ends_with_valid_histogram():
    hist = numpy.array([1, 1, 0, 0, 0, 1, 1])
    assert len(remove_from_ends(hist).nonzero()[0]) == 0


def test_remove_from_ends_with_invalid_histogram():
    hist = numpy.array([1.0])
    assert arrayNpEquals(remove_from_ends(hist), hist)


def test_normalize_with_valid_histogram():
    hist = numpy.array([1, 2, 3, 2, 1])
    assert numpy.absolute(numpy.sum(normalize(hist)) - 1.0) < 0.00000001


def test_normalize_with_invalid_histogram():
    hist = numpy.array([])
    assert arrayNpEquals(normalize(hist), hist)


def test_calculate_continuous_distribution_with_valid_histogram():
    hist = numpy.array([1.0, 2.0, 3.0, 4.0])
    assert arrayNpEquals(calculate_continuous_distribution(hist),
                         numpy.array([1.0, 3.0, 6.0, 10.0]))


def test_continuous_distribution_with_invalid_histogram():
    hist = numpy.array([])
    assert arrayNpEquals(calculate_continuous_distribution(hist), hist)


def test_largest_with_valid_histogram():
    hist = numpy.array([2.0, 4.0, 1.0, 3.0])
    assert arrayNpEquals(largest(hist, 0.5), numpy.array([4.0, 3.0]))


def test_largest_with_invalid_histogram():
    hist = numpy.array([])
    assert arrayNpEquals(largest(hist, 0.5), numpy.array([]))


def test_calculate_derivatives_with_valid_histogram():
    hist = numpy.array([1, 2, 4, 2, 1])
    assert arrayNpEquals(calculate_derivatives(hist),
                         numpy.array([1.0, 2.0, -2.0, -1.0]))


def test_calculate_derivatives_with_invalid_histogram():
    hist = numpy.array([])
    assert arrayNpEquals(calculate_derivatives(hist), numpy.array([]))


def test_calculate_local_min_values_with_valid_histogram():
    hist = numpy.array([2.0, 1.0, 2.0, 4.0, 3.0, 2.0, 3.0])
    assert calculate_local_min_values(hist, 2) == \
        [LocationData(1, 1.0), LocationData(5, 2.0)]


def test_calculate_local_min_values_with_invalid_histogram():
    hist = numpy.array([])
    assert arrayEquals(calculate_local_min_values(hist, 2), [])


def test_calculate_local_max_values_with_valid_histogram():
    hist = numpy.array([2.0, 1.0, 2.0, 4.0, 3.0, 2.0, 3.0])
    assert calculate_local_max_values(hist) == [LocationData(3, 4.0)]


def test_calculate_local_max_values_with_invalid_histogram():
    hist = numpy.array([])
    assert arrayEquals(calculate_local_max_values(hist, 2), [])


def test_calculate_local_minimums_with_valid_histogram():
    hist = numpy.array([2.0, 1.0, 2.0, 4.0, 3.0, 2.0, 3.0])
    mins = calculate_local_minimums(hist)

    assert len(mins) == 2
    assert mins[0].index == 1 and mins[0].value == 1.0
    assert mins[1].index == 5 and mins[1].value == 2.0


def test_calculate_local_minimums_with_invalid_histogram():
    hist = numpy.array([])
    assert arrayEquals(calculate_local_minimums(hist), [])


def test_calculate_local_maximums_with_valid_histogram():
    hist = numpy.array([2.0, 1.0, 2.0, 4.0, 3.0, 2.0, 3.0])
    maxs = calculate_local_maximums(hist)

    assert len(maxs) == 1
    assert maxs[0].index == 3 and maxs[0].value == 4.0


def test_calculate_local_maximums_with_invalid_histogram():
    hist = numpy.array([])
    assert arrayEquals(calculate_local_maximums(hist), [])


def test_calc_mean_with_valid_histogram():
    hist = numpy.array([1.0, 2.0, 3.0, 2.0, 1.0])
    assert calc_mean(hist) == 3.0


def test_calc_mean_with_invalid_histogram():
    hist = numpy.array([])
    hist_2 = numpy.array([1.0, -1.0])

    assert calc_mean(hist) == 0.0
    assert calc_mean(hist_2) == 0.0


def test_variance_with_valid_histogram():
    hist = numpy.array([1.0, 2.0, 3.0, 2.0, 3.0])
    mean = calc_mean(hist)

    assert numpy.absolute(calc_variance(hist, mean) - 2.686) < 0.01


def test_variance_with_invalid_histogram():
    hist = numpy.array([])
    hist_2 = numpy.array([1.0, -1.0])

    mean = calc_mean(hist)
    mean_2 = calc_mean(hist_2)

    assert calc_variance(hist, mean) == 0.0
    assert calc_variance(hist_2, mean_2) == 0.0


def test_standard_deviation_with_valid_histogram():
    hist = numpy.array([1.0, 2.0, 3.0, 2.0, 3.0])

    assert numpy.absolute(calc_standard_deviation(hist) - 1.639) < 0.01


def test_standard_deviation_with_invalid_histogram():
    hist = numpy.array([])
    hist_2 = numpy.array([1.0, -1.0])

    assert calc_standard_deviation(hist) == 0.0
    assert calc_standard_deviation(hist_2) == 0.0


def test_roughness_with_valid_histogram():
    hist = numpy.array([0.0, 0.5, 1.0, 0.5, 2.0, 0.5, 0.0])

    assert calculate_roughness(hist) == 2.0


def test_roughness_with_empty_histogram():
    hist = numpy.array([])

    assert calculate_roughness(hist) == 0.0


def test_calculate_peak_value_with_valid_histogram():
    hist = numpy.array([0.0, 0.5, 1.0, 0.5, 2.0, 0.5, 0.0, 2.0])

    assert arrayNpEquals(calculate_peak_value(hist),
                         numpy.array([-1.0]).astype(numpy.float32))


def test_calculate_peak_value_with_invalid_histogram():
    hist = numpy.array([])

    assert arrayNpEquals(calculate_peak_value(hist), numpy.array([]))
