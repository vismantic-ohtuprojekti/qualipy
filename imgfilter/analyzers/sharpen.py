import cv2

from analyzer import Analyzer


class Sharpen(Analyzer):

    """Analyzer for sharpening an image"""

    def __init__(self):
        """Initializes a sharpen analyzer"""
        self.name = 'sharpen'
        self.data = None

    def run(self, image, image_path):
        """Runs the sharpen analyzer

        :param image: image data as a numpy matrix
        :param image_path: path to the image file
        """
        self.data = sharpen(image)


def sharpen(image):
    """Sharpens an image

    :param image: image data as a numpy matrix
    """
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    return cv2.addWeighted(image, 1.5, blur, -0.5, 0)
