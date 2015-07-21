from analyzer import Analyzer

import cv2
import numpy

class ColorImage(Analyzer):

    def __init__(self):
        self.name = 'color_image'
        self.data = None

    def run(self, image, image_path):
        self.data = cv2.imread(image_path)
