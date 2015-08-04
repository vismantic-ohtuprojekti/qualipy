import imgfilter
from imgfilter.filters import *


POSTERIZED_IMAGE = 'tests/images/posterized.png'
NON_POSTERIZED_IMAGE = 'tests/images/non_posterized.jpg'


def test_recognizes_posterized_image():
    assert not imgfilter.process(POSTERIZED_IMAGE, [Posterized()])


def test_recognizes_non_posterized_image():
    assert imgfilter.process(NON_POSTERIZED_IMAGE, [Posterized()])
