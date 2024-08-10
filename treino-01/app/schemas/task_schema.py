from typing import Optional

from pydantic import BaseModel, Field

from app.enums.status_task import StatusTask


class TaskSchemaBase(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    subtitle: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=5, max_length=256)
    status: StatusTask = Field(ge=1, le=5)
    task_group_id: int

    class Config:
        from_attributes = True


class TaskSchemaBaseResponse(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=50)
    subtitle: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=5, max_length=256)
    status: StatusTask = Field(ge=1, le=5)
    task_group_id: int

    class Config:
        from_attributes = True


class TaskSchemaUpdate(TaskSchemaBase):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusTask] = None
    task_group_id: Optional[str] = None
