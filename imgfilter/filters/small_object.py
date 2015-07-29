"""
Filter for detecting images where the object is too small
in comparison to the size of the image.
"""

import numpy

from ..utils.image_utils import read_image
from ..utils.object_extraction import extract_object
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
    speed = 5

    def __init__(self, threshold=0.05, invert_threshold=False,
                 is_saliency_map=False):
        """Initializes a small object filter

        :param min_ratio: minimum ratio for an object to be considered
                          too small in comparison to the whole image
        :type min_ratio: float
        :param is_saliency_map: whether the image is already a saliency map
        :type is_saliency_map: bool
        """
        super(ObjectTooSmall, self).__init__(threshold, invert_threshold)
        self.is_saliency_map = is_saliency_map

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Checks if the object in an image is too small.

        :returns: float
        """
        if self.is_saliency_map:
            obj = read_image(image_path, ROI)
        else:
            _, obj = extract_object(image_path)

        prediction = get_object_ratio(obj)

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
