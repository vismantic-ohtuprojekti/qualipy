import numpy
import pytest

from qualipy.filters.exposure import *


OVER_EXPOSED_IMAGE = 'tests/images/over_exposure_sample.jpg'
UNDER_EXPOSED_IMAGE = 'tests/images/under_exposure_sample.jpg'
GOOD_IMAGE = 'tests/images/exposure_sample_good.jpg'


def test_normalized_clipping_percentage_for_black_image():
    img = numpy.ones((10, 10)).astype(numpy.uint8)
    assert round(normalized_clipping_percentage(img)) == 0


def test_normalized_clipping_percentage_for_white_image():
    img = numpy.ones((10, 10)).astype(numpy.uint8)
    img[:, :] = 255
    assert round(normalized_clipping_percentage(img)) == 50


def test_recognizes_over_exposed():
    assert Exposure().predict(OVER_EXPOSED_IMAGE)


def test_recognizes_under_exposed():
    assert Exposure().predict(OVER_EXPOSED_IMAGE)


def test_doesnt_recognize_normal_image():
    assert not Exposure().predict(GOOD_IMAGE)


def test_setting_threshold():
    assert not Exposure(threshold=1).predict(OVER_EXPOSED_IMAGE)


def test_inverting_threshold():
    assert Exposure(1.01, invert_threshold=True).predict(OVER_EXPOSED_IMAGE)


def test_can_return_float():
    assert type(Exposure().predict(OVER_EXPOSED_IMAGE,
                                   return_boolean=False)) != bool


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        assert Exposure().predict(0)
