import numpy
import cv2
import sys
import math

from analyzer import Analyzer

class Exposure(Analyzer):

    """ Anayzer for over-exposure data from image
    """
    def __init__(self):
        self.name = "exposure"
        self.parameters = {}
        
    def run(self, image, image_path):
        """ Checks if image is over-exposed
        """

        self.data = get_input_vectors(image_path)

def calc_mean(histogram):
    values = 0
    for i, value in enumerate(histogram):
        values += (value * i)
    return float(values / sum(histogram))

def calc_variance(histogram, mean):
    variance = 0
    for i, value in enumerate(histogram):
        variance += math.pow((mean - i), 2) * value
    return float(variance / sum(histogram))

def calc_clipping_percentage(histogram, threshold):
    value = 0
    for values in histogram[threshold:]:
        value += values
    return float(value / sum(histogram))

def get_input_vectors(image_path):
    image = cv2.imread(image_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram = cv2.calcHist([image_gray], [0], None, [256], [0, 256])
    
    mean = calc_mean(histogram)
    devitation = math.sqrt(calc_variance(histogram, mean))
    clipping_percent = calc_clipping_percentage(histogram, 250)
    
    vectors = []
    # vectors.append(mean)
    # vectors.append(devitation)
    vectors.append(clipping_percent)
    
    return vectors
    
if __name__ == "__main__":
    image_path = sys.argv[1]
    image = cv2.imread(image_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    histogram = cv2.calcHist([image_gray], [0], None, [256], [0, 256])
    # histogram = [10, 0, 0, 0, 0, 5, 0, 0, 0, 0, 10]
    print histogram
    
    mean = calc_mean(histogram)
    variance = calc_variance(histogram, mean)
    
    print mean
    print variance
    print math.sqrt(variance)
    print calc_clipping_percentage(histogram, 250)
    
    cv2.imshow("image", image_gray)
    cv2.waitKey()
    #cv2.imshow("gray", gray)
