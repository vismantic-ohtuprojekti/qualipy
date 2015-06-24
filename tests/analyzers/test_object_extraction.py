import os
import cv2

from imgfilter.analyzers.object_extraction import *


# def test_object_extraction_returns_two_images():
#     a, b = run_object_extraction('tests/images/lama.jpg')
#     assert os.path.exists(a)
#     assert os.path.exists(b)


# def test_returned_images_are_of_same_sizess():
#     a, b = run_object_extraction('tests/images/lama.jpg')
#     assert cv2.imread(a, 0).shape == cv2.imread('images/lama.jpg', 0).shape
#     assert cv2.imread(b, 0).shape == cv2.imread('images/lama.jpg', 0).shape
