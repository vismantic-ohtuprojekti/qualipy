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
    for filter_name in request['filters']:
        # Read posible params
        params = ''
        if request.get(filter_name) is not None:
            for param in request.get(filter_name):
                params = params + param + '=' + request[filter_name][param] + ','
            params = params[0:len(params)-1]

        # Create filter
        filter_create_command = intoCamelCase(filter_name) + '(' + params + ')'
        print filter_create_command
        exec('filters.append(' + filter_create_command + ')')

    return process(request['images'], filters)


def intoCamelCase(filter_name):
    """Turns filter name which is in snake
    case to camel case

    :param filter_name: filter name which is supposed to be turned into camel case
    """
    camel_case_name = filter_name[0].upper()

    last_was_ = False
    for i in range(1, len(filter_name)):
        if last_was_:
            last_was_ = False
            continue

        character = filter_name[i]

        if character == '_':
            last_was_ = True
            camel_case_name = camel_case_name + filter_name[i + 1].upper()
        else:
            camel_case_name = camel_case_name + filter_name[i]

    return camel_case_name
