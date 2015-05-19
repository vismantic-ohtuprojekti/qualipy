import os
import exifread

folder = os.path.dirname(__file__)

# Open image file for reading (binary mode)
image = open(folder + "/test_image.jpeg", 'rb')

# Return Exif tags
tags = exifread.process_file(image)

exposure = tags['EXIF ExposureTime']
length_normal = tags['EXIF FocalLength']
iso =  tags['EXIF ISOSpeedRatings']
length35mm =  tags['EXIF FocalLengthIn35mmFilm']

def imageHasSufficentExposureAndFocalLength():
    if exposure > 30:
        return False;
    else:
        return True;

print imageHasSufficentExposureAndFocalLength()

"""
for tag in tags.keys():
    if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):
        print "Key: %s, value %s" % (tag, tags[tag])

"""
