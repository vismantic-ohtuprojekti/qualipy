import numpy as np
import cv2
import math

from matplotlib import pyplot as plt


class LocationData(object):
    def __init__(self, index, value):
        self.index = index
        self.value = value

    def __repr__(self):
        return 'index: ' + str(self.index) + ' value: ' + str(self.value)


def draw_histrogram(histogram):
    plt.plot(histogram, color = 'red')
    plt.xlim([0, histogram.shape[0]])
    plt.show()


def calc_mean(histogram):
    values = 0
    for i, value in enumerate(histogram):
        values += (value * i)

    return float(values / sum(histogram))


def calc_variance(histogram, mean):
    variance = 0
    for i, value in enumerate(histogram):
        variance += math.pow((mean - i), 2) * value

    return float(variance / sum(histogram))


def calc_standard_deviation(histogram):
    mean = calc_mean(histogram)
    variance = calc_variance(histogram, mean)

    return math.sqrt(variance)


def normalize(histogram):
    return np.divide(histogram.astype(np.float32), np.sum(histogram).astype(np.float32)).astype(np.float32)


def remove_from_ends(histogram):
    ends_removed = histogram

    # Remove black
    ends_removed[0] = 0
    ends_removed[1] = 0

    # Remove white
    ends_removed[ends_removed.shape[0] - 1] = 0
    ends_removed[ends_removed.shape[0] - 2] = 0

    return ends_removed


def calculate_continuous_distribution(histogram):
    continuous_distribution = []

    current_sum = 0.0
    for i in range(0, histogram.shape[0]):
        current_sum += float(histogram[i])
        continuous_distribution.append(current_sum)

    return np.array(continuous_distribution).astype(np.float32)


def calculate_local_maximums(histogram):
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
    max_values = []

    local_maximums = calculate_local_maximums(histogram)
    local_maximums.sort(key = lambda data: data.value)
    local_maximums.reverse()

    for i in range(0, amount):
        max_values.append(local_maximums[i])

    return max_values


def calculate_min_values(histogram, amount = 1):
    min_values = []

    local_minimums = calculate_local_minimums(histogram)
    local_minimums.sort(key = lambda data: data.value)

    for i in range(0, amount):
        min_values.append(local_minimums[i])

    return min_values


def calculate_peak_value(histogram):
    peak_values = []

    local_end_points = calculate_local_maximums(histogram) + calculate_local_minimums(histogram)
    local_end_points.sort(key = lambda data: data.index)

    for i in range(1, len(local_end_points) - 2, 1):
        peak_value = (float(local_end_points[i].value) - float(local_end_points[i - 1].value)) + (float(local_end_points[i].value) - float(local_end_points[i + 1].value))
        peak_value /= 2.0
        peak_values.append(peak_value)

    return np.array(peak_values).astype(np.float32)


def calculate_roughness(histogram):
    local_end_points = calculate_local_maximums(histogram) + calculate_local_minimums(histogram)
    local_end_points.sort(key = lambda data: data.index)

    roughness = 0.0
    for i in range(0, len(local_end_points) - 1):
        difference = np.abs(float(local_end_points[i + 1].value) - float(local_end_points[i].value))
        distance = float(local_end_points[i + 1].index) - float(local_end_points[i].index)

        roughness += difference * (1.0 / distance)

    return roughness


def calculate_extream_values(histogram):
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
    derivates = []

    for i in range(0, histogram.shape[0] - 1):
        derivates.append(float(histogram[i + 1]) - float(histogram[i]))

    return np.array(derivates).astype(np.float32)


def largest(histogram, prosent):
    largest = []

    amount = int(histogram.shape[0] * prosent)
    sorted = np.sort(histogram)
    sorted = sorted[::-1]

    for i in range(0, amount):
        largest.append(sorted[i])

    return np.array(largest).astype(np.float32)
