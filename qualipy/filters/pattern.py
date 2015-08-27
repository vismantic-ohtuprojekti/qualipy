"""
Filter for detecting pattern-like images.

The image is first turned into grayscale, after which discrete
fast fourier transformation is applied to construct the magnitude
spectrum of the image. Then frequencies which have intermediate
or low intensities are removed from the magnitude spectrum and
all frequencies with high intensity are intensified to the max
value. After this the distance from the center for each high
intensity frequency is calculated. From this set of distances
anomalies are removed by using the local outlier factor method.

The max from the set of distances is taken. This max distance is
then used as a radius for a circle, and all points outside this
circle in the magnitude spectrum are excluded and the density of
high frequencies is calculated. This density is used to estimate
how pattern-like the image is. Pattern-like images usually exhibit
smaller density than non-pattern-like images.
"""

import cv2
import numpy

from ..utils.image_utils import *
from ..utils.statistic_common import *

from filter import Filter


def distances_from_center(height, width):
    """Returns a matrix of distances from each element to the center of
    a matrix of certain size.

    :param height: height of the matrix
    :type height: int
    :param width: width of the matrix
    :type width: int
    :returns: numpy.ndarray -- the distance matrix
    """
    yy, xx = numpy.mgrid[:height, :width]
    return (xx - width / 2.0) ** 2 + (yy - height / 2.0) ** 2


def pattern_recognition(magnitude_spectrum):
    """Returns a prediction of how pattern-like an image is

    :param magnitude_spectrum: magnitude spectrum of a two-color image
    :type magnitude_spectrum: numpy.ndarray
    :returns: float
    """
    circle = distances_from_center(*magnitude_spectrum.shape)

    mask = magnitude_spectrum > 0.7
    all_distances = numpy.sqrt(circle[mask].flatten())

    all_distances = remove_anomalies(all_distances, 0.4)
    max_distances = get_max_values(all_distances, 20)
    max_distance_avg = numpy.mean(max_distances)

    # Calculate all points that don't fall into a circle
    # with a radius of max_distance_avg, and exclude those
    # from the mask calculated previously
    donut = circle >= max_distance_avg ** 2
    intense_points = numpy.sum(mask & numpy.logical_not(donut))
    all_points = magnitude_spectrum.size - numpy.sum(donut)

    return intense_points / float(all_points)


def scaled_prediction(prediction):
    """Scales the prediction

    :param prediction: the prediction to scale
    :type prediction: float
    :returns: float
    """
    if prediction < 0.05:
        return 1.0
    elif prediction > 0.4:
        return 0.0
    else:
        return 1 - linear_normalize(prediction, 0.0, 0.4).item(0)


class Pattern(Filter):

    """Filter for detecting pattern-like images"""

    name = 'pattern'
    speed = 3

    def __init__(self, threshold=0.5, invert_threshold=False):
        """Initializes a blurred image filter

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        """
        super(Pattern, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Predict if a given image is pattern-like

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
        image = read_color_image(image_path, ROI)
        two_color_gray_image = cv2.cvtColor(reduce_colors(image, 2),
                                            cv2.COLOR_BGR2GRAY)

        magnitude_spectrum = count_magnitude_spectrum(two_color_gray_image)
        prediction = scaled_prediction(pattern_recognition(magnitude_spectrum))

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
