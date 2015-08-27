"""
Filter for detecting images that have highlights

This filter recognizes images that contain one or more bright
areas, for example the sun or spotlights from concerts. The
difference to the exposure filter is that the bright area must
be contiguous and the result is either 0 or 1.

The image is first converted to grayscale and blurred to remove
unwanted noise. Then the image is thresholded so that pixels with
intensity over 250 are white and the rest are black, to help
identify distinct highlighted areas. To count how many highlighted
areas exist, OpenCV's findContours method is used to look for
the areas in the thresholded image, and of the areas found, only
those that are not either too small or rectangular are counted.
"""

import cv2

from ..utils.image_utils import read_image
from ..utils.histogram_analyzation import *

from filter import Filter


def count_areas(contours, num_sides=7, area_size=50):
    """Counts the number of areas that are not rectangular or too small
    from the list of contours.

    :param contours: list of contours
    :returns: int -- number of non-rectangular objects found
    """
    count = 0
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) > num_sides and cv2.contourArea(cnt) > area_size:
            count += 1
    return count


class Highlights(Filter):

    """Filter for detecting images that have highlights"""

    name = 'highlights'
    speed = 1

    def __init__(self, threshold=0.5, invert_threshold=False):
        """Initializes an highlights filter

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        """
        super(Highlights, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Predict if a given image has highlights

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
        image = read_image(image_path, ROI)
        blur = cv2.GaussianBlur(image, (5, 5), 0)  # remove unwanted noise
        ret, thresh = cv2.threshold(blur, 250, 255, 0)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
        areas = count_areas(contours)
        prediction = 1 if areas > 0 else 0

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
