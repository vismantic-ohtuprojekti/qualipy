import cv2
import numpy as np

from filter import Filter

POSITIVE_VALUE = 255
NEGATIVE_VALUE = 0
MARK_VALUE = 100
LIMIT_VALUE = 120

class Coordinate(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def eq(self, other):
        return other.x == self.x and other.y == self.y


def preprocess(image):
    for y in range(0, image.shape[1]):
        for x in range(0, image.shape[0]):

            if image[x, y] > LIMIT_VALUE:
                image[x, y] = POSITIVE_VALUE
            else:
                image[x, y] = NEGATIVE_VALUE


def get_neighbors(coordinate, image):
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbor = Coordinate(coordinate.x + i, coordinate.y + j)

            if image[neighbor.x, neighbor.y] == POSITIVE_VALUE:
                image[neighbor.x, neighbor.y] = MARK_VALUE
                neighbors.append(neighbor)

    return neighbors


def breadth_first_search(start_coordinate, image):
    size = 0

    to_handle = []
    to_handle.append(start_coordinate)

    while (len(to_handle) != 0):
        current = to_handle.pop(0)

        image[current.x, current.y] = MARK_VALUE
        size = size + 1

        neighbors = get_neighbors(current, image)
        to_handle = to_handle + neighbors

    return size


class MultipleSalientRegions(Filter):

    def __init__(self):
        self.name = 'multiple_salient_regions'
        self.parameters = {}

    def required(self):
        return {'extract_object'}

    def run(self):
        salient_map, binarized = self.parameters['extract_object']

        preprocess(salient_map)

        areas = np.array([])

        for y in range(0, salient_map.shape[1]):
            for x in range(0, salient_map.shape[0]):

                if salient_map[x, y] == POSITIVE_VALUE:
                    areas = np.append(areas, breadth_first_search(Coordinate(x, y), salient_map) )

        prediction = np.power( np.sum(areas) / np.amax(areas), 2 ) - 1.0

        if prediction > 1.0:
            return 1.0
        else:
            return prediction
