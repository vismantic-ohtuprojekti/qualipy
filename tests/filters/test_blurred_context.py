import numpy
import pytest

from qualipy.filters.blurred_context import *


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
    assert BlurredContext().predict(BLURRED_CONTEXT)


def test_doesnt_recognize_normal_image():
    assert not BlurredContext().predict(NON_BLURRED_CONTEXT)


def test_setting_threshold():
    assert not BlurredContext(threshold=1).predict(BLURRED_CONTEXT)


def test_inverting_threshold():
    assert BlurredContext(1.01, invert_threshold=True).predict(BLURRED_CONTEXT)


def test_can_return_float():
    assert type(BlurredContext().predict(BLURRED_CONTEXT,
                                         return_boolean=False)) == float


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        BlurredContext().predict(0)


def test_training_with_too_few_images_causes_exception():
    with pytest.raises(ValueError):
        BlurredContext().train([BLURRED_CONTEXT], [0])


def test_training_with_invalid_number_of_labels_causes_exception():
    with pytest.raises(ValueError):
        BlurredContext().train([BLURRED_CONTEXT], [])


def test_training_with_invalid_paths_causes_exception():
    with pytest.raises(IOError):
        BlurredContext().train(['fail'], [])


def test_invalid_svm_file_causes_exception():
    with pytest.raises(TypeError):
        BlurredContext(svm_file=0)


def test_invalid_load_path_causes_exception():
    with pytest.raises(TypeError):
        BlurredContext().load(0)


def test_svm_file_not_found_causes_exception():
    with pytest.raises(ValueError):
        BlurredContext().load('fail')


def test_invalid_save_path_causes_exception():
    with pytest.raises(TypeError):
        BlurredContext().save(0)
