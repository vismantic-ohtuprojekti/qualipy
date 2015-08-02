import imgfilter
from imgfilter.filters import *


PATTERN = 'tests/images/pattern.jpg'
NON_PATTERN = 'tests/images/lama.jpg'


def test_recognizes_pattern_image():
    assert not imgfilter.process(PATTERN, [Pattern()])


def test_doesnt_recognize_non_pattern_image():
    assert imgfilter.process(NON_PATTERN, [Pattern()])
