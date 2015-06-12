import numpy as np

import analyzers.common.statistic_common

def test_removes_anomalies_correctly():
    original = np.array([-10.0, 1.0, 2.0, 3.0, 4.0, 10.0])
    anomalies_removed = statistic_common.remove_anomalies(original, 0.1)

    assert(-10.0 not in anomalies_removed)
    assert(10.0 not in anomalies_removed)

    for i in range(1, original.shape[0] - 1):
        assert(original[i] in anomalies_removed)


def test_count_local_outliner_factors():
    outliner_factor = statistic_common.count_local_outliner_factor(2.0, np.array([-10.0, 1.0, 3.0, 4.0]))

    assert(1.0 - outliner_factor <= 0.00001)


def test_linear_normalize():
    value = 4.0
    max = 10.0
    min = 0.0

    normalized = statistic_common.linear_normalize(value, min, max)
    assert(0.4 - normalized <= 0.00001)


def test_linear_normalize_all():
    values = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])

    #normalized_values = np.around(statistic_common.linear_normalize_all(values), decimals = 1)
    #for norm in np.arange(0.0, 0.8, 0.1):
    #    rounded = np.around(np.array([norm]), decimals = 1)
    #    assert(rounded[0] in normalized_values)


def test_avarage():
    originals = np.array([1.0, 8.0, 5.0, 6.0])
    avarage = statistic_common.avarage(originals)
    assert(avarage == 5.0)


def test_max_values():
    originals = np.array([1.0, 8.0, 5.0, 6.0, 1.0, 0.3, 0.2, 9.0])
    three_maxes = statistic_common.get_max_values(originals, 3)

    assert(9.0 in three_maxes)
    assert(8.0 in three_maxes)
    assert(6.0 in three_maxes)


def test_find_neighbors():
    sorted_array = np.array([0.0, 0.1, 0.2, 0.3, 0.5, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3])
    index = 4

    five_neighbors = statistic_common.find_neighbors(index, 5, sorted_array)
    assert(0.3 in five_neighbors)
    assert(0.2 in five_neighbors)
    assert(0.8 in five_neighbors)
    assert(0.1 in five_neighbors)
    assert(0.9 in five_neighbors)
