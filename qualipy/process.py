"""
Functionality for easily running several filters on one or
several images simultaneously.
"""

import json
import inspect
from operator import attrgetter
from collections import Iterable


def process(images, filters, ROIs=None, return_predictions=False,
            combine_results=True, sort_filters=True):
    """Processes an image or a list of images using the specified
    set of filters. Each filter is applied to each image and the
    results are returned as dict of dicts, where the name of the
    image acts as a key to a bool or a dict of filter results.

    :param image_paths: a path to a single image as a string or a
                        or a list of image paths
    :type image_paths: str, tuple or list
    :param filters: a list of filter objects to apply to each image
    :type filters: list
    :param ROIs: a single ROI as a 4-tuple (x0, y0, w, h) or a list
                 of ROIs (should be of same length as images), None
                 if not needed
    :type ROIs: list
    :param return_predictions: return predictions as floats
                               in range [0, 1] instead of bools
    :type return_predictions: bool
    :param combine_results: combine the results of the filters
                            into a single bool, which is false
                            if one or more filters returned a
                            positive result, and true otherwise
    :type combine_results: bool
    :param sort_filters: run filters in order of their speed
    :type sort_filters: bool
    :returns: dict -- if combine_results is set to True, each
                      value is boolean, otherwise all filter
                      results are contained in a dict, where
                      the results are bools or floats depending
                      on the return_predictions parameter
    """
    if sort_filters:
        filters.sort(key=attrgetter('speed'))

    # process single image
    if isinstance(images, str) or isinstance(images, unicode):
        return {images: __process_image(images, filters, ROIs,
                                        return_predictions, combine_results)}

    # process list or other iterable of images
    elif isinstance(images, Iterable):
        return __process_images(images, filters, ROIs,
                                return_predictions, combine_results)

    raise TypeError("images needs to be a str, 2-tuple or an iterable")


def process_request(request_json):
    """Process a list of images from a JSON request.
    Example JSON request:

    { "images": {
        "ko.jpg": [ 0, 1, 2, 3 ],
        "ok.jpg": null
        },
    "filters": {
        "whole_blur": { "threshold": 0.5}
        },
    "return_predictions": false,
    "combine_results": true,
    "sort_filters": true
    }

    :param request_json: the JSON request
    :type request_json: str
    :returns: see the documentation for the process function
    """
    import qualipy.filters
    filter_classes = inspect.getmembers(qualipy.filters, inspect.isclass)

    try:
        request = json.loads(request_json)
    except:
        raise ValueError("Invalid JSON format")

    if 'images' not in request or 'filters' not in request:
        raise ValueError("images or filters array not in JSON")

    images, ROIs = __parse_images_and_ROIs(request['images'])
    filters = __collect_filters(request['filters'], filter_classes)

    return_predictions = __get_argument(request, 'return_predictions', False)
    combine_results = __get_argument(request, 'combine_results', True)
    sort_filters = __get_argument(request, 'sort_filters', True)

    return process(images, filters, ROIs, return_predictions, combine_results,
                   sort_filters)


def __process_images(images, filters, ROIs, return_predictions,
                     combine_results):
    """Process a list of images"""
    if ROIs is None:
        return {image: __process_image(image, filters, None,
                return_predictions, combine_results)
                for image in images}

    if len(images) != len(ROIs):
        raise ValueError("image and ROI lists need to be of same length")

    return {image: __process_image(image, filters, roi,
            return_predictions, combine_results)
            for image, roi in zip(images, ROIs)}


def __process_image(image, filters, ROI, return_predictions, combine_results):
    """Process a single image by running given list of filters on it."""
    args, results = __get_predict_args(image, ROI, return_predictions), {}

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


def __get_predict_args(image, ROI, return_predictions):
    """Helper function for formatting arguments given to the predict
    function."""
    if ROI is not None:
        if type(ROI) != tuple:
            raise TypeError("invalid type ROI for image: %s" % image)

        if len(ROI) != 4:
            raise TypeError("invalid length ROI for image: %s" % image)

    return image, not return_predictions, ROI


def __get_filter(name, filter_classes):
    for _, filter in filter_classes:
        if filter.name == name:
            return filter
    return None


def __get_argument(request, arg_name, default):
    if arg_name in request:
        return request[arg_name]
    return default


def __parse_images_and_ROIs(request_images):
    images, ROIs = [], []
    for image, ROI in request_images.iteritems():
        if ROI is None or (isinstance(ROI, list) and len(ROI) == 4):
            images.append(image)
            ROIs.append(None if ROI is None else tuple(ROI))
        else:
            raise ValueError("invalid ROI for image %s" % image)
    return images, ROIs


def __collect_filters(request_filters, filter_classes):
    filters = []
    for filter_name, params in request_filters.iteritems():
        filter_obj = __get_filter(filter_name, filter_classes)
        if filter_obj is None:
            raise ValueError

        try:
            # instantiate a filter object with the given parameters
            filters.append(filter_obj(**params))
        except TypeError:
            raise ValueError("Invalid parameters for filter %s" % filter_name)

    return filters
