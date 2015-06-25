import numpy

from imgfilter.filters.multiple_salient_regions import *

def test_works_for_saliency_map_with_two_areas():
    saliency_map = np.array([0, 0, 255, 255], [0, 0, 0, 0], [255, 255, 0, 0])
    filter = MultipleSalientRegions()
    filter.parameters['extract_object'] = (saliency_map, 0)

    assert (filter.run() > 0.5)


def test_works_for_saliency_map_with_one_area():
    saliency_map = np.array([0, 0, 0, 0], [0, 0, 0, 0], [255, 255, 0, 0])
    filter = MultipleSalientRegions()
    filter.parameters['extract_object'] = (saliency_map, 0)

    assert (filter.run() < 0.5)
