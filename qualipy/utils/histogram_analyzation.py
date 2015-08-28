"""
Contains various functions for analyzing one-dimensional histograms.
"""

from operator import attrgetter

import numpy


class LocationData(object):

    """Contains both index and value of some histogram value.
    Has variables index and value to represent index and value of
    histogram value.
    """

    def __init__(self, index, value):
        self.index = index
        self.value = value

    def __repr__(self):
        return 'index: ' + str(self.index) + ' value: ' + str(self.value)

    def __eq__(self, other):
        return other.index == self.index and other.value == self.value


def calc_mean(histogram):
    """Calculates mean of given histogram

    :param histogram: histogram to calculate the mean for
    :type histogram: numpy.ndarray
    :returns: float -- mean of given histogram
    """
    if histogram.shape[0] == 0:
        return 0

    values = 0
    for i, value in enumerate(histogram):
        values += (value * (i + 1))

    if sum(histogram) == 0:
        return 0

    return float(values / sum(histogram))


def calc_variance(histogram, mean):
    """Calculates variance of given histogram

    :param histogram: histogram to calculate the variance for
    :type histogram: numpy.ndarray
    :returns: float -- variance of given histogram
    """
    if histogram.shape[0] == 0:
        return 0

    variance = 0
    for i, value in enumerate(histogram):
        variance += (mean - i) ** 2 * value

    if sum(histogram) == 0:
        return 0

    return float(variance / sum(histogram))


def calc_standard_deviation(histogram):
    """Calculates standard deviation of given histogram

    :param histogram: histogram to calculate standard deviation for
    :type histogram: numpy.ndarray
    :returns: float -- standard deviation of given histogram
    """
    mean = calc_mean(histogram)
    variance = calc_variance(histogram, mean)

    if variance < 0.0:
        return 0.0

    return numpy.sqrt(variance)


def normalize(histogram):
    """Normalizes a histogram

    :param histogram: the histogram to normalize
    :type histogram: numpy.ndarray
    :returns: numpy.ndarray -- the normalized histogram
    """
    if histogram.shape[0] == 0 or numpy.sum(histogram) == 0.0:
        return numpy.array([])

    return numpy.divide(histogram.astype(numpy.float32),
                        numpy.sum(histogram).astype(numpy.float32)).astype(numpy.float32)


def remove_from_ends(histogram):
    """Sets two of the first and last values in the histogram to zero.
    This can be used for example to remove the effect of totally black
    and white areas of an image in some calculations.

    :param histogram: the histogram to modify
    :type histogram: numpy.ndarray
    :returns: numpy.ndarray -- reference to the original histogram
    """
    if histogram.shape[0] < 2:
        return histogram

    # Remove black
    histogram[0] = histogram[1] = 0

    # Remove white
    histogram[-1] = histogram[-2] = 0

    return histogram


def calculate_continuous_distribution(histogram):
    """Calculates the continuous distribution of a given histogram.

    :param histogram: the histogram to calculate the distribution for
    :type histogram: numpy.ndarray
    :returns: numpy.ndarray -- the continuous distribution
    """
    return numpy.cumsum(histogram).astype(numpy.float32)


def calculate_local_maximums(histogram):
    """Calculates local max points of histogram, meaning all points where
    the derivative turns from positive to negative.

    :param histogram: histogram whichs local max points are calculated
    :type histogram: numpy.ndarray
    :returns: local max points of the histogram as an array of LocationData objects
    """
    diffs = numpy.diff(histogram)
    local_maximums = (diffs[1:] < 0) & (diffs[:-1] > 0)

    local_maximum_locations = []
    for i, elem in enumerate(local_maximums, start=1):
        if elem:
            local_maximum_locations.append(LocationData(i, histogram[i]))

    return local_maximum_locations


def calculate_local_minimums(histogram):
    """Calculates local min points of histogram, meaning all points where
    the derivative turns from negative to positive.

    :param histogram: histogram whichs local min points are calculated
    :type histogram: numpy.ndarray
    :returns: local min points of the histogram as an array of LocationData objects
    """
    diffs = numpy.diff(histogram)
    local_minimums = (diffs[1:] > 0) & (diffs[:-1] < 0)

    local_minimum_locations = []
    for i, elem in enumerate(local_minimums, start=1):
        if elem:
            local_minimum_locations.append(LocationData(i, histogram[i]))

    return local_minimum_locations


def calculate_local_max_values(histogram, amount=1):
    """Retrieves given amount of largest local maximums from a given histogram.

    :param histogram: the histogram which a given amount of largest values
                      are retrieved for
    :type histogram: numpy.ndarray
    :param amount: defines how many largest local maximums are to be
                   retrieved
    :type amount: int
    :returns: list -- a list which contains the largest local maximums from
                      largest to smallest
    """
    local_maximums = calculate_local_maximums(histogram)
    local_maximums.sort(key=attrgetter('value'), reverse=True)
    return local_maximums[:amount]


