import cv2
import numpy

from imgfilter.machine_learning.svm import SVM
from imgfilter.utils.utils import scaled_prediction, partition_matrix
from .. import get_data

from filter import Filter


def edge_ratio(obj):
    return numpy.count_nonzero(obj) / float(obj.size)


def normalize(arr):
    arr_min = numpy.min(arr)
    arr_max = numpy.max(arr)
    return (arr - arr_min) / float(arr_max - arr_min)


def histogram_features(hist, maximum, step):
    means, maxes, max_diffs = [], [], []

    for i in xrange(step, maximum, step):
        view = hist[i - step:i]
        means.append(numpy.mean(view))
        maxes.append(numpy.max(view))
        max_diffs.append(numpy.max(numpy.diff(view)))

    return numpy.array(means, dtype=numpy.float32), \
        numpy.array(maxes, dtype=numpy.float32), \
        numpy.array(max_diffs, dtype=numpy.float32)


def color_channel_feature(space, maximum, step):
    hist = cv2.calcHist([space.flatten()], [0], None, [maximum],
                        [0, maximum - 1]).T[0]

    features = tuple([normalize(feat) for feat in
                      histogram_features(hist, maximum, step)])
    return numpy.concatenate(features)


def contrast(luminance):

    def RMS_contrast(view):
        norm = numpy.array(view, dtype=numpy.float32).flatten() / 255.
        intensities = (numpy.sum(norm) / norm.size - norm) ** 2
        return numpy.sum(intensities) / norm.size

    parts = partition_matrix(luminance, 16)
    return numpy.array([RMS_contrast(part) for part in parts],
                       dtype=numpy.float32)


def edges(gray):
    gray_lap = cv2.Laplacian(gray, cv2.CV_16S, ksize=3)
    edges = cv2.convertScaleAbs(gray_lap)
    parts = partition_matrix(edges, 16)

    return numpy.array([edge_ratio(part) for part in parts],
                       dtype=numpy.float32)


def get_input_vector(image):
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

    def __init__(self):
        """Initializes a HDR image filter"""
        self.parameters = {}

    def required(self):
        return {'color_image'}

    def run(self):
        svm = SVM()
        svm.load(get_data('svm/hdr.yml'))

        vector = get_input_vector(self.parameters['color_image'])
        return scaled_prediction(svm.predict(vector))
