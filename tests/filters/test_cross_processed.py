import pytest

from imgfilter.filters.cross_processed import *

CROSS_PROCESSED = 'tests/images/cross_processed.png'
NON_CROSS_PROCESSED = 'tests/images/framed.jpg'


def test_recognizes_cross_processed():
    assert CrossProcessed().predict(CROSS_PROCESSED)


def test_doesnt_recognize_normal_image():
    assert not CrossProcessed().predict(NON_CROSS_PROCESSED)


def test_setting_threshold():
    assert not CrossProcessed(threshold=1).predict(CROSS_PROCESSED)


def test_inverting_threshold():
    assert CrossProcessed(1.01, invert_threshold=True).predict(CROSS_PROCESSED)


def test_can_return_float():
    assert type(CrossProcessed().predict(CROSS_PROCESSED,
                                         return_boolean=False)) == float


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        assert CrossProcessed().predict(0)
