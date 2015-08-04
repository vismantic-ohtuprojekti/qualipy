import numpy

import imgfilter
from imgfilter.filters.whole_blur import *


BLURRED = 'tests/images/blurred.jpg'
NON_BLURRED = 'tests/images/lama.jpg'


def test_recognizes_blurred_image():
    assert not imgfilter.process(BLURRED, [WholeBlur()])


def test_doesnt_recognize_non_blurred_image():
    assert imgfilter.process(NON_BLURRED, [WholeBlur()])


def test_input_vector_is_of_right_size():
    mat = numpy.random.randint(80, size=(10, 15)).astype(numpy.uint8)
    assert len(get_input_vector(mat)) == 104


def test_input_vector_is_of_right_type():
    mat = numpy.random.randint(80, size=(10, 15)).astype(numpy.uint8)
    assert get_input_vector(mat).dtype == numpy.float32
