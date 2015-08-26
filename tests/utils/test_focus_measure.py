import cv2

from qualipy.utils.focus_measure import *

IMAGE = cv2.imread('tests/images/lama.jpg', 0)
BLURRED = cv2.blur(IMAGE, (10, 10))


def test_LAPV_returns_less_for_blurred_image():
    assert LAPV(BLURRED) < LAPV(IMAGE)


def test_LAPM_returns_less_for_blurred_image():
    assert LAPM(BLURRED) < LAPM(IMAGE)


def test_TENG_returns_less_for_blurred_image():
    assert TENG(BLURRED) < TENG(IMAGE)


def test_MLOG_returns_less_for_blurred_image():
    assert MLOG(BLURRED) < MLOG(IMAGE)
