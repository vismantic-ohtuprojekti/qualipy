import pytest

from qualipy.filters import *


PATTERN = 'tests/images/pattern.jpg'
NON_PATTERN = 'tests/images/lama.jpg'


def test_recognizes_pattern():
    assert Pattern().predict(PATTERN)


def test_doesnt_recognize_normal_image():
    assert not Pattern().predict(NON_PATTERN)


def test_setting_threshold():
    assert not Pattern(threshold=1).predict(PATTERN)


def test_inverting_threshold():
    assert Pattern(1.01, invert_threshold=True).predict(PATTERN)


def test_can_return_float():
    assert type(Pattern().predict(PATTERN, return_boolean=False)) != bool


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        assert Pattern().predict(0)
