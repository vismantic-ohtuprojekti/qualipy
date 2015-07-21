import numpy


def get_max_values(array_1D, count):
    sorted_array = numpy.sort(array_1D)
    return sorted_array[-count::]


@numpy.vectorize
def linear_normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)


def linear_normalize_all(array_1D):
    max_value = numpy.amax(array_1D)
    min_value = numpy.amin(array_1D)
    return linear_normalize(array_1D, min_value, max_value)


def count_local_outlier_factor(entry, neighbors):
    outliers = numpy.abs(entry - neighbors)
    return numpy.mean(outliers)


def find_neighbors(index, k, sorted_array):
    dist = numpy.argsort(numpy.abs(sorted_array - sorted_array[index]))
    return sorted_array[dist[1:k + 1]]


def remove_anomalies(array_1D, max_outline_diff):
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
