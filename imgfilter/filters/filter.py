import operator

import numpy


class Filter(object):

    """An abstract class representing a filter"""

    def __init__(self, threshold, invert_threshold):
        self.threshold = threshold
        self.invert_threshold = invert_threshold
        self.compare_func = operator.gt

    def predict(self, image_path, return_boolean=True, ROI=None):
        pass

    def train(self, images, labels, svm, read_image, get_input_vector):
        samples = []
        for image in images:
            img = read_image(image)
            if img is None:
                continue
            samples.append(get_input_vector(img))

        samples = numpy.array(samples, dtype=numpy.float32)
        labels = numpy.array(labels, dtype=numpy.float32)
        svm.train(samples, labels)

    def boolean_result(self, prediction):
        if self.invert_threshold:
            return self.compare_func(self.threshold, prediction)
        return self.compare_func(prediction, self.threshold)

    def __eq__(self, threshold):
        self.threshold = threshold
        self.compare_func = operator.eq
        return self

    def __ne__(self, threshold):
        self.threshold = threshold
        self.compare_func = operator.ne
        return self

    def __lt__(self, threshold):
        self.threshold = threshold
        self.compare_func = operator.lt
        return self

    def __gt__(self, threshold):
        self.threshold = threshold
        self.compare_func = operator.gt
        return self

    def __le__(self, threshold):
        self.threshold = threshold
        self.compare_func = operator.le
        return self

    def __ge__(self, threshold):
        self.threshold = threshold
        self.compare_func = operator.ge
        return self
