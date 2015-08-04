import inspect
import json

import imgfilter.filters
from .process import process


FILTERS = inspect.getmembers(imgfilter.filters, inspect.isclass)


def get_filter(name):
    for _, filter in FILTERS:
        if filter.name == name:
            return filter
    return None


def get_argument(request, arg_name, default):
    if arg_name in request:
        return request[arg_name]
    return default


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
    """
    request = json.loads(request_json)

    filters = []
    for filter_name, params in request['filters'].iteritems():
        filter_obj = get_filter(filter_name)
        if filter_obj is None:
            raise ValueError
        filters.append(filter_obj(**params))

    return_predictions = get_argument(request, 'return_predictions', False)
    combine_results = get_argument(request, 'combine_results', True)
    sort_filters = get_argument(request, 'sort_filters', True)

    images = [(img, tuple(roi) if roi else None)
              for img, roi in request['images'].items()]

    return process(images, filters, return_predictions, combine_results,
                   sort_filters)
