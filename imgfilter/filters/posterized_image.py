import numpy as np
import cv2

from imgfilter.machine_learning.svm import SVM
from .. import get_data

from ..utils.statistic_common import linear_normalize

from filter import Filter


def get_input_vector(img):
    hist = cv2.calcHist([img], [0], None, [256], [0,255])

    peaks = np.array([])
    move_status = 'level'

    sum_of_derivates = 0.0

    for i in range(0, hist.shape[0] - 1):
        # Calculate derivate
        current_derivate = hist[i + 1] - hist[i]

        # Update move status based on current derivate
        current_move_status = ''
        if current_derivate < 0:
            current_move_status = 'decreasing'
        elif current_derivate > 0:
            current_move_status = 'increasing'
        else:
            current_move_status = 'level'

        # Check if found a peak and update peaks
        if move_status == 'increasing' and current_move_status == 'decreasing':
            peaks = np.append(peaks, hist[i])

        # Update derivate sum
        sum_of_derivates += np.abs(current_derivate)

        # Update move status
        move_status = current_move_status

    # Caluculate average of derivate and number of peaks
    derivate_average = (1.0 / 255.0) * sum_of_derivates
    number_of_peaks = peaks.shape[0]

    result = np.array([derivate_average[0], number_of_peaks])
    return result.astype(np.float32)
    

class Posterized(Filter):

    name = 'posterized'

    def __init__(self):
        self.parameters = {}

    def required(self):
        return {'image'}

    def run(self):
        svm = SVM()
        svm.load(get_data('svm/posterized.yml'))
        prediction = svm.predict(get_input_vector(self.parameters['image']))
        if prediction < -1.0:
            return 0.0
        elif prediction > 1.0:
            return 1.0
        else:
            return (prediction - (-1.0)) / (1.0 - (-1.0))
