import time
import os
from .celery import worker
from .db import init_db, db_session_factory
from .models import Result


def store_task_result(task_id, result):
    init_db(os.environ['SQLALCHEMY_DATABASE_URI'])
    session = db_session_factory()
    try:
        result_object = session.query(Result).filter_by(task_id=task_id).one()
        result_object.result = str(result)
        session.add(result_object)
        session.commit()
    finally:
        session.close()

@worker.task
def add(x, y):
    # Counting is hard
    time.sleep(3)
    result = x + y
    store_task_result(add.request.id, result)
    return result
