import cv2
import numpy

from imgfilter.analyzers.reduce_colors import *

IMAGE = cv2.imread('tests/images/lama.jpg')


def test_reduces_image_correctly_to_one_color():
    reduced = reduce_colors(IMAGE, 1)
    assert len(numpy.unique(reduced)) == 3


def test_reduces_image_correctly_to_two_colors():
    reduced = reduce_colors(IMAGE, 2)
    assert len(numpy.unique(reduced)) == 6
