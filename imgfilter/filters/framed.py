import numpy as np
import cv2
from matplotlib import pyplot as plt

from filter import Filter

class Framed(Filter):

    name = 'framed'

    def __init__(self):
        self.parameters = {}

    def required(self):
        return {'image'}

    def run(self):
        image = self.parameters['image']
        height, width = image.shape
        contours = findContours(image)
        return analyzeContours(contours, height, width)
        
def analyzeContours(contours, height, width):

    # Checks if there is four contours (one rectangle) or eight (two rectangles)
    if(len(contours[0]) != 4 and len(contours[0]) != 8):
        return 0

    i = 0
    eka = [1, 1]
    toka = [1, 1]
    switch = True
    found = False
    x = 0
    
    # Check contours are orthogonal
    for val in np.nditer(contours[0]):
        if i % 2 == 0:
            switch = not switch            
        if switch:
            toka[0] = x
            toka[1] = val
        else:
            eka[0] = x
            eka[0] = val
        
        for num in eka:
            if num in toka:
                found = True
        if found:
            found = False
        else:
            return 0
        i += 1
        x = val
        
    return 1

# Converts the image to contain only edges and finds contours in that image
def findContours(image):
    #ret,thresh = cv2.threshold(image,100,255,0)
    thresh = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    return contours
    
# Shows images with contours drawn in them
def showImages(image, contours):
    cv2.drawContours(image, contours[0], -1, (128,128,128), 10)
    cv2.imshow("edges", image)
    cv2.waitKey()
