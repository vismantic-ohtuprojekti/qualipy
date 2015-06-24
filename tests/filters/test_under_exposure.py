import cv2

from imgfilter.utils.utils import clipping_percentage

IMAGE = cv2.imread('tests/images/uni_scene1_minus_3.png', 0)
HIST = cv2.calcHist([IMAGE], [0], None, [256], [0, 256])


def test_clipping_percentage_returns_one_if_threshold_is_zero():
    assert round(clipping_percentage(HIST, 0, False), 5) == 0


def test_clipping_percentage_returns_zero_if_threshold_is_max():
    assert round(clipping_percentage(HIST, 256, False), 5) == 1


def test_clipping_percentage_returns_correct_value():
    assert round(clipping_percentage(HIST, 5, False), 3) == .023
