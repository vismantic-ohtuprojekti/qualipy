import os.path

import numpy

from filter import Filter
from ..utils.svm import SVM


class SVMFilter(Filter):

    """An abstract class representing a filter that uses SVM"""

    def __init__(self, threshold, invert_threshold, svm_file):
        super(SVMFilter, self).__init__(threshold, invert_threshold)

        if not (isinstance(svm_file, str) or
                isinstance(svm_file, unicode)):
            raise TypeError("svm_file should be a string")

        self.svm = SVM()
        self.load(svm_file)

    def train(self, images, labels, save_path, read_image,
              get_input_vector):
        """Train an SVM-based filter

        :param images: list of file paths to images
        :type images: list
        :param labels: list of labels for the corresponding images, every
                       label should be either 0 or 1
        :type labels: list
        :param save_path: file path to save the resulting SVM model to,
                          None if not needed
        :type save_path: str
        :param read_image: function to use for reading the image from a path
        :type read_image: function
        :param get_input_vector: function to use for constructing the input
                                 vector for a sample image
        :type get_input_vector: function
        """
        samples = []
        for image in images:
            img = read_image(image)
            if img is None:
                raise IOError("unable to read image: %s" % image)
            samples.append(get_input_vector(img))

        samples = numpy.array(samples, dtype=numpy.float32)
        labels = numpy.array(labels, dtype=numpy.float32)

        if len(samples) != len(labels):
            raise ValueError("samples and labels should have same length")

        try:
            self.svm.train(samples, labels)
        except:
            raise ValueError("too few training samples")

        if save_path is not None:
            self.save(save_path)

    def load(self, path):
        """Load an SVM model from a file.

        :param path: path to the SVM data file
        :type path: str
        """
        if not (isinstance(path, str) or isinstance(path, unicode)):
            raise TypeError("path should be a string")

        if not os.path.isfile(path):
            raise ValueError("invalid file path for SVM model")

        self.svm.load(path)

    def save(self, path):
        """Save the current SVM model to a file.

        :param path: path to the destination file
        :type path: str
        """
        if not (isinstance(path, str) or isinstance(path, unicode)):
            raise TypeError("path should be a string")

        self.svm.save(path)
