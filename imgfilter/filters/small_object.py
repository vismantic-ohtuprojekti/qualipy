import numpy

from filter import Filter


class ObjectTooSmall(Filter):

    def __init__(self, min_ratio=0.05):
        self.name = 'object_too_small'
        self.parameters = {}
        self.min_ratio = min_ratio

    def required(self):
        return {'extract_object'}

    def run(self):
        _, obj = self.parameters['extract_object']
        ratio = numpy.count_nonzero(obj) / float(obj.size)
        return ratio < self.min_ratio
