import cv2
import numpy

from .. import get_data
from ..machine_learning.svm import SVM
from ..utils.image_utils import read_image
from ..utils.utils import scaled_prediction

from filter import Filter


def get_input_vector(img):
    hist = cv2.calcHist([img], [0], None, [256], [0, 255])

    diffs = numpy.diff(hist.T[0])  # calculate derivatives
    sum_of_derivatives = numpy.sum(numpy.abs(diffs))
    derivative_average = sum_of_derivatives / 255.
    number_of_peaks = numpy.sum((diffs[:-1] > 0) & (diffs[1:] < 0))

    return numpy.array([derivative_average, number_of_peaks],
                       dtype=numpy.float32)


class Posterized(Filter):

    name = 'posterized'
    speed = 1

    def __init__(self, threshold=0.5, invert_threshold=False):
        super(Posterized, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True):
        svm = SVM()
        svm.load(get_data('svm/posterized.yml'))
        prediction = svm.predict(get_input_vector(read_image(image_path)))
        prediction = scaled_prediction(prediction)

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
