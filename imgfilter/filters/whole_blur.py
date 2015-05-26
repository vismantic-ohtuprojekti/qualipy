import cv2
import numpy

from .. import get_data
from ..svm import SVM
from ..image_util import sharpen, to_grayscale
from ..focus_measure import MLOG, LAPV, TENG, LAPM
from ..utils import partition_matrix, normalize, flatten
from ..exif import analyzePictureExposure

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


def make_prediction(img):
    svm = SVM()
    svm.load(get_data('svm/whole_blur.yml'))

    input_vec = get_input_vector(img)
    return svm.predict(input_vec)


def is_blurred(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise IOError("No such file")

    prediction_1 = make_prediction(image)
    prediction_2 = analyzePictureExposure(image_path)

    if prediction_2 is None:
        prediction_2 = prediction_1

    final_prediction = (prediction_1 + prediction_2) / 2.0
