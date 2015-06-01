import sys
import accuracy_test_lib
import imgfilter.filters.whole_blur

if __name__ == '__main__':
    blurred_folder = sys.argv[1]
    originals = sys.argv[2]
    extensions = ['.jpg', '.JPG', '.jpeg', '.png']

    test = accuracy_test_lib.AccuracyTest(imgfilter.filters.whole_blur.is_blurred, ((True, blurred_folder), (False, originals)), extensions)
    test.run()

    result = test.get_result()
    print 'Accuracy for all samples: ', result.get_accuracy()
    print 'Accuracy for blurred images: ', result.get_accuracy_for_type(True)
    print 'Accuracy for non blurred images: ', result.get_accuracy_for_type(False)
    result.save("accuracy_test_save.txt")
