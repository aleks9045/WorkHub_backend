from sqlalchemy import Column, MetaData, Integer, String, DATE, ForeignKey

from backend.database import Base


class TaskModel(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(1024), nullable=False)
    contact = Column(String, nullable=False)
