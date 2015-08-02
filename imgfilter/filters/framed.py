import cv2
import numpy

from ..utils.image_utils import read_image
from filter import Filter


def findContours(image):
    """Converts the image to contain only edges and finds
       contours in that image"""
    thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    return contours


def analyzeContours(contours, height, width):

    # Checks if there is four contours (one rectangle)
    # or eight (two rectangles)
    if len(contours[0]) != 4 and len(contours[0]) != 8:
        return 0

    first = [1, 1]
    second = [1, 1]
    x = 0

    # Check contours are orthogonal
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
        """Initializes a framed filter"""
        super(Framed, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True, ROI=None):
        image = read_image(image_path, ROI)
        height, width = image.shape
        contours = findContours(image)
        prediction = analyzeContours(contours, height, width)

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
