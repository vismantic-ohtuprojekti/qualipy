"""
Wrapper for OpenCV's support vector machine implementation.
"""

import cv2


class StatModel(object):

    def __init__(self):
        self.fn = None

    def load(self, fn):
        self.fn = fn
        self.model.load(fn)

    def save(self, fn):
        self.model.save(fn)


class SVM(StatModel):

    def __init__(self):
        """Initializes an SVM"""
        self.model = cv2.SVM()

    def train(self, samples, labels):
        """Trains the SVM from a list of samples and their associated labels

        :param samples: list of samples to use for training
        :type samples: numpy.ndarray
        :param labels: labels for the samples
        :type labels: numpy.ndarray
        """
        params = dict(kernel_type=cv2.SVM_RBF, svm_type=cv2.SVM_C_SVC)
        self.model.train_auto(samples, labels, None, None, params)

    def predict(self, sample):
        """Predict a class for a sample.

        :param sample: the sample to classify
        :returns: numpy.float32
        """
        return self.model.predict(sample, True)

    def __getstate__(self):
        return self.fn

    def __setstate__(self, state):
        self.__init__()
        self.fn = state

        if self.fn is not None:
            self.model.load(state)
