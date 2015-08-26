import numpy as np

from qualipy.utils.histogram_analyzation import *

def arrayNpEquals(arr1, arr2):
    comp = arr1 == arr2
    for i in range(0, comp.shape[0]):
        if comp[i] != True:
            return False

    return True

def arrayEquals(arr1, arr2):
    comp = arr1 == arr2
    for i in range(0, len(comp)):
        if comp[i] != True:
            return False

    return True


def test_remove_from_ends():
    hist = np.array([1, 1, 0, 0, 0, 1, 1])
    assert len(remove_from_ends(hist).nonzero()[0]) == 0

def test_normalize():
    hist = np.array([1, 2, 3, 2, 1])
    assert np.absolute(np.sum(normalize(hist)) - 1.0) < 0.00000001

def test_calculate_continuous_distribution():
    hist = np.array([1.0, 2.0, 3.0, 4.0])
    assert arrayNpEquals(calculate_continuous_distribution(hist), np.array([1.0, 3.0, 6.0, 10.0]))

def test_largest():
    hist = np.array([2.0, 4.0, 1.0, 3.0])
    assert arrayNpEquals(largest(hist, 0.5), np.array([4.0, 3.0]))

def test_calculate_derivates():
    hist = np.array([1, 2, 4, 2, 1])
    assert arrayNpEquals(calculate_derivates(hist), np.array([1.0, 2.0, -2.0, -1.0]))

def test_calculate_min_values():
    hist = np.array([2.0, 1.0, 2.0, 4.0, 3.0, 2.0, 3.0])
    assert calculate_min_values(hist, 2) == [LocationData(1, 1.0), LocationData(5, 2.0)]

def test_calculate_max_values():
    hist = np.array([2.0, 1.0, 2.0, 4.0, 3.0, 2.0, 3.0])
    assert calculate_max_values(hist) == [LocationData(3, 4.0)]

def test_calculate_local_minimums():
    hist = np.array([2.0, 1.0, 2.0, 4.0, 3.0, 2.0, 3.0])
    mins = calculate_local_minimums(hist)

    assert len(mins) == 2
    assert mins[0].index == 1 and mins[0].value == 1.0
    assert mins[1].index == 5 and mins[1].value == 2.0

def test_calculate_local_maximums():
    hist = np.array([2.0, 1.0, 2.0, 4.0, 3.0, 2.0, 3.0])
    maxs = calculate_local_maximums(hist)

    assert len(maxs) == 1
    assert maxs[0].index == 3 and maxs[0].value == 4.0

def test_calc_mean():
    hist = np.array([1.0, 2.0, 3.0, 2.0, 1.0])
    assert calc_mean(hist) == 2.0
