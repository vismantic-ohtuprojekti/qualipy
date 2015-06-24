import numpy

from imgfilter.filters.small_object import *


def test_returns_correct_object_ratio():
    img = numpy.zeros(10000).reshape(100, 100)
    img[20:30, 20:30] = 255
    assert round(get_object_ratio(img), 5) == 0.01
