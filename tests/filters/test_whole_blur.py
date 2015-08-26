import numpy
import pytest

from qualipy.filters.whole_blur import *


BLURRED = 'tests/images/blurred.jpg'
NON_BLURRED = 'tests/images/lama.jpg'


def test_input_vector_is_of_right_size():
    mat = numpy.random.randint(80, size=(10, 15)).astype(numpy.uint8)
    assert len(get_input_vector(mat)) == 104


def test_input_vector_is_of_right_type():
    mat = numpy.random.randint(80, size=(10, 15)).astype(numpy.uint8)
    assert get_input_vector(mat).dtype == numpy.float32


def test_recognizes_whole_blur():
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


def test_training_with_too_few_images_causes_exception():
    with pytest.raises(ValueError):
        WholeBlur().train([BLURRED], [0])


def test_training_with_invalid_number_of_labels_causes_exception():
    with pytest.raises(ValueError):
        WholeBlur().train([BLURRED], [])


def test_invalid_svm_file_causes_exception():
    with pytest.raises(TypeError):
        WholeBlur(svm_file=0)


def test_invalid_load_path_causes_exception():
    with pytest.raises(TypeError):
        WholeBlur().load(0)


def test_svm_file_not_found_causes_exception():
    with pytest.raises(ValueError):
        WholeBlur().load('fail')


def test_invalid_save_path_causes_exception():
    with pytest.raises(TypeError):
        WholeBlur().save(0)
