from sqlalchemy import Column, MetaData, Integer, String, ForeignKey

from backend.database import Base
from backend.services.tasks.models import TaskModel

metadata = MetaData()


class FileModel(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)


class FileTaskModel(Base):
    __tablename__ = "file_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file = Column(Integer, ForeignKey(FileModel.id, ondelete="CASCADE"), nullable=False)
    task = Column(Integer, ForeignKey(TaskModel.id, ondelete="CASCADE"), nullable=False)


class PhotoTaskModel(Base):
    __tablename__ = "photo_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    photo = Column(Integer, ForeignKey(FileModel.id, ondelete="CASCADE"), nullable=False)
    task = Column(Integer, ForeignKey(TaskModel.id, ondelete="CASCADE"), nullable=False)
