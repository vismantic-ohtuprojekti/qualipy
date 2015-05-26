import accurancy_test_lib
import exifread
import imgfilter.filters.whole_blur

if __name__ == '__main__':
    blurred_folder = ['', '']
    originals = ['']
    extensions = ['.jpg', '.JPG', '.jpeg', '.png']

    test = accurancy_test_lib.AccurancyTest(imgfilter.filters.whole_blur.is_blurred, ((True, blurred_folder), (False, originals)), extensions)
    test.run()

    result = test.get_result()
    print 'Accuracy for all samples: ', result.get_accurancy()
    print 'Accuracy for blurred images: ', result.get_accurancy_for_type(True)
    print 'Accuracy for non blurred images: ', result.get_accurancy_for_type(False)
    result.save("accuracy_test_save.txt")
