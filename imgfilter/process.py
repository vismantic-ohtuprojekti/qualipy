"""
Functionality for easily running several filters on one or
several images simultaneously.
"""

from operator import attrgetter


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

    if isinstance(images, list):
        return __process_images(images, filters,
                                return_predictions, combine_results)
    elif isinstance(images, tuple):
        return __process_image(images, filters,
                               return_predictions, combine_results)
    elif isinstance(images, str):
        return __process_image((images, None), filters,
                               return_predictions, combine_results)
    else:
        raise TypeError


def __process_image(image, filters, return_predictions, combine_results):
    results = {}
    for filt in filters:
        if isinstance(image, str):
            prediction = filt.predict(image, not return_predictions)
        elif isinstance(image, tuple):
            img, ROI = image
            prediction = filt.predict(img, not return_predictions, ROI)
        else:
            raise TypeError

        if not return_predictions and combine_results and prediction:
            return False
        results[filt.name] = prediction

    if not return_predictions and combine_results:
        return True
    return results


def __process_images(images, filters, return_predictions, combine_results):
    return {image: __process_image(image, filters,
                                   return_predictions, combine_results)
            for image in images}
