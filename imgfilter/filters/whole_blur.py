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
weighed by analyzing the probability of motion blur from the image’s
exif data, if possible.
"""

import numpy

from .. import get_data
from ..machine_learning.svm import SVM
from ..analyzers.blur_detection.focus_measure import *
from ..analyzers.blur_detection.exif import analyze_picture_exposure
from ..analyzers.common.result_combination import collective_result
from ..utils.utils import partition_matrix, normalize, flatten

from filter import Filter


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


def scaled_prediction(prediction):
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


class WholeBlur(Filter):

    """Filter for detecting blurred images"""

    def __init__(self):
        """Initializes a blurred image filter"""
        self.name = 'whole_blur'
        self.parameters = {}

    def required(self):
        return {'exif', 'sharpen'}

    def run(self):
        """Checks if the image is blurred.

        :returns: float
        """
        exif = self.parameters['exif']
        exif_prediction = analyze_picture_exposure(exif)
        algo_prediction = self.make_prediction_focus()

        return collective_result([algo_prediction,
                                  exif_prediction], 0.2)

    def make_prediction_focus(self):
        svm = SVM()
        svm.load(get_data('svm/whole_blur.yml'))

        input_vec = get_input_vector(self.parameters['sharpen'])
        return scaled_prediction(svm.predict(input_vec))
