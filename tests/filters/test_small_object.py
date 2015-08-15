import tempfile

import cv2
import numpy
import pytest

from imgfilter.filters.small_object import *


def run_filter(saliency_map, filter_obj):
    with tempfile.NamedTemporaryFile(suffix='.jpg') as temp:
        cv2.imwrite(temp.name, saliency_map)
        return filter_obj.predict(temp.name)


def test_returns_correct_object_ratio():
    img = numpy.zeros((100, 100))
    img[20:30, 20:30] = 255
    assert round(get_object_ratio(img), 5) == 0.01


def test_recognizes_small_object():
    img = numpy.zeros((100, 100))
    img[25:30, 25:30] = 255
    assert run_filter(img, ObjectTooSmall(is_saliency_map=True))


def test_doesnt_recognize_normal_image():
    img = numpy.zeros((100, 100))
    img[20:50, 20:50] = 255
    assert not run_filter(img, ObjectTooSmall(is_saliency_map=True))


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        assert ObjectTooSmall().predict(0)
