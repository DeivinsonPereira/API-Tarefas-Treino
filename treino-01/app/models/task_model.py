from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship

from app.core.configs import settings


class TaskModel(settings.DB_BASE_URL):
    __tablename__ = 'task'

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, index=True)
    title = Column(String(50), index=True, unique=True, nullable=False)
    subtitle = Column(String(100), index=True, unique=True, nullable=True)
    description = Column(String(256), index=True, nullable=False)
    status = Column(Integer, index=True)
    task_group_id = Column(Integer, ForeignKey('task_group.id'))
    task_group = Relationship('TaskGroupModel', back_populates='tasks', lazy='joined')
