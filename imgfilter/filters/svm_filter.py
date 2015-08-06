import numpy

from filter import Filter
from ..machine_learning.svm import SVM


class SVMFilter(Filter):

    """An abstract class representing a filter that uses SVM"""

    def __init__(self, threshold, invert_threshold, svm_file):
        super(SVMFilter, self).__init__(threshold, invert_threshold)

        if not isinstance(svm_file, str):
            raise TypeError("svm_file should be a string")

        self.svm = SVM()
        self.load(svm_file)

    def train(self, images, labels, save_path, read_image,
              get_input_vector):
        samples = []
        for image in images:
            img = read_image(image)
            if img is None:
                continue
            samples.append(get_input_vector(img))

        samples = numpy.array(samples, dtype=numpy.float32)
        labels = numpy.array(labels, dtype=numpy.float32)
        self.svm.train(samples, labels)

        if save_path is not None:
            self.save(save_path)

    def load(self, path):
        """Load an SVM model from a file.

        :param path: path to the SVM data file
        :type path: str
        """
        if not isinstance(path, str):
            raise TypeError("path should be a string")

        self.svm.load(path)

    def save(self, path):
        """Save the current SVM model to a file.

        :param path: path to the destination file
        :type path: str
        """
        if not isinstance(path, str):
            raise TypeError("path should be a string")

        self.svm.save(path)
