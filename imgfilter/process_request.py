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


def process_request(request_json):
    """Process json request which contains two arrays
    one array which contains path of the images and
    other which contains which filters to apply for
    given images

    :param request_json: json which contains the two arrays
    """
    request = json.loads(request_json)

    filters = []
    for filter_name, params in request['filters'].iteritems():
        filter_obj = get_filter(filter_name)
        if filter_obj is None:
            raise ValueError
        filters.append(filter_obj(**params))

    return process(request['images'], filters)
