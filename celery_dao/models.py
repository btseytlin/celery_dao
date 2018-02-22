from sqlalchemy import Column, Integer, String
from .db import Base


class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    task_id = Column(String())
    result = Column(String())