"""
Filter for detecting images that are of unconventional size.
Images with aspect ratio over 16:9 or 9:16 are considered
to be of unconventional size by default.
"""

from ..utils.image_utils import read_image
from filter import Filter


class UnconventionalSize(Filter):

    """Filter for detecting images of unconventional size"""

    name = 'unconventional_size'
    speed = 1

    def __init__(self, threshold=16. / 9., invert_threshold=False):
        """Initializes an unconventional size image filter

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        """
        super(UnconventionalSize, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Check if a given image is of unconventional size

        :param image_path: path to the image
        :type image_path: str
        :param return_boolean: whether to return the result as a
                               boolean depending on the chosen
                               threshold or the image's aspect
                               ratio (longer side divided by shorter)
        :type return_boolean: bool
        :param ROI: possible region of interest as a 4-tuple
                    (x0, y0, width, height), None if not needed
        :returns: the prediction as a bool or float depending on the
                  return_boolean parameter
        """
        height, width = read_image(image_path, ROI).shape
        aspect_ratio = max(height, width) / float(min(height, width))

        if return_boolean:
            return self.boolean_result(aspect_ratio)
        return aspect_ratio
