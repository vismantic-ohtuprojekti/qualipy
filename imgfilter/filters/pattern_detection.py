import statistic_common
import image_processing_common

import cv2
import numpy as np
from matplotlib import pyplot as plt


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


def logaritmic_tarnsformation2D(array_2D):
    c = 1 / np.log(1 + np.abs(np.amax(array_2D)))
    return c * np.log(1 + np.abs(array_2D))


def count_magnitude_spectrum(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    return logaritmic_tarnsformation2D(fshift)


def pattern_regonition(image_path):
    # Turn into gray scale
    image = cv2.imread(image_path)
    image = reduce_colors(image, 2)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Count magnitude spectrum
    magnitude_spectrum = count_magnitude_spectrum(image)

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


    all_distances = statistic_common.remove_anomalies(all_distances, 0.4)
    max_distances = statistic_common.get_max_values(all_distances, 20)

    max_distance_avg = statistic_common.avarage(max_distances)
    magnitude_spectrum = mark_all_points_outside_circle(magnitude_spectrum, max_distance_avg)

    all_points = np.where(magnitude_spectrum != 1)
    intense_points = np.where(magnitude_spectrum == 2)

    a = float(len(all_points) * len(all_points[0]))
    b = float(len(intense_points) * len(intense_points[0]))

    return b / a