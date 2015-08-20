Celery
****************

Usage
-----
Celery can be used to process multiple images at the same time, by dividing the filtering process between workers. To start, you must first configure the tasks.py to contain correct broker and backend-databases, for example::

    app = Celery('tasks', backend='redis://localhost', 
    broker='redis://localhost:6379/0')

and then starting a worker in the root folder of the project::

    celery -A tasks worker --loglevel=info
    
The workers have two tasks they can process: *celery_process* and *celery_process_request*. They are identical to the *process* and *process_request* functions in process.py file and are described in more detail in their documentation.

Example
-------
After the worker/workers have started, you can use the following example to assign tasks to workers::

    import imgfilter
    from tasks import *

    if __name__ == "__main__":
        path = 'tests/images/'
        path = [os.path.join(path,fn) for fn in next(os.walk(path))[2]]
        
    for img in path:
        result = celery_process.delay(img,
            [ Fisheye(),
            WholeBlur(),
            BlurredContext(),
            Framed(),
            Highlights(),
            ], None, True, True, False)
        
        print img, result

