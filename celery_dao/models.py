from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String())
    result = db.Column(db.String())