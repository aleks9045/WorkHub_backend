from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from backend.database import Base
from backend.services.tasks.models import TaskModel


class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    email = Column(String, nullable=True, unique=True)
    yandex = Column(String, nullable=True)
    full_name = Column(String(32), nullable=False)
    hashed_password = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    specialization = Column(String, nullable=True)
    admin = Column(Boolean, nullable=False)


class UserTaskModel(Base):
    __tablename__ = "user_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String, ForeignKey(UserModel.email, ondelete="CASCADE"), nullable=False)
    task = Column(Integer, ForeignKey(TaskModel.id, ondelete="CASCADE"), nullable=False)
