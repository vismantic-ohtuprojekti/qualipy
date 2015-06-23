import json
from filters import *


def process_request(request_json):
    """Process json request which contains two arrays
    one array which contains path of the images and
    other which contains which filters to apply for
    given images

    :param request_json: json which contains the two arrays
    """
    request = json.loads(request_json)

    filters = []
    for filter_create_command in request['filters']:
        exec('filters.append(' + filter_create_command + ')')

    return process(request['images'], filters)
