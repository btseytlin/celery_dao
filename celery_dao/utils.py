import sqlite3
from .config import Config


def setup_db():

    con = get_db_connection()
    try:
        cursor = con.cursor()

        setup_sql = """
            CREATE TABLE IF NOT EXISTS results
                (
                 id integer primary key, 
                 task_id varchar(200) not null, 
                 result varchar(200)
            );
        """
        cursor.execute(setup_sql)

        con.commit()
    finally:
        con.close()


def get_db_connection():
    con = sqlite3.connect(Config.DB_PATH)
    return con