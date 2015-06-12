import numpy
from imgfilter.filters.unconventional_size import UnconventionalSize


def test_gives_true_when_ratio_too_high():
    size = UnconventionalSize(16/9.0)
    img = numpy.ones(200).reshape(20, 10)
    img = {'image': img}
    size.parameters = img
    assert size.run() == True
    
def test_gives_false_when_ratio_correct():
    size = UnconventionalSize(16/9.0)
    img = numpy.ones(100).reshape(10, 10)
    img = {'image': img}
    size.parameters = img
    assert size.run() == False
    
def test_gives_false_when_ratio_correct():
    size = UnconventionalSize(16/9.0)
    img = numpy.ones(200).reshape(10, 20)
    img = {'image': img}
    size.parameters = img
    assert size.run() == True
    
    
    


