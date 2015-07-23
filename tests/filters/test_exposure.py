import cv2
import imgfilter
from imgfilter.filters import *

OVER_EXPOSED_IMAGE = 'tests/images/over_exposure_sample.jpg'
UNDER_EXPOSED_IMAGE = 'tests/images/under_exposure_sample.jpg'
GOOD_IMAGE = 'tests/images/exposure_sample_good.jpg'

def test_recognizes_over_exposed_image():
	res = imgfilter.process(OVER_EXPOSED_IMAGE, [Exposure()])
	assert res['exposure'] > 0.5    

def test_recognizes_under_exposed_image():
	res = imgfilter.process(UNDER_EXPOSED_IMAGE, [Exposure()])
	assert res['exposure'] > 0.5    

def test_recognizes_under_exposed_image():
	res = imgfilter.process(GOOD_IMAGE, [Exposure()])
	assert res['exposure'] < 0.5    
