import numpy


def get_max_values(array_1D, count):
    """
    Retrieves count amount of max values from given array
    :param array_1D: array whichs max values are to be retrieved
    :param count: defines how many values should be retrieved
    :returns: retrieved values as numpy array
    """
    sorted_array = numpy.sort(array_1D)
    return sorted_array[-count::]


@numpy.vectorize
def linear_normalize(value, min_value, max_value):
    """
    Linearly normalizes given value between zero and one so that given min value
    will map to zero and given max value will map to one
    :param value: value to be normalized
    :param min_value: value that will be mapped to zero
    :param max_value: value that will be mapped to one
    :returns: normalized value as float
    """
    return (value - min_value) / (max_value - min_value)


def linear_normalize_all(array_1D):
    """
    Normalzes all values in given array between one and zero so that highest
    value in array is mapped to one and smallest to zero.
    :param array_1D: array to be normalized
    :returns: normalized array
    """
    max_value = numpy.amax(array_1D)
    min_value = numpy.amin(array_1D)
    return linear_normalize(array_1D, min_value, max_value)


def count_local_outlier_factor(entry, neighbors):
    """
    Calculates local outliner factor for given entry using given neighbors.
    Local outliner factor is average distance from neighbors
    :param entry: entry which local outliner factor is calculated for
    :param neighbors: neighbors which are used to calculate local outliner
    factor for entry
    :returns: local outliner factor for entry
    """
    outliers = numpy.abs(entry - neighbors)
    return numpy.mean(outliers)


def find_neighbors(index, k, sorted_array):
    """
    Finds k nearest neighbors from given sorted array for element in given index
    :param index: index which k nearest neighbors are retrieved
    :param k: defines how many neighbors are retrieved
    :param sorted_array: sorted array where all elements are
    :returns: list which contains k nearest neighbors for element in given index
    """
    dist = numpy.argsort(numpy.abs(sorted_array - sorted_array[index]))
    return sorted_array[dist[1:k + 1]]


def remove_anomalies(array_1D, max_outline_diff):
    """
    Removes anomalies from given one dimensional array. This is done by
    calculating local outliner factor for all elements and discarding those
    which have larger outliner factor than given max outline difference
    :param array_1D: array which from anomalies are removed from
    :param max_outline_diff: what is the max outlier_factor that is accepted
    :returns: array from which anomalies are removed
    """
    sorted_array = numpy.sort(array_1D)
    outlier_factors = numpy.array([])
    k = 4

    # Count outline factors
    for i in xrange(sorted_array.shape[0]):
        neighbors = find_neighbors(i, k, sorted_array)
        outlier_factor = count_local_outlier_factor(sorted_array[i], neighbors)
        outlier_factors = numpy.append(outlier_factors, outlier_factor)

    outlier_factors = linear_normalize_all(outlier_factors)
    outlier_factor_avg = numpy.mean(outlier_factors)

    x = (numpy.abs(outlier_factors - outlier_factor_avg) <= max_outline_diff) | \
        (outlier_factors <= outlier_factor_avg)
    return sorted_array[x]
