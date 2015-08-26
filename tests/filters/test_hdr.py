import cv2
import pytest

from qualipy.filters.hdr import *


NON_HDR_IMAGE_PATH = 'tests/images/hdr1.jpg'
HDR_IMAGE_PATH = 'tests/images/hdr2.jpg'

NON_HDR_IMAGE = cv2.imread(NON_HDR_IMAGE_PATH)
HDR_IMAGE = cv2.imread(HDR_IMAGE_PATH)

NON_HDR_IMAGE_GRAY = cv2.cvtColor(NON_HDR_IMAGE, cv2.COLOR_BGR2GRAY)
HDR_IMAGE_GRAY = cv2.cvtColor(HDR_IMAGE, cv2.COLOR_BGR2GRAY)


def test_hdr_image_has_lower_contrast():
    assert RMS_contrast(NON_HDR_IMAGE_GRAY) > RMS_contrast(HDR_IMAGE_GRAY)


def test_hdr_image_has_higher_edge_ratio():
    assert edges(NON_HDR_IMAGE_GRAY)[0] < edges(HDR_IMAGE_GRAY)[0]


def test_histogram_features_returns_correct_amount_of_features():
    hist = cv2.calcHist([HDR_IMAGE_GRAY.flatten()], [0], None, [256],
                        [0, 255]).T[0]
    features = histogram_features(hist, 256, 16)

    assert len(features) == 3


def test_input_vector_is_of_right_size():
    assert len(get_input_vector(HDR_IMAGE)) == 694


def test_input_vector_is_of_right_type():
    assert get_input_vector(HDR_IMAGE).dtype == numpy.float32


def test_recognizes_hdr_image():
    assert HDR().predict(HDR_IMAGE_PATH)


def test_doesnt_recognize_normal_image():
    assert not HDR().predict(NON_HDR_IMAGE_PATH)


def test_setting_threshold():
    assert not HDR(threshold=1).predict(HDR_IMAGE_PATH)


def test_inverting_threshold():
    assert HDR(1.01, invert_threshold=True).predict(HDR_IMAGE_PATH)


def test_can_return_float():
    assert type(HDR().predict(HDR_IMAGE_PATH, return_boolean=False)) != bool


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        assert HDR().predict(0)


def test_training_with_too_few_images_causes_exception():
    with pytest.raises(ValueError):
        HDR().train([HDR_IMAGE_PATH], [0])


def test_training_with_invalid_number_of_labels_causes_exception():
    with pytest.raises(ValueError):
        HDR().train([HDR_IMAGE_PATH], [])


def test_invalid_svm_file_causes_exception():
    with pytest.raises(TypeError):
        HDR(svm_file=0)


def test_invalid_load_path_causes_exception():
    with pytest.raises(TypeError):
        HDR().load(0)


def test_svm_file_not_found_causes_exception():
    with pytest.raises(ValueError):
        HDR().load('fail')


def test_invalid_save_path_causes_exception():
    with pytest.raises(TypeError):
        HDR().save(0)
