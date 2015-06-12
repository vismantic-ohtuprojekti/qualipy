import numpy as np


def avarage(array_1D):
    return np.sum(array_1D) / array_1D.shape[0]

def get_max_values(array_1D, count):
    max_values = np.array([])
    sorted_array = np.sort(array_1D)
    for i in range(sorted_array.shape[0] - 1, sorted_array.shape[0] - count - 1, -1):
        if i < 0 or i >= sorted_array.shape[0]:
            break
        max_values = np.append(max_values, sorted_array[i])
    return max_values


def linear_normalize(value, min_value, max_value):
    return (value - min_value) / max_value


def linear_normalize_all(array_1D):
    max_value = np.amax(array_1D)
    min_value = np.amin(array_1D)

    scaled = np.array([])

    for entry in np.nditer(array_1D):
        scaled = np.append(scaled, linear_normalize(entry, min_value, max_value))

    return scaled


def count_local_outliner_factor(entry, neighbors):
    outliners = np.array([])

    for neighbor in neighbors:
        outliners = np.append(outliners, np.absolute(entry - neighbor))

    return np.sum(outliners) / outliners.shape[0]

def find_neighbors(index, k, sorted_array):
    neighbors = np.array([])
    left_index = index - 1
    right_index = index + 1

    while neighbors.shape[0] < k:
        dist_left = float('inf')
        dist_right = float('inf')

        if left_index >= 0:
            dist_left = np.absolute(sorted_array[index] - sorted_array[left_index])

        if right_index < sorted_array.shape[0]:
            dist_right = np.absolute(sorted_array[index] - sorted_array[right_index])

        if left_index < 0 and right_index >= sorted_array.shape[0]:
            break

        if dist_left <= dist_right:
            neighbors = np.append(neighbors, sorted_array[left_index])
            left_index = left_index - 1
        else:
            neighbors = np.append(neighbors, sorted_array[right_index])
            right_index = right_index + 1

    return neighbors


def remove_anomalies(array_1D, max_outline_diff):
    sorted_array = np.sort(array_1D)
    outliner_factors = np.array([])
    k = 4

    # Count outline factors
    for i in range(0, sorted_array.shape[0]):
        neighbors = find_neighbors(i, k, sorted_array)
        outliner_factor = count_local_outliner_factor(sorted_array[i], neighbors)
        outliner_factors = np.append(outliner_factors, outliner_factor)


    anomalies_removed = np.array([])
    outliner_factors = linear_normalize_all(outliner_factors)
    outliner_factor_avg = np.sum(outliner_factors) / outliner_factors.shape[0]

    for i in range(0, outliner_factors.shape[0]):
        if np.absolute(outliner_factors[i] - outliner_factor_avg) <= max_outline_diff or outliner_factors[i] <= outliner_factor_avg:
            anomalies_removed = np.append(anomalies_removed, sorted_array[i])

    return anomalies_removed
