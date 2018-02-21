from .celery import worker
from .utils import get_db_connection, setup_db
import time


def store_task_result(task_id, result):
    setup_db()
    con = get_db_connection()
    try:
        cur = con.cursor()
        insert_sql = f'INSERT INTO results (task_id, result) VALUES ("{task_id}", "{result}")'
        cur.execute(insert_sql)
        con.commit()
    finally:
        con.close()

@worker.task
def add(x, y):
    # Counting is hard
    time.sleep(3)
    result = x + y
    store_task_result(add.request.id, result)
    return result
