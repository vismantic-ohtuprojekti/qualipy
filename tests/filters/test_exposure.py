import imgfilter
from imgfilter.filters import *


OVER_EXPOSED_IMAGE = 'tests/images/over_exposure_sample.jpg'
UNDER_EXPOSED_IMAGE = 'tests/images/under_exposure_sample.jpg'
GOOD_IMAGE = 'tests/images/exposure_sample_good.jpg'


def test_recognizes_over_exposed_image():
    assert not imgfilter.process(OVER_EXPOSED_IMAGE, [Exposure()])


def test_recognizes_under_exposed_image():
    assert not imgfilter.process(UNDER_EXPOSED_IMAGE, [Exposure()])


def test_doesnt_recognize_good_image():
    assert imgfilter.process(GOOD_IMAGE, [Exposure()])
