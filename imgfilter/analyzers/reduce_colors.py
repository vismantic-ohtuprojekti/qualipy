"""
Analyzer for reducing the number of colors in an image to a
certain amount. Uses the k-nearest neighbors method.
"""

from analyzer import Analyzer

import cv2
import numpy


def reduce_colors(image, colors):
    """Reduces the number of colors in a given image to certain
    amount. The algorithm uses the k-nearest neighbors method to
    do this. The given image must have colors, meaning three color
    channels. The algorithm is taken from
    "http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans
    /py_kmeans_opencv/py_kmeans_opencv.html"

    :param image: the image to process (must have three channels)
    :type image: numpy.ndarray
    :param colors: how many colors the final image should have
    :type colors: int
    :returns: numpy.ndarray
    """
    Z = image.reshape((-1, 3)).astype(numpy.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(Z, colors, criteria, 10,
                                    cv2.KMEANS_RANDOM_CENTERS)

    center = numpy.uint8(center)
    res = center[label.flatten()]
    return res.reshape(image.shape)


class ReduceColors(Analyzer):

    """Analyzer for reducing the number of colors in an image"""

    def __init__(self):
        """Initializes an analyzer for reducing colors"""
        self.name = 'reduce_colors'
        self.data = None

    def run(self, image, image_path):
        """Runs the analyzer for reducing colors

        :param image: the image matrix
        :type image: numpy.ndarray
        :param image_path: path to the image file
        :type image_path: str
        """
        color_image = cv2.imread(image_path)
        self.data = reduce_colors(color_image, 2)
