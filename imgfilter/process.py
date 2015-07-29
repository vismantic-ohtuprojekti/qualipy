"""
Functionality for easily running several filters on one or
several images simultaneously.
"""

from operator import attrgetter


def process(images, filters, return_predictions=False,
            combine_results=True, sort_filters=True):
    """Processes an image or a list of images using the specified
    set of filters. Each filter is applied to each image and the
    results are returned as list of maps, where the name of the
    filter acts as a key.

    :param image_paths: an image or a list of images to process
    :param filters: a list of filters to apply to each image
    :type filters: list
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
    """Processes a single image.

    :param image: path to an image
    :type image: str
    :param filters: list of filters to use
    :type filters: list
    :returns: dict
    """
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
    """Processes a list of images.

    :param image: list of image paths
    :type image: list
    :param filters: list of filters to use
    :type filters: list
    :returns: dict
    """
    return {image: __process_image(image, filters,
                                   return_predictions, combine_results)
            for image in images}
