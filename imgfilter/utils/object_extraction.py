import os
import tempfile
from ctypes import cdll, c_char_p, c_bool

import cv2


def _saliency(image_path, saliency_map_path, saliency_mask_path):
    """Python wrapper for running the saliency detection.

    :param image_path: path to the image file
    :type image_path: str
    :param saliency_map_path: path to save the generated saliency map
    :type saliency_map_path: str
    :param saliency_mask_path: path to save the binarized saliency map
    :type saliency_mask_path: str
    :returns: bool -- whether the saliency detection was succesful
    """
    from .. import get_data

    saliency_lib = os.getenv('SALIENCY_SO_PATH')
    if saliency_lib is None:
        saliency_lib = get_data("object_extraction/saliency.so")

    SaliencyDetector = cdll.LoadLibrary(saliency_lib)
    SaliencyDetector.saliency.restype = c_bool

    cimage_path = c_char_p(image_path)
    csaliency_map_path = c_char_p(saliency_map_path)
    csaliency_mask_path = c_char_p(saliency_mask_path)

    return SaliencyDetector.saliency(cimage_path, csaliency_map_path,
                                     csaliency_mask_path)


def _run_object_extraction(image_path):
    """Runs an object extraction algorithm on an image and returns
    the path to the resulting image.

    :param image: path to the image file
    :type image_path: str
    :returns: str -- path to the resulting image
    """
    mktemp = lambda: tempfile.mkstemp(suffix=".jpg")[1]
    temp1, temp2 = mktemp(), mktemp()

    if not _saliency(image_path, temp1, temp2):
        return None

    return temp1, temp2


def extract_object(image_path):
    full, binarized = _run_object_extraction(image_path)
    data = (cv2.imread(full, cv2.CV_LOAD_IMAGE_GRAYSCALE),
            cv2.imread(binarized, cv2.CV_LOAD_IMAGE_GRAYSCALE))

    os.unlink(full)
    os.unlink(binarized)
    return data
