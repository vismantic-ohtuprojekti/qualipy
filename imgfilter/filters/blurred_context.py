import cv2
import numpy
import tempfile
import subprocess

from .. import get_data
from whole_blur import is_blurred as whole_blur


def run_object_extraction(image_path):
    temp1 = tempfile.mkstemp(suffix=".jpg")[1]
    temp2 = tempfile.mkstemp(suffix=".jpg")[1]
    subprocess.call([get_data("object_extraction/extract_object"),
                     image_path, temp1, temp2])
    return temp2


def vertical_blur(obj_mask, tmp_file):
    mask = numpy.all(obj_mask != 255, 0)
    cv2.imwrite(tmp_file, obj_mask[:, mask])
    return whole_blur(tmp_file)


def horizontal_blur(obj_mask, tmp_file):
    mask = numpy.all(obj_mask != 255, 1)
    cv2.imwrite(tmp_file, obj_mask[mask])
    return whole_blur(tmp_file)


def is_blurred(image_path):
    extracted_object = run_object_extraction(image_path)
    obj_mask = cv2.imread(extracted_object, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    return vertical_blur(obj_mask, extracted_object) or \
        horizontal_blur(obj_mask, extracted_object)
