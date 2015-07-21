"""
Functionality for easily running several filters on one or
several images simultaneously.
"""

import cv2

from analyzers import *


ANALYZERS = [Exif(),
             MagnitudeSpectrum(),
             ObjectExtraction(),
             Sharpen(),
             Resize(),
             ReduceColors(),
             ColorImage(),
             ]


def read_image(image_path):
    """Read an image from a file as grayscale

    :param image_path: path to the image file
    :type image_path: str
    :returns: numpy.ndarray
    """
    return cv2.imread(image_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    # return cv2.imread(image_path, cv2.CV_LOAD_IMAGE_COLOR)


def process(image_paths, filters):
    """Processes an image or a list of images using the specified
    set of filters. Each filter is applied to each image and the
    results are returned as list of maps, where the name of the
    filter acts as a key.

    :param image_paths: an image or a list of images to process
    :param filters: a list of filters to apply to each image
    :type filters: list
    :returns: dict
    """
    if isinstance(image_paths, list):
        return process_images(image_paths, filters)
    elif isinstance(image_paths, str):
        return process_image(image_paths, filters)
    else:
        raise TypeError


def collect_analyzers(required_analyzers):
    """Create list of analyzer objects from a list of their names

    :param required_analyzers: list of analyzers' names
    :type required_analyzers: list
    :returns: list -- list of analyzer objects
    """
    analyzer_objects = []
    for req in required_analyzers:
        for analyzer in ANALYZERS:
            if analyzer.name == req:
                analyzer_objects.append(analyzer)
                break

    return analyzer_objects


def run_analyzers(image, image_path, filters):
    if not filters:
        return {}

    required_analyzers = set.union(*[filter.required() for filter in filters])
    analyzer_objects = collect_analyzers(required_analyzers)

    analyzer_results = {'image': image}
    for analyzer in analyzer_objects:
        analyzer.run(image, image_path)
        analyzer_results[analyzer.name] = analyzer.get_copy()

    return analyzer_results


def process_image(image, filters):
    """Processes a single image.

    :param image: path to an image
    :type image: str
    :param filters: list of filters to use
    :type filters: list
    :returns: dict
    """
    filter_results = {}
    analyzer_results = run_analyzers(read_image(image), image, filters)
    for filter in filters:
        for analyzer in filter.required():
            filter.parameters[analyzer] = analyzer_results[analyzer]
        filter_results[filter.name] = filter.run()

    return filter_results


def process_images(images, filters):
    """Processes a list of images.

    :param image: list of image paths
    :type image: list
    :param filters: list of filters to use
    :type filters: list
    :returns: dict
    """
    return [process_image(image, filters) for image in images]
