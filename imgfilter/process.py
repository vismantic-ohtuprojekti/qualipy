import cv2

from analyzers import *


ANALYZERS = [Exif(),
             MagnitudeSpectrum(),
             ObjectExtraction(),
             Sharpen()
             ]


def read_image(image_path):
    return cv2.imread(image_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)


def process(image_paths, filters):
    if isinstance(image_paths, list):
        return process_images(image_paths, filters)
    elif isinstance(image_paths, str):
        return process_image(image_paths, filters)
    else:
        raise TypeError


def process_images(images, filters):
    return [process_image(image, filters) for image in images]


def collect_analyzers(required_analyzers):
    analyzer_objects = []
    for req in required_analyzers:
        for analyzer in ANALYZERS:
            if analyzer.name == req:
                analyzer_objects.append(analyzer)
                break

    return analyzer_objects


def run_analyzers(image, image_path, filters):
    required_analyzers = set.union(*[filter.required() for filter in filters])
    analyzer_objects = collect_analyzers(required_analyzers)

    analyzer_results = {'image': image}
    for analyzer in analyzer_objects:
        analyzer.run(image, image_path)
        analyzer_results[analyzer.name] = analyzer.get_copy()

    return analyzer_results


def process_image(image, filters):
    filter_results = {}
    analyzer_results = run_analyzers(read_image(image), image, filters)
    for filter in filters:
        for analyzer in filter.required():
            filter.parameters[analyzer] = analyzer_results[analyzer]
        filter_results[filter.name] = filter.run()

    return filter_results
