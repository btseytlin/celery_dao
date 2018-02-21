from .celery import worker
from .utils import get_db_connection
import time

def store_task_result(task_id, result):
    con = get_db_connection()
    try:
        cur = con.cursor()

        insert_sql = f'INSERT INTO `results` (`task_id`, `result`) VALUES (\'{task_id}\', \'{str(result)})\''
        cur.execute(insert_sql)
        cur.commit()
    finally:
        con.close()

@worker.task
def add(x, y):
    # Counting is hard
    time.sleep(10)
    result = x + y
    store_task_result(add.request.id, result)
    return result
