import cv2
import numpy

from ..machine_learning.svm import SVM
from ..utils.utils import *
from ..utils.image_utils import read_color_image
from .. import get_data

from filter import Filter


def histogram_features(hist, maximum, step):
    """Get features from a histogram.

    :param hist: a histogram representing a color channel
    :type hist: numpy.ndarray
    :param maximum: maximum value of the color channel
    :type maximum: int
    :param step: in how big steps should the histogram be sampled
    :type step: int
    """
    means, maxes, max_diffs = [], [], []

    for i in xrange(step, maximum, step):
        view = hist[i - step:i]
        means.append(numpy.mean(view))
        maxes.append(numpy.max(view))
        max_diffs.append(numpy.max(numpy.diff(view)))

    return numpy.array(means, dtype=numpy.float32), \
        numpy.array(maxes, dtype=numpy.float32), \
        numpy.array(max_diffs, dtype=numpy.float32)


def color_channel_feature(channel, maximum, step):
    """Calculate features from a color channel based on its histogram.

    :param channel: the color channel
    :type channel: numpy.ndarray
    :param maximum: maximum value of the color channel
    :type maximum: int
    :param step: in how big steps should the histogram be sampled
    :type step: int
    """
    hist = cv2.calcHist([channel.flatten()], [0], None, [maximum],
                        [0, maximum - 1]).T[0]

    features = tuple([normalize(feat) for feat in
                      histogram_features(hist, maximum, step)])
    return numpy.concatenate(features)


def RMS_contrast(luminance):
    """Calculates the RMS contrast of an image.
    See https://en.wikipedia.org/wiki/Contrast_%28vision%29#RMS_contrast

    :param luminance: matrix representing luminance of each image pixel
    :type luminance: numpy.ndarray
    :returns: numpy.ndarray
    """
    norm = numpy.array(luminance, dtype=numpy.float32).flatten() / 255.
    intensities = (numpy.sum(norm) / norm.size - norm) ** 2
    return numpy.sum(intensities) / norm.size


def contrast(luminance):
    """Calculates the contrast in parts of an image.

    :param luminance: matrix representing luminance of each image pixel
    :type luminance: numpy.ndarray
    :returns: numpy.ndarray
    """
    parts = partition_matrix(luminance, 16)
    return numpy.array([RMS_contrast(part) for part in parts],
                       dtype=numpy.float32)


def edge_ratio(obj):
    return numpy.count_nonzero(obj) / float(obj.size)


def edges(gray):
    """Calculate ratio of edges present in parts of an image.

    :param gray: grayscale image matrix
    :type gray: numpy.ndarray
    :returns: numpy.ndarray
    """
    gray_lap = cv2.Laplacian(gray, cv2.CV_16S, ksize=3)
    edges = cv2.convertScaleAbs(gray_lap)
    parts = partition_matrix(edges, 16)

    return numpy.array([edge_ratio(part) for part in parts],
                       dtype=numpy.float32)


def get_input_vector(image):
    """Get input vector for use in SVM.

    :param image: the color image matrix
    :type img: numpy.ndarray
    :returns: numpy.ndarray -- the input vector
    """
    XYZ = cv2.cvtColor(image, cv2.COLOR_BGR2XYZ)
    YUV = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    X, Y, Z = cv2.split(XYZ)
    y, u, v = cv2.split(YUV)

    histY = color_channel_feature(Y, 256, 16)
    histy = color_channel_feature(y, 256, 16)
    histu = color_channel_feature(u, 240, 15)
    histv = color_channel_feature(v, 240, 15)

    cont = contrast(Y)
    edge = edges(gray)

    return numpy.concatenate((histY, histy, histu, histv,
                              cont, edge)).astype(numpy.float32)


class HDR(Filter):

    """Filter for detecting HDR images"""

    name = 'hdr'
    speed = 2

    def __init__(self, threshold=0.5, invert_threshold=False):
        """Initializes a HDR image filter"""
        super(HDR, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True):
        """Detects if an image is a HDR image.

        :returns: float
        """
        svm = SVM()
        svm.load(get_data('svm/hdr.yml'))

        vector = get_input_vector(read_color_image(image_path))
        prediction = scaled_prediction(svm.predict(vector))

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
