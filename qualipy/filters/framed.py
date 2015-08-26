"""
Filter for detecting framed images.

The filter recognizes images that are framed, or in other words,
images that have four homogeneous edges around them. It doesn't
recognize images where only two sides are the same color or images
where the frames have a texture added in them.

The filter first binarizes the image with adaptive thresholding and
uses the findContours-method from OpenCV to detect any rectangles
in the image. If the method returns four coordinates (for each
corner of the image), they are analyzed to see if they form an
rectangle, which is the case in framed images.
"""

import cv2
import numpy

from ..utils.image_utils import read_image
from filter import Filter


def findContours(image):
    """Converts the image to contain only edges and finds
    contours in that image.

    :param image: the image matrix
    :type image: numpy.ndarray
    """
    thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    return contours


def analyzeContours(contours):
    """Checks if the first layer of contours (contours[0]) is rectangular
    by checking if there are 4 coordinates in contours that are perpendicular
    to each other.
    """
    if len(contours[0]) != 4 and len(contours[0]) != 8:
        return 0

    first, second, prev = [1, 1], [1, 1], 0
    for i, val in enumerate(numpy.nditer(contours[0])):
        if i % 2:
            second = [prev, val]
        else:
            first = [prev, val]

        # compare pair to the previous pair
        for num in first:
            if num in second:
                break
        else:
            return 0

        prev = val

    return 1


class Framed(Filter):

    """Filter for detecting images with frames"""

    name = 'framed'
    speed = 1

    def __init__(self, threshold=0.5, invert_threshold=False):
        """Initializes an framed filter

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        """
        super(Framed, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Predict if a given image has a frame

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
        contours = findContours(image)
        prediction = analyzeContours(contours)

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
