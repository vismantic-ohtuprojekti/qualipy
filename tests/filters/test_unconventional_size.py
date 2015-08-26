import tempfile

import cv2
import numpy
import pytest

from qualipy.filters.unconventional_size import *


def run_filter(img, filter_obj):
    with tempfile.NamedTemporaryFile(suffix='.jpg') as temp:
        cv2.imwrite(temp.name, img)
        return filter_obj.predict(temp.name)


def test_gives_true_when_ratio_too_high():
    img = numpy.ones(200).reshape(20, 10)
    assert run_filter(img, UnconventionalSize())


def test_gives_true_when_ratio_too_low():
    img = numpy.ones(200).reshape(10, 20)
    assert run_filter(img, UnconventionalSize())


def test_gives_false_when_ratio_correct():
    img = numpy.ones(100).reshape(10, 10)
    assert not run_filter(img, UnconventionalSize())


def test_setting_threshold():
    img = numpy.ones(200).reshape(20, 10)
    assert not run_filter(img, UnconventionalSize(threshold=3))


def test_inverting_threshold():
    img = numpy.ones(200).reshape(20, 10)
    assert run_filter(img, UnconventionalSize(threshold=3,
                                              invert_threshold=True))


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        assert UnconventionalSize().predict(0)
