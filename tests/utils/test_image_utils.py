import cv2
import numpy
import tempfile
import pytest

from qualipy.utils.image_utils import *
from qualipy.utils.focus_measure import *

IMAGE_PATH = 'tests/images/lama.jpg'
IMAGE = cv2.imread(IMAGE_PATH)
IMAGE_GRAY = cv2.cvtColor(IMAGE, cv2.COLOR_BGR2GRAY)


def test_raises_exception_for_invalid_image_path():
    with pytest.raises(IOError):
        read_image('fail')


def test_raises_exception_for_invalid_image():
    with tempfile.NamedTemporaryFile(suffix='.jpg') as temp:
        with open(temp.name, 'w') as out:
            out.write('fail')
        with pytest.raises(IOError):
            read_image(temp.name)


def test_can_read_valid_image():
    assert read_image(IMAGE_PATH).shape == IMAGE_GRAY.shape


def test_extract_roi_works():
    assert extract_ROI(IMAGE_PATH, IMAGE,
                       (20, 20, 20, 20)).shape == (20, 20, 3)


def test_fails_for_invalid_roi():
    with pytest.raises(TypeError):
        extract_ROI(IMAGE_PATH, IMAGE_GRAY, (0, 0, 0))


def test_fails_for_too_large_roi():
    with pytest.raises(ValueError):
        extract_ROI(IMAGE_PATH, IMAGE_GRAY, (0, 0, 1e5, 1e5))


def test_reduces_image_correctly_to_one_color():
    reduced = reduce_colors(IMAGE, 1)
    assert len(numpy.unique(reduced)) == 3


def test_reduces_image_correctly_to_two_colors():
    reduced = reduce_colors(IMAGE, 2)
    assert len(numpy.unique(reduced)) == 6


def test_resize_smaller_image_than_max_size_returns_same_size_image():
    assert resize(numpy.eye(100), 200).shape == (100, 100)


def test_resizes_too_tall_image_correctly():
    assert resize(numpy.ones(1000).reshape(5, 200), 100).shape == (100, 2)


def test_resizes_too_wide_image_correctly():
    assert resize(numpy.ones(1000).reshape(200, 5), 100).shape == (2, 100)


def test_resize_too_tall_and_wide_image_correctly():
    assert resize(numpy.eye(100), 10).shape == (10, 10)


def test_sharpen_returns_more_in_focus_for_blurred_image():
    assert LAPV(sharpen(IMAGE)) > LAPV(IMAGE)
