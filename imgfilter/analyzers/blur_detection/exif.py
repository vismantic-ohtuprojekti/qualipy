from __future__ import division

import math

# To be done:
# def calculateEffectiveFocalLength(focal_length):

# WIP
def analyze_picture_backgroundblur(tags):
    if tags and "EXIF FocalLength" in tags and "EXIF ":
        exposure = tags["EXIF FocalLength"]
        exposure = float(exposure.printable)
        return get_exposure_ratio(exposure)

    return None


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
