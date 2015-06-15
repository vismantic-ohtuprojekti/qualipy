import numpy
from imgfilter.analyzers.resize import *


def test_resize_smaller_image_than_max_size_returns_same_size_image():
    assert resize(numpy.eye(100), 200).shape == (100, 100)


def test_resizes_too_tall_image_correctly():
    assert resize(numpy.ones(1000).reshape(5, 200), 100).shape == (100, 2)


def test_resizes_too_wide_image_correctly():
    assert resize(numpy.ones(1000).reshape(200, 5), 100).shape == (2, 100)


def test_resize_too_tall_and_wide_image_correctly():
    assert resize(numpy.eye(100), 10).shape == (10, 10)
