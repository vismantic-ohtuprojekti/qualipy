import cv2
import numpy as np

from filter import Filter

class MultipleSalientRegions(Filter):

    name = 'multiple_salient_regions'

    def __init__(self):
        self.parameters = {}

    def required(self):
        return {'extract_object'}

    def run(self):
        salient_map, binarized = self.parameters['extract_object']

        # Count threshold
        rounded_salient_map = np.sort( np.around(salient_map.ravel(), decimals=-1) )
        unique_array, count_array = np.unique(rounded_salient_map, return_counts=True)

        unique_array = unique_array[::-1]
        count_array = count_array[::-1]

        smallest_large_index = int(unique_array.shape[0] * (3.0/4.0))

        limit = np.average(unique_array[0:smallest_large_index], axis=0, weights=count_array[0:smallest_large_index])

        # Thresh is the image which has been wiltered with threshold
        ret, thresh = cv2.threshold(salient_map, limit, 255, cv2.THRESH_BINARY)

        # Find coherent regions
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        # Count areas of coderent regions
        areas = np.array([])
        for contour in contours:
            areas = np.append(areas, cv2.contourArea(contour))

        # If areas is empty empty regions in image
        if areas.shape[0] == 0:
            return 1.0

        # Count prediction
        prediction = np.power( np.sum(areas) / np.amax(areas), 2 ) - 1.0

        # scale prediction
        if prediction > 1.0:
            return 1.0
        else:
            return prediction
