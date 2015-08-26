import numpy
import pytest

from qualipy.filters.posterized import *


POSTERIZED = 'tests/images/posterized.png'
NON_POSTERIZED = 'tests/images/non_posterized.jpg'


def test_input_vector_is_of_right_size():
    img = numpy.zeros((100, 100), dtype=numpy.float32)
    assert len(get_input_vector(img)) == 1


def test_input_vector_is_of_right_type():
    img = numpy.zeros((100, 100), dtype=numpy.float32)
    assert get_input_vector(img).dtype == numpy.float32


def test_recognizes_posterized():
    assert Posterized().predict(POSTERIZED)


def test_doesnt_recognize_normal_image():
    assert not Posterized().predict(NON_POSTERIZED)


def test_setting_threshold():
    assert not Posterized(threshold=1).predict(POSTERIZED)


def test_inverting_threshold():
    assert Posterized(1.01, invert_threshold=True).predict(POSTERIZED)


def test_can_return_float():
    assert type(Posterized().predict(POSTERIZED, return_boolean=False)) != bool


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        assert Posterized().predict(0)
