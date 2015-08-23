"""
Wrapper for OpenCV's support vector machine implementation.
"""

import cv2


class StatModel(object):

    def __init__(self):
        self.model_file = True

    def load(self, model_file):
        self.model_file = model_file
        self.model.load(model_file)

    def save(self, model_file):
        self.model.save(model_file)


class SVM(StatModel):

    def __init__(self):
        """Initializes an SVM"""
        super(SVM, self).__init__()
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
        """Get the current state of the object, namely the file path to
        the current SVM model. Used by the pickle module for serialization.

        :returns: str -- the current state
        """
        return self.model_file

    def __setstate__(self, state):
        """Set the current state of the object, namely the file path to
        an SVM model. Used by the pickle module for serialization.

        :param state: the new state
        :type state: str
        """
        self.__init__()
        self.model_file = state

        if self.model_file is not True:
            self.load(state)
