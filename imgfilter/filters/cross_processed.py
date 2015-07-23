import numpy as np
import cv2

from matplotlib import pyplot as plt

from filter import Filter

def calculate_continuous_distribution(distribution):
    continuous_distribution = np.array([])

    current_sum = 0.0
    for i in range(0, distribution.shape[0]):
        current_sum += distribution[i]
        continuous_distribution = np.append(continuous_distribution, current_sum)

    return continuous_distribution


def retrieve_darkest(image):
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sorted_by_pixel_value = np.sort(gray_scale.flatten())
    return sorted_by_pixel_value[0:np.rint(sorted_by_pixel_value.shape[0] * 0.2):1]


def retrieve_ligthest(image):
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sorted_by_pixel_value = np.sort(gray_scale.flatten())
    return sorted_by_pixel_value[np.rint(sorted_by_pixel_value.shape[0] * 0.8):sorted_by_pixel_value.shape[0]:1]


def cross_processed_prediction(image):
    ligthest_and_darkest = np.append(retrieve_ligthest, retrieve_darkest(image))

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist_hue = cv2.calcHist([hsv], [0], None, [30], [0,180])

    normalized = np.divide(hist_hue.astype(np.float32), np.sum(hist_hue))
    continuous_distribution = calculate_continuous_distribution(normalized)

    points_with_huge_derivate = np.array([])
    for i in range(0, continuous_distribution.shape[0] - 1):
        current_derivate = continuous_distribution[i + 1] - continuous_distribution[i]

        if current_derivate >= 0.025:
            points_with_huge_derivate = np.append(points_with_huge_derivate, i)

    if points_with_huge_derivate.shape[0] == 0:
        return 0.0

    number_of_areas = 0
    previous_index = points_with_huge_derivate[0]
    for i in range(0, points_with_huge_derivate.shape[0]):
        if points_with_huge_derivate[i] != previous_index + 1:
            number_of_areas += 1

        previous_index = points_with_huge_derivate[i]

    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    plt.plot(hist_hue, color = 'red')
    plt.xlim([0,30])
    plt.show()

    return 1.0 / number_of_areas


class CrossProcessed(Filter):

    name = 'cross_processed'

    def __init__(self):
        self.parameters = {}

    def required(self):
        return {'color_image'}

    def run(self):
        return cross_processed_prediction(self.parameters['color_image'])
