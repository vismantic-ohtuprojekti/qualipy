import numpy as np
import cv2
from .. import get_data
from ..utils.image_utils import read_image, read_color_image
from ..utils.utils import partition_matrix, scaled_prediction

from svm_filter import SVMFilter

class Fisheye(SVMFilter):

    name = 'fisheye'
    speed = 1
    
    def __init__(self, threshold=0.5, invert_threshold=False, svm_file=None):
        """Initializes an framed filter

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        """
        if svm_file is None:
            super(Fisheye, self).__init__(
                threshold, invert_threshold,
                get_data('svm/fisheye.yml'))
        else:
            super(Fisheye, self).__init__(threshold, invert_threshold,
                                                 svm_file)

    def predict(self, image_path, return_boolean=True, ROI=None):
        input_vec = self.get_input_vector(read_image(image_path, ROI))
        prediction = scaled_prediction(self.svm.predict(input_vec))
    
        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
    
    def get_input_vector(self, image):
        #grey = read_image(image, None)
        parts = partition_matrix(image, 5)
        return np.array([self.calc_mean_lines(part) for part in parts],
                       dtype=np.float32)
            
    def calc_mean_lines(self, image):
        #blur = cv2.GaussianBlur(image,(5,5),0)
        edges = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 4)
        lines = cv2.HoughLines(edges,1,np.pi/180,60)
        a = 0
        i = 0.00001
        if lines != None:
            for rho,theta in lines[0]:
                a += np.cos(theta)
                i += 1.0
            
        #print float(a / i)
        #cv2.imshow('original', edges)
        #cv2.waitKey(0)
        return float(a / i)
