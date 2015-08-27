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

import cv2
import numpy
from numpy.lib.stride_tricks import as_strided

from .. import get_data
# from ..algorithms.exif import analyze_background_blur
# from ..utils.result_combination import collective_result
from ..utils.image_utils import read_image, resize, read_exif_tags
from ..utils.utils import partition_matrix, scaled_prediction, jit

from svm_filter import SVMFilter


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

    # for each pixel, create a view to a patch_size x patch_size
    # matrix where the pixel is in the center of the matrix
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


class BlurredContext(SVMFilter):

    """Filter for detecting images that have a blurred context"""

    name = 'blurred_context'
    speed = 4

    def __init__(self, threshold=0.5, invert_threshold=False, svm_file=None):
        """Initializes a blurred context filter

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
            super(BlurredContext, self).__init__(
                threshold, invert_threshold,
                get_data('svm/blurred_context.yml'))
        else:
            super(BlurredContext, self).__init__(threshold, invert_threshold,
                                                 svm_file)

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Predict if a given image has a blurred context

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
        input_vec = get_input_vector(resize(read_image(image_path, ROI), 500))
        algo_prediction = scaled_prediction(self.svm.predict(input_vec))

        # exif_tags = read_exif_tags(image)
        # exif_prediction = analyze_background_blur(exif_tags)

        if return_boolean:
            return self.boolean_result(algo_prediction)
        return algo_prediction
        # return collective_result([algo_prediction, exif_prediction], 0.0)

    def train(self, images, labels, save_path=None):
        """Retrain the filter with new training images.

        :param images: list of image paths to training images
        :type images: list
        :param labels: list of labels associated with the images,
                       0 for negative and 1 for positive
        :type labels: list
        :param save_path: possible file path to save the resulting
                          model to, None if not needed
        :type save_path: str
        """
        super(BlurredContext, self).train(
            images, labels, save_path,
            lambda img: cv2.imread(img, cv2.CV_LOAD_IMAGE_GRAYSCALE),
            lambda img: get_input_vector(resize(img, 500)))
