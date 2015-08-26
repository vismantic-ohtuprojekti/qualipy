import sys

import qualipy
import accuracy_test_lib


def run_accuracy_test(filter):
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: %s POSITIVES NEGATIVES\n' % sys.argv[0])
        sys.exit(1)

    positives = [sys.argv[1]]
    negatives = [sys.argv[2]]
    extensions = ['.jpg', '.JPG', '.jpeg', '.png']

    def get_prediction(path):
        return not qualipy.process(path, [filter])

    test = accuracy_test_lib.AccuracyTest(get_prediction,
            ((True, positives), (False, negatives)), extensions)
    test.run()

    result = test.get_result()
    print 'Accuracy for all samples: ', result.get_accuracy()
    print 'Accuracy for positive images: ', result.get_accuracy_for_type(True)
    print 'Accuracy for negative images: ', result.get_accuracy_for_type(False)
