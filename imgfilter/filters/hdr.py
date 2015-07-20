import cv2
import numpy
import math
from imgfilter.machine_learning.svm import SVM
from imgfilter.analyzers.resize import resize
from imgfilter.utils.utils import scaled_prediction
from .. import get_data

from filter import Filter

svm = SVM()

class Hdr(Filter):
    
    name = "hdr"
    
    def __init__(self):
        self.parameters = {}
        
    def required(self):
        return {'image'}
    
    def run(self):
        image = self.parameters['image']
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        #hist = cv2.calcHist([hsv], [0, 1], None, [16, 4], [0, 180, 0, 256])
        hue = cv2.calcHist([hsv], [0], None, [180], [0, 180])
        sat = cv2.calcHist([hsv], [1], None, [256], [0, 256])
        value = cv2.calcHist([hsv], [2], None, [256], [0, 256])
        #histogram = cv2.calcHist([gray], [0], None, [256], [0, 256])
        
        gray = cv2.GaussianBlur(gray,(3,3),0)

        gray_lap = cv2.Laplacian(gray,cv2.CV_16S,ksize = 3,scale = 1,delta = 0)
        edges = cv2.convertScaleAbs(gray_lap)

        cv2.imshow('laplacian', edges)
        cv2.waitKey(0)

        print calc_standard_deviation(hue)
        print calc_clipping_percent(sat, 240)
        print calc_mean(sat)
        # print calc_standard_deviation(sat)
        print "---"
        print calc_clipping_percent(value, 250)
        print calc_standard_deviation(value)
        print calc_edge_ratio(edges)
        """
        svm.load(get_data('svm/hdr.yml'))
        vectors = get_input_vectors(image)
        data = numpy.asarray(vectors).astype(numpy.float32)
        return scaled_prediction(svm.predict(data))
    
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

def calc_standard_deviation(histogram):
    mean = calc_mean(histogram)
    variance = calc_variance(histogram, mean)

    return math.sqrt(variance)

def calc_clipping_percent(histogram, threshold):
    return float(numpy.sum(histogram[threshold:])) / numpy.sum(histogram)

def calc_edge_ratio(obj):
    return numpy.count_nonzero(obj) / float(obj.size)

def get_input_vectors(image):
    # image = cv2.imread(image, cv2.CV_LOAD_IMAGE_COLOR)
    image = resize(image, 500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    hue = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    sat = cv2.calcHist([hsv], [1], None, [256], [0, 256])
    value = cv2.calcHist([hsv], [2], None, [256], [0, 256])

    # gray = cv2.GaussianBlur(gray,(3,3),0)
    gray_lap = cv2.Laplacian(gray,cv2.CV_16S,ksize = 3,scale = 1,delta = 0)
    edges = cv2.convertScaleAbs(gray_lap)
    edges = cv2.calcHist([gray], [0], None, [256], [0, 256])
    
    vectors = []
    
    #vectors.append(hue)
    #vectors.append(sat)
    #vectors.append(value)
    
    vectors.append(calc_clipping_percent(sat, 240))
    vectors.append(calc_mean(sat))
    vectors.append(calc_standard_deviation(sat))
    
    vectors.append(calc_clipping_percent(value, 254))
    vectors.append(calc_standard_deviation(value))
    vectors.append(calc_mean(edges))

    return vectors
    
"""
def normal_std(histogram):
    values_1 = 0
    values_2 = 0
    for i, value in enumerate(histogram):
        values_1 += math.pow((value * i), 2)
        values_2 += (value * i)
        
    avg_1 = float(values_1 / sum(histogram))
    avg_2 = float(values_2 / sum(histogram))
    mean = math.pow(avg_2, 2)
    return avg_1 - mean
"""
