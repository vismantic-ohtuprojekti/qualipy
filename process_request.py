import imgfilter
from imgfilter.filters import *

import json
import inspect

def get_all_filter_class_names():
    filter_class_names = []
    filter_modules = inspect.getmembers(imgfilter.filters)

    for module_info in filter_modules:
        if '_' not in module_info[0] and module_info[0][0].isupper():
            filter_class_names.append(module_info[0])

    return filter_class_names


def get_all_filter_names(filter_class_names):
    filter_names = []

    for class_name in filter_class_names:
        exec ('filter = ' + class_name + '()')
        filter_names.append( (class_name, filter.name) )

    return filter_names


def class_name_for_name(filter_name, class_and_filter_names):
    for class_and_filter_name in class_and_filter_names:
        if filter_name == class_and_filter_name[1]:
            return class_and_filter_name[0]

    return None


def process_request(request_json):
    """Process json request which contains two arrays
    one array which contains path of the images and
    other which contains which filters to apply for
    given images

    :param request_json: json which contains the two arrays
    """

    class_and_filter_names = get_all_filter_names( get_all_filter_class_names() )

    request = json.loads(request_json)

    filters = []
    for filter_info in request['filters']:
        for filter_name in filter_info:
            exec ('filters.append(' + class_name_for_name(filter_name, class_and_filter_names) + '())')

    return imgfilter.process(request['images'], filters)
