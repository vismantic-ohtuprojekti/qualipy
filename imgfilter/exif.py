from __future__ import division
from fractions import Fraction

import os
import sys
import glob
import math
import exifread

# iso =  tags['EXIF ISOSpeedRatings']
# length35mm = float(tags['EXIF FocalLengthIn35mmFilm'].printable)

# To be done:
# def calculateEffectiveFocalLength(focal_length):

def normalize_exposure(exposure):
    min_exposure = -10
    max_exposure = -2

    return (exposure - min_exposure) / (max_exposure - min_exposure)

def getExposureRatio(exposure):
    if exposure < 1 / 1000:
        return 0.0
    if exposure > 1 / 4:
        return 1.0

    exposure = math.log(exposure, 2)
    return normalize_exposure(exposure)

def parseExif(pathToImage):
    with open(pathToImage, 'rb') as image:
        tags = exifread.process_file(image, details=False)
    return tags

if __name__ == "__main__":
    points = 0
    num_files = 0
    for filename in glob.glob('*.jpg'):
        tags = parseExif(filename)
        if "EXIF ExposureTime" not in tags:
            continue

        exposure = tags["EXIF ExposureTime"]
        exposure = eval(exposure.printable)
        ratio = getExposureRatio(exposure)
        print filename + ": " + str(ratio)
        points += ratio
        num_files += 1

    print "Average: "
    print points / num_files
