from typing import Optional, List

from pydantic import BaseModel, Field

from app.schemas.task_schema import TaskSchemaBase


class TaskGroupSchemaBase(BaseModel):
    title: str = Field(min_length=3, max_length=15)
    description: str = Field(min_length=10, max_length=256)

    class Config:
        from_attributes = True


class TaskGroupSchemaBaseWithId(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=15)
    description: str = Field(min_length=10, max_length=256)


class TaskGroupSchemaTasks(TaskGroupSchemaBase):
    tasks: Optional[List[TaskSchemaBase]]

    class Config:
        from_attributes = True


class TaskGroupSchemaUpdate(TaskGroupSchemaBase):
    title: Optional[str] = None
    description: Optional[str] = None


class TaskGroupSchemaResponseTest(BaseModel):
    success: bool
    message: str
    list: List[TaskGroupSchemaTasks]
