## Broker settings.
BROKER_URL = 'redis://localhost:6379/0'

# List of modules to import when celery starts.
CELERY_IMPORTS = ('tasks', )

## Using the database to store task state and results.
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_ANNOTATIONS = {'tasks.process_image': {'rate_limit': '100/s'}}
