import numpy as np
import cv2
from ..utils.image_utils import read_image
from ..utils.utils import partition_matrix
from ..utils.histogram_analyzation import *

#from matplotlib import pyplot as plt

from filter import Filter

class Highlights(Filter):

    name = 'highlights'
    speed = 2
    
    def __init__(self, threshold=0.5, invert_threshold=False):
        """Initializes an highlights filter

        :param threshold: threshold at which the given prediction is changed
                          from negative to positive
        :type threshold: float
        :param invert_threshold: whether the result should be greater than
                                 the given threshold (default) or lower
                                 for an image to be considered positive
        :type invert_threshold: bool
        """
        super(Highlights, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True, ROI=None):
        image = read_image(image_path, ROI)   
        blur = cv2.GaussianBlur(image,(5,5),0)
        ret,thresh = cv2.threshold(blur,250,255,0)
        
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        areas = count_areas(contours)
        
        prediction = 1 if areas > 0 else 0
        
        #if prediction == 0:
        #    show_debug(image, thresh, areas)
        
        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
   
def count_areas(contours, num_sides = 7, area_size = 50):
    """Counts the number of areas that are not rectangular or too small from the list of contours

    :param image: contours
    :returns: int -- number of non-rectangular objects found
    """

    i = 0
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        if len(approx) > num_sides and cv2.contourArea(cnt) > area_size:
            i += 1
    return i

def show_debug(image, thresh, areas):
    cv2.imshow('orig', image)
    cv2.imshow('highlight', thresh)
    print areas
    cv2.waitKey(0)
 
def find_threshold(normalized):
    for i, value in enumerate(normalized):
        if value > 0.99:
            return i
            
#hist = cv2.calcHist([image], [0], None, [255], [0, 255])
#normalized = normalize(hist)
#normalized = calculate_continuous_distribution(normalized)
#threshold = find_threshold(normalized)
#if threshold > 0:
#    threshold == 250
    
