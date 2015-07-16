from __future__ import division

import sys
import glob
import math
import exifread
import imgfilter.machine_learning.svm 

def analyze_background_blur(tags):
    """ Calculates and returns an estimated hyperfocal distance that tells
    how far an object must be to be in focus. 
    Values near zero mean hyperfocal distance is so low, 
    that most likely everything in the picture is sharp. 
    Values near 1 mean that all the objects has to be 
    hundreds of meters away to be in focus.
    """
    if tags and "EXIF FocalLength" in tags:
        if "EXIF FNumber" in tags:
            aperture = eval(str(tags["EXIF FNumber"]))
        elif "EXIF ApertureValue" in tags:
            aperture = eval(str(tags["EXIF ApertureValue"]))
        else:
            return None

        focal = eval(str(tags["EXIF FocalLength"]))
        return get_background_blur_ratio(focal, aperture)

    return None


def analyze_picture_exposure(tags):
    """ Parses exif from given image and returns a float between 0 and 1,
    where values closer to 0 indicate low motion blur probability and 
    values closer to 1 indicate high motion-blur probability. 
    Returns None if no exif is found.
    """
    if tags and "EXIF ExposureTime" in tags:
        exposure = tags["EXIF ExposureTime"]
        exposure = eval(str(exposure))
        return get_exposure_ratio(exposure)
    return None

def get_image_vectors(tags):
    vectors = []
    vectors.append(analyze_picture_exposure(tags))
    # vectors.append(get_focal_value(tags))
    # vectors.append(get_iso_value(tags))
    # vectors.append(get_aperture_value(tags))
    if None in vectors:
        return None
    return vectors

def get_exposure_value(tags):
    if tags and "EXIF ExposureTime" in tags:
        exposure = tags["EXIF ExposureTime"]
        exposure = eval(str(exposure))
        return exposure
    return None

def get_focal_value(tags):
    if tags and "EXIF FocalLength" in tags:
        return eval(str(tags["EXIF FocalLength"]))
    return None

def get_iso_value(tags):
    if tags and "EXIF ISOSpeedRatings" in tags:
        iso = tags["EXIF ISOSpeedRatings"]
        iso = eval(str(iso))
        return iso
    return None

def get_aperture_value(tags):
    if tags and "EXIF FocalLength" in tags:
        if "EXIF FNumber" in tags:
            return eval(str(tags["EXIF FNumber"]))
        elif "EXIF ApertureValue" in tags:
            return eval(str(tags["EXIF ApertureValue"]))
        else:
            return None
    return None

def get_background_blur_ratio(focal, aperture):
    if aperture < 0.001:
        return None

    # circle of confusion size:
    coc = 0.015

    # hyperfocal calculation:
    hyperfocal = (math.pow(focal, 2) / (aperture * coc)) + focal

    # hyperfocal thresholds in millimeters
    min_threshold = 200
    max_threshold = 100000

    # normalize:
    hyperfocal = math.log(hyperfocal, 2)
    min_threshold = math.log(min_threshold, 2)
    max_threshold = math.log(max_threshold, 2)

    hyperfocal = (hyperfocal - min_threshold) / (max_threshold - min_threshold)

    if hyperfocal < 0:
        return 0.0
    if hyperfocal > 1:
        return 1.0

    return hyperfocal


def get_exposure_ratio(exposure):
    # min and max exposure threshold values
    min_exposure = 1/2000
    max_exposure = 1/4

    # normalize:
    exposure = math.log(exposure, 2)
    min_exposure = math.log(min_exposure, 2)
    max_exposure = math.log(max_exposure, 2)

    exposure = (exposure - min_exposure) / (max_exposure - min_exposure)

    if exposure < 0:
        return 0.0
    if exposure > 1:
        return 1.0

    return exposure


def get_images_in_folder():
    types = ('*.jpg', '*.jpeg')
    images = []
    for files in types:
        images.extend(glob.glob(files))
    return sorted(images)

def parse_exif(image_path):
    """Parses the exif tags from an image.

    :param image_path: path to the image file
    """
    with open(image_path, 'rb') as image:
        return exifread.process_file(image, details=False)

    
if __name__ == "__main__":
    total_exp = 0
    total_back = 0
    num_files = 0
    images = get_images_in_folder()
    tags = None
    for image in images:
        tags = parse_exif(image)
        exp = analyze_picture_exposure(tags)
        back = analyze_background_blur(tags)
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