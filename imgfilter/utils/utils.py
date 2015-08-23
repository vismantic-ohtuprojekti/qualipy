"""
Common utilities used in the library.
"""
from functools import wraps

import numpy


# Numba integration
# If Numba is installed, certain functions are automatically
# sped-up by Numba's JIT compilation.
try:
    import numba
    jit = numba.jit

except ImportError:

    def jit(func):
        return func


def file_cache(f):
    """Decorator for caching the result of a function
    for a single parameter at a time. If the function
    is called with a new parameter, the currently
    cached value is deleted.
    """

    cache = {'sig': None, 'val': None}

    @wraps(f)
    def wrapper(*args, **kwargs):
        sig = (args, tuple(sorted(kwargs.items())))

        if sig == cache['sig']:
            return cache['val']

        result = f(*args, **kwargs)
        cache['val'] = result
        cache['sig'] = sig

        return result

    return wrapper


def partition_matrix(matrix, n):
    """Partitions a matrix into n x n blocks of equal size

    :param matrix: the matrix to partition
    :type matrix: numpy.ndarray
    :param n: the size of the side of one partition
    :type n: int
    :returns: list -- list of the partitions
    """
    height, width = matrix.shape
    y_stride, x_stride = height / n, width / n

    partitions = [matrix]
    for y in xrange(0, y_stride * n, y_stride):
        for x in xrange(0, x_stride * n, x_stride):
            partitions.append(matrix[y : y + y_stride,
                                     x : x + x_stride])

    return partitions


def normalize(arr):
    """Normalizes an array of values to the range [0, 1]

    :param arr: the array to normalize
    :type arr: numpy.ndarray
    :returns: numpy.ndarray
    """
    arr_min, arr_max = numpy.min(arr), numpy.max(arr)

    if arr_min == arr_max:
        return numpy.ones(len(arr))

    return (arr - arr_min) / (arr_max - arr_min)


def flatten(lists):
    """Flattens a list of lists into a single list

    :param lists: the list of lists to flatten
    :type lists: list
    :returns: list -- the flattened list
    """
    return [item for sublist in lists for item in sublist]


def scaled_prediction(prediction):
    """Scales the prediction to range [0, 1].

    :param prediction: the prediction to scale
    :type prediction: float
    :returns: float -- the scaled prediction
    """
    pred = 1 - (1 + prediction) / 2.

    if pred < 0:
        return 0
    if pred > 1:
        return 1

    return pred


def clipping_percentage(histogram, threshold, over_threshold):
    """Calculates percentage of images high of low intensity pixels

    :param histogram: intensity histogram
    :type histogram: numpy.ndarray
    :param threshold: threshold intensity which is used to get
                      intensity amounts over or under it
    :type threshold: int
    :param over_threshold: whether to get the intensity amount over
                          (True) or under (False) threshold
    :type over_threshold: bool
    :returns: float -- the clipping percentage
    """
    total = numpy.sum(histogram)
    if total < 0.0005:  # avoid division by zero
        return 0

    if over_threshold:
        return float(numpy.sum(histogram[threshold:])) / total
    else:
        return float(numpy.sum(histogram[:threshold])) / total
