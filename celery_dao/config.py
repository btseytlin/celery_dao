import os
class Config:
    DB_PATH = os.environ.get('DB_PATH','db.db')