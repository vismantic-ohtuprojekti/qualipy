"""
Filter for detecting multiple salient regions.

The detection works by first extracting the full saliency map
using an object extraction algorithm. The saliency map is binarized
using a threshold which is calculated individually for each image
as the weighted average of 3/4 of the biggest saliency values.
Using this threshold, the image is binarized into solid regions.
All regions and their sizes are calculated using OpenCV's contour
detection. The actual prediction is constructed by dividing the
sum of of the areas of all the regions by the area of the largest
region and squaring the result. This way if the saliency map
contains some small independent areas, the whole image is not
considered to have multiple salient regions.
"""

import cv2
import numpy

from filter import Filter


def count_threshold(saliency_map):
    """Calculates the threshold used for the binarization.

    :param saliency_map: the full saliency map
    :type saliency_map: numpy.ndarray
    :returns: int -- the threshold
    """
    rounded_saliency_map = numpy.around(saliency_map, decimals=-1)
    unique, count = numpy.unique(rounded_saliency_map, return_counts=True)

    smallest_large_index = unique.shape[0] * 3 / 4
    return numpy.average(unique[-smallest_large_index:], axis=0,
                         weights=count[-smallest_large_index:])


def count_areas(saliency_map):
    """Returns a list of areas of all coherent white regions produced by
    binarization using a calculated threshold.

    :param saliency_map: the full saliency map
    :type saliency_map: numpy.ndarray
    :returns: numpy.ndarray -- list of the areas of the regions
    """
    # count threshold and use it to binarize the saliency map
    limit = count_threshold(saliency_map)
    _, thresh = cv2.threshold(saliency_map, limit, 255, cv2.THRESH_BINARY)

    # find coherent regions
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    return numpy.array([cv2.contourArea(contour) for contour in contours])


class MultipleSalientRegions(Filter):

    """Filter for detecting images with multiple salient regions"""

    name = 'multiple_salient_regions'

    def __init__(self, is_saliency_map=False):
        """Initializes a multiple salient regions filter

        :param is_saliency_map: whether the image is already a saliency map
        :type is_saliency_map: bool
        """
        self.parameters = {}
        self.is_saliency_map = is_saliency_map

    def required(self):
        return {'image', 'extract_object'}

    def run(self):
        """Checks if the image contains multiple salient regions.

        :returns: float
        """
        if self.is_saliency_map:
            saliency_map = self.parameters['image']
        else:
            saliency_map, _ = self.parameters['extract_object']

        areas = count_areas(saliency_map)

        # if areas is empty, there are no salient regions in the image
        if not areas.shape[0]:
            return 1.0

        prediction = (numpy.sum(areas) / numpy.amax(areas)) ** 2 - 1.0
        return min(prediction, 1)
