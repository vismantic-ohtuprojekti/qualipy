import numpy
import pytest

from imgfilter.filters.whole_blur import *


BLURRED = 'tests/images/blurred.jpg'
NON_BLURRED = 'tests/images/lama.jpg'


def test_input_vector_is_of_right_size():
    mat = numpy.random.randint(80, size=(10, 15)).astype(numpy.uint8)
    assert len(get_input_vector(mat)) == 104


def test_input_vector_is_of_right_type():
    mat = numpy.random.randint(80, size=(10, 15)).astype(numpy.uint8)
    assert get_input_vector(mat).dtype == numpy.float32


def test_recognizes_blurred_context():
    assert WholeBlur().predict(BLURRED)


def test_doesnt_recognize_normal_image():
    assert not WholeBlur().predict(NON_BLURRED)


def test_setting_threshold():
    assert not WholeBlur(threshold=1).predict(BLURRED)


def test_inverting_threshold():
    assert WholeBlur(1.01, invert_threshold=True).predict(BLURRED)


def test_can_return_float():
    assert type(WholeBlur().predict(BLURRED, return_boolean=False)) != bool


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        assert WholeBlur().predict(0)
