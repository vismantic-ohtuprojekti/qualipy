Celery
****************

Usage
-----
Celery can be used to process multiple images at the same time, by dividing the filtering process between workers. To start, you must first configure celeryconfig.py to include correct broker address and task modules, for example if you are using Redis::

    ## Broker settings.
    BROKER_URL = 'redis://localhost:6379/0'

    # List of modules to import when celery starts.
    CELERY_IMPORTS = ('tasks', )

    ## Using the database to store task state and results.
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    CELERY_ANNOTATIONS = {'tasks.process_image': {'rate_limit': '100/s'}}

and then starting a worker in the root folder of the project::

    celery -A tasks worker --loglevel=info

The tasks.py contains one task, **process_image()**, which should be used to filter single images. It is identical to the qualipy.process-function.

However tasks.py also includes **celery_process()** and **celery_process_request()**-functions, that should be used when filtering a list of images simultaneously. The usage is similar to to **qualipy.process()** and **qualipy.process_request()**-functions, but instead of returning the results, the functions return a celery.result.ResultSet.

Example usage
-------------

The ResultSet can be queried to give the status of the process by using the **tasks.get_job_status()**-function, which returns the percentage of tasks that are finished::

    import qualipy
    import os
    import time
    from qualipy.filters import *
    from tasks import *

    if __name__ == "__main__":
        path = 'tests/images/'
        path = [os.path.join(path,fn) for fn in next(os.walk(path))[2]]

        results = celery_process(path, 
        [Exposure(negative_under_exposed = True),
        Fisheye()
        ],
        return_predictions = True
        )

        for i in range(100):
            print get_job_status(results)
            time.sleep(1)
            if results.ready():
                print results.get()
                break

Results from given example::

    0.0
    12.5
    25.0
    25.0
    31.25
    50.0
    56.25
    62.5
    68.75
    87.5
    [{'tests/images/exposure_sample_good.jpg': {'fisheye': 0, 'exposure': 0.28520000000000001}},
    {'tests/images/cross_processed.png': {'fisheye': 1, 'exposure': 0.97881355932203395}},
    {'tests/images/pattern.jpg': {'fisheye': 1, 'exposure': 0.22315558802045288}},
    {'tests/images/under_exposure_sample.jpg': {'fisheye': 0, 'exposure': -1}}] and so on...

You could simply just use the **results.get()** if you want to get the results as soon as they are ready.

The **celery_process_request()**-function works the same way::

    results = celery_process_request('{ "images": {"tests/images/exif.JPG": [ 50, 50, 200, 200 ],
     "tests/images/lama.jpg": [ 50, 50, 200, 200 ]},
     "filters": {"hdr": { },"pattern": { },"blurred_context": { }},
     "return_predictions": false,"combine_results": true,"sort_filters": true}')

    print results.get()

Results from given sample::

    [{u'tests/images/lama.jpg': False}, {u'tests/images/exif.JPG': False}]

Last but not least, processing single images with celery::

    result = process_image.delay('tests/images/exif.JPG',
        [Framed(),
        Highlights(),
        ], None, True, True, False)

    print result.get()

Results from given sample::

    {'tests/images/exif.JPG': {'highlights': 0, 'framed': 0}}

