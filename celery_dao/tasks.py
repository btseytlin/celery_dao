import time
from .celery import worker
def store_task_result(task_id, result):
    from .app import create_app
    app = create_app()
    from .models import db, Result
    with app.app_context():
        result_object = Result.query.filter_by(task_id=task_id).one()
        result_object.result = str(result)
        db.session.add(result_object)
        db.session.commit()

@worker.task
def add(x, y):
    # Counting is hard
    time.sleep(10)
    result = x + y
    store_task_result(add.request.id, result)
    return result
