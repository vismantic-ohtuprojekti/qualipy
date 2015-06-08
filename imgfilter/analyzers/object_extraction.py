import cv2
import tempfile
import subprocess

from analyzer import Analyzer


class ObjectExtraction(Analyzer):

    """Analyzer for running an object extraction algorithm on an image"""

    def __init__(self):
        """Initializes an object extraction analyzer"""
        self.name = 'extract_object'
        self.data = None

    def run(self, image, image_path):
        """Runs the object extraction analyzer

        :param image: image data as a numpy matrix
        :param image_path: path to the image file
        """
        obj = run_object_extraction(image_path)
        self.data = cv2.imread(obj, cv2.CV_LOAD_IMAGE_GRAYSCALE)


def run_object_extraction(image_path):
    """Runs an object extraction algorithm on an image and returns
    the path to the resulting image.

    :param image: path to the image file
    """
    mktemp = lambda: tempfile.mkstemp(suffix=".jpg")[1]
    temp1, temp2 = mktemp(), mktemp()

    from .. import get_data
    subprocess.call([get_data("object_extraction/extract_object"),
                     image_path, temp1, temp2])
    return temp2
