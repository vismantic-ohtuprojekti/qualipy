import cv2

from imgfilter.analyzers.sharpen import *
from imgfilter.analyzers.blur_detection.focus_measure import *

IMAGE = cv2.imread('tests/images/lama.jpg', 0)


def test_sharpen_returns_more_in_focus_for_blurred_image():
    assert LAPV(sharpen(IMAGE)) > LAPV(IMAGE)
