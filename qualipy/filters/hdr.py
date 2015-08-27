"""Filter for detecting HDR images.

We focus on detecting images that have a very noticeable or bad
HDR effect. Several features based on experimentation are looked
for in images. As the objective of high-dynamic-range imaging is
to reproduce a greater dynamic range of luminance, we look at the
luminance of the image by extracting the Y channel of the image
converted into the XYZ color space. We also consider the chrominance
of the image (as luma is typically paired with chrominance) by
looking at the U and V channels of the image converted into the YUV
color space.

Additionally, we calculate the contrast of the image, as HDR images
often exhibit a lower amount of contrast than normal images
(broadening the tonal range comes at the expense of decreased
contrast). The contrast is calculated with the root mean squared
contrast formula. The final feature is the amount of edges present
in comparison to the size of the image, calculated using a Laplacian
edge detector. HDR images usually have a higher amount of edges
present than their normal counterparts.

Finally, these features are fed into a support vector machine, which
has by default been trained with 200 non-HDR and 200 HDR images
collected from various sources and labeled by hand.
"""

import cv2
import numpy

from ..utils.utils import *
from ..utils.image_utils import read_color_image
from .. import get_data

from svm_filter import SVMFilter


def histogram_features(hist, maximum, step):
    """Extract features from a histogram, namely the mean,
    max and maximum difference at certain intervals.

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
    """Calculates the ratio of amount of edges in the image to the size
    of the image
    """
    return numpy.count_nonzero(obj) / float(obj.size)


def edges(gray):
    """Calculate ratio of edges present in parts of an image.

    :param gray: grayscale image matrix
    :type gray: numpy.ndarray
    :returns: numpy.ndarray
    """
    # Laplacian edge detector
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


class HDR(SVMFilter):

    """Filter for detecting HDR images"""

    name = 'hdr'
    speed = 2

    def __init__(self, threshold=0.5, invert_threshold=False, svm_file=None):
        """Initializes a HDR image filter

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
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
            super(HDR, self).__init__(threshold, invert_threshold,
                                      get_data('svm/hdr.yml'))
        else:
            super(HDR, self).__init__(threshold, invert_threshold, svm_file)

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Predict if a given image is a HDR image

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
        vector = get_input_vector(read_color_image(image_path, ROI))
        prediction = scaled_prediction(self.svm.predict(vector))

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction

    def train(self, images, labels, save_path=None):
        """Retrain the filter with new training images.

        :param images: list of image paths to training images
        :type images: list
        :param labels: list of labels associated with the images,
                       0 for negative and 1 for positive
        :type labels: list
        :param save_path: possible filepath to save the resulting
                          model to, None if not needed
        :type save_path: str
        """
        super(HDR, self).train(images, labels, save_path,
                               cv2.imread, get_input_vector)
