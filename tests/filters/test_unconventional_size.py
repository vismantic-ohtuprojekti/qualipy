import cv2
import numpy
import tempfile

import imgfilter
from imgfilter.filters.unconventional_size import UnconventionalSize


def run_filter(img):
    with tempfile.NamedTemporaryFile(suffix='.jpg') as temp:
        cv2.imwrite(temp.name, img)
        return imgfilter.process(temp.name, [UnconventionalSize()])


def test_gives_true_when_ratio_too_high():
    img = numpy.ones(200).reshape(20, 10)
    assert not run_filter(img)


def test_gives_true_when_ratio_too_low():
    img = numpy.ones(200).reshape(10, 20)
    assert not run_filter(img)


def test_gives_false_when_ratio_correct():
    img = numpy.ones(100).reshape(10, 10)
    assert run_filter(img)
