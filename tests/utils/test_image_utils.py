import cv2
import numpy

from imgfilter.utils.image_utils import *
from imgfilter.utils.focus_measure import *

IMAGE = cv2.imread('tests/images/lama.jpg')


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
