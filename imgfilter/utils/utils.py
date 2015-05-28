import os
import numpy


def partition_matrix(matrix, n):
    height, width = matrix.shape
    y_stride, x_stride = height / n, width / n

    partitions = [matrix]
    for y in xrange(0, y_stride * n, y_stride):
        for x in xrange(0, x_stride * n, x_stride):
            partitions.append(matrix[y : y + y_stride,
                                     x : x + x_stride])

    return partitions


def normalize(arr):
    arr_min, arr_max = numpy.min(arr), numpy.max(arr)

    if arr_min == arr_max:
        return numpy.ones(len(arr))

    return (arr - arr_min) / (arr_max - arr_min)


def flatten(lists):
    return [item for sublist in lists for item in sublist]
