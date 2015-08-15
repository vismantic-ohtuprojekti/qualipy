from imgfilter.utils.histogram_analyzation import *


def test_remove_from_ends():
    hist = numpy.array([1, 1, 0, 0, 0, 1, 1])
    assert len(remove_from_ends(hist).nonzero()[0]) == 0
