import tempfile

import numpy
import pytest

from qualipy.filters.multiple_salient_regions import *


def run_filter(saliency_map, filter_obj, return_boolean=True):
    with tempfile.NamedTemporaryFile(suffix='.jpg') as temp:
        cv2.imwrite(temp.name, saliency_map)
        return filter_obj.predict(temp.name, return_boolean=return_boolean)


def test_works_for_saliency_map_with_one_area():
    saliency_map = numpy.zeros((100, 100), dtype=numpy.uint8)
    saliency_map[10:20, 10:20] = 255

    assert not run_filter(saliency_map,
                          MultipleSalientRegions(is_saliency_map=True))


def test_works_for_saliency_map_with_two_areas():
    saliency_map = numpy.zeros((100, 100), dtype=numpy.uint8)
    saliency_map[10:20, 10:20] = 255
    saliency_map[80:90, 80:90] = 255

    assert run_filter(saliency_map,
                      MultipleSalientRegions(is_saliency_map=True))


def test_works_for_saliency_map_with_no_areas():
    saliency_map = numpy.zeros((100, 100), dtype=numpy.uint8)

    assert not run_filter(saliency_map,
                          MultipleSalientRegions(is_saliency_map=True))


def test_can_return_float():
    saliency_map = numpy.zeros((100, 100), dtype=numpy.uint8)
    saliency_map[10:20, 10:20] = 255
    assert type(run_filter(saliency_map,
                           MultipleSalientRegions(is_saliency_map=True),
                           False)) != bool


def test_setting_threshold():
    saliency_map = numpy.zeros((100, 100), dtype=numpy.uint8)
    saliency_map[10:20, 10:20] = 255
    saliency_map[80:90, 80:90] = 255

    assert not run_filter(saliency_map,
                          MultipleSalientRegions(threshold=1,
                                                 is_saliency_map=True))


def test_inverting_threshold():
    saliency_map = numpy.zeros((100, 100), dtype=numpy.uint8)
    saliency_map[10:20, 10:20] = 255
    saliency_map[80:90, 80:90] = 255

    assert run_filter(saliency_map,
                      MultipleSalientRegions(threshold=1.01,
                                             invert_threshold=1,
                                             is_saliency_map=True))


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        assert MultipleSalientRegions().predict(0)
