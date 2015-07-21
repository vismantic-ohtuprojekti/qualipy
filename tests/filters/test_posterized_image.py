import imgfilter
from imgfilter.filters import *

POSTERIZED_IMAGE = 'tests/images/posterized.jpeg'
NON_POSTERIZED_AIMGE = 'tests/images/non_posterized.jpeg'

def should_recognize_posterized_image():
    assert imgfilter.process(POSTERIZED_IMAGE, [Posterized()]) > 0.5

def should_recognize_non_posterized_image():
    assert imgfilter.process(NON_POSTERIZED_IMAGE, [Posterized()]) < 0.5
