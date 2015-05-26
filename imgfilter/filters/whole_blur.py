import cv2
import numpy

from .. import get_data
from ..svm import SVM
from ..image_util import sharpen, to_grayscale
from ..focus_measure import MLOG, LAPV, TENG, LAPM
from ..utils import partition_matrix, normalize, flatten
from ..exif import analyzePictureExposure
from ..result_combination import collective_result_certain_limit

def get_input_vector(img):

    def apply_measures(view):
        sharpened = sharpen(view)
        return [MLOG(sharpened),
                LAPV(sharpened),
                TENG(sharpened),
                LAPM(sharpened)]

    gray = to_grayscale(img)
    parts = [apply_measures(part) for part in partition_matrix(gray, 5)]

    normalized_columns = numpy.apply_along_axis(normalize, 0, parts)
    return numpy.array(flatten(normalized_columns), dtype=numpy.float32)


def make_prediction_focus(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None

    svm = SVM()
    svm.load(get_data('svm/whole_blur.yml'))

    input_vec = get_input_vector(img)
    prediction = svm.predict(input_vec)
    return 1.0 - (1.0 + prediction) / 2.0


def is_blurred(image_path):
    return 0.5 <= collective_result_certain_limit([make_prediction_focus, analyzePictureExposure], 0.2, image_path)
