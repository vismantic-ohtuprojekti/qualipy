import cv2

from analyzer import Analyzer


class Resize(Analyzer):

    def __init__(self):
        self.name = 'resize'
        self.data = None

    def run(self, image, image_path):
        self.data = resize(image, 500)


def resize(image, size):
    height, width = image.shape

    if max(height, width) <= size:
        return image

    ratio = max(height, width) / float(size)
    height /= ratio
    width /= ratio
    return cv2.resize(image, (int(height), int(width)))
