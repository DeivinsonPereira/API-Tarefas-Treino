from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Relationship

from app.core.configs import settings


class TaskGroupModel(settings.DB_BASE_URL):
    __tablename__ = 'task_group'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    title = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(256), nullable=False, index=True)
    tasks = Relationship(
        'TaskModel',
        back_populates='task_group',
        cascade='all, delete-orphan',
        uselist=True,
        lazy='joined')
