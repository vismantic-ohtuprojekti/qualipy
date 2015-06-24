import cv2
import numpy

from filter import Filter


class OverExposed(Filter):

    """Filter for detecting overexposure"""

    name = "over_exposure"

    def __init__(self):
        self.parameters = {}

    def required(self):
        return {'image'}

    def run(self):
        """ Checks if image is over-exposed
        """
        image = self.parameters['image']
        histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
        # Normalize:
        clip = clipping_percentage(histogram, 250) * 50
        return min(1, clip)


def clipping_percentage(histogram, threshold):
    total = numpy.sum(histogram)
    if total < 0.0005:  # avoid division by zero
        return 0
    return float(numpy.sum(histogram[threshold:])) / total
