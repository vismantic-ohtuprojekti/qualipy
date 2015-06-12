from ..analyzers.common.statistic_common import *

from filter import Filter

import cv2
import numpy as np

def logaritmic_tarnsformation2D(array_2D):
    c = 1 / np.log(1 + np.abs(np.amax(array_2D)))
    return c * np.log(1 + np.abs(array_2D))


def count_magnitude_spectrum(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    return logaritmic_tarnsformation2D(fshift)


def mark_all_points_outside_circle(array_2D, radii):
    """
    Sets all points to 1 which are outside of circle which has center
    at the midle of the given 2D array. Radii of the circle is
    given as a parameter.

    param array_2D: Array which is processed
    param radii: Radii of circle
    """
    center = np.array((array_2D.shape[0]/2.0, array_2D.shape[1]/2.0))

    for x in range(0, array_2D.shape[0]):
        for y in range(0, array_2D.shape[1]):
            distance_from_center = np.abs(np.linalg.norm(center - np.array((x,y))))

            if distance_from_center > radii:
                array_2D[x,y] = 1

    return array_2D


def pattern_regonition(two_color_image, magnitude_spectrum):
    """
    Counts prediction for image

    param two_color_image: Image where colors are reduced only to two
    param magnitude_spectrum: Magnitude spectrum of two color image
    """
    # Turn into gray scale
    #two_color_image = cv2.cvtColor(two_color_image, cv2.COLOR_BGR2GRAY)

    # Center of the image
    center = np.array((magnitude_spectrum.shape[0]/2.0, magnitude_spectrum.shape[1]/2.0))

    all_distances = np.array([])

    for x in xrange(0, magnitude_spectrum.shape[0]):
        for y in xrange(0, magnitude_spectrum.shape[1]):
            # Count distance from the center of the image
            distance_from_center = np.abs(np.linalg.norm(center - np.array((x,y))))

            # Make magnitude spectrum to contain only high values
            # and count all non zero points
            if magnitude_spectrum[x,y] > 0.70:
                magnitude_spectrum[x,y] = 2
                all_distances = np.append(all_distances, distance_from_center)
            else:
                magnitude_spectrum[x,y] = 0


    all_distances = remove_anomalies(all_distances, 0.4)
    max_distances = get_max_values(all_distances, 20)

    max_distance_avg = avarage(max_distances)
    magnitude_spectrum = mark_all_points_outside_circle(magnitude_spectrum, max_distance_avg)

    all_points = np.where(magnitude_spectrum != 1)
    intense_points = np.where(magnitude_spectrum == 2)

    a = float(len(all_points) * len(all_points[0]))
    b = float(len(intense_points) * len(intense_points[0]))

    return b / a


def scaled_prediction(prediction):
    if prediction < 0.05:
        return 1.0
    elif prediction > 0.4:
        return 0.0
    else:
        return linear_normalize(prediction, 0.0, 0.4)


class PatternDetection(Filter):

    def __init__(self):
        self.name = 'pattern_detection'
        self.parameters = {}


    def required(self):
        return {'reduce_colors'}


    def run(self):
        magnitude_spectrum = count_magnitude_spectrum(self.parameters['reduce_colors'])
        return scaled_prediction(pattern_regonition(self.parameters['reduce_colors'], magnitude_spectrum))
