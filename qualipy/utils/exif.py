"""
Contains functionality for analyzing the exif data of an image.
"""

from __future__ import division

import math
import exifread


def analyze_background_blur(tags):
    """Calculates and returns an estimated hyperfocal distance that tells
    how far an object must be to be in focus. Values near zero mean
    hyperfocal distance is so low, that most likely everything in the
    picture is sharp. Values near 1 mean that all the objects has to be
    hundreds of meters away to be in focus.

    :param tags: the exif tags
    :type tags: dict
    :returns: float -- the estimated hyperfocal distance, None if not able
                       to calculate the value due to missing EXIF value
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
    """Parses exif from given image and returns a float between 0 and 1,
    where values closer to 0 indicate low motion blur probability and
    values closer to 1 indicate high motion-blur probability.

    :param tags: the exif tags
    :type tags: dict
    :returns: float -- the estimated motion blur probability, None if not
                       able to calculate the value due to missing EXIF value
    """
    if tags and "EXIF ExposureTime" in tags:
        exposure = tags["EXIF ExposureTime"]
        exposure = eval(str(exposure))
        return get_exposure_ratio(exposure)
    return None


def get_exposure_value(tags):
    """Extracts exposure value from given tags
    """
    if tags and "EXIF ExposureTime" in tags:
        exposure = tags["EXIF ExposureTime"]
        exposure = eval(str(exposure))
        return exposure
    return None


def get_focal_value(tags):
    """Extracts focal length value from given tags
    """
    if tags and "EXIF FocalLength" in tags:
        return eval(str(tags["EXIF FocalLength"]))
    return None


def get_iso_value(tags):
    """Extracts ISO value from given tags
    """
    if tags and "EXIF ISOSpeedRatings" in tags:
        iso = tags["EXIF ISOSpeedRatings"]
        iso = eval(str(iso))
        return iso
    return None


def get_aperture_value(tags):
    """Extracts aperture values from given tags if focal
    length also exists
    """
    if tags and "EXIF FocalLength" in tags:
        if "EXIF FNumber" in tags:
            return eval(str(tags["EXIF FNumber"]))
        elif "EXIF ApertureValue" in tags:
            return eval(str(tags["EXIF ApertureValue"]))
        else:
            return None
    return None


def get_background_blur_ratio(focal, aperture):
    """Calculates hyperfocal length from given focal and aperture values
    and returns an estimation on how likely the background is blurred
    """
    if aperture < 0.001:
        return None

    # circle of confusion size
    coc = 0.015

    # hyperfocal calculation
    hyperfocal = focal ** 2 / (aperture * coc) + focal

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
    """Calculates the probability of motion blur in an image using
    the given exposure time. Exposure of over 1/4 seconds is most likely
    to be motion blurred.
    """
    # min and max exposure threshold values
    min_exposure = 1 / 2000
    max_exposure = 1 / 4

    # normalize
    exposure = math.log(exposure, 2)
    min_exposure = math.log(min_exposure, 2)
    max_exposure = math.log(max_exposure, 2)

    exposure = (exposure - min_exposure) / (max_exposure - min_exposure)

    if exposure < 0:
        return 0.0
    if exposure > 1:
        return 1.0

    return exposure


def parse_exif(image_path):
    """Parses the exif tags from an image

    :param image_path: path to the image file
    :type image_path: str
    :returns: dict -- the exif tags
    """
    with open(image_path, 'rb') as image:
        return exifread.process_file(image, details=False)
