"""Filter for detecting posterized images.

The posterized image detection first loads the given image as a grayscale
image and calculates a histogram of its pixel intensities. From this
histogram the value for each local max point is calculated which measures
how sharp the peak is. Calculating the value takes into account how wide
the peak is, meaning how large the distance between the local minimum
before and the local maximum after it is. The second feature measured is
how large the peak is, meaning how big is the average difference between
the value at the local maximum and two local minimums next to it.
Posterized images have naturally more sharp peaks since colors in the
image are lacking many different shades.
"""

import cv2
import numpy as np

from ..utils.image_utils import read_image
from ..utils.histogram_analyzation import normalize, largest, calculate_peak_value
from ..utils.statistic_common import linear_normalize

from filter import Filter


def get_input_vector(img):
    """Returns a numpy array which contains the average of 20 percent of
    the largest peak values of the histogram of a given image. This value
    can be used to predict whether an image is posterized or not. The
    result can also be given to an SVM.

    :param img: image to be processed
    :type img: numpy.ndarray
    :returns: a numpy array which contains the prediction
    """
    hist = cv2.calcHist([img], [0], None, [256], [0, 255]).T[0]
    hist = normalize(hist)
    peak_values = calculate_peak_value(hist)

    if len(peak_values) == 0:
        return np.array([0.0]).astype(np.float32)

    largest_peak_values = largest(peak_values, 0.2)
    return np.array([np.average(largest_peak_values)]).astype(np.float32)


class Posterized(Filter):

    """Filter for detecting posterized images"""

    name = 'posterized'
    speed = 1

    def __init__(self, threshold=0.5, invert_threshold=False):
        """Initializes a posterized image filter

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        """
        super(Posterized, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Predict if a given image is posterized

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
        prediction = get_input_vector(image)[0]

        if prediction > 0.004:
            prediction = 1.0
        elif prediction < 0.0:
            prediction = 0.0
        else:
            prediction = linear_normalize(prediction, 0.0, 0.004).item(0)

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
