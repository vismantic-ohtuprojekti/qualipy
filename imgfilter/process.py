def process_image(image, filters):
    required_analyzers = set()

    for filter, optional_parameters in filters:
        filter.set_optional_parameters(optional_parameters)
        
        for key, value in filter.parameters:
            if value is None:
                # union
                required_analyzers.update(key)
    
    analyzers_results = {}
    for analyzer in required_analyzers:
        # Analyzer.run() -> Celery
        
    filter_results = {}
    for filter, optional_parameters in filters:
        for key, value in filter.parameters:
            if value is None:
                filter.parameters[key] = analyzers_results[key]
                # filter_results[filter.name] = filter.run() -> Celery
    
    return filter_results


def process(image_paths, filters):
    if isinstance(image_paths, list):
        results_for_images = []
        for image in image_paths:
            # process_image -> Celery
        return results_for_images
            

    else:
        return process_image(image_paths, filters)
