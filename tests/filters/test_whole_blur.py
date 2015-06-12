import numpy

from imgfilter.filters.whole_blur import *


def test_input_vector_is_of_right_size():
    mat = numpy.random.randint(80, size=(10, 15)).astype(numpy.uint8)
    assert len(get_input_vector(mat)) == 104


def test_input_vector_is_of_right_type():
    mat = numpy.random.randint(80, size=(10, 15)).astype(numpy.uint8)
    assert get_input_vector(mat).dtype == numpy.float32
