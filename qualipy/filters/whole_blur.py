"""
Filter for detecting blurred images.

Four focus measure algorithms that are described in "Analysis of focus
measure operators for shape-from-focus" (Pattern recognition, 2012) by
Pertuz et al are applied to the whole image. Focus measures measure
the relative degree of focus of an image, and the implementations are
based on their respective MATLAB implementations.

The image is also divided into 5x5 equal-sized rectangles, and the
focus measures are applied to these parts as well. As described by
Mavridaki et al. in their paper "No-reference blur assessment in
natural images using Fourier transform and spatial pyramids" (IEEE
Int. Conf. on Image Processing (ICIP 2014), 2004), this is done to
avoid the possibility of images having non-blurred parts misleading
the focus measures.

The outcomes of the focus measure algorithms for the whole image and
the smaller parts are concatenated into an input vector for a support
vector machine used for the prediction. By default, the SVM has been
trained with the CERTH Image Blur Dataset. The final prediction is
weighed by analyzing the probability of motion blur from the image's
exif data, if possible.
"""

import numpy

from .. import get_data
from ..utils.focus_measure import *
from ..utils.exif import analyze_picture_exposure
from ..utils.result_combination import collective_result
from ..utils.utils import *
from ..utils.image_utils import read_image, sharpen, read_exif_tags

from svm_filter import SVMFilter


def get_input_vector(img):
    """Get input vector for use in SVM.

    :param img: the image matrix
    :type img: numpy.ndarray
    :returns: numpy.ndarray -- the input vector
    """
    def apply_measures(view):
        return [MLOG(view),
                LAPV(view),
                TENG(view),
                LAPM(view)]

    parts = [apply_measures(part) for part in partition_matrix(img, 5)]
    normalized_columns = numpy.apply_along_axis(normalize, 0, parts)

    return numpy.array(flatten(normalized_columns), dtype=numpy.float32)


def make_prediction_focus(svm, image_path, ROI):
    input_vec = get_input_vector(sharpen(read_image(image_path, ROI)))
    return scaled_prediction(svm.predict(input_vec))


class WholeBlur(SVMFilter):

    """Filter for detecting blurred images"""

    name = 'whole_blur'
    speed = 2

    def __init__(self, threshold=0.5, invert_threshold=False, svm_file=None):
        """Initializes a blurred image filter

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
            super(WholeBlur, self).__init__(threshold, invert_threshold,
                                            get_data('svm/whole_blur.yml'))
        else:
            super(WholeBlur, self).__init__(threshold, invert_threshold,
                                            svm_file)

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Predict if a given image is blurred

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
        exif = read_exif_tags(image_path)
        exif_prediction = analyze_picture_exposure(exif)
        algo_prediction = make_prediction_focus(self.svm, image_path, ROI)

        prediction = collective_result([algo_prediction,
                                        exif_prediction], 0.2)

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
        super(WholeBlur, self).train(
            images, labels, save_path,
            lambda img: cv2.imread(img, cv2.CV_LOAD_IMAGE_GRAYSCALE),
            lambda img: get_input_vector(sharpen(img)))
