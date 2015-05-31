from __future__ import division

import sys
import glob
import math
import exifread

# iso =  tags['EXIF ISOSpeedRatings']
# length35mm = float(tags['EXIF FocalLengthIn35mmFilm'].printable)

# To be done:
# def calculateEffectiveFocalLength(focal_length):

# WIP
def analyze_picture_backgroundblur(image):
    tags = parseExif(image)
    if "EXIF FocalLength" in tags and "EXIF ":
        exposure = tags["EXIF FocalLength"]
        exposure = float(exposure.printable)
        return getExposureRatio(exposure)
    return None

def normalize_exposure(exposure):
    """ Normalizes the given exposure-value to a float between 0 and 1
    
    :param exposure: float, usually between 1/4000 and 30
    """
    exposure = math.log(exposure, 2)
    min_exposure = -10
    max_exposure = -2 				# 0.5-arvo vastaa noin 1/60-valotusaikaa

    return (exposure - min_exposure) / (max_exposure - min_exposure)

def getExposureRatio(exposure):
    if exposure < 1 / 1000:
        return 0.0
    if exposure > 1 / 4:
        return 1.0

    return normalize_exposure(exposure)

def parseExif(pathToImage):
    """ Parses exif-data from given image (.jpg or .tiff) and returns it as a dictionary
    """
    with open(pathToImage, 'rb') as image:
        tags = exifread.process_file(image, details=False)
    return tags

def analyzePictureExposure(image):
    """ Parses exif from given image and returns a float between 0 and 1, where values closer to 0 indicate low motion blur probability and values closer to 1 indicate high motion-blur probability. Returns None if no exif is found.
    """
    tags = parseExif(image)
    if "EXIF ExposureTime" in tags:
        exposure = tags["EXIF ExposureTime"]
        exposure = eval(exposure.printable)
        return getExposureRatio(exposure)
    return None

def getImagesInFolder():
    types = ('*.jpg', '*.JPG', '*.jpeg')
    images = []
    for files in types:
    	images.extend(glob.glob(files))
    return sorted(images)

if __name__ == "__main__":
    points = 0
    num_files = 0
    images = getImagesInFolder()
    for image in images:
        tags = parseExif(image)
        if "EXIF ExposureTime" not in tags:
            continue

        exposure = tags["EXIF ExposureTime"]
        exposure = eval(exposure.printable)
        ratio = getExposureRatio(exposure)
        print image + ": " + str(ratio)
        points += ratio
        num_files += 1
    if num_files > 0:
        print "Average: "
        print points / num_files
    else:
        print "No images found!"
