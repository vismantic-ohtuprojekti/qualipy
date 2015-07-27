import cv2

import imgfilter
from imgfilter.filters import *
from imgfilter.filters.hdr import *


NON_HDR_IMAGE_PATH = 'tests/images/hdr1.jpg'
HDR_IMAGE_PATH = 'tests/images/hdr2.jpg'

NON_HDR_IMAGE = cv2.imread(NON_HDR_IMAGE_PATH)
HDR_IMAGE = cv2.imread(HDR_IMAGE_PATH)

NON_HDR_IMAGE_GRAY = cv2.cvtColor(NON_HDR_IMAGE, cv2.COLOR_BGR2GRAY)
HDR_IMAGE_GRAY = cv2.cvtColor(HDR_IMAGE, cv2.COLOR_BGR2GRAY)


def test_recognizes_hdr_image():
    res = imgfilter.process(HDR_IMAGE_PATH, [HDR()])
    assert res['hdr'] > 0.5


def test_recognizes_non_hdr_image():
    res = imgfilter.process(NON_HDR_IMAGE_PATH, [HDR()])
    assert res['hdr'] < 0.5


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
