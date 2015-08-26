"""
Filter for detecting over- and underexposed image.

The image is first converted to grayscale and a histogram of its
intensities is produced. The filter then calculates the percentage
of pixels with greater than 250 intensity and normalizes the result
(result * 50) to a float between 0 and 1. If there are no pixels
over 250 intensity, the picture is recognized as underexposed.
"""

import cv2

from ..utils.image_utils import read_image
from ..utils.utils import clipping_percentage

from filter import Filter


def normalized_clipping_percentage(image):
    histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
    clip = clipping_percentage(histogram, 250, True)
    return clip * 50  # normalize


class Exposure(Filter):

    """Filter for detecting over- and underexposure"""

    name = "exposure"
    speed = 1

    def __init__(self, threshold=0.5, invert_threshold=False,
                 negative_under_exposed=False):
        """Initializes an exposure filter

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        :param negative_under_exposed: whether underexposed images should
                                       return -1 instead of 1. The threshold
                                       and boolean logic is unaffected by
                                       the flag
        :type negative_under_exposed: bool
        """
        super(Exposure, self).__init__(threshold, invert_threshold)
        self.negative_exp = negative_under_exposed

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Predict if a given image is over- or underexposed

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
        clip = normalized_clipping_percentage(image)

        # return -1 for under-exposed if flag is set
        if clip < 0.0001:
            prediction = -1 if self.negative_exp else 1
        else:
            prediction = min(1, clip)

        if return_boolean:
            return self.boolean_result(abs(prediction))
        return prediction
