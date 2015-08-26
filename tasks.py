from celery import Celery
import qualipy

app = Celery('tasks', backend='', broker='')

@app.task
def celery_process(images, filters, ROIs=None, return_predictions=False,
            combine_results=False, sort_filters=True):
    return qualipy.process(images, filters, ROIs, return_predictions,
            combine_results, sort_filters)

@app.task
def celery_process_request(json):
    return qualipy.process_request(json)

