import os
import cv2
import tempfile

from ctypes import cdll, c_char_p, c_bool
from analyzer import Analyzer


def saliency(image_path, saliency_map_path, saliency_mask_path):
    from .. import get_data

    saliency_lib = get_data("object_extraction/saliency.so")
    SaliencyDetector = cdll.LoadLibrary(saliency_lib)
    SaliencyDetector.saliency.restype = c_bool

    cimage_path = c_char_p(image_path)
    csaliency_map_path = c_char_p(saliency_map_path)
    csaliency_mask_path = c_char_p(saliency_mask_path)

    return SaliencyDetector.saliency(cimage_path, csaliency_map_path,
                                     csaliency_mask_path)


def run_object_extraction(image_path):
    """Runs an object extraction algorithm on an image and returns
    the path to the resulting image.

    :param image: path to the image file
    """
    mktemp = lambda: tempfile.mkstemp(suffix=".jpg")[1]
    temp1, temp2 = mktemp(), mktemp()

    if not saliency(image_path, temp1, temp2):
        return None

    os.unlink(temp1)
    return temp2


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
        os.unlink(obj)
