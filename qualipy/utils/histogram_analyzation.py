import numpy as np
import math


class LocationData(object):
    """Contains both index and value of some histogram value.
    Has variables index and value to present index and value of histogram value.
    Also has equals and to string implementations
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

    :param histogram: histogram whichs mean is calculated (numpy array)
    :returns: returns mean of given histogram as float
    """
    if histogram.shape[0] == 0:
        return 0

    values = 0
    for i, value in enumerate(histogram):
        values += (value * i)

    return float(values / sum(histogram))


def calc_variance(histogram, mean):
    """Calculates variance of given histogram

    :param histogram: histogram whichs variance is calculated (numpy array)
    :returns: returns variance of given histogram as float
    """
    if histogram.shape[0] == 0:
        return 0

    variance = 0
    for i, value in enumerate(histogram):
        variance += math.pow((mean - i), 2) * value

    return float(variance / sum(histogram))


def calc_standard_deviation(histogram):
    """Calculates standard deviation of given histogram

    :param histogram: histogram whichs standard deviation is calculated (numpy array)
    :returns: returns standard deviation of given histogram as float
    """
    mean = calc_mean(histogram)
    variance = calc_variance(histogram, mean)

    return math.sqrt(variance)


def normalize(histogram):
    """Makes normalized histgram from given histgram.

    :param histogram: histogram whichs normalized histgram is calculated (numpy array)
    :returns: returns normalized histogram (numpy array)
    """
    if histogram.shape[0] == 0:
        return np.array([])

    return np.divide(histogram.astype(np.float32), np.sum(histogram).astype(np.float32)).astype(np.float32)


def remove_from_ends(histogram):
    """Sets two of the first and last values in the histogram to be zero.
    This can be used for example to remove effect of totally black and white
    areas of image in other calculations.

    :param histogram: histogram whichs ends are removed (numpy array)
    :returns: histgram which ends are removed (numpy array)
    """
    ends_removed = histogram

    # Remove black
    ends_removed[0] = 0
    ends_removed[1] = 0

    # Remove white
    ends_removed[ends_removed.shape[0] - 1] = 0
    ends_removed[ends_removed.shape[0] - 2] = 0

    return ends_removed


def calculate_continuous_distribution(histogram):
    """Calculates continuous distribution of given histogram.

    :param histogram: histogram whichs continuous distribution is calculated (numpy array)
    :returns: continuous distribution of given histogram (numpy array)
    """
    continuous_distribution = []

    current_sum = 0.0
    for i in range(0, histogram.shape[0]):
        current_sum += float(histogram[i])
        continuous_distribution.append(current_sum)

    return np.array(continuous_distribution).astype(np.float32)


def calculate_local_maximums(histogram):
    """Calculates local max points of histogram. Meaning all points where
    derivate turns from positive to negative.

    :param histogram: histogram whichs local max points are calculated (numpy array)
    :returns: Local max points of given histogram as array of LocationData objects
    """
    local_maximums = []

    derivate_status = 'level'

    for i in range(0, histogram.shape[0] - 1):
        current_derivate = float(histogram[i + 1]) - float(histogram[i])

        current_derivate_status = ''
        if current_derivate < 0.0:
            current_derivate_status = 'decreasing'
        elif current_derivate > 0.0:
            current_derivate_status = 'increasing'
        else:
            current_derivate_status = 'level'

        if derivate_status == 'increasing' and current_derivate_status == 'decreasing':
            local_maximums.append(LocationData(i, histogram[i]))

        derivate_status = current_derivate_status

    return local_maximums


def calculate_local_minimums(histogram):
    """Calculates local min points of histogram. Meaning all points where
    derivate turns from negative to positive.

    :param histogram: histogram whichs local min points are calculated (numpy array)
    :returns: Local min points of given histogram as array of LocationData objects
    """
    local_minimums = []

    derivate_status = 'level'

    for i in range(0, histogram.shape[0] - 1):
        current_derivate = float(histogram[i + 1]) - float(histogram[i])

        current_derivate_status = ''
        if current_derivate < 0.0:
            current_derivate_status = 'decreasing'
        elif current_derivate > 0.0:
            current_derivate_status = 'increasing'
        else:
            current_derivate_status = 'level'

        if derivate_status == 'decreasing' and current_derivate_status == 'increasing':
            local_minimums.append(LocationData(i, histogram[i]))

        derivate_status = current_derivate_status

    return local_minimums


def calculate_max_values(histogram, amount = 1):
    """Retrieves given amount of largest values from given histogram.

    :param histogram: histogram which given amount of largest values are retrieved (numpy array)
    :param amount: defines how many largest values are to be retrieved. Default value is set to one
    :returns: Array which contains largest values from largest to smallest (python array)
    """
    max_values = []

    local_maximums = calculate_local_maximums(histogram)
    local_maximums.sort(key = lambda data: data.value)
    local_maximums.reverse()

    for i in range(0, amount):
        max_values.append(local_maximums[i])

    return max_values


