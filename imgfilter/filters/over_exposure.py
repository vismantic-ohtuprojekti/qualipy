import numpy
import cv2
import sys
import math

from filter import Filter
from imgfilter.machine_learning.svm import SVM
from .. import get_data

class OverExposed(Filter):

    def __init__(self):
        self.name = "over_exposed"
        self.parameters = {}
        
    def required(self):
        return {'exposure'}

    def run(self):
        """ Checks if image is over-exposed
        """
        svm = SVM()
        svm.load(get_data('svm/over_exposure.yml'))

        input_vec = self.parameters['exposure']
        input_vec = numpy.asarray(input_vec).astype(numpy.float32)
        algo_prediction = self.scaled_prediction(svm.predict(input_vec))

        return algo_prediction
    
    def scaled_prediction(self, prediction):
        pred = 1 - (1 + prediction) / 2

        if pred < 0:
            return 0
        if pred > 1:
            return 1

        return pred

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
