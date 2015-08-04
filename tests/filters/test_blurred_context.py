import numpy

import imgfilter
from imgfilter.filters.blurred_context import *

BLURRED_CONTEXT = 'tests/images/blurred_context.jpg'
NON_BLURRED_CONTEXT = 'tests/images/exposure_sample_good.jpg'


def test_blurry_degree_works_for_all_zeroes():
    assert -0.001 < blurry_degree(numpy.array([0, 0, 0])) < 0.001


def test_blurry_degree_returns_first_values_ratio():
    assert round(blurry_degree(numpy.array([1, 1, 2])) - 1 / 4., 3) == 0


def test_blurmap_returns_correct_size_matrix():
    mat = numpy.eye(10)
    assert blurmap(mat).shape == (6, 6)


def test_input_vector_is_of_right_size():
    mat = numpy.eye(50)
    assert len(get_input_vector(mat)) == 101


def test_input_vector_is_of_right_type():
    mat = numpy.eye(50)
    assert get_input_vector(mat).dtype == numpy.float32


def test_recognizes_blurred_context():
    assert not imgfilter.process(BLURRED_CONTEXT, [BlurredContext()])


def test_doesnt_recognize_normal_image():
    assert imgfilter.process(NON_BLURRED_CONTEXT, [BlurredContext()])
