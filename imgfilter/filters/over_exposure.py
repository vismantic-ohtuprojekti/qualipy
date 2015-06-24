import cv2
import numpy
from ..utils.utils import clipping_percentage


from filter import Filter


class OverExposed(Filter):

    """Filter for detecting overexposure"""

    def __init__(self):
        self.name = "over_exposure"
        self.parameters = {}

    def required(self):
        return {'image'}

    def run(self):
        """ Checks if image is over-exposed
        """
        image = self.parameters['image']
        histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
        # Normalize:
        clip = clipping_percentage(histogram, 250, True) * 50
        return min(1, clip)
