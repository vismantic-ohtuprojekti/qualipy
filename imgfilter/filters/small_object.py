"""
Filter for detecting images where the object is too small
in comparison to the size of the image.
"""

import numpy

from filter import Filter


def get_object_ratio(obj):
    """Calculate the ratio of the object's size in comparison to the whole image

    :param obj: the binarized object image
    :type obj: numpy.ndarray
    :returns: float -- the ratio
    """
    return numpy.count_nonzero(obj) / float(obj.size)


class ObjectTooSmall(Filter):

    """Filter for detecting images where the object is too small"""

    name = 'object_too_small'

    def __init__(self, min_ratio=0.05, is_saliency_map=False):
        """Initializes a small object filter

        :param min_ratio: minimum ratio for an object to be considered
                          too small in comparison to the whole image
        :type min_ratio: float
        :param is_saliency_map: whether the image is already a saliency map
        :type is_saliency_map: bool
        """
        self.parameters = {}
        self.min_ratio = min_ratio
        self.is_saliency_map = is_saliency_map

    def required(self):
        return {'image', 'extract_object'}

    def run(self):
        """Checks if the object in an image is too small.

        :returns: float
        """
        if self.is_saliency_map:
            obj = self.parameters['image']
        else:
            _, obj = self.parameters['extract_object']

        return get_object_ratio(obj) < self.min_ratio
