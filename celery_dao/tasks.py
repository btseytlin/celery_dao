from .celery import worker
import time
@worker.task
def add(x, y):
    time.sleep(10) #Counting is hard
    return x + y