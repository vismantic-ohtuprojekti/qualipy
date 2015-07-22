"""
Analyzer for resizing an image.
"""

import cv2

from analyzer import Analyzer


class Resize(Analyzer):

    """Analyzer for resizing an image"""

    def __init__(self):
        """Initializes a resize analyzer"""
        self.name = 'resize'
        self.data = None

    def run(self, image, image_path):
        """Runs the resize analyzer

        :param image: the image matrix
        :type image: numpy.ndarray
        :param image_path: path to the image file
        :type image_path: str
        """
        self.data = resize(image, 500)


def resize(image, size):
    """Resizes an image matrix so that the longest side
    of an image is the specified size at maximum.

    :param image: the image matrix
    :type image: numpy.ndarray
    :param size: the maximum size for one side of the image
    :type size: int
    :returns: numpy.ndarray
    """
    height, width = image.shape

    if max(height, width) <= size:
        return image

    ratio = max(height, width) / float(size)
    height /= ratio
    width /= ratio
    return cv2.resize(image, (int(height), int(width)))
