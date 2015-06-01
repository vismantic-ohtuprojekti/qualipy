import cv2

from analyzer import Analyzer


class Sharpen(Analyzer):

    def __init__(self):
        self.name = 'sharpen'
        self.data = None

    def run(self, image, image_path):
        self.data = sharpen(image)


def sharpen(image):
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    return cv2.addWeighted(image, 1.5, blur, -0.5, 0)
