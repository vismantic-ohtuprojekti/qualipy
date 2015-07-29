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
        """Initializes an unconventional size filter"""
        super(UnconventionalSize, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True):
        """Checks if the image is of unconventional size

        :returns: bool
        """
        height, width = read_image(image_path).shape
        aspect_ratio = max(height, width) / float(min(height, width))

        if return_boolean:
            return self.boolean_result(aspect_ratio)
        return aspect_ratio
