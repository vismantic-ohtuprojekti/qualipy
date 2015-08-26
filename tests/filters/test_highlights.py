import pytest

from qualipy.filters.highlights import *


HIGHLIGHTS = 'tests/images/highlights.jpg'
NON_HIGHLIGHTS = 'tests/images/framed.jpg'


def test_recognizes_highlights():
    assert Highlights().predict(HIGHLIGHTS)


def test_doesnt_recognize_normal_image():
    assert not Highlights().predict(NON_HIGHLIGHTS)


def test_setting_threshold():
    assert not Highlights(threshold=1).predict(HIGHLIGHTS)


def test_inverting_threshold():
    assert Highlights(1.01, invert_threshold=True).predict(HIGHLIGHTS)


def test_can_return_float():
    assert type(Highlights().predict(HIGHLIGHTS, return_boolean=False)) != bool


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        assert Highlights().predict(0)
