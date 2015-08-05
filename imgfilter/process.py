"""
Functionality for easily running several filters on one or
several images simultaneously.
"""

from operator import attrgetter
from collections import Iterable


def process(images, filters, return_predictions=False,
            combine_results=True, sort_filters=True):
    """Processes an image or a list of images using the specified
    set of filters. Each filter is applied to each image and the
    results are returned as dict of dicts, where the name of the
    image acts as a key to a dict of filter results.

    :param image_paths: an image or a list of images to process
    :type image_paths: str or list
    :param filters: a list of filters to apply to each image
    :type filters: list
    :param return_predictions: return predictions as a floats
                               in range [0, 1] instead of bools
    :type return_predictions: bool
    :param combine_results: combine the results of the filters
                            into a single bool, which is false
                            if one or more filters returned a
                            positive result, and true otherwise
    :type combine_results: bool
    :param sort_filters: run filters in order of their speed
    :type sort_filters: bool
    :returns: dict
    """
    if sort_filters:
        filters.sort(key=attrgetter('speed'))

    if isinstance(images, str) or (isinstance(images, tuple) and
                                   len(images) == 2):
        return __process_image(images, filters,
                               return_predictions, combine_results)
    elif isinstance(images, Iterable):
        return __process_images(images, filters,
                                return_predictions, combine_results)

    raise TypeError("images needs to be a str, 2-tuple or an iterable")


def __process_images(images, filters, return_predictions, combine_results):
    """Process a list of images"""
    return {image: __process_image(image, filters,
                                   return_predictions, combine_results)
            for image in images}


def __process_image(image, filters, return_predictions, combine_results):
    """Process a single image by running given list of filters on it."""
    args, results = __get_predict_args(image, return_predictions), {}

    for filt in filters:
        prediction = filt.predict(*args)

        # if the result should be returned as a single boolean,
        # return False straightaway after getting a positive result
        if not return_predictions and combine_results and prediction:
            return False

        results[filt.name] = prediction

    if not return_predictions and combine_results:
        return True
    return results


def __get_predict_args(image, return_predictions):
    """Helper function for formatting arguments given to the predict
    function."""
    if isinstance(image, str):
        return image, not return_predictions
    if isinstance(image, tuple) and len(image) == 2:
        img, ROI = image

        if ROI is not None and len(ROI) != 4:
            raise TypeError("invalid length ROI for image: " + str(image))

        return img, not return_predictions, ROI

    raise TypeError("invalid image parameter: {}, needs to be a "
                    "str or a 2-tuple".format(image))
