import cv2
import numpy
from ..utils.utils import clipping_percentage

from filter import Filter


class UnderExposed(Filter):

    """Filter for detecting underexposure"""

    def __init__(self):
        self.name = "under_exposure"
        self.parameters = {}

    def required(self):
        return {'image'}

    def run(self):
        """ Checks if image is under-exposed
        """
        image = self.parameters['image']
        histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
        # Normalize:
        clip = clipping_percentage(histogram, 5, False) * 50
        return min(1, clip)
        

