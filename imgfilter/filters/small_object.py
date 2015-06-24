"""
Filter for detecting images where the object is too small
in comparison to the size of the image.
"""

import numpy

from filter import Filter


def get_object_ratio(obj):
    return numpy.count_nonzero(obj) / float(obj.size)


class ObjectTooSmall(Filter):

    """Filter for detecting images where the object is too small"""

    name = 'object_too_small'

    def __init__(self, min_ratio=0.05):
        """Initializes a small object filter

        :param min_ratio: minimum ratio for an object to be considered
                          too small in comparison to the whole image
        :type min_ratio: float
        """
        self.parameters = {}
        self.min_ratio = min_ratio

    def required(self):
        return {'extract_object'}

    def run(self):
        """Checks if the object in an image is too small.

        :returns: float
        """
        _, obj = self.parameters['extract_object']
        return get_object_ratio(obj) < self.min_ratio
