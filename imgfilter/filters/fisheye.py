import cv2
import numpy

from .. import get_data
from ..utils.image_utils import read_image
from ..utils.utils import partition_matrix, scaled_prediction

from svm_filter import SVMFilter


def get_input_vector(image):
    """Get input vector for use in SVM

    :parem image: the image matrix
    :type image: numpy.ndarray
    :returns: numpy.ndarray -- the input vector
    """
    parts = partition_matrix(image, 5)
    return numpy.array([mean_lines(part) for part in parts],
                       dtype=numpy.float32)


def mean_lines(image):
    """Calculate the average angle of straight lines in an image

    :param image: the image matrix
    :type image: numpy.ndarray
    :returns: float -- the average angle
    """
    edges = cv2.adaptiveThreshold(image, 255,
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 11, 4)
    lines = cv2.HoughLines(edges, 1, numpy.pi / 180, 60)

    a, i = 0, 0.00001
    if lines is not None:
        for rho, theta in lines[0]:
            a += numpy.cos(theta)
            i += 1.0

    return a / i


class Fisheye(SVMFilter):

    name = 'fisheye'
    speed = 1

    def __init__(self, threshold=0.5, invert_threshold=False,
                 svm_file=None):
        """Initializes an framed filter

        :param threshold: threshold at which the resulting prediction
                          is changed from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        :param svm_file: path to a file to load an SVM model from, overrides
                         the default SVM model
        :type svm_file: str
        """
        if svm_file is None:
            super(Fisheye, self).__init__(
                threshold, invert_threshold,
                get_data('svm/fisheye.yml'))
        else:
            super(Fisheye, self).__init__(
                threshold, invert_threshold, svm_file)

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Predict if a given image is taken through a fisheye lens

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
        input_vec = get_input_vector(read_image(image_path, ROI))
        prediction = scaled_prediction(self.svm.predict(input_vec))

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