def calculate_min_values(histogram, amount = 1):
    """Retrieves given amount of smallest values from given histogram.

    :param histogram: histogram which given amount of smallest values are retrieved (numpy array)
    :param amount: defines how many smallest values are to be retrieved. Default value is set to one
    :returns: Array which contains smallest values from smallest to largest (python array)
    """
    min_values = []

    local_minimums = calculate_local_minimums(histogram)
    local_minimums.sort(key = lambda data: data.value)

    for i in range(0, amount):
        min_values.append(local_minimums[i])

    return min_values


def calculate_peak_value(histogram):
    """Calculates peak value for all peaks (local max points) in given histogram.
    First histogram is normalized then all local max and min points are calculated.
    Then for each max point average difference from both preciding and trailing
    local min points is calculated.

    :param histogram: histogram which peak values are calculated (numpy array)
    :returns: peak values of given histogram (numpy array)
    """
    if histogram.shape[0] == 0:
        return 0

    peak_values = []

    local_end_points = calculate_local_maximums(histogram) + calculate_local_minimums(histogram)
    local_end_points.sort(key = lambda data: data.index)

    for i in range(1, len(local_end_points) - 2, 1):
        peak_value = (float(local_end_points[i].value) - float(local_end_points[i - 1].value)) + (float(local_end_points[i].value) - float(local_end_points[i + 1].value))
        peak_value /= 2.0
        peak_values.append(peak_value)

    return np.array(peak_values).astype(np.float32)


def calculate_roughness(histogram):
    """Calculates roughness of given histogram. This is done by first calculating
    local min points and local max points. This array is sorted by index.
    Then for each of these points absolute value of values of current point
    and next point is calculated and also difference between their indexs
    is calculated. usinf these to values roughness is calculated so that
    larger value distance and smaller index distance leads to higher
    roughness value. Sum of these values is is histgram's roughness value.

    :param histogram: histogram which's roughness is calculated
    :returns: roughness value for given histogram
    """
    local_end_points = calculate_local_maximums(histogram) + calculate_local_minimums(histogram)
    local_end_points.sort(key = lambda data: data.index)

    roughness = 0.0
    for i in range(0, len(local_end_points) - 1):
        difference = np.abs(float(local_end_points[i + 1].value) - float(local_end_points[i].value))
        distance = float(local_end_points[i + 1].index) - float(local_end_points[i].index)

        roughness += difference * (1.0 / distance)

    return roughness


def calculate_extream_values(histogram):
    """Calculates extream values of given histogram. Calculates how many large
    separate regions are in the given histogram. This method is not completly
    reliable and results may in some casses differ from what person would
    define as large separate areas.

    :param histogram: histogram which's roughness is calculated
    :returns:
    """
    histogram = normalize(histogram)

    # Calculate limit
    max_values = calculate_max_values(histogram, 10)
    min_values = calculate_min_values(histogram, 10)

    sum = 0.0
    for i in range(0, len(max_values)):
        sum += np.abs(max_values[i].value - min_values[i].value)

    limit = sum / float(len(max_values))

    extream_values = calculate_local_maximums(histogram) + calculate_local_minimums(histogram)
    extream_values.sort(key = lambda data: data.index)

    if len(extream_values) == 0 or len(extream_values) == 1 or len(extream_values) == 2:
        return extream_values

    i = 0
    while i < len(extream_values) - 1:
        difference = np.abs(extream_values[i + 1].value - extream_values[i].value)

        if difference >= limit:
            i = i + 2
        else:
            del extream_values[i + 1]

    return extream_values


def calculate_derivates(histogram):
    """Calculates derivates of given histogram

    :param histogram: histogram which derivates are calculated (numpy array)
    :returns: derivates of given histogram (numpy array)
    """
    derivates = []

    for i in range(0, histogram.shape[0] - 1):
        derivates.append(float(histogram[i + 1]) - float(histogram[i]))

    return np.array(derivates).astype(np.float32)


def largest(histogram, prosent):
    """Retrieves prosentage of largest values from given histogram

    :param histogram: histogram which largest values are retrieved (numpy array)
    :param prosent: defines how big prosentage of largest values are retrieved
    :returns: array of largest values (numpy array)
    """
    largest = []

    amount = int(histogram.shape[0] * prosent)
    sorted = np.sort(histogram)
    sorted = sorted[::-1]

    if amount == 0:
        amount = histogram.shape[0]

    for i in range(0, amount):
        largest.append(sorted[i])

    return np.array(largest).astype(np.float32)
