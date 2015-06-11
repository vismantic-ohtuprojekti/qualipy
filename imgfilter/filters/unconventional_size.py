import numpy as np
import cv2

from imgfilter.machine_learning.svm import SVM
from .. import get_data

from filter import Filter

def get_input_vector(img):
	
	return np.array([img.shape[1], img.shape[0]]) 
	
class UnconventionalSize(Filter):
	
	def __init__(self, min_aspect, max_aspect):
		self.name = 'unconventional_size'
		self.parameters = {}
		self.min_aspect = min_aspect
		self.max_aspect = max_aspect
        
	def required(self):
		return {'image'}

	def run(self):

		input_vec = get_input_vector(self.parameters['image'])
		aspect_ratio = input_vec[0]/input_vec[1]
		if aspect_ratio >= self.min_aspect and aspect_ratio <= self.max_aspect:
			return False
		else:
			return True
