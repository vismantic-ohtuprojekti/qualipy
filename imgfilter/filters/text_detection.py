import cv2
import numpy as np
from ..utils.pytesseract import img_to_str
from ..utils.image_utils import read_color_image

from filter import Filter

from matplotlib import pyplot as plt

class TextDetection(Filter):
    name = 'text_detection'
    speed = 10

    def __init__(self, threshold=0.5, invert_threshold=False):
        super(TextDetection, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True, ROI=None):
        
        if len(img_to_str('tesseract', image_path)) >  1:
            prediction = 1.0
        else:
            prediction = 0.0
        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
