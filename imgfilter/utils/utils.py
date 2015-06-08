import numpy


def partition_matrix(matrix, n):
    """Partitions a matrix into n x n blocks of equal size

    :param matrix: the matrix to partition
    :param n: the size of the side of one partition
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
    """
    arr_min, arr_max = numpy.min(arr), numpy.max(arr)

    if arr_min == arr_max:
        return numpy.ones(len(arr))

    return (arr - arr_min) / (arr_max - arr_min)


def flatten(lists):
    """Flattens a list of lists into a single list

    :param lists: the list of lists to flatten
    """
    return [item for sublist in lists for item in sublist]
