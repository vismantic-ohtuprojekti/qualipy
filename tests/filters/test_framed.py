import pytest

from qualipy.filters.framed import *


FRAMED = 'tests/images/framed.jpg'
NON_FRAMED = 'tests/images/lama.jpg'


def test_recognizes_framed():
    assert Framed().predict(FRAMED)


def test_doesnt_recognize_normal_image():
    assert not Framed().predict(NON_FRAMED)


def test_setting_threshold():
    assert not Framed(threshold=1).predict(FRAMED)


def test_inverting_threshold():
    assert Framed(1.01, invert_threshold=True).predict(FRAMED)


def test_can_return_float():
    assert type(Framed().predict(FRAMED, return_boolean=False)) != bool


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        assert Framed().predict(0)
