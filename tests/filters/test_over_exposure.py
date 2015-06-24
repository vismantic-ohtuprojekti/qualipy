import cv2

from imgfilter.filters.over_exposure import *


IMAGE = cv2.imread('tests/images/lama.jpg', 0)
HIST = cv2.calcHist([IMAGE], [0], None, [256], [0, 256])


def test_clipping_percentage_returns_one_if_threshold_is_zero():
    assert round(clipping_percentage(HIST, 0), 5) == 1


def test_clipping_percentage_returns_zero_if_threshold_is_max():
    assert round(clipping_percentage(HIST, 256), 5) == 0


def test_clipping_percentage_returns_correct_value():
    assert round(clipping_percentage(HIST, 250), 3) == 0.004
