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

from ..utils.image_utils import read_image
from ..utils.object_extraction import extract_object

from filter import Filter


def count_threshold(saliency_map):
    """Calculates the threshold used for the binarization.
    Calculated as the weighted average of 3/4 of the biggest
    saliency values.

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
    speed = 5

    def __init__(self, threshold=0.5, invert_threshold=False,
                 is_saliency_map=False):
        """Initializes a multiple salient regions filter

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        :param: is_saliency_map: whether the given image is already a
                                 saliency map
        :type is_saliency_map: bool
        """
        super(MultipleSalientRegions, self).__init__(threshold,
                                                     invert_threshold)
        self.is_saliency_map = is_saliency_map

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Predict if a given image has multiple salient regions

        :param image_path: path to the image
        :type image_path: str
        :param return_boolean: whether to return the result as a
                               float between 0 and 1 or as a boolean
                               (threshold is given to the class)
        :type return_boolean: bool
        :param ROI: possible region of interest as a 4-tuple
                    (x0, y0, width, height), None if not needed
        :returns: the prediction as a bool or float depending on the
                  return_boolean parameter
        """
        if self.is_saliency_map:
            saliency_map = read_image(image_path, ROI)
        else:
            saliency_map, _ = extract_object(image_path)

        areas = count_areas(saliency_map)

        # if areas is empty, there are no salient regions in the image
        if not areas.shape[0]:
            return False if return_boolean else 0.

        prediction = (numpy.sum(areas) / numpy.amax(areas)) ** 2 - 1.0
        prediction = min(prediction, 1)  # limit prediction to range [0, 1]

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
