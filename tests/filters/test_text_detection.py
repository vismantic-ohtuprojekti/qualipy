import pytest

from qualipy.filters import TextDetection


TEXT = 'tests/images/text.jpg'
NON_TEXT = 'tests/images/lama.jpg'


def test_recognizes_text():
    assert TextDetection().predict(TEXT)


def test_doesnt_recognize_normal_image():
    assert not TextDetection().predict(NON_TEXT)


def test_setting_threshold():
    assert not TextDetection(threshold=1).predict(TEXT)


def test_inverting_threshold():
    assert TextDetection(1.01, invert_threshold=True).predict(TEXT)


def test_can_return_float():
    assert type(TextDetection().predict(TEXT, return_boolean=False)) != bool


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        assert TextDetection().predict(0)


def test_wrong_tesseract_path_raises_exception():
    with pytest.raises(OSError):
        assert TextDetection(tesseract_path='fail').predict(TEXT)