def calculate_local_min_values(histogram, amount=1):
    """Retrieves given amount of smallest local minimums from a given histogram.

    :param histogram: the histogram which a given amount of smallest values
                      are retrieved for
    :type histogram: numpy.ndarray
    :param amount: defines how many largest local minimums are to be
                   retrieved
    :type amount: int
    :returns: list -- a list which contains the largest local minimums from
                      smallest to largest
    """
    local_minimums = calculate_local_minimums(histogram)
    local_minimums.sort(key=attrgetter('value'))
    return local_minimums[:amount]


def calculate_peak_value(histogram):
    """Calculates peak value for all peaks (local max points) in a given histogram.
    First the histogram is normalized, then all local max and min points are
    calculated. Then for each max point, the average difference from both
    preceeding and trailing local min points is calculated.

    :param histogram: the histogram to calculate the peak values for
    :type histogram: numpy.ndarray
    :returns: numpy.ndarray -- the peak values
    """
    if histogram.shape[0] == 0:
        return numpy.array([])

    peak_values = []
    local_end_points = calculate_local_maximums(histogram) + \
                       calculate_local_minimums(histogram)
    local_end_points.sort(key=attrgetter('index'))

    for i in xrange(1, len(local_end_points) - 2):
        peak_value = (float(local_end_points[i].value) -
                      float(local_end_points[i - 1].value)) + \
                     (float(local_end_points[i].value) -
                      float(local_end_points[i + 1].value))
        peak_value /= 2.0
        peak_values.append(peak_value)

    return numpy.array(peak_values).astype(numpy.float32)


def calculate_roughness(histogram):
    """Calculates roughness of a given histogram. This is done by first calculating
    local min points and local max points, sorted by index. Then for each of
    these points the absolute value of values of the current point and the next
    point is calculated and also the difference between their indexes is
    calculated. Using these two values, the roughness is calculated so that a
    larger value distance and smaller index distance leads to a higher
    roughness value. The sum of these values is the histogram's roughness
    value.

    :param histogram: the histogram to calculate the roughness for
    :type histogram: numpy.ndarray
    :returns: float -- the roughness value
    """
    local_end_points = calculate_local_maximums(histogram) + \
                       calculate_local_minimums(histogram)
    local_end_points.sort(key=attrgetter('index'))

    roughness = 0.0
    for i in xrange(len(local_end_points) - 1):
        difference = numpy.abs(float(local_end_points[i + 1].value) -
                               float(local_end_points[i].value))
        distance = float(local_end_points[i + 1].index) - \
                   float(local_end_points[i].index)
        roughness += difference / distance

    return roughness


def calculate_extreme_values(histogram):
    """Calculates extreme values of given histogram. Calculates how many large
    separate regions are in the given histogram. This method is not completely
    reliable and results may in some casses differ from what a person would
    define as large separate areas.

    :param histogram: the histogram to calculate the extreme values for
    :type histogram: numpy.ndarray
    :returns: numpy.ndarray -- the extreme values
    """
    histogram = normalize(histogram)

    # Calculate limit
    max_values = calculate_local_max_values(histogram, 10)
    min_values = calculate_local_min_values(histogram, 10)

    diff_sum = 0.
    for max_val, min_val in zip(max_values, min_values):
        diff_sum += numpy.abs(max_val.value - min_val.value)

    limit = diff_sum / float(len(max_values))

    extreme_values = calculate_local_maximums(histogram) + \
                     calculate_local_minimums(histogram)
    extreme_values.sort(key=attrgetter('index'))

    if 0 <= len(extreme_values) <= 2:
        return extreme_values

    i = 0
    while i < len(extreme_values) - 1:
        difference = numpy.abs(extreme_values[i + 1].value -
                               extreme_values[i].value)

        if difference >= limit:
            i += 2
        else:
            del extreme_values[i + 1]

    return extreme_values


def calculate_derivatives(histogram):
    """Calculates derivatives of a given histogram

    :param histogram: the histogram to calculate derivatives for
    :type histogram: numpy.ndarray
    :returns: numpy.ndarray -- the derivatives
    """
    return numpy.diff(histogram).astype(numpy.float32)


def largest(histogram, percent):
    """Retrieves percentage of largest values from given histogram

    :param histogram: the histogram to retrieve the values from
    :type histogram: numpy.ndarray
    :param percent: percentage of largest values to retrieve
    :returns: numpy.ndarray -- the largest values
    """
    amount = int(histogram.shape[0] * percent)
    sorted = numpy.sort(histogram)[::-1]

    if amount == 0:
        amount = histogram.shape[0]

    return sorted[:amount].astype(numpy.float32)
