"""
Filter for detecting text in images

Uses tesseract-ocr through a python wrapper, which creates a tesseract-ocr
process and feeds the input image to it. Then filter makes prediction
based on the string the tesseract-returns to it. If the string length is
longer than one then there is considered to be a text in the image.
"""

from ..utils.tesseract import img_to_str

from filter import Filter


class TextDetection(Filter):

    """Filter for detecting text in images"""

    name = 'text_detection'
    speed = 3

    def __init__(self, threshold=0.5, invert_threshold=False,
                 tesseract_path='tesseract'):
        """Initializes a text detection filter

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        :param tesseract_path: path to the tesseract executable
        :type tesseract_path: str
        """
        super(TextDetection, self).__init__(threshold, invert_threshold)
        self.tesseract_path = tesseract_path

    def predict(self, image_path, return_boolean=True, ROI=None):
        """Predict if a given image has text.

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
        if not (isinstance(image_path, str) or
                isinstance(image_path, unicode)):
            raise TypeError("image_path must be a string")

        if len(img_to_str(self.tesseract_path, image_path)) > 1:
            prediction = 1.0
        else:
            prediction = 0.0

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
