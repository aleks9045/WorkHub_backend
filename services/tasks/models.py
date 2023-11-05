from sqlalchemy import Column, MetaData, Integer, String, DATE, ForeignKey

from backend.database import Base


class ProjectModel(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=False)


class CategoryModel(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, nullable=False)


class TaskModel(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=False)
    begin = Column(DATE, nullable=False)
    end = Column(DATE, nullable=False)
    when_end = Column(String, nullable=True)
    status = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    comment = Column(String(1024), nullable=False)
    category = Column(String, nullable=False)
    project = Column(Integer, ForeignKey(ProjectModel.id, ondelete="CASCADE"), nullable=False)


class CategoryProjectModel(Base):
    __tablename__ = "category_project"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(Integer, ForeignKey(ProjectModel.id, ondelete="CASCADE"), nullable=False)
    category = Column(Integer, ForeignKey(CategoryModel.id, ondelete="CASCADE"), nullable=False)


class CategoryTaskModel(Base):
    __tablename__ = "category_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(Integer, ForeignKey(TaskModel.id, ondelete="CASCADE"), nullable=False)
    category = Column(Integer, ForeignKey(CategoryModel.id, ondelete="CASCADE"), nullable=False)
