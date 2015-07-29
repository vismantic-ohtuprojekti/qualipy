import cv2

from ..utils.image_utils import read_image
from ..utils.utils import clipping_percentage

from filter import Filter


class Exposure(Filter):

    """Filter for detecting over- and underexposure"""

    name = "exposure"
    speed = 1

    def __init__(self, threshold=0.5, invert_threshold=False):
        super(Exposure, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True):
        """ Checks if image is over- or underexposed
        """
        image = read_image(image_path)
        histogram = cv2.calcHist([image], [0], None, [256], [0, 256])

        # normalize
        clip = clipping_percentage(histogram, 250, True) * 50

        prediction = 1 if clip < 0.0001 else min(1, clip)

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
