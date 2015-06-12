import numpy

from .. import get_data
from ..machine_learning.svm import SVM
from ..analyzers.blur_detection.focus_measure import *
from ..analyzers.blur_detection.exif import analyze_picture_exposure
from ..analyzers.common.result_combination import collective_result
from ..utils.utils import partition_matrix, normalize, flatten

from filter import Filter


def get_input_vector(img):

    def apply_measures(view):
        return [MLOG(view),
                LAPV(view),
                TENG(view),
                LAPM(view)]

    parts = [apply_measures(part) for part in partition_matrix(img, 5)]
    normalized_columns = numpy.apply_along_axis(normalize, 0, parts)

    return numpy.array(flatten(normalized_columns), dtype=numpy.float32)


class WholeBlur(Filter):

    def __init__(self):
        self.name = 'whole_blur'
        self.parameters = {}

    def required(self):
        return {'exif', 'sharpen'}

    def run(self):
        exif = self.parameters['exif']
        exif_prediction = analyze_picture_exposure(exif)
        algo_prediction = self.make_prediction_focus()

        return collective_result([algo_prediction,
                                  exif_prediction], 0.2)

    def make_prediction_focus(self):
        svm = SVM()
        svm.load(get_data('svm/whole_blur.yml'))

        input_vec = get_input_vector(self.parameters['sharpen'])
        return self.scaled_prediction(svm.predict(input_vec))

    def scaled_prediction(self, prediction):
        pred = 1 - (1 + prediction) / 2

        if pred < 0:
            return 0
        if pred > 1:
            return 1

        return pred
