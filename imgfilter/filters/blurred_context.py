"""
Filter for detecting images that have a blurred context.

The filter first constructs a so-called "blur map" from the image
using the method described by Su et al in their paper Blurred Image
Region Detection and Classification (Proceedings of the 19th ACM
International Conference on Multimedia, 2011): for each pixel, its
"blurry degree" is estimated using the singular values of a 5x5px
patch (larger patches can be used for slightly better results, but
at cost in runtime) surrounding the pixel.

This blur map is then broken into 100 partitions of equal size and
the mean value of each partition is used as variable in an input
vector that is fed into a support vector machine. The default support
vector machine has been trained using 450 blurred and 450 undistorted
images that were downloaded from Flickr and labeled by hand.
"""

import numpy
from numpy.lib.stride_tricks import as_strided

from .. import get_data
from ..machine_learning.svm import SVM
from ..analyzers.blur_detection.exif import analyze_background_blur
from ..analyzers.common.result_combination import collective_result
from ..utils.utils import partition_matrix, jit

from filter import Filter


@jit
def blurry_degree(lambdas):
    """Calculates the blurry degree of a patch from its singular
    values obtained from a singular value decomposition. The value
    is calculated as the ratio of the smallest (the input list
    should be ordered) value to the sum of all values.

    :param lambdas: ordered list of singular values
    :type lambdas: numpy.ndarray
    :returns: numpy.float32
    """
    return lambdas[0] / (numpy.sum(lambdas) + 0.001)


@jit
def blurmap(img):
    """Constructs a blurmap from an image.

    :param img: the image matrix
    :type img: numpy.ndarray
    :returns: numpy.ndarray
    """
    patch_size = 5
    patches = as_strided(img,
                         shape=(img.shape[0] - patch_size + 1,
                                img.shape[1] - patch_size + 1,
                                patch_size, patch_size),
                         strides=img.strides * 2)

    svd = numpy.linalg.svd(patches, full_matrices=False, compute_uv=False)
    return numpy.apply_along_axis(blurry_degree, 2, svd)


def get_input_vector(img):
    """Get input vector for use in SVM.

    :param img: the image matrix
    :type img: numpy.ndarray
    :returns: numpy.ndarray -- the input vector
    """
    parts = partition_matrix(blurmap(img), 10)
    return numpy.array([numpy.mean(part) for part in parts],
                       dtype=numpy.float32)


def scaled_prediction(self, prediction):
    """Scales the prediction to range [0, 1].

    :param prediction: the prediction to scale
    :type prediction: float
    :returns: float
    """
    pred = 1 - (1 + prediction) / 2

    if pred < 0:
        return 0
    if pred > 1:
        return 1

    return pred


class BlurredContext(Filter):

    """Filter for detecting images that have a blurred context"""

    name = 'blurred_context'

    def __init__(self):
        """Initializes a blurred context filter"""
        self.parameters = {}

    def required(self):
        return {'resize', 'exif'}

    def run(self):
        """Checks if the background of an image is blurred.

        :returns: float
        """
        svm = SVM()
        svm.load(get_data('svm/blurred_context.yml'))

        input_vec = get_input_vector(self.parameters['resize'])
        algo_prediction = scaled_prediction(svm.predict(input_vec))

        exif_tags = self.parameters['exif']
        exif_prediction = analyze_background_blur(exif_tags)

        return algo_prediction
        # return collective_result([algo_prediction, exif_prediction], 0.0)
