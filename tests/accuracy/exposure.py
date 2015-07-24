import sys
import accuracy_test_lib
from imgfilter.filters import *
import imgfilter
    
def get_prediction(path):
    res = imgfilter.process(path, [Exposure()])['exposure']
    print res
    return res >= 0.5

if __name__ == '__main__':
    positives = [sys.argv[1]]
    negatives = [sys.argv[2]]
    extensions = ['.jpg', '.JPG', '.jpeg', '.png']
    
    test = accuracy_test_lib.AccuracyTest(get_prediction, ((True, positives), (False, negatives)), extensions)
    test.run()
    
    result = test.get_result()
    print 'Accuracy for all samples: ', result.get_accuracy()
    print 'Accuracy for positive images: ', result.get_accuracy_for_type(True)
    print 'Accuracy for negative images: ', result.get_accuracy_for_type(False)
