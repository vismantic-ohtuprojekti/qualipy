import cv2
import numpy

from ..utils.image_utils import read_image
from filter import Filter


def findContours(image):
    """Converts the image to contain only edges and finds
       contours in that image.
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

    first = [1, 1]
    second = [1, 1]
    x = 0

    # Iterate coordinates and compare each pair to the previous.
    for i, val in enumerate(numpy.nditer(contours[0])):
        if i % 2:
            second[0] = x
            second[1] = val
        else:
            first[0] = x
            first[1] = val

        for num in first:
            if num in second:
                break
        else:
            return 0

        x = val

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
        image = read_image(image_path, ROI)
        contours = findContours(image)
        prediction = analyzeContours(contours)

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
