from celery import Celery
import imgfilter

app = Celery('tasks', backend='', broker='')

@app.task
def celery_process(images, filters, ROIs=None, return_predictions=False,
            combine_results=False, sort_filters=True):
    return imgfilter.process(images, filters, ROIs, return_predictions,
            combine_results, sort_filters)

@app.task
def celery_process_request(json):
    return imgfilter.process_request(json)

