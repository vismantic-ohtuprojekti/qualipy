import inspect
import json

import imgfilter.filters
from .process import process


FILTERS = inspect.getmembers(imgfilter.filters, inspect.isclass)


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
    request = json.loads(request_json)

    if 'images' not in request or 'filters' not in request:
        raise ValueError("images or filters array not in JSON")

    images = __parse_images(request['images'])
    filters = __collect_filters(request['filters'])

    return_predictions = __get_argument(request, 'return_predictions', False)
    combine_results = __get_argument(request, 'combine_results', True)
    sort_filters = __get_argument(request, 'sort_filters', True)

    return process(images, filters, return_predictions, combine_results,
                   sort_filters)


def __get_filter(name):
    for _, filter in FILTERS:
        if filter.name == name:
            return filter
    return None


def __get_argument(request, arg_name, default):
    if arg_name in request:
        return request[arg_name]
    return default


def __parse_images(request_images):
    images = []
    for image, ROI in request_images.iteritems():
        if ROI is None or (isinstance(ROI, list) and len(ROI) == 4):
            images.append((image, ROI))
        else:
            raise ValueError("invalid ROI for image %s" % image)
    return images


def __collect_filters(request_filters):
    filters = []
    for filter_name, params in request_filters.iteritems():
        filter_obj = __get_filter(filter_name)
        if filter_obj is None:
            raise ValueError
        filters.append(filter_obj(**params))
    return filters
