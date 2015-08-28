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

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        :param is_saliency_map: whether the given image is already a
                                saliency map
        :type is_saliency_map: bool
        """
        super(ObjectTooSmall, self).__init__(threshold, invert_threshold)
        self.is_saliency_map = is_saliency_map

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Checks if the object in an image is too small.

        :param image_path: path to the image
        :type image_path: str
        :param return_boolean: whether to return the result as a
                               boolean depending on the chosen
                               threshold or the ratio of the object's
                               size compared to the size of the image
        :type return_boolean: bool
        :param ROI: possible region of interest as a 4-tuple
                    (x0, y0, width, height), None if not needed
        :returns: the prediction as a bool or float depending on the
                  return_boolean parameter
        """
        if self.is_saliency_map:
            obj = read_image(image_path, ROI)
        else:
            _, obj = extract_object(image_path)

        prediction = get_object_ratio(obj)

        if return_boolean:
            return not self.boolean_result(prediction)
        return prediction
