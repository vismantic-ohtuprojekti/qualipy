import numpy
from numpy.lib.stride_tricks import as_strided

from .. import get_data
from ..machine_learning.svm import SVM
from ..utils.utils import partition_matrix

from filter import Filter


def blurmap(img):

    def blurry_degree(lambdas):
        return ((lambdas[0] + lambdas[1]) /
                (numpy.sum(lambdas) + 0.001))

    patch_size = 10
    patches = as_strided(img,
                         shape=(img.shape[0] - patch_size + 1,
                                img.shape[1] - patch_size + 1,
                                patch_size, patch_size),
                         strides=img.strides * 2)

    svd = numpy.linalg.svd(patches, full_matrices=False, compute_uv=False)
    return numpy.apply_along_axis(blurry_degree, 2, svd)


def get_input_vector(img):
    parts = partition_matrix(blurmap(img), 10)
    return numpy.array([numpy.mean(part) for part in parts],
                       dtype=numpy.float32)


class BlurredContext(Filter):

    def __init__(self):
        self.name = 'blurred_context'
        self.parameters = {}

    def required(self):
        return {'resize'}

    def run(self):
        """Checks if the background of the image is blurred.

        :param image_path: the filepath to the image file.
        """
        svm = SVM()
        svm.load(get_data('svm/blurred_context.yml'))

        input_vec = get_input_vector(self.parameters['resize'])
        return self.scaled_prediction(svm.predict(input_vec))

    def scaled_prediction(self, prediction):
        return 1 - (1 + prediction) / 2
