import numpy as np

from imgfilter.machine_learning.svm import SVM
from .. import get_data

from filter import Filter


def get_input_vector(img):
    # TO DO: Get quality of low resolution from image
    return np.array([1])


class LowResolution(Filter):

    def __init__(self):
        self.name = 'low_resolution'
        self.parameters = {}

    def required(self):
        return {'image'}

    def run(self):
        svm = SVM()
        svm.load(get_data('svm/low_resolution.yml'))

        input_vec = get_input_vector(self.parameters['image'])
        return svm.predict(input_vec)