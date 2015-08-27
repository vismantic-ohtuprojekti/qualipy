import pytest

from qualipy.utils.tesseract import *


TEXT = 'tests/images/text.jpg'


def test_img_to_str_works_for_valid_image():
    assert img_to_str('tesseract', TEXT) == 'Text'


def test_img_to_str_fails_for_invalid_path():
    with pytest.raises(OSError):
        assert img_to_str('tesseract', 'fail')


def test_img_to_str_fails_for_invalid_tesseract_path():
    with pytest.raises(OSError):
        assert img_to_str('fail', TEXT)
