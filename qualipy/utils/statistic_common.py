"""
Contains functionality for removing anomalies from
one-dimensional arrays and normalizing one-dimensional
arrays.
"""

import numpy


def get_max_values(array_1D, count):
    """Retrieves count amount of max values from a given array

    :param array_1D: the array to retrieve max values for
    :type array_1D: numpy.ndarray
    :param count: how many values should be retrieved
    :type count: int
    :returns: numpy.ndarray -- the retrieved values
    """
    sorted_array = numpy.sort(array_1D)
    return sorted_array[-count::]


@numpy.vectorize
def linear_normalize(value, min_value, max_value):
    """Linearly normalizes given value between zero and one so
    that the given min value will map to zero and the given max
    value will map to one

    :param value: the value to be normalized
    :type value: float
    :param min_value: the value that will be mapped to zero
    :type min_value: float
    :param max_value: the value that will be mapped to one
    :type max_value: float
    :returns: float -- the normalized value
    """
    return (value - min_value) / (max_value - min_value)


def linear_normalize_all(array_1D):
    """Normalizes all values in given array between one and zero so
    that the highest value in the array is mapped to one and the
    smallest to zero.

    :param array_1D: the array to be normalized
    :type array_1D: float
    :returns: numpy.ndarray -- the normalized array
    """
    max_value = numpy.amax(array_1D)
    min_value = numpy.amin(array_1D)
    return linear_normalize(array_1D, min_value, max_value)


def count_local_outlier_factor(entry, neighbors):
    """Calculates local outlier factor for a given entry using given
    neighbors. Local outlier factor is the average distance from neighbors

    :param entry: entry which local outlier factor is calculated for
    :param neighbors: neighbors which are used to calculate local
                      outlier factor for entry
    :returns: local outlier factor for entry
    """
    outliers = numpy.abs(entry - neighbors)
    return numpy.mean(outliers)


def find_neighbors(index, k, sorted_array):
    """Finds k nearest neighbors from a given sorted array for an element
    in a given index

    :param index: the index at which the k nearest neighbors are retrieved
    :type index: int
    :param k: defines how many neighbors are retrieved
    :type k: int
    :param sorted_array: sorted array where all the elements are
    :type sorted_array: numpy.ndarray
    :returns: list -- the k nearest neighbors for the element in a given index
    """
    dist = numpy.argsort(numpy.abs(sorted_array - sorted_array[index]))
    return sorted_array[dist[1:k + 1]]


def remove_anomalies(array_1D, max_outline_diff):
    """Removes anomalies from a given one-dimensional array. This is done by
    calculating local outlier factor for all elements and discarding those
    which have a larger outlier factor than the given max outline difference

    :param array_1D: the array to remove anomalies from
    :type array_1D: numpy.ndarray
    :param max_outline_diff: what is the max outlier factor that is accepted
    :type max_outline_diff: float
    :returns: numpy.ndarray -- the original array excluding the anomalies
    """
    sorted_array = numpy.sort(array_1D)
    outlier_factors = numpy.array([])
    k = 4

    # count outline factors
    for i in xrange(sorted_array.shape[0]):
        neighbors = find_neighbors(i, k, sorted_array)
        outlier_factor = count_local_outlier_factor(sorted_array[i], neighbors)
        outlier_factors = numpy.append(outlier_factors, outlier_factor)

    outlier_factors = linear_normalize_all(outlier_factors)
    outlier_factor_avg = numpy.mean(outlier_factors)

    x = (numpy.abs(outlier_factors - outlier_factor_avg) <= max_outline_diff) | \
        (outlier_factors <= outlier_factor_avg)
    return sorted_array[x]
