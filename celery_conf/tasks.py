import json
import inspect

import qualipy

from celery import Celery
from celery import group

app = Celery()
# celery config file here:
app.config_from_object('sampleconfig')


@app.task
def process_image(image, filters, ROI=None, return_predictions=False,
                  combine_results=False, sort_filters=True):
    """Processes one image with process-function and returns the resulting value.
    """
    return qualipy.process(image, filters, ROI, return_predictions,
                           combine_results, sort_filters)


def celery_process(images, filters, ROIs=None, return_predictions=False,
                   combine_results=False, sort_filters=True):
    """Process a list of images by dividing the task into smaller celery-tasks.
    Returns a celery.result.ResultSet
    """
    if ROIs is None:
        return group(process_image.s(img, filters, None, return_predictions,
                                     combine_results, sort_filters)
                     for img in images)()

    if len(images) != len(ROIs):
        raise ValueError("image and ROI lists need to be of same length")

    return group(process_image.s(img, filters, ROI, return_predictions,
                                 combine_results, sort_filters)
                 for img, ROI in zip(images, ROIs))()


def get_job_status(job):
    """Returns the status of the job(celery.result.ResultSet) as a percentage
    of completed tasks
    """
    total = len(job.results)
    return (float(job.completed_count()) / total) * 100


def celery_process_request(request_json):
    """Works the same as process_request-function, but
    returns a celery.result.ResultSet instead of list of results.
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

    return group(process_image.s(img, filters, ROI, return_predictions,
                                 combine_results, sort_filters)
                 for img, ROI in zip(images, ROIs))()


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
            filters.append(filter_obj(**params))
        except TypeError:
            raise ValueError("Invalid parameters for filter %s" % filter_name)

    return filters
