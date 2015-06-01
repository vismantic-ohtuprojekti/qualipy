from __future__ import division

import sys
import glob
import math
import exifread

def analyze_background_blur(tags):
    if tags and "EXIF FocalLength" in tags and "EXIF ApertureValue" in tags:
        focal = eval(tags["EXIF FocalLength"].printable)
        aperture = eval(tags["EXIF ApertureValue"].printable)
        return get_background_blur_ratio(focal, aperture)
    return None
    
def get_background_blur_ratio(focal, aperture):
    """ Calculates and returns an estimated hyperfocal distance that tells
     how far an object must be to be in focus. 
     Values near zero mean hyperfocal distance is so low, 
     that most likely everything in the picture is sharp. 
     Values near 1 mean that all the objects has to be 
     hundreds of meters away to be in focus.
    """
    coc = 0.015
    # hyperfocal calculation:
    hyperfocal = (math.pow(focal, 2) / (aperture * coc)) + focal
    
    # normalize:
    hyperfocal = math.log(hyperfocal, 2)
           
    min_hyp = 6.6
    max_hyp = 15
    hyperfocal = (hyperfocal - min_hyp) / (max_hyp - min_hyp)
    
    if hyperfocal < 0:
        return 0
    if hyperfocal > 1:
        return 1
    return hyperfocal
    
def normalize_exposure(exposure):
    """ Normalizes the given exposure-value to a float between 0 and 1
    :param exposure: float, usually between 1/4000 and 30
    """
    exposure = math.log(exposure, 2)
    min_exposure = -10
    max_exposure = -2  # 0.5-arvo vastaa noin 1/60-valotusaikaa

    return (exposure - min_exposure) / (max_exposure - min_exposure)

def get_exposure_ratio(exposure):
    if exposure < 1 / 1000:
        return 0.0
    if exposure > 1 / 4:
        return 1.0

    return normalize_exposure(exposure)

def analyze_picture_exposure(tags):
    """ Parses exif from given image and returns a float between 0 and 1,
    where values closer to 0 indicate low motion blur probability and 
    values closer to 1 indicate high motion-blur probability. 
    Returns None if no exif is found.
    """
    if tags and "EXIF ExposureTime" in tags:
        exposure = tags["EXIF ExposureTime"]
        exposure = eval(exposure.printable)
        return get_exposure_ratio(exposure)
    return None

"""
def getImagesInFolder():
    types = ('*.jpg', '*.JPG', '*.jpeg')
    images = []
    for files in types:
    	images.extend(glob.glob(files))
    return sorted(images)

if __name__ == "__main__":
    total_exp = 0
    total_back = 0
    num_files = 0
    images = getImagesInFolder()
    for image in images:
        exp = analyzePictureExposure(image)
        back = analyze_background_blur(image)
        if exp != None and back != None:
            print image + ": " + str(exp) + " -- " + str(back)
            total_exp += exp
            total_back += back
            num_files += 1
    if num_files > 0:
        print "Average: "
        print str(total_exp / num_files) + ", " + str(total_back / num_files)
    else:
        print "No images found!"
"""
