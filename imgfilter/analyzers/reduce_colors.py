from analyzer import Analyzer

import cv2
import numpy as np

def reduce_colors(image, colors):
    """
    Reduces colors of given image to given amount. Algorithm uses K-nearest neighbors
    method to do this. Given image must have colors meaning three channels. Algorithm
    taken from here "http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans
    /py_kmeans_opencv/py_kmeans_opencv.html"

    param image: image to process (must have three channels)
    param colors: how many colors the final image should have
    """
    Z = image.reshape((-1,3))

    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = colors
    ret,label,center=cv2.kmeans(Z,K,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((image.shape))
    return res2

class ReduceColors(Analyzer):

    def __init__(self):
        self.name = 'reduce_colors'
        self.data = None

    def run(self, image, image_path):
        color_image = cv2.imread(image_path)
        self.data = reduce_colors(color_image, 2)
