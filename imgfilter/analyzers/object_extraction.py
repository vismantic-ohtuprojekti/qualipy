import cv2
import tempfile
import subprocess

from analyzer import Analyzer


class ObjectExtraction(Analyzer):

    def __init__(self):
        self.name = 'extract_object'
        self.data = None

    def run(self, image, image_path):
        obj = run_object_extraction(image_path)
        self.data = cv2.imread(obj, cv2.CV_LOAD_IMAGE_GRAYSCALE)


def run_object_extraction(image_path):
    mktemp = lambda: tempfile.mkstemp(suffix=".jpg")[1]
    temp1, temp2 = mktemp(), mktemp()

    from .. import get_data
    subprocess.call([get_data("object_extraction/extract_object"),
                     image_path, temp1, temp2])
    return temp2
