import numpy
import tempfile

import imgfilter
from imgfilter.filters.multiple_salient_regions import *


def run_filter(saliency_map):
    with tempfile.NamedTemporaryFile(suffix='.jpg') as temp:
        cv2.imwrite(temp.name, saliency_map)
        return imgfilter.process(temp.name, [MultipleSalientRegions()])


# def test_works_for_saliency_map_with_one_area():
#     saliency_map = numpy.zeros((100, 100), dtype=numpy.uint8)
#     saliency_map[10:20, 10:20] = 255

#     assert run_filter(saliency_map)


# def test_works_for_saliency_map_with_two_areas():
#     saliency_map = numpy.zeros((100, 100), dtype=numpy.uint8)
#     saliency_map[10:20, 10:20] = 255
#     saliency_map[80:90, 80:90] = 255

#     assert not run_filter(saliency_map)
