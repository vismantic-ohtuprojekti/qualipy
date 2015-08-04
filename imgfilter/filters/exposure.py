import cv2

from ..utils.image_utils import read_image
from ..utils.utils import clipping_percentage

from filter import Filter


class Exposure(Filter):

    """Filter for detecting over- and underexposure"""

    name = "exposure"
    speed = 1

    def __init__(self, threshold=0.5, invert_threshold=False):
        """Initializes an exposure filter

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        """
        super(Exposure, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Predict if a given image is over- or underexposed

        :param image_path: path to the image
        :type image_path: str
        :param return_boolean: whether to return the result as a
                               float between 0 and 1 or as a boolean
                               (threshold is given to the class)
        :type return_boolean: bool
        :param ROI: possible region of interest as a 4-tuple
                    (x0, y0, width, height), None if not needed
        :returns: the prediction as a bool or float depending on the
                  return_boolean parameter
        """
        image = read_image(image_path, ROI)
        histogram = cv2.calcHist([image], [0], None, [256], [0, 256])

        # normalize
        clip = clipping_percentage(histogram, 250, True) * 50

        prediction = 1 if clip < 0.0001 else min(1, clip)

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
