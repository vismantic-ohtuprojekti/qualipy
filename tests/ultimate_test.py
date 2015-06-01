import accurancy_test
import exif
import imgfilter.filters.whole_blur



blurred_folder = ['/home/pyjopy/Desktop/blurratut/natural_blur']
originals = ['/home/pyjopy/Desktop/blurratut/originals']

extensions = ['.jpg', '.JPG', '.jpeg']
test = accurancy_test.AccurancyTest(imgfilter.filters.whole_blur.is_blurred, ((True, blurred_folder), (False, originals)), extensions)

test.run()
result = test.get_result()
print result.get_accurancy()
print result.get_accurancy_for_type(True)
print result.get_accurancy_for_type(False)
result.save("exif_test_result.txt")
