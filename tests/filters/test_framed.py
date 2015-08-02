import imgfilter
from imgfilter.filters import *


FRAMED = 'tests/images/framed.jpg'
NON_FRAMED = 'tests/images/lama.jpg'


def test_recognizes_framed_image():
    assert not imgfilter.process(FRAMED, [Framed()])


def test_doesnt_recognize_non_framed_image():
    assert imgfilter.process(NON_FRAMED, [Framed()])
