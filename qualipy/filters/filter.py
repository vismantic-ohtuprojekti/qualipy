import operator


class Filter(object):

    """An abstract class representing a filter"""

    def __init__(self, threshold, invert_threshold):
        self.threshold = threshold
        self.invert_threshold = invert_threshold
        self.compare_func = operator.gt

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
